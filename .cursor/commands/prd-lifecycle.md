---
description: "Run end-to-end PRD lifecycle — research-backed generation, quality gate loop, cascade sync, and stakeholder review"
---

# PRD Lifecycle — Planning PRD Lifecycle Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/planning/prd-lifecycle-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- Meeting URL, transcript, or topic description as primary input
- `--skip research,quality,cascade,review`: skip specific phases (comma-separated)
- `--max-iterations N`: quality gate loop iterations (default: 2)
- `--dry-run`: show execution plan without running

### Examples

```
/prd-lifecycle https://notion.so/meeting/xxxxx
/prd-lifecycle "AI-powered stock screening feature for retail investors"
/prd-lifecycle --skip cascade,review
/prd-lifecycle "mobile app redesign" --max-iterations 1
/prd-lifecycle --dry-run
```
