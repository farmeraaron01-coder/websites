# insurance_hermes — install state

Snapshot of the hermes runtime on the VPS after initial setup. Update this
file when tools are enabled, providers change, or paths move.

## VPS file locations (inside the hermes container / on the VPS)

| Purpose      | Path                  |
| ------------ | --------------------- |
| Settings     | `/opt/data/config.yaml` |
| API keys     | `/opt/data/.env`        |
| Cron jobs    | `/opt/data/cron/`       |
| Sessions     | `/opt/data/sessions/`   |
| Logs         | `/opt/data/logs/`       |

These live on the VPS only. Nothing under `/opt/data/` is in this git repo.
`/opt/data/.env` contains real secrets — never copy its contents into the
repo or paste into chat.

## Tool availability (as of last setup)

Enabled:
- Vision (image analysis)
- Browser Automation (local browser)
- Image Generation (OpenAI, via Codex auth)
- Text-to-Speech (Edge TTS)
- Terminal / Commands
- Task Planning (todo)
- Skills (view, create, edit)

Disabled — waiting on keys in `/opt/data/.env`:
- **Mixture of Agents** — needs `OPENROUTER_API_KEY`
- **Web Search & Extract** — needs at least one of:
  `EXA_API_KEY`, `PARALLEL_API_KEY`, `FIRECRAWL_API_KEY` (+ optional
  `FIRECRAWL_API_URL`), `TAVILY_API_KEY`, or `SEARXNG_URL`
- **Skills Hub (GitHub)** — needs `GITHUB_TOKEN`
  (fine-grained PAT, read-only on the skills repo is usually enough)

## CLI cheatsheet

```bash
# First-time / re-run setup
hermes setup            # full wizard
hermes setup model      # change model / provider
hermes setup terminal   # change terminal backend
hermes setup gateway    # configure messaging (Telegram)
hermes setup tools      # configure tool providers (add API keys)

# Config inspection / editing
hermes config                       # view current settings
hermes config edit                  # open config in editor
hermes config set <key> <value>     # set a specific value

# Direct file edits
nano /opt/data/config.yaml
nano /opt/data/.env

# Run
hermes                  # start chatting (interactive)
hermes gateway          # start messaging gateway (Telegram bridge)
hermes doctor           # check for issues
```

## Next steps to enable more tools

1. Decide which web-search provider (Tavily and Exa are the common picks
   — Tavily has a generous free tier; Exa is stronger for semantic
   search).
2. Create a fine-grained GitHub PAT for Skills Hub. Scope: read access to
   the skills repo only. Store under `GITHUB_TOKEN` in `/opt/data/.env`.
3. (Optional) OpenRouter key if we want Mixture of Agents.
4. After adding keys, run `hermes doctor` to verify, or restart the
   container to pick them up.
