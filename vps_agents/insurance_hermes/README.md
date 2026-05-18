# insurance_hermes

Hermes agent running on a Hostinger VPS, managed via Docker.

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
3. Verify SSH works:
   ```bash
   ssh -i "$VPS_SSH_KEY_PATH" -p "$VPS_PORT" "$VPS_USER@$VPS_HOST"
   ```

## Secrets policy

- `.env` is **gitignored**. Do not commit it.
- SSH private keys live under `~/.ssh/`, never inside this repo.
- If a secret leaks into a commit, rotate it immediately on Hostinger
  before scrubbing history.

## What lives here later

- `docker-compose.yml` — service definition once the agent code exists
- `Dockerfile` — image build for the hermes agent
- Application code (added in a follow-up commit)
