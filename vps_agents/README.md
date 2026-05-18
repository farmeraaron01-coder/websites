# vps_agents

Agents and services that run on Hostinger VPS instances managed via Docker.

## Layout

Each subfolder is one agent / service:

- `insurance_hermes/` — Hermes agent for insurance workflows

## Conventions

- Every agent folder has a `.env.example` checked into git with placeholder values.
- The real `.env` lives next to it locally and on the VPS, but is **gitignored**.
- SSH keys, API keys, and passwords are **never** committed.
- Each agent has its own `README.md` documenting how to run it and what env vars it needs.
