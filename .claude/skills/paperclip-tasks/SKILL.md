---
name: paperclip-tasks
description: >-
  Create, assign, track, and manage Paperclip tasks (issues) with atomic
  checkout, delegation, and status transitions. Use when the user asks to
  "create a paperclip task", "list tasks", "assign task", "checkout issue",
  "update task status", "delegate work", "paperclip issue", "페이퍼클립 작업", "태스크
  생성", "이슈 체크아웃", "태스크 할당", "작업 위임", "이슈 목록", or any Paperclip issue
  management operation. Do NOT use for company/agent/goal management (use
  paperclip-control). Do NOT use for agent creation or heartbeats (use
  paperclip-agents). Do NOT use for installation (use paperclip-setup).
disable-model-invocation: true
---

# Paperclip Tasks — Issue Management (MCP-Integrated)

Manage the full lifecycle of Paperclip issues via MCP tools: create, checkout, update, release, and delegate.
**v2.0**: All CRUD operations use MCP tools; checkout/release integrated with mission-control task flow.

## Prerequisites

- Paperclip server running at `http://localhost:3100`. If not, see `paperclip-setup`.
- `paperclip-mcp` server registered in `.cursor/mcp.json`
- ThakiCloud company ID: `b573bdbe-785a-4f39-b1e9-f2b623e40a92`

## Issue Lifecycle

Status values: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`, `cancelled`.
Priority values: `critical`, `high`, `medium`, `low`.

## Workflow (MCP-First)

### 1. List Issues

```
Tool: paperclip_list_issues
Input: { "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92" }
```

### 2. Create Issue

```
Tool: paperclip_create_issue
Input: {
  "companyId": "b573bdbe-785a-4f39-b1e9-f2b623e40a92",
  "title": "Implement cost dashboard",
  "body": "Show per-agent token spend visualization",
  "priority": "high",
  "labels": ["frontend", "feature"]
}
```

### 3. Atomic Checkout

**Critical**: Always checkout before working on a task. Returns `409` if another agent owns it.

```
Tool: paperclip_checkout_issue
Input: { "issueId": "<issue-uuid>", "agentId": "<agent-uuid>" }
```

**Never retry a 409.** Pick a different task instead.

**Mission-control integration**: When `mission-control` delegates a sub-task, it should:
1. Call `paperclip_create_issue` with the task details
2. Call `paperclip_checkout_issue` to atomically claim it
3. Execute the work via subagent
4. Call `paperclip_update_issue` to set status to `done`
5. Call `paperclip_release_issue` to release the lock

### 4. Update Issue

```
Tool: paperclip_update_issue
Input: {
  "issueId": "<issue-uuid>",
  "status": "in_progress",
  "body": "Updated: completed API integration, starting tests"
}
```

### 5. Release Task

Unassign a checked-out task:

```
Tool: paperclip_release_issue
Input: { "issueId": "<issue-uuid>" }
```

### 6. Delegation (Subtasks)

Create child issues via `paperclip_create_issue` with parent context in the body.
Link to GitHub issues using the `pr-to-issue-linker` pattern:

1. Create Paperclip issue with `labels: ["github-synced"]`
2. Create corresponding GitHub issue via `gh issue create`
3. Include Paperclip issue ID in the GitHub issue body for cross-reference

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `paperclip_list_issues` | List all issues in company |
| `paperclip_create_issue` | Create new task/issue |
| `paperclip_checkout_issue` | Atomic task lock |
| `paperclip_release_issue` | Release task lock |
| `paperclip_update_issue` | Update status/fields |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `409 Conflict` on checkout | Task owned by another agent | Pick a different task |
| MCP tool returns connection error | Paperclip not running | See `paperclip-setup` |
| `400` on create | Missing required `title` | Ensure title is provided |
| Task stuck in `in_progress` | Agent crashed without releasing | Call `paperclip_release_issue` |

## Related Skills

- `paperclip-control` — Company, goals, approvals, dashboard (MCP-integrated)
- `paperclip-agents` — Agent creation, heartbeats, budgets (MCP-integrated)
- `paperclip-setup` — Installation and configuration
- `paperclip-bridge` — Bidirectional sync between mission-control and Paperclip
