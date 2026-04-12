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
  version: "2.0.0"
  category: execution
---

# Paperclip Agents — Agent Setup and Operations (MCP-Integrated)

Create agents, manage heartbeats, enforce budgets, and track costs via MCP tools.
**v2.0**: Core operations use MCP tools; heartbeat integrated with daily pipeline.

## Prerequisites

- Paperclip server running at `http://localhost:3100`. If not, see `paperclip-setup`.
- `paperclip-mcp` server registered in `.cursor/mcp.json`
- ThakiCloud company ID: `b573bdbe-785a-4f39-b1e9-f2b623e40a92`

## Agent Adapter Types

| Adapter | Description | Key Config |
|---------|-------------|------------|
| `process` | Spawn local child process | `command`, `args`, `cwd`, `env` |
| `claude_local` | Claude Code local agent | `cwd`, `model`, `instructionsFilePath` |
| `codex_local` | OpenAI Codex local agent | `cwd`, `model` |
| `cursor_local` | Cursor agent (local) | `cwd`, `model` |
| `http` | External webhook agent | `url`, `method`, `headers` |

## Workflow (MCP-First)

### 1. List Agents

```
Tool: paperclip_list_agents
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

### 2. Create Agent (Hire Request)

Submit via CLI (goes through governance approval):

```bash
cd ~/work/thakicloud/paperclip
curl -sS -X POST "http://localhost:3100/api/companies/b573bdbe-785a-4f39-b1e9-f2b623e40a92/agent-hires" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "frontend-dev",
    "role": "engineer",
    "title": "Frontend Engineer",
    "adapterType": "cursor_local",
    "adapterConfig": { "cwd": "/Users/hanhyojung/work/thakicloud/ai-platform-webui" },
    "runtimeConfig": { "heartbeat": { "enabled": true, "intervalSec": 300 } }
  }'
```

Monitor approval status via `paperclip_list_approvals` MCP tool.

### 3. Send Heartbeat

Use MCP tool `paperclip_heartbeat`:

```
Tool: paperclip_heartbeat
Input: { "agentId": "<agent-uuid>", "status": "active — processing daily pipeline" }
```

**Daily pipeline integration**: The `daily-am-orchestrator` should call `paperclip_heartbeat` for each registered agent during Phase 0.5 to keep agents alive and report status.

### 4. Cost Tracking

Use MCP tool `paperclip_log_cost` after any agent work:

```
Tool: paperclip_log_cost
Input: {
  "agentId": "<agent-uuid>",
  "amountCents": 12,
  "description": "daily-stock-check analysis run",
  "metadata": { "provider": "anthropic", "model": "claude-sonnet-4-20250514", "inputTokens": 15000, "outputTokens": 3000 }
}
```

**MEMORY.md integration**: After logging costs, update `memory/topics/workspace-facts.md` with cumulative daily spend if it exceeds the soft alert threshold (80% of monthly budget).

### 5. Budget Check

Use MCP tool `paperclip_get_budget`:

```
Tool: paperclip_get_budget
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

Budget rules:
- **80% threshold**: Soft alert — record in MEMORY.md, notify Slack
- **100% threshold**: Hard pause — do not spawn expensive subagents

### 6. Agent Lifecycle (CLI)

```bash
cd ~/work/thakicloud/paperclip

# Pause agent
curl -sS -X POST "http://localhost:3100/api/agents/<agent-id>/pause"

# Resume agent
curl -sS -X POST "http://localhost:3100/api/agents/<agent-id>/resume"

# Terminate agent
curl -sS -X POST "http://localhost:3100/api/agents/<agent-id>/terminate"
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `paperclip_list_agents` | List all agents in company |
| `paperclip_heartbeat` | Keep agent alive, update status |
| `paperclip_log_cost` | Record cost event (tokens, API calls) |
| `paperclip_get_budget` | Check remaining budget |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Heartbeat skipped | Agent paused or budget exceeded | Resume agent or increase budget |
| `409` on heartbeat | Active run already exists | Wait for current run to complete |
| Cost events rejected | Invalid `agentId` | Verify with `paperclip_list_agents` |
| Hire request pending | Governance approval required | Approve via `paperclip-control` |

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard (MCP-integrated)
- `paperclip-tasks` — Issue/task CRUD and checkout (MCP-integrated)
- `paperclip-setup` — Installation and configuration
- `paperclip-bridge` — Bidirectional sync between mission-control and Paperclip
