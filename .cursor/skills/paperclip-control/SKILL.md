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
  version: "1.0.0"
  category: execution
---

# Paperclip Control — Core Orchestration

Manage the Paperclip control plane: companies, agents, goals, approvals, costs, and dashboard overview.

## Prerequisites

- Paperclip server running (default `http://localhost:3100`). If not running, see `paperclip-setup`.
- CLI available via `pnpm paperclipai` from `~/work/thakicloud/paperclip/`
- Context profile configured (or use `--api-base` / `--company-id` flags)

## Environment

Set these before using curl examples:

```bash
export API_BASE="http://localhost:3100"
export API_KEY="<your-api-key>"  # or from context: pnpm paperclipai context show
```

Or configure a persistent context profile:

```bash
cd ~/work/thakicloud/paperclip
pnpm paperclipai context set --api-base http://localhost:3100 --company-id <company-id>
pnpm paperclipai context show
```

All CLI commands inherit `api-base` and `company-id` from the active context.

## Workflow

### 1. Dashboard Overview

```bash
pnpm paperclipai dashboard get --company-id <company-id>
```

Returns: agent count, active/paused/terminated counts, pending approvals, total spend, stale tasks, recent activity.

### 2. Company Management

```bash
pnpm paperclipai company list
pnpm paperclipai company get <company-id>
pnpm paperclipai company delete <id-or-prefix> --yes --confirm <same-id-or-prefix>
```

Company deletion requires server-side `PAPERCLIP_ENABLE_COMPANY_DELETION=true`.

### 3. Agent Overview

```bash
pnpm paperclipai agent list --company-id <company-id>
pnpm paperclipai agent get <agent-id>
```

For agent lifecycle operations (pause/resume/terminate), heartbeats, and agent budgets, see `paperclip-agents`.

### 4. Goal Management

Goals align all work to the company mission. Levels: `company`, `team`, `agent`, `task`.

```bash
# List goals
curl -sS "$API_BASE/api/companies/<company-id>/goals" -H "Authorization: Bearer $API_KEY"

# Create goal
curl -sS -X POST "$API_BASE/api/companies/<company-id>/goals" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"...","level":"company","description":"..."}'

# Update goal
curl -sS -X PATCH "$API_BASE/api/goals/<goal-id>" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title"}'
```

### 5. Approval Governance

```bash
pnpm paperclipai approval list --company-id <company-id> [--status pending]
pnpm paperclipai approval get <approval-id>
pnpm paperclipai approval approve <approval-id> [--decision-note "Approved"]
pnpm paperclipai approval reject <approval-id> [--decision-note "Not now"]
pnpm paperclipai approval request-revision <approval-id> [--decision-note "Revise config"]
pnpm paperclipai approval resubmit <approval-id> [--payload '{"...":"..."}']
pnpm paperclipai approval comment <approval-id> --body "Discussion note"
```

Approval types: `hire_agent`, `approve_ceo_strategy`.

### 6. Cost and Budget Overview

```bash
# Summary
curl -sS "$API_BASE/api/companies/<company-id>/costs/summary" -H "Authorization: Bearer $API_KEY"

# By agent
curl -sS "$API_BASE/api/companies/<company-id>/costs/by-agent" -H "Authorization: Bearer $API_KEY"

# By project
curl -sS "$API_BASE/api/companies/<company-id>/costs/by-project" -H "Authorization: Bearer $API_KEY"

# Update company budget
curl -sS -X PATCH "$API_BASE/api/companies/<company-id>/budgets" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"monthlyBudgetCents": 100000}'
```

For agent-level budgets, see `paperclip-agents`. Budget rules: soft alert at 80%, hard pause at 100%.

### 7. Activity Log

```bash
pnpm paperclipai activity list --company-id <company-id> [--agent-id <id>] [--entity-type issue]
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ECONNREFUSED` on `:3100` | Server not running | `cd ~/work/thakicloud/paperclip && pnpm dev` |
| `401 Unauthorized` | Missing or invalid API key | Set `--api-key` or configure context |
| `403 Forbidden` | Valid token but insufficient permissions | Check agent role and company scope |
| `404` on company endpoints | Wrong `company-id` | Run `pnpm paperclipai company list` |
| `429 Too Many Requests` | Rate limited | Wait and retry with backoff |
| Approval stuck in `pending` | Board has not reviewed | Check dashboard, notify board |

## References

- `references/api-endpoints.md` — Full REST API endpoint reference
- `references/cli-commands.md` — Complete CLI command reference

## Related Skills

- `paperclip-tasks` — Issue/task CRUD and checkout
- `paperclip-agents` — Agent creation, heartbeats, budgets
- `paperclip-setup` — Installation and configuration

## Examples

### Example 1: Standard usage

**User says:** "Check paperclip status"

**Actions:**
1. Gather necessary context from the project and user
2. Execute the skill workflow as documented above
3. Deliver results and verify correctness