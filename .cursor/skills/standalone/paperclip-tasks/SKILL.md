---
name: paperclip-tasks
description: >-
  Create, assign, track, and manage Paperclip tasks (issues) with atomic
  checkout, delegation, and status transitions. Use when the user asks to
  "create a paperclip task", "list tasks", "assign task", "checkout issue",
  "update task status", "delegate work", "paperclip issue", "페이퍼클립 작업",
  "태스크 생성", "이슈 체크아웃", "태스크 할당", "작업 위임", "이슈 목록",
  or any Paperclip issue management operation. Do NOT use for company/agent/goal
  management (use paperclip-control). Do NOT use for agent creation or heartbeats
  (use paperclip-agents). Do NOT use for installation (use paperclip-setup).
metadata:
  author: thaki
  version: "1.0.0"
  category: execution
---

# Paperclip Tasks — Issue Management

Manage the full lifecycle of Paperclip issues: create, assign, checkout, update, comment, delegate, and release.

## Prerequisites

- Paperclip server running (default `http://localhost:3100`). If not running, see `paperclip-setup`.
- CLI available via `pnpm paperclipai` from `~/work/thakicloud/paperclip/`
- Context profile configured with `company-id`. See `paperclip-control` for environment setup.
- Set `API_BASE` and `API_KEY` env vars for curl examples (see `paperclip-control`).

## Issue Lifecycle

Status values: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`, `cancelled`.
Priority values: `critical`, `high`, `medium`, `low`.

For the full lifecycle diagram, blocked task protocol, and comment conventions, see `references/issue-lifecycle.md`.

## Workflow

### 1. List Issues

```bash
pnpm paperclipai issue list --company-id <company-id> \
  [--status todo,in_progress] \
  [--assignee-agent-id <agent-id>] \
  [--match "search text"]
```

Search with the `q` parameter via REST:

```bash
curl -sS "$API_BASE/api/companies/<company-id>/issues?q=dockerfile&status=todo" \
  -H "Authorization: Bearer $API_KEY"
```

### 2. Get Issue Details

```bash
pnpm paperclipai issue get <issue-id-or-identifier>
```

Returns: issue fields, project context, ancestor chain (parent hierarchy), workspace details.

### 3. Create Issue

```bash
pnpm paperclipai issue create --company-id <company-id> \
  --title "Implement cost dashboard" \
  [--description "Show per-agent token spend..."] \
  [--status todo] \
  [--priority high]
```

Via REST (with parent and goal linkage for subtasks):

```bash
curl -sS -X POST "$API_BASE/api/companies/<company-id>/issues" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement cost chart component",
    "description": "React component for per-agent spend visualization",
    "status": "todo",
    "priority": "medium",
    "parentId": "<parent-issue-id>",
    "goalId": "<goal-id>",
    "projectId": "<project-id>",
    "assigneeAgentId": "<agent-id>"
  }'
```

Always set `parentId` and `goalId` on subtasks.

### 4. Update Issue

```bash
pnpm paperclipai issue update <issue-id> \
  [--status in_progress] \
  [--comment "Starting work on this"]
```

Updatable fields: `title`, `description`, `status`, `priority`, `assigneeAgentId`, `projectId`, `goalId`, `parentId`, `billingCode`.

### 5. Atomic Checkout

**Critical**: Always checkout before working on a task. Checkout is atomic — returns `409 Conflict` if another agent owns the task.

```bash
pnpm paperclipai issue checkout <issue-id> --agent-id <agent-id> \
  [--expected-statuses todo,backlog,blocked]
```

Via REST:

```bash
curl -sS -X POST "$API_BASE/api/issues/<issue-id>/checkout" \
  -H "Authorization: Bearer $API_KEY" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -H "Content-Type: application/json" \
  -d '{"agentId":"<agent-id>","expectedStatuses":["todo","backlog","blocked"]}'
```

**Never retry a 409.** Pick a different task instead.

### 6. Release Task

Unassign a checked-out task:

```bash
pnpm paperclipai issue release <issue-id>
```

### 7. Comments

```bash
pnpm paperclipai issue comment <issue-id> --body "Progress update" [--reopen]
```

Via REST:

```bash
curl -sS -X POST "$API_BASE/api/issues/<issue-id>/comments" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"body":"## Update\n\n- Completed API integration\n- Next: add tests"}'
```

### 8. Delegation (Subtasks)

Create child issues to delegate work:

```bash
curl -sS -X POST "$API_BASE/api/companies/<company-id>/issues" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Write unit tests for cost API",
    "parentId": "<parent-issue-id>",
    "goalId": "<goal-id>",
    "assigneeAgentId": "<subordinate-agent-id>",
    "status": "todo",
    "priority": "medium"
  }'
```

Rules:
- Always set `parentId` to link to the parent task
- Always set `goalId` unless creating top-level company work
- Set `billingCode` for cross-team delegation
- Never cancel cross-team tasks — reassign to your manager instead

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `409 Conflict` on checkout | Task owned by another agent | Pick a different task; never retry |
| `404` on issue get | Wrong issue ID or identifier | Use `issue list` to find correct ID |
| `400` on create | Missing required fields | Ensure `title` and `company-id` are provided |
| Task stuck in `in_progress` | Agent paused or crashed | Release the task, then reassign |
| Missing parent chain | `parentId` not set on subtask | Update issue to set `parentId` |
| Invalid `goalId` or `projectId` | ID does not exist in company | Verify with `goal list` or `project list` via REST |

## References

- `references/issue-lifecycle.md` — Status transitions, blocked protocol, delegation rules, comment conventions

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard
- `paperclip-agents` — Agent creation, heartbeats, budgets
- `paperclip-setup` — Installation and configuration

## Examples

### Example 1: Standard usage

**User says:** "Create a paperclip task"

**Actions:**
1. Gather necessary context from the project and user
2. Execute the skill workflow as documented above
3. Deliver results and verify correctness
