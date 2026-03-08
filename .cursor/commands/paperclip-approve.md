## Paperclip Approve

List and manage pending Paperclip governance approvals — approve, reject, or request revisions.

### Usage

```
/paperclip-approve                           # list pending approvals
/paperclip-approve list [--status pending]   # list with filter
/paperclip-approve get <approval-id>         # approval details
/paperclip-approve approve <approval-id>     # approve
/paperclip-approve reject <approval-id>      # reject
/paperclip-approve revise <approval-id>      # request revision
/paperclip-approve comment <approval-id> "Note"  # add comment
```

### Workflow

1. **Parse action** — determine operation from `$ARGUMENTS` (default: list pending)
2. **Fetch approvals** — get pending approvals with linked issues
3. **Present for decision** — show approval details, payload, and context
4. **Execute decision** — approve, reject, or request revision
5. **Report** — confirmation with approval status

### Execution

Read and follow the `paperclip-control` skill (`.cursor/skills/paperclip-control/SKILL.md`) for approval commands.

### Examples

List all pending approvals:
```
/paperclip-approve
```

Approve an agent hire:
```
/paperclip-approve approve <approval-id> --decision-note "Approved"
```
