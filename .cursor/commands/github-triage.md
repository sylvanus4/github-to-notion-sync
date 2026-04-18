## GitHub Triage

Auto-triage incoming GitHub issues and PRs: classify by type, assign priority, suggest assignees, and update project fields.

### Usage

```
/github-triage                         # triage all open unassigned issues
/github-triage --prs                   # include pull requests
/github-triage --since yesterday       # only recent items
/github-triage --dry-run               # preview assignments without applying
```

### Workflow

1. **Fetch** — Collect open issues and PRs from GitHub
2. **Classify** — Categorize by type (bug, feature, chore, question)
3. **Prioritize** — Assign P0-P3 priority based on labels, content, and impact
4. **Route** — Suggest assignees from CODEOWNERS and git blame
5. **Update** — Apply labels, priority, and assignee to GitHub project fields
6. **Report** — Per-user digest of newly assigned items

### Execution

Read and follow the `sprint-orchestrator` skill (`.cursor/skills/review/sprint-orchestrator/SKILL.md`) for auto-triage, classification, priority assignment, and project field updates.

### Examples

Full triage pass:
```
/github-triage
```

Preview triage without applying:
```
/github-triage --dry-run --since "3 days ago"
```
