# fetch-infographic

Daily: fetch recent posts from Instagram accounts (Meta Business Discovery), rank by engagement,
save the top 5 + images; a Claude scheduled task then picks the best and writes brief.md.

## Setup (each person, on their own machine)
1. Python 3 (python.org install: run "Install Certificates.command" once).
2. Copy `.env.example` to `.env` (`chmod 600 .env`) and fill in YOUR OWN values:
   IG_USER_ID, IG_TOKEN (long-lived, ~60 days), OUT_DIR, ACCOUNTS.
   Requires an Instagram Business/Creator account linked to a Facebook Page and a Meta app
   (see developers.facebook.com, Graph API Explorer: permissions instagram_basic, pages_show_list, pages_read_engagement).
   NEVER share or commit `.env`.
3. Test: `python3 fetch.py`  -> prints the dated output folder.
4. In Claude desktop, ask Claude to create a scheduled task that runs `python3 <this folder>/fetch.py`,
   views the images in candidates/, picks the best post, and writes brief.md + reference.jpg in the dated folder
   (use your style-guide.md for the image prompt). Schedules run only while the Mac is on and the app is open.
5. Use a Meta PAGE access token (type PAGE, no expiry; get it from Graph API Explorer: GET me/accounts) so no renewal is needed. If the token ever stops working, fetch a fresh Page token and update IG_TOKEN.

## Run without a schedule (one command)
Open this folder in Claude desktop (Code tab) and type:
    /daily-brief
It runs fetch.py, picks the best post and writes brief.md + reference.jpg. Running it again the same day picks a DIFFERENT post and writes brief-2.md, brief-3.md ... (nothing is overwritten). Optional: `/daily-brief --days 14 --top 8`.
(The command lives in `.claude/commands/daily-brief.md`.)

## Auto-cleanup
Each time fetch.py runs successfully it deletes dated result folders (YYYY-MM-DD) older than 24 hours
(by their newest file's modified time; today's folder and style-guide/reference files are never touched).
Change with `--keep-hours 72` or `KEEP_HOURS=72` in .env. Preview with `python3 fetch.py --dry-run-cleanup`.
Deleted folders go to Google Drive's trash (kept ~30 days).
