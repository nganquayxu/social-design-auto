#!/usr/bin/env python3
"""One-time: sign in to Google in your browser and save GOOGLE_REFRESH_TOKEN into .env.
Needs GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET (OAuth client type "Desktop app") in .env."""
import http.server, json, re, sys, threading, urllib.parse, urllib.request, webbrowser
from pathlib import Path

ENV = Path(__file__).parent / ".env"
env = {}
for line in ENV.read_text().splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"):
    if not env.get(k):
        sys.exit(f"Missing {k} in .env")

result = {}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        result["code"] = q.get("code", [None])[0]
        result["error"] = q.get("error", [None])[0]
        self.send_response(200); self.end_headers()
        self.wfile.write(b"You can close this tab and return to the terminal.")

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", 0), H)
redirect = f"http://127.0.0.1:{srv.server_port}"
url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": env["GOOGLE_CLIENT_ID"], "redirect_uri": redirect, "response_type": "code",
    "scope": "https://www.googleapis.com/auth/drive.file", "access_type": "offline", "prompt": "consent",
    **({"login_hint": env["DRIVE_ACCOUNT"]} if env.get("DRIVE_ACCOUNT") else {})})
if "--no-browser" in sys.argv:
    print("Open this URL in a browser/profile signed in to the Drive owner's Google account (private window works),")
    print("on THIS computer. After you allow access it redirects to a local page; then come back here:\n")
    print(url + "\n")
else:
    print("Opening browser to sign in with the Google account that owns the Drive...")
    webbrowser.open(url)
threading.Thread(target=srv.handle_request).start()
while "code" not in result:
    threading.Event().wait(0.3)
if not result["code"]:
    sys.exit(f"Auth failed: {result['error']}")
body = urllib.parse.urlencode({"code": result["code"], "client_id": env["GOOGLE_CLIENT_ID"],
        "client_secret": env["GOOGLE_CLIENT_SECRET"], "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data=body, timeout=30))
if "refresh_token" not in tok:
    sys.exit("No refresh_token returned (revoke the app at myaccount.google.com/permissions and retry).")
text = ENV.read_text()
ENV.write_text(re.sub(r"^GOOGLE_REFRESH_TOKEN=.*$", lambda m: "GOOGLE_REFRESH_TOKEN=" + tok["refresh_token"], text, flags=re.M))
print("OK: GOOGLE_REFRESH_TOKEN saved to .env")
