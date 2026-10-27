#!/usr/bin/env python3
"""Minimal Google Drive helper (stdlib only, OAuth refresh token, scope drive.file).
  python3 gdrive.py upload-dir <local_dir> [--keep-hours 24]
      Uploads every file in <local_dir> into Drive: <DRIVE_FOLDER_NAME>/<basename of local_dir>/,
      then moves date folders (YYYY-MM-DD) older than --keep-hours to the Drive trash.
  python3 gdrive.py upload <file> [<folder_path>]   e.g. folder_path "2026-10-27"
Env (or .env next to this file): GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN, DRIVE_FOLDER_NAME
"""
import json, mimetypes, os, re, sys, uuid, datetime as dt, urllib.parse, urllib.request, urllib.error
from pathlib import Path

API = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"


def load_env():
    env = dict(os.environ)
    p = Path(__file__).parent / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


ENV = load_env()
ROOT_NAME = ENV.get("DRIVE_FOLDER_NAME", "Fetch Infographic Auto")
_token = None


def req(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            body = resp.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"Drive API HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def access_token():
    global _token
    if _token:
        return _token
    for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"):
        if not ENV.get(k):
            sys.exit(f"Missing {k}")
    body = urllib.parse.urlencode({"client_id": ENV["GOOGLE_CLIENT_ID"], "client_secret": ENV["GOOGLE_CLIENT_SECRET"],
                                   "refresh_token": ENV["GOOGLE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    _token = req("https://oauth2.googleapis.com/token", data=body)["access_token"]
    return _token


def auth():
    return {"Authorization": f"Bearer {access_token()}"}


def find_folder(name, parent=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent:
        q += f" and '{parent}' in parents"
    r = req(f"{API}/files?" + urllib.parse.urlencode({"q": q, "fields": "files(id,name)"}), headers=auth())
    return r["files"][0]["id"] if r.get("files") else None


def ensure_folder(name, parent=None):
    fid = find_folder(name, parent)
    if fid:
        return fid
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent:
        meta["parents"] = [parent]
    return req(f"{API}/files?fields=id", data=json.dumps(meta).encode(),
               headers={**auth(), "Content-Type": "application/json"}, method="POST")["id"]


def upload_file(path, parent):
    path = Path(path)
    q = f"name='{path.name}' and '{parent}' in parents and trashed=false"
    existing = req(f"{API}/files?" + urllib.parse.urlencode({"q": q, "fields": "files(id)"}), headers=auth()).get("files")
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    meta = {"name": path.name} if existing else {"name": path.name, "parents": [parent]}
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
            f"--{boundary}\r\nContent-Type: {mime}\r\n\r\n").encode() + path.read_bytes() + f"\r\n--{boundary}--".encode()
    hdr = {**auth(), "Content-Type": f"multipart/related; boundary={boundary}"}
    if existing:
        req(f"{UPLOAD}/{existing[0]['id']}?uploadType=multipart", data=body, headers=hdr, method="PATCH")
    else:
        req(f"{UPLOAD}?uploadType=multipart", data=body, headers=hdr, method="POST")
    print(f"uploaded {path.name}")


def trash_old(root_id, keep_hours):
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=keep_hours)
    q = f"'{root_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    for f in req(f"{API}/files?" + urllib.parse.urlencode({"q": q, "fields": "files(id,name,modifiedTime)"}), headers=auth()).get("files", []):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["name"]) and dt.datetime.fromisoformat(f["modifiedTime"].replace("Z", "+00:00")) < cutoff:
            req(f"{API}/files/{f['id']}", data=json.dumps({"trashed": True}).encode(),
                headers={**auth(), "Content-Type": "application/json"}, method="PATCH")
            print(f"trashed old folder {f['name']}")


def upload_dir(d, keep_hours=24):
    """Upload a dated local folder to Drive: <DRIVE_FOLDER_NAME>/<folder name>/ and trash old date folders."""
    d = Path(d)
    root = ensure_folder(ROOT_NAME)
    day = ensure_folder(d.name, root)
    subs = {}
    for p in sorted(d.rglob("*")):
        if p.is_file():
            if p.parent == d:
                upload_file(p, day)
            else:
                subs[p.parent] = subs.get(p.parent) or ensure_folder(p.parent.name, day)
                upload_file(p, subs[p.parent])
    trash_old(root, keep_hours)


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "upload-dir":
        upload_dir(a[1], float(a[a.index("--keep-hours") + 1]) if "--keep-hours" in a else 24)
        return
    root = ensure_folder(ROOT_NAME)
    if a[0] == "upload":
        parent = ensure_folder(a[2], root) if len(a) > 2 else root
        upload_file(a[1], parent)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
