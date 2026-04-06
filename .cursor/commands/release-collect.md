---
description: "Collect and validate release candidate PRs for the weekly Thursday deployment"
---

# Release Collect — Tuesday PR Collection

## Skill Reference

Read and follow the skill at `.cursor/skills/release/release-collector/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: scan all configured repos for `release:thu` PRs
- `--repo <owner/repo>`: scan a specific repository only
- `--skip-notion`: collect and validate without updating Notion
- `--skip-slack`: collect without posting to Slack
- `--dry-run`: validate PRs and show report without any side effects

### Examples

```
/release-collect                                    # full Tuesday collection
/release-collect --repo thakicloud/ai-platform      # scan one repo
/release-collect --dry-run                          # preview without updates
/release-collect --skip-slack                       # collect without Slack post
```
