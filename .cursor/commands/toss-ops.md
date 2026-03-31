---
description: "Run unified Toss Securities operations — snapshot, parallel monitoring (FX/risk/recon/watchlist), signal bridge, and reporting"
---

# Toss Ops — Toss Securities Operations Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/trading/toss-ops-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: run full Toss operations workflow
- `--skip fx,risk,recon,watchlist,signal,journal,briefing`: skip components (comma-separated)
- `--mode snapshot-only`: only capture account snapshot
- `--mode monitor-only`: snapshot + parallel monitoring only
- `--dry-run`: show execution plan without running

### Examples

```
/toss-ops
/toss-ops --skip fx,journal
/toss-ops --mode snapshot-only
/toss-ops --dry-run
```
