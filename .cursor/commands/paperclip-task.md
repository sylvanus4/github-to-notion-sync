## Paperclip Task

Create, update, checkout, and manage Paperclip tasks (issues).

### Usage

```
/paperclip-task list [--status todo,in_progress]     # list tasks
/paperclip-task create "Task title" [--priority high] # create task
/paperclip-task get <issue-id>                        # get task details
/paperclip-task update <issue-id> --status done       # update status
/paperclip-task checkout <issue-id> --agent-id <id>   # checkout for agent
/paperclip-task release <issue-id>                    # release checkout
/paperclip-task comment <issue-id> "Comment body"     # add comment
/paperclip-task delegate <issue-id> "Subtask title"   # create subtask
```

### Workflow

1. **Parse action** — determine operation from `$ARGUMENTS`
2. **Execute** — run CLI command or REST call
3. **Report** — show result with issue identifier and status

### Execution

Read and follow the `paperclip-tasks` skill (`.cursor/skills/paperclip-tasks/SKILL.md`) for issue lifecycle, checkout rules, and delegation patterns.

### Examples

Create a high-priority task:
```
/paperclip-task create "Fix authentication bug" --priority critical
```

Checkout and start working:
```
/paperclip-task checkout PAP-42 --agent-id frontend-dev
```
