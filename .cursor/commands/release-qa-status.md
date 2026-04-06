---
description: "Track QA results and enforce the Wednesday quality gate for the weekly release"
---

# Release QA Status — Wednesday QA Gate

## Skill Reference

Read and follow the skill at `.cursor/skills/release/release-qa-gate/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: show current QA status for this week's release
- `record`: interactively record QA results for each item
- `enforce`: close the gate — items without QA results are set to Hold
- `--skip-slack`: update Notion without posting to Slack
- `--skip-gate`: record results without enforcing the gate

### Examples

```
/release-qa-status                  # show current QA status
/release-qa-status record           # record QA results interactively
/release-qa-status enforce          # close the gate (Wednesday EOD)
/release-qa-status enforce --skip-slack   # enforce without Slack notification
```
