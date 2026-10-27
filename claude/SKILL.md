---
name: daily-infographic-fetch
description: Fetch top Instagram posts from 4 finance-visual accounts, pick the best one, write a brief + image prompt into the synced Drive folder
---

Goal: every morning, pick the single best recent viral US-stock-investing post to inspire a new Spiking infographic, and save a ready-to-use brief for ChatGPT image generation.

Steps:
1. Run: python3 <PROJECT_DIR>/fetch.py
   - It prints the output folder path (a dated folder inside the Google Drive Desktop-synced folder "Fetch Infographic") and writes candidates.json plus images in a candidates/ subfolder. Instagram accounts come from ACCOUNTS in the .env (never print .env contents). It also deletes dated folders older than 24h.
   - If it exits with "Missing IG_TOKEN / IG_USER_ID" or an HTTP/token error (e.g. expired token), STOP and report that error clearly. Do not invent posts.
2. Read candidates.json and view each candidate image. Check the dated folder for existing brief.md / brief-N.md and never pick a post whose permalink was already chosen. Pick the ONE best post. Criteria, in order: (a) topic about US stocks/investing that many retail investors search for (top holdings, best/worst performers, Magnificent 7, how a company makes money, revenue breakdown, dividends, market cap rankings, ETF holdings, famous portfolios, AI infrastructure winners); (b) works as a simple LIST / ranked bars / waterfall / donut-list infographic with few numbers; (c) strong engagement rate; (d) timely. Skip personal / non-data / meme posts. Inspiration only: never reproduce another account's graphic or numbers verbatim.
3. Read <DRIVE_FOLDER>/style-guide.md and follow it (palette, typography, layout, prompt template). Extra rules from the user: the takeaway strip is OPTIONAL (omit by default); headline must be SIMPLE, CATCHY, curiosity-driven (e.g. "HOW X MAKES MONEY", "TOP 10 ..."), max ~6 words per line, truthful to the data; keep text minimal (no small notes); the Spiking logo must be the real spiking-logo-final.png from the Drive folder, never AI-generated. Name the 2-3 closest reference samples (sample-01..10) to attach.
4. In the dated folder write brief.md (if it exists write brief-2.md, brief-3.md ... never overwrite) containing:
   - Chosen post: account, permalink, likes, comments, engagement rate, why chosen (2-3 lines); runner-up.
   - Topic and the key data points to verify from primary sources (SEC filings, company reports, Fed, index providers). Mark every number taken from the Instagram post as UNVERIFIED; verify before designing.
   - Proposed headline (2 lines, caps), optional one-line subhead, hero visual type + the reference samples to attach, one-line source. Max 10-12 rows of data.
   - A filled-in image-generation prompt following the prompt template in style-guide.md.
   - Final section "Other ideas": use web search to find 3-5 other trending US-stock topics today (title, why trending, best primary data source, suggested list format). Topic ideas only; no copied graphics.
5. Copy the chosen candidate image to <dated folder>/reference.jpg (or reference-2.jpg etc. matching the brief number).
6. Final message: 3 lines max - chosen post, folder path, any warnings. Only write inside the dated folder; do not modify other Drive files.