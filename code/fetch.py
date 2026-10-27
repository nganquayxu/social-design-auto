#!/usr/bin/env python3
"""Fetch recent posts from Instagram accounts via Meta Business Discovery,
rank them, and save the top candidates (json + images) into the Drive folder.
Usage: python3 fetch.py [--days 7] [--top 5]
"""
import argparse, json, os, re, shutil, sys, time, datetime as dt, urllib.parse, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_ACCOUNTS = "EXAMPLE_ACCOUNT_NAME_HERE"
API = "https://graph.facebook.com/v23.0"


def load_env():
    env = dict(os.environ)
    p = HERE / ".env"
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def get_json(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {e.code} from Meta API: {body[:500]}")


def fetch_account(user_id, token, username, limit=25):
    fields = (f"business_discovery.username({username})"
              f"{{followers_count,media.limit({limit})"
              "{caption,like_count,comments_count,media_type,media_url,permalink,timestamp}}")
    q = urllib.parse.urlencode({"fields": fields, "access_token": token})
    data = get_json(f"{API}/{user_id}?{q}")
    bd = data.get("business_discovery", {})
    followers = bd.get("followers_count") or 1
    return followers, bd.get("media", {}).get("data", [])


def cleanup_old(out_root, keep_hours, today_dir, dry_run=False):
    """Delete dated result folders (YYYY-MM-DD) whose newest file is older than keep_hours.
    Only touches folders named like a date directly inside out_root; never today's folder."""
    cutoff = time.time() - keep_hours * 3600
    for d in sorted(out_root.iterdir()):
        if not (d.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d.name)) or d == today_dir:
            continue
        newest = max((p.stat().st_mtime for p in d.rglob("*")), default=d.stat().st_mtime)
        newest = max(newest, d.stat().st_mtime)
        if newest < cutoff:
            print(f"[cleanup] {'would delete' if dry_run else 'deleting'} {d.name}", file=sys.stderr)
            if not dry_run:
                shutil.rmtree(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3, help="only posts from the last N days (default 3)")
    ap.add_argument("--per-account", type=int, default=2, help="best N posts per account (default 2)")
    ap.add_argument("--top", type=int, default=0, help="optional overall cap on candidates (0 = no cap)")
    ap.add_argument("--keep-hours", type=float, default=24, help="delete result folders older than this (default 24)")
    ap.add_argument("--upload", action="store_true", help="also upload the dated folder to Google Drive (needs GOOGLE_* in env/.env; also on if UPLOAD_TO_DRIVE=1)")
    ap.add_argument("--dry-run-cleanup", action="store_true", help="only list folders that would be deleted")
    args = ap.parse_args()

    env = load_env()
    accounts = [a.strip() for a in env.get("ACCOUNTS", DEFAULT_ACCOUNTS).split(",") if a.strip()]
    out_root = Path(env["OUT_DIR"]).expanduser() if env.get("OUT_DIR") else None
    if out_root is None:
        sys.exit("Missing OUT_DIR in .env (folder where daily results are saved)")
    token, user_id = env.get("IG_TOKEN"), env.get("IG_USER_ID")
    if not token or not user_id:
        sys.exit("Missing IG_TOKEN / IG_USER_ID in .env (see .env.example)")

    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)
    posts = []
    for acct in accounts:
        try:
            followers, media = fetch_account(user_id, token, acct)
        except SystemExit as e:
            print(f"[warn] {acct}: {e}", file=sys.stderr)
            continue
        for m in media:
            ts = dt.datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
            if ts < cutoff or not m.get("media_url") or m.get("media_type") == "VIDEO":
                continue
            likes, comments = m.get("like_count", 0), m.get("comments_count", 0)
            m.update(account=acct, followers=followers,
                     score=likes + 3 * comments,
                     engagement_rate=round((likes + comments) / followers * 100, 3))
            posts.append(m)

    if not posts:
        sys.exit("No eligible posts found in the window.")

    posts.sort(key=lambda p: p["engagement_rate"], reverse=True)
    top, seen = [], {}
    for p in posts:
        if seen.get(p["account"], 0) < args.per_account:
            top.append(p)
            seen[p["account"]] = seen.get(p["account"], 0) + 1
    if args.top:
        top = top[: args.top]

    day = out_root / dt.date.today().isoformat()
    cand = day / "candidates"
    cand.mkdir(parents=True, exist_ok=True)
    for old in cand.glob("*.jpg"):  # drop images from an earlier run the same day
        old.unlink()
    for i, p in enumerate(top, 1):
        img = cand / f"{i:02d}_{p['account']}.jpg"
        try:
            urllib.request.urlretrieve(p["media_url"], img)
            p["local_image"] = str(img)
        except Exception as e:
            print(f"[warn] image download failed for {p['permalink']}: {e}", file=sys.stderr)
        p.pop("media_url", None)  # signed URL, expires
    (day / "candidates.json").write_text(json.dumps(top, indent=2, ensure_ascii=False))
    cleanup_old(out_root, env.get("KEEP_HOURS") and float(env["KEEP_HOURS"]) or args.keep_hours, day, args.dry_run_cleanup)
    if args.upload or env.get("UPLOAD_TO_DRIVE") in ("1", "true", "yes"):
        sys.path.insert(0, str(HERE))
        import gdrive
        gdrive.upload_dir(day, float(env.get("KEEP_HOURS") or args.keep_hours))
    print(str(day))


if __name__ == "__main__":
    main()
