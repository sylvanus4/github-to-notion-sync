---
description: "Run 3-layer AlphaEar intelligence pipeline — parallel data collection, parallel analysis, and report generation with optional visualization"
---

# AlphaEar Intel — AlphaEar Intelligence Orchestrator

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear/alphaear-orchestrator/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Flags

- No arguments: run full AlphaEar pipeline (no visualization)
- Ticker symbol (e.g., `NVDA`): focus analysis on that ticker
- `--skip news,stock,search,sentiment,predictor,signal,reporter`: skip components
- `--visualize`: include logic diagram generation
- `--dry-run`: show execution plan without running

### Examples

```
/alphaear-intel
/alphaear-intel NVDA
/alphaear-intel --visualize
/alphaear-intel AAPL --skip search --visualize
/alphaear-intel --dry-run
```
