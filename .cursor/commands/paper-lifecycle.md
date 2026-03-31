---
description: "Run end-to-end research paper lifecycle — discover, scout, review or generate slides, archive, and distribute"
---

# Paper Lifecycle — Research Paper Lifecycle Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/research/paper-lifecycle-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- arXiv URL (e.g., `https://arxiv.org/abs/2403.xxxxx`): process this specific paper
- `auto`: auto-classify recent arXiv papers and process the top one
- `--depth full` (default): complete lifecycle with full review
- `--depth slides-only`: skip review, generate slides directly
- `--depth scout-only`: discovery and scouting only
- `--dry-run`: show execution plan without running

### Examples

```
/paper-lifecycle https://arxiv.org/abs/2403.12345
/paper-lifecycle auto
/paper-lifecycle https://arxiv.org/abs/2403.12345 --depth slides-only
/paper-lifecycle auto --depth scout-only
/paper-lifecycle --dry-run
```
