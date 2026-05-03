---
name: commit-to-issue
description: Analyze recent git commits and create GitHub issues with ThakiCloud Project #5 field setup.
disable-model-invocation: true
---

Convert recent git commits into tracked GitHub issues.

## Process

1. **Analyze commits**: Read `git log` for recent commits (default: since last push)
2. **Group by feature**: Cluster related commits into logical work units
3. **Create issues**: For each group, create a GitHub issue via `gh issue create`
4. **Project setup**: Add each issue to ThakiCloud Project #5
5. **Set 5 fields**: Status, Priority, Size, Sprint, Estimate

## Issue Format

```
Title: <type>: <summary from commits>
Body:
- Commits included: [list of SHAs]
- Changes: [file-level summary]
- Impact: [affected components]
```

## Field Defaults

| Field | Default |
|-------|---------|
| Status | Done |
| Priority | Medium |
| Size | S |
| Sprint | Current week |
| Estimate | 1 |

## Rules

- Use `gh project item-add 5 --owner ThakiCloud` for project linking
- Never skip project field setup
- Group related commits — don't create 1:1 commit-to-issue mapping
