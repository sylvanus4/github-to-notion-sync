---
description: "Run options trading analysis: strategy selection, Greeks, P/L simulation, and theta income planning"
argument-hint: "Ticker and context (e.g., 'AAPL earnings next week, expecting 5% move' or 'SPY iron condor for weekly income')"
---

# Trading Options Analysis

## Skill References

Read and follow these skills based on the request:
1. `.cursor/skills/trading-options-strategy-advisor/SKILL.md` — strategy selection, Greeks, P/L simulation
2. `.cursor/skills/trading-options-theta/SKILL.md` — theta income strategies (credit spreads, iron condors, 0DTE)

## Your Task

User input: $ARGUMENTS

### Step 1: Market Context

1. Use `alphaear-stock` to get current price and recent history for the ticker
2. Check IV rank / IV percentile context via web search
3. Identify upcoming catalysts (earnings, FOMC, ex-dividend)

### Step 2: Strategy Analysis

Based on the user's context from `$ARGUMENTS`:

**If directional or event-driven:**
- Run `trading-options-strategy-advisor` for strategy selection
- Calculate Greeks and theoretical pricing
- Simulate P/L scenarios (bull, base, bear)
- Recommend specific strikes and expirations

**If income-focused (theta, premium selling):**
- Run `trading-options-theta` with the appropriate prompt
- Analyze credit spread setups, iron condors, or 0DTE opportunities
- Calculate max profit, max loss, breakevens
- Provide risk management rules

### Step 3: Position Sizing

- Use `trading-position-sizer` to calculate appropriate position size
- Account for max loss per trade (1-2% of portfolio)
- Factor in margin requirements

### Step 4: Report

Present:
- Strategy recommendation with rationale
- Specific trade setup (strikes, expiration, premium)
- Greeks snapshot
- P/L diagram description
- Risk management rules and exit criteria
- Position size recommendation

## Constraints

- Educational focus — include explanations for intermediate-level traders
- Always include max loss and risk/reward ratio
- Prefer defined-risk strategies over naked options
- Include time decay (theta) projections
