---
description: "Run edge research pipeline: convert market observations into research tickets and hypotheses"
argument-hint: "Market observation or strategy context (e.g., 'NVDA formed a VCP base with contracting volume near earnings')"
---

# Trading Edge Research Pipeline

## Skill References

Read and follow these skills in order:
1. `.cursor/skills/trading-edge-candidate-agent/SKILL.md`
2. `.cursor/skills/trading-trade-hypothesis-ideator/SKILL.md`

## Your Task

User input: $ARGUMENTS

### Step 1: Generate Research Ticket

Run the `trading-edge-candidate-agent` skill:
1. Convert the observation from `$ARGUMENTS` into a structured research ticket
2. Assign entry family (pivot_breakout or gap_up_continuation)
3. Generate `strategy.yaml` + `metadata.json`
4. Save to `outputs/reports/trading/edge_tickets/`

### Step 2: Generate Hypotheses

Run the `trading-trade-hypothesis-ideator` skill:
1. Build evidence summary from the research ticket
2. Generate 1-5 falsifiable hypothesis cards
3. Validate raw hypotheses with guardrails
4. Rank and export cards
5. Save to `outputs/reports/trading/hypotheses/`

### Step 3: Report

Present:
- Research ticket summary
- Hypothesis cards (ranked by priority)
- Recommended next steps (backtest, monitor, discard)

## Constraints

- No API keys required (local YAML/JSON operations)
- All output in English
- Include invalidation criteria for each hypothesis
