---
description: "Submit, track, and deploy hotfixes outside the regular weekly release cycle"
---

# Release Hotfix — Hotfix Queue Management

## Skill Reference

Read and follow the skill at `.cursor/skills/release/hotfix-manager/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: show current hotfix queue status
- `submit <PR_URL>`: validate and submit a hotfix PR
- `qa <PR_NUMBER> <pass|fail>`: record QA result for a hotfix
- `deploy <PR_NUMBER>`: mark a hotfix as deployed
- `rollback <PR_NUMBER>`: mark a hotfix as rolled back
- `--skip-slack`: suppress Slack alerts
- `--skip-notion`: suppress Notion updates

### Examples

```
/release-hotfix                                              # show hotfix queue
/release-hotfix submit https://github.com/org/repo/pull/456  # submit a hotfix PR
/release-hotfix qa 456 pass                                  # record QA pass
/release-hotfix deploy 456                                   # mark as deployed
/release-hotfix rollback 456                                 # mark as rolled back
```
