---
description: "Check and install prerequisites for all project skills — CLI tools, packages, env vars, MCP servers"
---

# Setup Doctor

## Skill Reference

Read and follow the skill at `.cursor/skills/setup-doctor/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Mode Selection

Parse `$ARGUMENTS` for the mode:

- **No arguments** → Full scan of all 13 capability groups
- `--group <name>` → Check a single group (valid: core-platform, llm-apis, slack, notion, google-workspace, huggingface, notebooklm, twitter, browser, media, trading-apis, ci-cd, github)
- `--fix` → Full scan + auto-install missing CLI tools and packages
- `--env` → Environment variable check only (Phase 3)
- `--report` → Full scan + write report to `outputs/setup-doctor-report.md`
- `--slack` → Full scan + post report to Slack `#효정-할일`

### Execution

Run the 5-phase workflow from the skill, then present the diagnostic report to the user with actionable next steps for any missing items.
