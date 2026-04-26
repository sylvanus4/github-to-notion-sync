---
name: session-preflight
description: >-
  Quick prerequisite check at session start: verify environment, tools, API keys,
  data freshness, and pending items before productive work begins. Prevents
  wasted cycles on misconfigured environments.
user_invocable: true
---

# Session Preflight

Run a quick health check at the start of a work session to verify that the
environment, tools, data, and pending items are ready for productive work.

## When to Use

- Starting a new work session or day
- After system updates or environment changes
- Before running pipelines that depend on external services
- User says "preflight", "health check", "check setup", "프리플라이트", "환경 점검"
- Automatically invoked by morning-ship and daily-am-orchestrator

## Do NOT Use

- Deep environment debugging (use setup-doctor)
- Full dependency audit (use dependency-auditor)
- Runtime monitoring (use service-health-doctor)

## Check Categories

### 1. Environment Basics

| Check | How | Pass Criteria |
|-------|-----|---------------|
| Python available | `python3 --version` | >= 3.10 |
| Node available | `node --version` | >= 18 |
| Git clean | `git status --porcelain` | No uncommitted .env or secret files |
| Disk space | `df -h .` | > 5GB free |
| Working directory | `pwd` | Expected project root |

### 2. API Keys & Credentials

Check presence (not values) of required environment variables:

| Variable | Required By |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Claude API calls |
| `SLACK_BOT_TOKEN` | Slack posting |
| `SLACK_USER_TOKEN` | Slack thread cleanup |
| `NOTION_API_KEY` | Notion MCP |
| `HF_TOKEN` | HuggingFace Hub |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` or `GOOGLE_APPLICATION_CREDENTIALS` | Google Workspace (verify: `gws drive files list 2>&1 | head -3`) |

Report: present / missing / expired (if checkable).

### 3. Data Freshness

| Data Source | Check | Stale If |
|-------------|-------|----------|
| Stock prices DB | Last sync timestamp | > 3 days old |
| Inbox queue | `data/ops/inbox.jsonl` pending count | > 20 pending items |
| Scan history | Last scan date per portal | > 7 days for daily portals |
| Batch state | `batch/batch-state.tsv` running items | Running > 30 min (likely stale) |
| Report index | `data/ops/report-index.jsonl` size | > 5000 entries (prune needed) |
| gbrain health | `gbrain health --json` composite score | Score < 50 (RED) |
| gbrain stale | `gbrain search "compiled-truth" --limit 50 --json` | Any compiled truth older than its sources |
| gbrain embeddings | `gbrain doctor --json` stale embeddings count | > 50 stale embeddings |

### 4. Pending Items

Scan for unfinished work:
- `tasks/todo.md` open items count
- `batch/batch-state.tsv` pending/error items
- `data/ops/inbox.jsonl` pending items
- Uncommitted git changes count

### 5. External Services

Quick connectivity check (non-blocking, skip on timeout):

| Service | Check Method |
|---------|-------------|
| Slack | Verify `SLACK_BOT_TOKEN` format |
| Notion | Check MCP server availability |
| GitHub | `gh auth status` |
| gbrain doctor | `~/.local/bin/gbrain doctor --json` (connectivity, schema, page count, stale embeddings) |
| gbrain health | `~/.local/bin/gbrain health --json` (composite 0-100 across freshness, links, embeddings, citations, filing, compiled truths) |
| gbrain features | `~/.local/bin/gbrain features --json` (v0.10 capability status: signal_detection, brain_first_lookup, citation_enforcement, filing_protocol, autopilot, webhook_transforms, cron_scheduler, acl) |
| gbrain autopilot | `~/.local/bin/gbrain autopilot status --json` (daemon running, last_sync, last_extract, last_embed) |

## Execution Flow

### Step 1: Run All Checks (parallel where possible)

Execute checks in categories 1-5. Each check returns:
- `PASS`: requirement met
- `WARN`: degraded but workable
- `FAIL`: blocking issue
- `SKIP`: check not applicable

### Step 2: Generate Report

```markdown
# Session Preflight Report
**Date:** YYYY-MM-DD HH:MM
**Overall:** READY / DEGRADED / BLOCKED

## Results

| Category | Status | Details |
|----------|--------|---------|
| Environment | PASS | Python 3.12, Node 20, 45GB free |
| API Keys | WARN | SLACK_USER_TOKEN missing |
| Data Freshness | PASS | All data < 3 days old |
| Pending Items | WARN | 5 inbox items, 2 todo items |
| Services | PASS | Slack, Notion, GitHub OK |
| gbrain | PASS | Health 85/100, Autopilot running, 0 stale truths |

## Action Items
1. [WARN] Set SLACK_USER_TOKEN for orphan cleanup
2. [WARN] Process 5 pending inbox items

## Recommendation
Environment is READY with minor warnings. Proceed with daily pipeline.
```

### Step 3: Recommend Next Action

Based on findings, suggest the most productive first action:
- If data stale: "Run `weekly-stock-update` first"
- If inbox full: "Process inbox before adding more items"
- If batch errors: "Retry failed batch items"
- If gbrain health < 50: "Run `gbrain-maintain` to fix brain health"
- If gbrain autopilot down: "Restart autopilot with `gbrain autopilot start`"
- If stale compiled truths: "Run `gbrain compile` on stale topics"
- If all clear: "Ready for daily pipeline"

## Output

- Report printed to console (not saved to file unless requested)
- If `BLOCKED`: list blocking issues with fix instructions
- If `DEGRADED`: list warnings with optional fixes
- If `READY`: single confirmation line

## Integration Points

- **morning-ship**: Runs preflight as first step
- **daily-am-orchestrator**: Phase 0 pre-flight
- **setup-doctor**: Delegates to setup-doctor for deep environment issues
- **pipeline-inbox**: Checks inbox queue depth
- **batch-agent-runner**: Checks for stale running items
- **gbrain**: Full v0.10 diagnostic (doctor + health score + features + autopilot + stale compiled truths)

## Constraints

- Total preflight must complete in < 30 seconds
- Never attempt to fix issues automatically (report only)
- Never read or display credential values
- Skip checks gracefully if a tool is unavailable
- Do not block the session on WARN items
