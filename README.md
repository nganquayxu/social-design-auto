# Spiking infographic workflow (backup)

- `code/`: scripts (`fetch.py` lists/ranks recent Instagram posts via Meta Business Discovery; `gdrive.py` + `get_google_token.py` optional Drive upload). Copy `.env.example` to `.env` and fill in your own values. NEVER commit `.env`.
- `claude/`: the Claude prompts. `SKILL.md` = the scheduled-task instructions (paths are for the original Mac; adapt for cloud), `daily-brief.md` = the `/daily-brief` slash command (goes in `.claude/commands/`).
- `chatgpt/`: files meant for ChatGPT (style guide etc.).

No secrets are stored in this repo. Tokens live in `.env` / environment variables only.
