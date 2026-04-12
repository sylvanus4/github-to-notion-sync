---
name: paperclip-setup
description: >-
  Install, configure, and deploy Paperclip instances for AI agent orchestration.
  Use when the user asks to "install paperclip", "set up paperclip", "configure
  paperclip", "deploy paperclip", "paperclip doctor", "start paperclip",
  "stop paperclip", "페이퍼클립 설치", "페이퍼클립 설정", "설정 확인",
  "paperclip onboard", "paperclip docker", or any installation, configuration,
  or deployment task. Do NOT use for runtime operations like task management
  (use paperclip-tasks), agent operations (use paperclip-agents), or governance
  (use paperclip-control).
metadata:
  author: thaki
  version: "2.0.0"
  category: execution
---

# Paperclip Setup — Installation and Configuration

Install, configure, and deploy Paperclip AI agent orchestration platform.
**v2.0**: MCP-integrated with health verification via `paperclip_dashboard` tool.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | >= 20 |
| pnpm | >= 9.15 |
| PostgreSQL | 17 (or use embedded PGlite) |

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai onboard --yes
```

This auto-detects the environment, sets up embedded PostgreSQL, and starts the server.

### Method 2: Manual Clone

```bash
git clone https://github.com/paperclipai/paperclip.git ~/work/thakicloud/paperclip
cd ~/work/thakicloud/paperclip
pnpm install --no-frozen-lockfile
pnpm dev
```

### Method 3: Docker Compose (Quickstart)

```bash
cd ~/work/thakicloud/paperclip
docker compose -f docker-compose.quickstart.yml up -d
```

Uses embedded PostgreSQL, requires `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `BETTER_AUTH_SECRET` in `.env`.

## Configuration

### Server Configuration

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai configure --section server
pnpm paperclipai configure --section storage
pnpm paperclipai configure --section llm
pnpm paperclipai configure --section database
```

### Deployment Modes

| Mode | Description |
|------|-------------|
| `local_trusted` | Loopback only, no auth, implicit board user |
| `authenticated` | Session auth (Better Auth), API keys for agents |

### Context Profiles

```bash
pnpm paperclipai context set --api-base http://localhost:3100 --company-id <id>
pnpm paperclipai context show
```

Profiles stored in `~/.paperclip/context.json`.

## Running

### Development

```bash
cd ~/work/thakicloud/paperclip
pnpm dev              # API + UI, watch mode
pnpm paperclipai run  # Production mode
```

## Health Verification (MCP-Integrated)

After startup, verify via the MCP bridge:

1. Call `paperclip_dashboard` with `companyId` = `b573bdbe-785a-4f39-b1e9-f2b623e40a92` (ThakiCloud)
2. Expect a JSON response with agent counts, pending approvals, and cost summary
3. If the tool call fails with a connection error, the instance is not running

### Auto-Repair Flow

If `paperclip_dashboard` returns a connection error:

1. Check if Paperclip process is running: `pgrep -f paperclipai`
2. If not running, start it: `cd ~/work/thakicloud/paperclip && pnpm paperclipai run &`
3. Wait for health: `curl -sf --max-time 2 http://127.0.0.1:3100/api/health`
4. Retry `paperclip_dashboard` MCP call

### Legacy Diagnostics

```bash
pnpm paperclipai doctor           # Check health
pnpm paperclipai doctor --repair  # Auto-repair issues
```

## Key Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection (omit for embedded PGlite) |
| `PORT` | Server port (default: 3100) |
| `SERVE_UI` | Serve UI from server (default: false in dev) |
| `PAPERCLIP_DEPLOYMENT_MODE` | `local_trusted` or `authenticated` |
| `BETTER_AUTH_SECRET` | Auth secret (authenticated mode) |

## Local File Layout

```
~/.paperclip/
├── context.json                          # Context profiles
└── instances/
    └── default/
        ├── config.json                   # Instance config
        ├── db/                           # Embedded PostgreSQL data
        ├── logs/                         # Server logs
        ├── data/
        │   ├── storage/                  # File storage
        │   └── backups/                  # DB backups
        └── secrets/
            └── master.key                # Encryption key
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED :3100` | Server not started | Run `pnpm paperclipai run` |
| Port already in use | Another process on 3100 | `lsof -i :3100` and kill |
| Embedded PG fails | Corrupted data dir | Delete `~/.paperclip/instances/default/db/` and restart |
| MCP tool call fails | `paperclip-mcp` not registered | Check `.cursor/mcp.json` has `paperclip` entry |

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard (MCP-integrated)
- `paperclip-tasks` — Issue/task CRUD and checkout (MCP-integrated)
- `paperclip-agents` — Agent creation, heartbeats, budgets (MCP-integrated)
- `paperclip-bridge` — Bidirectional sync between mission-control and Paperclip
