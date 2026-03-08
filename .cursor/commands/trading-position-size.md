---
description: "Calculate risk-based position size for a stock trade"
argument-hint: "TICKER entry:PRICE stop:PRICE account:SIZE risk:PCT (e.g., AAPL entry:185 stop:178 account:100000 risk:1.0)"
---

# Trading Position Size Calculator

## Skill Reference

Read and follow `.cursor/skills/trading-position-sizer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Parameters

Extract from `$ARGUMENTS`:
- Ticker symbol
- Entry price (`entry:XXX`)
- Stop-loss price (`stop:XXX`) or ATR (`atr:XXX`)
- Account size (`account:XXX`, default: 100000)
- Risk percentage (`risk:XXX`, default: 1.0)
- Max position % (`max-pos:XXX`, default: 10)
- Max sector % (`max-sector:XXX`, default: 30)

### Step 2: Calculate Position Size

Run the position sizing calculation using the `trading-position-sizer` skill:

```bash
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --entry ENTRY --stop STOP \
  --account-size ACCOUNT --risk-pct RISK \
  --max-position-pct MAX_POS --max-sector-pct MAX_SECTOR
```

### Step 3: Report

Present results:
- Recommended shares
- Dollar risk per share
- Total dollar risk
- Position size as % of portfolio
- Binding constraints (if any)
- Risk/reward ratio (if target provided)

## Constraints

- No API keys required (pure calculation)
- All methods: Fixed Fractional, ATR-Based, Kelly Criterion
- Never suggest position sizes exceeding max constraints
