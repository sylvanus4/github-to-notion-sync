---
description: "Run the weekly release operations loop — auto-routes to the correct phase based on day of week"
---

# Release Ops — Weekly Release Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/release/release-ops-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: auto-route based on today's day of week (KST)
- `collect`: force Tuesday collection phase
- `qa`: force Wednesday QA gate phase
- `deploy`: force Thursday deployment phase
- `hotfix`: hotfix management (any day)
- `status`: show current release cycle status
- `--force`: run a phase outside its scheduled day
- `--skip-slack`: suppress Slack notifications
- `--skip-notion`: suppress Notion updates

### Examples

```
/release-ops                    # auto-route to today's phase
/release-ops status             # show current cycle status
/release-ops collect            # run Tuesday collection
/release-ops qa                 # run Wednesday QA gate
/release-ops deploy             # run Thursday deployment
/release-ops hotfix             # manage hotfixes
/release-ops collect --force    # run collection on a non-Tuesday
```
