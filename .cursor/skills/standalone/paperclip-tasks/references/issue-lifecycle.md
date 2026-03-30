# Paperclip Issue Lifecycle

## Status Transitions

```
                    ┌─────────────┐
                    │   backlog   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
             ┌──────│    todo     │──────┐
             │      └──────┬──────┘      │
             │             │             │
             │      ┌──────▼──────┐      │
             │      │ in_progress │◄─────┘
             │      └──┬──────┬───┘
             │         │      │
             │   ┌─────▼──┐   │
             │   │ blocked │   │
             │   └─────┬──┘   │
             │         │      │
             │   ┌─────▼──────▼──┐
             │   │   in_review   │
             │   └───────┬───────┘
             │           │
             │    ┌──────▼──────┐
             │    │    done     │
             │    └─────────────┘
             │
      ┌──────▼──────┐
      │  cancelled  │
      └─────────────┘
```

## Status Definitions

| Status | Description |
|--------|-------------|
| `backlog` | Unplanned work, not yet prioritized |
| `todo` | Ready to be picked up by an agent |
| `in_progress` | Agent has checked out and is working |
| `blocked` | Work cannot proceed; needs external action |
| `in_review` | Work completed, pending human or agent review |
| `done` | Completed and verified |
| `cancelled` | Abandoned or no longer needed |

## Priority Levels

| Priority | Description |
|----------|-------------|
| `critical` | Immediate attention required |
| `high` | Important, do soon |
| `medium` | Normal priority |
| `low` | Can wait |

## Checkout Rules

1. **Always checkout before working.** Use `POST /api/issues/:id/checkout`.
2. Checkout is **atomic** — only one agent can own a task.
3. `409 Conflict` = another agent owns it. **Never retry a 409.**
4. If already checked out by you, the call succeeds normally.
5. Include `X-Paperclip-Run-Id` header for audit trail.

## Delegation Rules

1. **Always set `parentId`** on subtasks to maintain the hierarchy.
2. **Always set `goalId`** (unless creating top-level company work).
3. Set `billingCode` for **cross-team** delegation.
4. **Never cancel cross-team tasks** — reassign to your manager instead.

## Blocked Task Protocol

1. When blocked, PATCH status to `blocked` with a comment explaining the blocker.
2. On subsequent heartbeats, check the comment thread first.
3. If no new context since your last blocked comment, **skip the task** (do not post another comment).
4. Re-engage only when new comments, status changes, or event-based wakes occur.

## Comment Convention

Use concise markdown:

```markdown
## Update

- Completed X
- Blocked on Y — need Z from @AgentName
- Next: A, B, C
```

## Issue Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Issue title |
| `description` | string | Detailed description |
| `status` | enum | Current status |
| `priority` | enum | Priority level |
| `assigneeAgentId` | uuid | Assigned agent |
| `assigneeUserId` | uuid | Assigned board user |
| `projectId` | uuid | Parent project |
| `goalId` | uuid | Linked goal |
| `parentId` | uuid | Parent issue (for subtasks) |
| `billingCode` | string | Cross-team billing code |
| `requestDepth` | number | Delegation depth |
| `identifier` | string | Human-readable ID (e.g., `PAP-123`) |
