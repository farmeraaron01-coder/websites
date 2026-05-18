# insurance_hermes

Hermes agent running on a Hostinger VPS, managed via Docker.

> Current runtime status, VPS paths, enabled/disabled tools, and CLI
> cheatsheet live in [`INSTALL_STATE.md`](./INSTALL_STATE.md). Update that
> file when the install changes.

## Setup

1. Copy the env template:
   ```bash
   cp .env.example .env
   ```
2. Fill in the values in `.env`:
   - `VPS_HOST` — the VPS hostname / IP from Hostinger
   - `VPS_USER` — SSH user
   - `VPS_PORT` — SSH port (default `22`)
   - `VPS_SSH_KEY_PATH` — absolute path to the private key on your machine
   - `DOCKER_MANAGER_URL` — URL of the Docker management UI on the VPS
   - `TELEGRAM_BOT_TOKEN` — token from @BotFather (see "Telegram bot" below)
   - `TELEGRAM_ADMIN_CHAT_ID` — your Telegram numeric ID (from @userinfobot)
3. Verify SSH works:
   ```bash
   ssh -i "$VPS_SSH_KEY_PATH" -p "$VPS_PORT" "$VPS_USER@$VPS_HOST"
   ```

## Secrets policy

- `.env` is **gitignored**. Do not commit it.
- SSH private keys live under `~/.ssh/`, never inside this repo.
- If a secret leaks into a commit, rotate it immediately on Hostinger
  before scrubbing history.

## Telegram bot

The hermes agent talks to its operator over Telegram. Create the bot once
via [@BotFather](https://t.me/BotFather):

1. `/newbot` → pick a display name and a username ending in `bot`.
2. Copy the HTTP API token BotFather returns into `TELEGRAM_BOT_TOKEN` in `.env`.
3. Message [@userinfobot](https://t.me/userinfobot) to get your numeric user ID,
   put it in `TELEGRAM_ADMIN_CHAT_ID` so the bot only responds to you.
4. Optional: `/setdescription`, `/setuserpic`, `/setcommands` in BotFather later.

If the token leaks, run `/revoke` in BotFather to rotate it.

## What lives here later

- `docker-compose.yml` — service definition once the agent code exists
- `Dockerfile` — image build for the hermes agent
- Application code (added in a follow-up commit)
