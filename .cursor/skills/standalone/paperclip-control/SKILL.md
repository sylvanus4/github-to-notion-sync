---
name: paperclip-control
description: >-
  Interact with the Paperclip control plane to manage companies, goals,
  approvals, and dashboard overview. Use when the user asks to "check
  paperclip status", "list companies", "approve agent hire", "view org chart",
  "paperclip dashboard", "view costs", "paperclip approve", "페이퍼클립 상태",
  "회사 목록", "에이전트 승인", "paperclip 비용", "예산 조회", "활동 로그",
  or any Paperclip governance and oversight task. Do NOT use for task/issue
  CRUD (use paperclip-tasks). Do NOT use for agent creation, heartbeats, agent
  budgets, or agent lifecycle (use paperclip-agents). Do NOT use for
  installation or deployment (use paperclip-setup).
metadata:
  author: thaki
  version: "2.0.0"
  category: execution
---

# Paperclip Control — Core Orchestration (MCP-Integrated)

Manage the Paperclip control plane via MCP tool calls: dashboard, agents, approvals, costs, and governance.
**v2.0**: All primary operations use MCP tools instead of curl/CLI.

## Prerequisites

- Paperclip server running at `http://localhost:3100`. If not, see `paperclip-setup`.
- `paperclip-mcp` server registered in `.cursor/mcp.json`
- ThakiCloud company ID: `b573bdbe-785a-4f39-b1e9-f2b623e40a92`

## Workflow (MCP-First)

### 1. Dashboard Overview

Use MCP tool `paperclip_dashboard`:

```
Tool: paperclip_dashboard
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

Returns: agent count, active/paused/terminated counts, pending approvals, total spend, stale tasks, recent activity.

### 2. List Agents

Use MCP tool `paperclip_list_agents`:

```
Tool: paperclip_list_agents
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

For agent lifecycle operations (pause/resume/terminate), heartbeats, and agent budgets, see `paperclip-agents`.

### 3. Approval Governance

**List pending approvals** via MCP:

```
Tool: paperclip_list_approvals
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

**Approve/reject** via CLI (approval mutations require board-level access):

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai approval approve <approval-id> --decision-note "Approved"
pnpm paperclipai approval reject <approval-id> --decision-note "Not now"
```

**Slack notification pattern**: After processing approvals, post a summary to Slack `#효정-할일`:

```
Tool: slack_send_message (plugin-slack-slack MCP)
Input: {
  "channel_id": "C0AA8NT4T8T",
  "text": "Paperclip Approvals: N pending, M approved today"
}
```

### 4. Budget Overview

Use MCP tool `paperclip_get_budget`:

```
Tool: paperclip_get_budget
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

Returns monthly budget, current spend, remaining balance, and per-agent breakdown.

### 5. Goal Management (CLI)

Goals align all work to the company mission. Levels: `company`, `team`, `agent`, `task`.

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai goal list --company-id <company-id>
pnpm paperclipai goal create --company-id <company-id> --title "..." --level company
```

### 6. Activity Log (CLI)

```bash
pnpm paperclipai activity list --company-id <company-id> [--agent-id <id>]
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `paperclip_dashboard` | Full company overview |
| `paperclip_list_agents` | All registered agents |
| `paperclip_list_approvals` | Pending approval requests |
| `paperclip_get_budget` | Budget and spend summary |
| `paperclip_log_cost` | Record a cost event |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| MCP tool returns connection error | Paperclip not running | See `paperclip-setup` auto-repair |
| `401 Unauthorized` | API key mismatch | Check `PAPERCLIP_API_KEY` in `.cursor/mcp.json` |
| `404` on company endpoints | Wrong `companyId` | Use `b573bdbe-785a-4f39-b1e9-f2b623e40a92` |
| Approval stuck in `pending` | Board has not reviewed | Check dashboard, process via CLI |

## Related Skills

- `paperclip-tasks` — Issue/task CRUD and checkout (MCP-integrated)
- `paperclip-agents` — Agent creation, heartbeats, budgets (MCP-integrated)
- `paperclip-setup` — Installation and configuration
- `paperclip-bridge` — Bidirectional sync between mission-control and Paperclip
