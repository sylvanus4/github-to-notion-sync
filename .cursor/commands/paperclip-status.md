## Paperclip Status

Show the Paperclip dashboard: agent status, pending approvals, costs, and stale tasks.

### Usage

```
/paperclip-status                    # full dashboard overview
/paperclip-status agents             # agent list with status
/paperclip-status approvals          # pending approvals only
/paperclip-status costs              # cost summary
/paperclip-status activity           # recent activity log
```

### Workflow

1. **Parse scope** — determine what to show from `$ARGUMENTS` (default: full dashboard)
2. **Fetch data** — run appropriate CLI commands or REST calls
3. **Present** — formatted summary with counts, status, and actionable items

### Execution

Read and follow the `paperclip-control` skill (`.cursor/skills/paperclip-control/SKILL.md`) for CLI commands and API endpoints.

### Examples

Full dashboard:
```
/paperclip-status
```

Check only pending approvals:
```
/paperclip-status approvals
```
