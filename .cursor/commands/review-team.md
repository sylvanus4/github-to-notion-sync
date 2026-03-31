---
description: "Run multi-perspective code review — 3 parallel review skills (deep-review, simplify, test-suite) with deduplicated unified report"
---

# Review Team — Multi-Perspective Code Review Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/review/review-team-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: full 3-way review on recent changes
- `--skip deep,simplify,test`: skip specific reviewers (comma-separated)
- `--light`: reduce internal agents per skill for cost savings
- `--scope src/services/`: limit review to specific directory
- `--dry-run`: show execution plan without running

### Examples

```
/review-team
/review-team --light
/review-team --skip test
/review-team --scope backend/app/services/
/review-team --light --skip simplify
/review-team --dry-run
```
