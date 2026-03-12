---
name: paperclip-agents
description: >-
  Create, configure, and operate Paperclip agents with heartbeat scheduling,
  budget enforcement, and runtime skill injection. Use when the user asks to
  "create a paperclip agent", "hire an agent", "run heartbeat", "set agent
  budget", "inject skills", "pause agent", "resume agent", "에이전트 생성",
  "하트비트 실행", "예산 설정", "에이전트 예산", "에이전트 일시정지",
  "paperclip agent create", "paperclip heartbeat", or any agent lifecycle
  operation. Do NOT use for task/issue management (use paperclip-tasks). Do NOT
  use for company/goal/approval oversight or company budgets (use
  paperclip-control). Do NOT use for installation (use paperclip-setup).
metadata:
  author: thaki
  version: "1.0.0"
  category: execution
---

# Paperclip Agents — Agent Setup and Operations

Create agents, configure adapters, manage heartbeats, enforce budgets, and inject skills at runtime.

## Prerequisites

- Paperclip server running (default `http://localhost:3100`). If not running, see `paperclip-setup`.
- CLI available via `pnpm paperclipai` from `~/work/thakicloud/paperclip/`
- Context profile configured with `company-id`. See `paperclip-control` for environment setup.
- Set `API_BASE` and `API_KEY` env vars for curl examples (see `paperclip-control`).

## Agent Adapter Types

| Adapter | Description | Key Config |
|---------|-------------|------------|
| `process` | Spawn local child process | `command`, `args`, `cwd`, `env`, `timeoutSec` |
| `claude_local` | Claude Code local agent | `cwd`, `model`, `instructionsFilePath` |
| `codex_local` | OpenAI Codex local agent | `cwd`, `model` |
| `cursor_local` | Cursor agent (local) | `cwd`, `model` |
| `opencode_local` | OpenCode local agent | `cwd`, `model` |
| `http` | External webhook agent | `url`, `method`, `headers`, `payloadTemplate` |
| `openclaw` | OpenClaw SSE/webhook | `callbackUrl`, `paperclipApiUrl` |

Full JSON examples for each adapter: `references/adapter-configs.md`.

## Workflow

### 1. Discover Adapter Options

Before creating an agent, check available adapter configurations:

```bash
curl -sS "$API_BASE/llms/agent-configuration.txt" -H "Authorization: Bearer $API_KEY"
curl -sS "$API_BASE/llms/agent-configuration/claude_local.txt" -H "Authorization: Bearer $API_KEY"
curl -sS "$API_BASE/llms/agent-icons.txt" -H "Authorization: Bearer $API_KEY"
```

Compare existing agent configs:

```bash
curl -sS "$API_BASE/api/companies/<company-id>/agent-configurations" \
  -H "Authorization: Bearer $API_KEY"
```

### 2. Create Agent (Hire Request)

Submit a hire request (goes through governance approval):

```bash
curl -sS -X POST "$API_BASE/api/companies/<company-id>/agent-hires" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "frontend-dev",
    "role": "engineer",
    "title": "Frontend Engineer",
    "icon": "code",
    "reportsTo": "<manager-agent-id>",
    "capabilities": "React, TypeScript, Tailwind CSS development",
    "adapterType": "claude_local",
    "adapterConfig": {
      "cwd": "/path/to/project",
      "model": "claude-sonnet-4-20250514"
    },
    "runtimeConfig": {
      "heartbeat": {
        "enabled": true,
        "intervalSec": 300,
        "wakeOnDemand": true
      }
    },
    "sourceIssueId": "<issue-id>"
  }'
```

If governance is enabled, the response includes an `approval` object with `pending_approval` status. Monitor via `paperclip-control` skill.

### 3. Agent API Keys

Agents authenticate with Bearer tokens. Keys are hashed at rest (SHA-256).

```bash
# Create a new API key for an agent
curl -sS -X POST "$API_BASE/api/agents/<agent-id>/keys" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 4. Run Heartbeat

Heartbeats are short execution windows. The agent wakes, checks assignments, works, and exits.

```bash
pnpm paperclipai heartbeat run --agent-id <agent-id> \
  [--api-base http://localhost:3100] \
  [--api-key <token>]
```

Via REST:

```bash
curl -sS -X POST "$API_BASE/api/agents/<agent-id>/heartbeat/invoke" \
  -H "Authorization: Bearer $API_KEY"
```

Heartbeat states: `queued` → `running` → `succeeded` | `failed` | `cancelled` | `timed_out`.

Skip conditions: agent paused/terminated, active run already exists, budget exceeded.

### 5. Budget Management

```bash
# Set agent monthly budget (in cents)
curl -sS -X PATCH "$API_BASE/api/agents/<agent-id>/budgets" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"budgetMonthlyCents": 50000}'
```

Budget rules:
- **80% threshold**: Soft alert — agent should focus on critical tasks only
- **100% threshold**: Hard pause — agent is auto-paused, no new checkouts

For company-level budgets, see `paperclip-control`.

### 6. Cost Event Ingestion

Report token usage after agent work:

```bash
curl -sS -X POST "$API_BASE/api/companies/<company-id>/cost-events" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agentId": "<agent-id>",
    "issueId": "<issue-id>",
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "inputTokens": 15000,
    "outputTokens": 3000,
    "costCents": 12
  }'
```

### 7. Runtime Skill Injection

Agents load skills at runtime without retraining:

```bash
# List available skills
curl -sS "$API_BASE/api/skills/index" -H "Authorization: Bearer $API_KEY"

# Get specific skill content
curl -sS "$API_BASE/api/skills/paperclip" -H "Authorization: Bearer $API_KEY"
```

Skills are markdown files resolved from `skills/` directories.

### 8. Set Agent Instructions Path

```bash
curl -sS -X PATCH "$API_BASE/api/agents/<agent-id>/instructions-path" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "agents/frontend-dev/AGENTS.md"}'
```

Relative paths resolve against the agent's `adapterConfig.cwd`.

### 9. Agent Lifecycle

```bash
# Pause agent
curl -sS -X POST "$API_BASE/api/agents/<agent-id>/pause" -H "Authorization: Bearer $API_KEY"

# Resume agent
curl -sS -X POST "$API_BASE/api/agents/<agent-id>/resume" -H "Authorization: Bearer $API_KEY"

# Terminate agent
curl -sS -X POST "$API_BASE/api/agents/<agent-id>/terminate" -H "Authorization: Bearer $API_KEY"
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Heartbeat skipped | Agent paused or budget exceeded | Resume agent or increase budget |
| `409` on heartbeat invoke | Active run already exists | Wait for current run to complete |
| Agent not waking | Heartbeat disabled in runtimeConfig | Set `heartbeat.enabled: true` |
| Cost events rejected | Invalid `agentId` or `issueId` | Verify IDs exist in the company |
| Hire request pending | Governance approval required | Approve via `paperclip-control` |
| Invalid `adapterType` | Unsupported adapter | Check `$API_BASE/llms/agent-configuration.txt` |
| `400` on hire request | Invalid `adapterConfig` payload | Validate against adapter-specific docs |

## References

- `references/adapter-configs.md` — Full JSON examples for all adapter types and injected env vars

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard
- `paperclip-tasks` — Issue/task CRUD and checkout
- `paperclip-setup` — Installation and configuration

## Examples

### Example 1: Standard usage

**User says:** "Create a paperclip agent"

**Actions:**
1. Gather necessary context from the project and user
2. Execute the skill workflow as documented above
3. Deliver results and verify correctness