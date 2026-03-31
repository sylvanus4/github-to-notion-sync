---
description: "Run full market intelligence analysis — dispatch 4 analyst agents in parallel (macro, sector, news, technical), synthesize findings, and optionally deep-dive on a specific ticker"
---

# Trading Intel — Market Intelligence Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/trading/trading-intel-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: run all 4 analysts, no deep-dive ticker
- Ticker symbol (e.g., `NVDA`): run all analysts + deep-dive on that ticker
- `--skip env,sector,news,tech`: skip specific analysts (comma-separated)
- `--dry-run`: show execution plan without running

### Examples

```
/trading-intel
/trading-intel NVDA
/trading-intel AAPL --skip sector
/trading-intel --dry-run
```
