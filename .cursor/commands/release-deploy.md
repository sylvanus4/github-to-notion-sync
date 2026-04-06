---
description: "Run Thursday deployment operations — lock release list, announce, track, and confirm deployment"
---

# Release Deploy — Thursday Deployment

## Skill Reference

Read and follow the skill at `.cursor/skills/release/release-deployer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: run full Thursday deployment lifecycle (lock → announce → track → confirm)
- `lock`: lock the release list only
- `announce`: post pre-deploy announcement to Slack
- `confirm`: post post-deploy confirmation and collect improvement points
- `--skip-slack`: suppress Slack announcements
- `--deploy-time <HH:MM>`: override default deployment time (default: 14:00 KST)

### Examples

```
/release-deploy                     # full Thursday deployment lifecycle
/release-deploy lock                # lock the release list
/release-deploy announce            # post pre-deploy announcement
/release-deploy confirm             # post-deploy confirmation + retrospective
/release-deploy --deploy-time 16:00 # deploy at 4 PM instead of 2 PM
```
