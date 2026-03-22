---
description: "Auto-triage incoming GitHub issues and PRs — classify, prioritize, label, and suggest assignees"
---

## Sprint Triage

Automatically triage open issues and PRs: classify by type, assign priority, add labels, and suggest assignees.

### Usage

```
/sprint-triage                              # triage all untriaged issues/PRs
/sprint-triage --since yesterday            # only items created since yesterday
/sprint-triage --repo ThakiCloud/tkai-deploy # triage a specific repo
/sprint-triage --dry-run                    # preview triage decisions without applying
```

### Execution

Read and follow the skill at `.cursor/skills/sprint-orchestrator/SKILL.md`.

User input: $ARGUMENTS

1. Fetch untriaged issues and PRs via GitHub MCP
2. Classify each item (bug, feature, chore, urgent)
3. Assign priority and labels
4. Suggest assignees based on code ownership and workload
5. Update GitHub issues/PRs with triage results (unless `--dry-run`)
6. Post triage summary to Slack
