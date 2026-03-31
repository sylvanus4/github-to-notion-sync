---
description: "Run unified quality gate — CI checks + 3 parallel AI scans (security, dependency, performance) with deduplicated dashboard"
---

# Quality Gate — Security & Quality Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/review/quality-gate-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: run full gate (CI + 3 AI scans)
- `--skip security,deps,perf,ci`: skip specific scans (comma-separated)
- `--force`: continue even if CI gate fails
- `--dry-run`: show execution plan without running

### Examples

```
/quality-gate
/quality-gate --skip perf
/quality-gate --force
/quality-gate --skip ci,deps --dry-run
```
