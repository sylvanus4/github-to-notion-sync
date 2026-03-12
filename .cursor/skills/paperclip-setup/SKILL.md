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
  version: "1.0.0"
  category: execution
---

# Paperclip Setup — Installation and Configuration

Install, configure, and deploy Paperclip AI agent orchestration platform.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | >= 20 |
| pnpm | >= 9.15 |
| PostgreSQL | 17 (or use embedded PGlite) |

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
npx paperclipai onboard --yes
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

### Method 4: Docker Compose (Production)

```bash
cd ~/work/thakicloud/paperclip
docker compose up -d
```

Uses external PostgreSQL 17, configures `PAPERCLIP_DEPLOYMENT_MODE=authenticated` and `PAPERCLIP_DEPLOYMENT_EXPOSURE=private`.

## Configuration

### Server Configuration

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai configure --section server
pnpm paperclipai configure --section storage
pnpm paperclipai configure --section llm
pnpm paperclipai configure --section database
pnpm paperclipai configure --section logging
pnpm paperclipai configure --section secrets
```

### Deployment Modes

| Mode | Description |
|------|-------------|
| `local_trusted` | Loopback only, no auth, implicit board user |
| `authenticated` | Session auth (Better Auth), API keys for agents |

| Exposure | Description |
|----------|-------------|
| `private` | Allowed hostnames only |
| `public` | Open access |

Set mode via config or env var:

```bash
PAPERCLIP_DEPLOYMENT_MODE=authenticated pnpm paperclipai run
```

### Allow Authenticated Hostname

For Tailscale or custom DNS:

```bash
pnpm paperclipai allowed-hostname my-hostname
```

### Context Profiles

Store connection defaults locally:

```bash
pnpm paperclipai context set --api-base http://localhost:3100 --company-id <id>
pnpm paperclipai context show
pnpm paperclipai context list
pnpm paperclipai context use <profile-name>
```

Profiles stored in `~/.paperclip/context.json`.

### Data Directory Isolation

Isolate all state (config, db, logs, storage, secrets):

```bash
pnpm paperclipai run --data-dir ./tmp/paperclip-dev
```

### Storage Providers

- `local_disk` — Default for local single-user installs
- `s3` — S3-compatible object storage for production

```bash
pnpm paperclipai configure --section storage
```

## Running

### Development

```bash
cd ~/work/thakicloud/paperclip
pnpm dev              # API + UI, watch mode
pnpm dev:once         # One-shot without file watching
pnpm dev:server       # Server only
pnpm dev:ui           # UI only
```

### Production

```bash
pnpm build
pnpm paperclipai run
```

### Instance Selection

```bash
pnpm paperclipai run --instance dev
```

## Diagnostics

```bash
pnpm paperclipai doctor           # Check health
pnpm paperclipai doctor --repair  # Auto-repair issues
```

### Database

```bash
pnpm db:generate    # Generate migration
pnpm db:migrate     # Apply migrations
pnpm paperclipai db:backup  # Manual backup
```

Automatic backups: every 60 minutes, 30-day retention, stored in `~/.paperclip/instances/<id>/data/backups/`.

### Environment Variables

```bash
pnpm paperclipai env   # Print all env vars for deployment
```

Key env vars:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection (omit for embedded PGlite) |
| `PORT` | Server port (default: 3100) |
| `SERVE_UI` | Serve UI from server (default: false in dev) |
| `PAPERCLIP_DEPLOYMENT_MODE` | `local_trusted` or `authenticated` |
| `PAPERCLIP_DEPLOYMENT_EXPOSURE` | `private` or `public` |
| `PAPERCLIP_HOME` | Base home directory |
| `PAPERCLIP_INSTANCE_ID` | Instance identifier |
| `BETTER_AUTH_SECRET` | Auth secret (authenticated mode) |
| `PAPERCLIP_ENABLE_COMPANY_DELETION` | Allow company deletion |

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

## Verification Checklist

After setup, verify:

1. `curl http://localhost:3100/api/health` returns `200`
2. UI loads at `http://localhost:3100`
3. `pnpm paperclipai company list` returns empty list or existing companies
4. `pnpm paperclipai doctor` shows no errors
5. For runtime context configuration, see `paperclip-control`

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED :3100` | Server not started | Run `pnpm dev` |
| Port already in use | Another process on 3100 | `lsof -i :3100` and kill, or change `PORT` |
| pnpm install fails | Lockfile mismatch | Use `--no-frozen-lockfile` |
| Embedded PG fails | Corrupted data dir | Delete `~/.paperclip/instances/default/db/` and restart |
| Build errors on `cursor-local` | Missing `@types/node` | Known issue; does not affect server startup |
| Migration errors | Schema drift | Run `pnpm db:migrate` |
| Auth errors in `authenticated` mode | Missing `BETTER_AUTH_SECRET` | Set env var or run `pnpm paperclipai auth bootstrap-ceo` |

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard
- `paperclip-tasks` — Issue/task CRUD and checkout
- `paperclip-agents` — Agent creation, heartbeats, budgets

## Examples

### Example 1: Standard usage

**User says:** "Install paperclip"

**Actions:**
1. Gather necessary context from the project and user
2. Execute the skill workflow as documented above
3. Deliver results and verify correctness