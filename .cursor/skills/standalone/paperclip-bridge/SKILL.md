---
name: paperclip-bridge
description: >-
  Bidirectional sync orchestrator between mission-control's tasks/todo.md and
  Paperclip issues. Ensures both systems stay in sync: new todo items create
  Paperclip issues, completed Paperclip issues mark todos as done, and status
  changes propagate in both directions. Use when the user asks to "sync
  paperclip", "bridge tasks", "sync todo with paperclip", "paperclip bridge",
  "태스크 동기화", "페이퍼클립 브릿지", "todo paperclip sync", or any request
  to synchronize work items between mission-control and Paperclip. Do NOT use
  for Paperclip-only task management (use paperclip-tasks). Do NOT use for
  mission-control-only orchestration (use mission-control). Do NOT use for
  Paperclip installation (use paperclip-setup).
metadata:
  author: thaki
  version: "1.0.0"
  category: orchestration
---

# Paperclip Bridge — Bidirectional Task Sync

Orchestrate bidirectional synchronization between `tasks/todo.md` (mission-control)
and Paperclip issues (agent orchestration platform).

## Prerequisites

- Paperclip server running at `http://localhost:3100` (see `paperclip-setup`)
- `paperclip-mcp` server registered in `.cursor/mcp.json`
- ThakiCloud company ID: `b573bdbe-785a-4f39-b1e9-f2b623e40a92`
- `tasks/todo.md` exists in the project root

## Sync Model

```
tasks/todo.md  <──── paperclip-bridge ────>  Paperclip Issues
  (source of truth         (bidirectional)        (agent tracking
   for planning)                                   + governance)
```

### Direction 1: todo.md → Paperclip

When new items appear in `tasks/todo.md` that don't have a Paperclip issue:

1. Read `tasks/todo.md` and parse unchecked `- [ ]` items
2. For each item without a `[PC:xxx]` annotation:
   - Call `paperclip_create_issue` with the item text as title
   - Annotate the todo item with `[PC:<issue-id>]` suffix
3. Write back the annotated `tasks/todo.md`

### Direction 2: Paperclip → todo.md

When Paperclip issues are completed that correspond to todo items:

1. Call `paperclip_list_issues` to get all company issues
2. Filter for `status: done` or `status: cancelled`
3. For each completed issue, find the matching `[PC:<id>]` in `tasks/todo.md`
4. Mark the item as `- [x]` and move to Completed section with date stamp

### Status Mapping

| todo.md | Paperclip Issue |
|---------|----------------|
| `- [ ]` (unchecked) | `todo` or `backlog` |
| `- [ ]` (in Current Tasks) | `in_progress` |
| `- [x]` (checked) | `done` |
| Removed/deleted | `cancelled` |

## Workflow

### Full Sync

Execute both directions sequentially:

1. **Read** `tasks/todo.md` — parse all items with/without `[PC:xxx]` annotations
2. **Fetch** Paperclip issues via `paperclip_list_issues`
3. **Create** missing Paperclip issues for unannotated todo items
4. **Update** todo items whose Paperclip issues have changed status
5. **Write** updated `tasks/todo.md`
6. **Report** sync summary: N created, M completed, K status-updated

### Mission-Control Task Delegation

When `mission-control` delegates work through `paperclip-bridge`:

1. Create todo item in `tasks/todo.md`
2. Call `paperclip_create_issue` → get `issueId`
3. Call `paperclip_checkout_issue` → atomic lock
4. Delegate to subagent
5. On completion: `paperclip_update_issue(status: done)` + `paperclip_release_issue`
6. Mark todo as `- [x]` in `tasks/todo.md`

### Annotation Format

Todo items are annotated with Paperclip issue IDs:

```markdown
## Current Tasks

- [ ] Implement cost dashboard [PC:a1b2c3d4-e5f6-7890-abcd-ef1234567890]
- [ ] Add approval workflow [PC:b2c3d4e5-f6a7-8901-bcde-f12345678901]
- [ ] Fix memory leak (no Paperclip tracking needed)

## Completed

### Sprint 2026-W15 (Completed: 2026-04-10)

- [x] Build MCP bridge server [PC:c3d4e5f6-a7b8-9012-cdef-123456789012]
```

## MCP Tools Used

| Tool | Usage |
|------|-------|
| `paperclip_list_issues` | Fetch current Paperclip issue states |
| `paperclip_create_issue` | Create issues for new todo items |
| `paperclip_update_issue` | Sync status changes |
| `paperclip_checkout_issue` | Lock issue for active work |
| `paperclip_release_issue` | Release issue after work |

## Conflict Resolution

When both sides have changed:

1. **Paperclip wins for status** — if Paperclip says `done` but todo says unchecked, mark todo as done
2. **todo.md wins for existence** — if a todo item is deleted, cancel the Paperclip issue
3. **Neither wins for content** — if both title/body changed, keep both and flag for human review

## Examples

### Example 1: Initial sync

**User says:** "Sync my todos with Paperclip"

**Actions:**
1. Read `tasks/todo.md`
2. Call `paperclip_list_issues` to get existing issues
3. Create Paperclip issues for unannotated items
4. Update completed items from Paperclip status
5. Write back annotated `tasks/todo.md`
6. Report: "Created 3 issues, marked 1 as done, 5 already synced"

### Example 2: Post-pipeline sync

**User says:** "Bridge tasks after today pipeline"

**Actions:**
1. Read pipeline outputs to identify completed work
2. Update corresponding Paperclip issues to `done`
3. Log costs via `paperclip_log_cost` for each completed analysis
4. Sync todo.md to reflect completions
5. Post summary to Slack

## Related Skills

- `paperclip-tasks` — Individual issue CRUD (MCP-integrated)
- `paperclip-control` — Dashboard, approvals, governance
- `paperclip-agents` — Agent lifecycle, heartbeats, costs
- `mission-control` — Multi-skill workflow orchestration
