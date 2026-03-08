---
description: "Comprehensive market breadth analysis: breadth scoring + uptrend ratio + top detection"
---

# Trading Market Breadth Analysis

## Skill References

Read and follow these skills in order:
1. `.cursor/skills/trading-market-breadth-analyzer/SKILL.md`
2. `.cursor/skills/trading-uptrend-analyzer/SKILL.md`
3. `.cursor/skills/trading-market-top-detector/SKILL.md`

## Your Task

User input: $ARGUMENTS

### Step 1: Market Breadth Scoring

Run the `trading-market-breadth-analyzer` skill:
1. Fetch CSV data from TraderMonty's GitHub
2. Calculate 6-component score (0-100):
   - Overall Breadth
   - Sector Participation
   - Sector Rotation
   - Momentum
   - Mean Reversion Risk
   - Historical Context

### Step 2: Uptrend Ratio Diagnosis

Run the `trading-uptrend-analyzer` skill:
1. Analyze ~2,800 US stocks across 11 sectors
2. Calculate 5-component composite (0-100):
   - Market Breadth
   - Sector Participation
   - Sector Rotation
   - Momentum
   - Historical Context
3. Check warning overlays (Late Cycle, High Selectivity)

### Step 3: Market Top Detection

Run the `trading-market-top-detector` skill:
1. Check O'Neil Distribution Days
2. Assess Minervini Leading Stock Deterioration
3. Evaluate Monty Defensive Rotation
4. Calculate 6-component tactical timing score

### Step 4: Unified Assessment

Synthesize into a single report:
- Overall market health grade (A-F)
- Breadth score with trend direction
- Top detection signal status
- Exposure guidance (full/reduce/defensive)
- Key risk signals

Save to `outputs/reports/trading/market_breadth_YYYY-MM-DD.md`.

## Constraints

- Uses free GitHub CSV data (no API keys)
- All output in English
- Include "This is not financial advice" disclaimer
