---
name: local-dev-runner
description: >-
  Start, stop, and manage the full local development environment on macOS. Use
  when the user asks to run the project locally, start/stop services, or set up
  the development stack from scratch. Do NOT use for diagnosing specific service
  failures after startup (use diagnose) or reviewing infrastructure
  configuration (use sre-devops-expert). Korean triggers: "로컬 실행", "개발 환경".
metadata:
  version: "1.1.0"
  category: "execution"
  author: "thaki"
---
# Local Development Runner

Manage the project's local development stack: start, stop, health-check, and
troubleshoot services running on macOS.

## Workflow

### Step 1: Discover Project Stack

Before starting, identify the project's development stack:

1. Check for `docker-compose.yml` / `docker-compose.yaml` / `compose.yml`
2. Check for startup scripts: `scripts/dev-start.sh`, `Makefile`, `package.json` scripts
3. Check for `.env.example` or `.env.template`
4. Read any `README.md` or `docs/development.md` for setup instructions

### Step 2: Environment Setup

1. Copy `.env.example` → `.env` if `.env` does not exist
2. Verify required environment variables are set
3. Install dependencies based on project type:
   - Python: `pip install -e .` or `uv pip install -e .`
   - Node.js: `npm install`
   - Go: `go mod download`

### Step 3: Start Infrastructure

Start infrastructure services (databases, caches, message queues) via Docker:

```bash
docker compose up -d
```

Wait for health checks to pass before proceeding to application services.

### Step 4: Start Application Services

Start application services in dependency order:
1. Stateless services first (no external dependencies)
2. Data services (depend on DB/cache)
3. AI/ML services (depend on models/GPU)
4. Gateway and frontend (depend on backend services)

For each service, verify it responds on its health endpoint before starting
the next tier.

### Step 4.5: Start Paperclip Agent Orchestrator

Start the Paperclip instance if not already running:

```bash
# Check if Paperclip is already listening
curl -sf --max-time 2 http://127.0.0.1:3100/api/health >/dev/null 2>&1 && echo "Paperclip already running" && exit 0

# Start Paperclip (onboard --yes handles first-time setup automatically)
cd ~/work/thakicloud/paperclip && pnpm paperclipai run &
```

Wait for the health endpoint before proceeding:

```bash
for i in $(seq 1 30); do
  curl -sf --max-time 2 http://127.0.0.1:3100/api/health >/dev/null 2>&1 && break
  sleep 1
done
```

Paperclip provides agent orchestration, cost governance, and task management
at `http://127.0.0.1:3100`. The ThakiCloud company is pre-configured.

### Step 5: Health Check

Verify all services are healthy:

```bash
# If a status script exists
bash scripts/dev-status.sh

# Otherwise, check each service
curl -sf http://localhost:<PORT>/health
```

### Step 6: Report Status

Report the status of all services to the user with a table showing:
- Service name
- Port
- Status (healthy / unhealthy / not running)

## Cleanup Before Start

Prevent duplicate processes before starting:

```bash
lsof -i :<PORT> | grep LISTEN
docker stop <conflicting-container>
pkill -f "<service-pattern>"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | `lsof -i :<port>` to find PID, then `kill <pid>` |
| Docker compose fails | `docker compose down` then restart |
| Import errors | Reinstall dependencies |
| DB connection error | Check database container status and credentials |
| Cache connection refused | Check cache container status and password |
| Frontend build error | Delete `node_modules`, reinstall |

## Examples

### Example 1: Start full stack

**User says:** "Start the dev environment"

**Actions:**
1. Discover project stack (docker-compose, scripts, env files)
2. Setup environment variables
3. Start infrastructure via Docker
4. Start application services in order
5. Run health checks
6. Report status

**Result:** Full local development stack running and verified.

### Example 2: Stop all services

**User says:** "Stop the dev environment"

**Actions:**
1. Stop Paperclip (`pkill -f "paperclipai" || true`)
2. Stop application services (pkill or script)
3. Stop Docker containers (`docker compose down`)
4. Verify no lingering processes

**Result:** All services stopped cleanly.
