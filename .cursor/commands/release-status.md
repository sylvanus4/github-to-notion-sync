---
description: "Show the current weekly release cycle status — collection, QA, deployment, and hotfix overview"
---

# Release Status — Cycle Overview

## Skill Reference

Read and follow the skill at `.cursor/skills/release/release-ops-orchestrator/SKILL.md` (Mode 3: Status Overview).

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: show current week's release status
- `--post`: post the status report to `#release-control`
- `--week <YYYY-MM-DD>`: show status for a specific week (Monday date)
- `--verbose`: include per-item details

### Examples

```
/release-status                     # current week status
/release-status --post              # post status to Slack
/release-status --week 2026-03-30   # status for a specific week
/release-status --verbose           # detailed per-item breakdown
```
