---
description: "Run weekly strategy review: sector rotation + technicals + macro + bubble risk"
---

# Trading Weekly Strategy Review

## Skill References

Read and follow these skills in order:
1. `.cursor/skills/trading-sector-analyst/SKILL.md`
2. `.cursor/skills/trading-market-environment-analysis/SKILL.md`
3. `.cursor/skills/trading-us-market-bubble-detector/SKILL.md`
4. `.cursor/skills/trading-uptrend-analyzer/SKILL.md`

## Your Task

User input: $ARGUMENTS

### Step 1: Sector Rotation

Run the `trading-sector-analyst` skill to identify rotation patterns and current market cycle phase.

### Step 2: Macro Environment

Run the `trading-market-environment-analysis` skill for a comprehensive global macro briefing covering indices, FX, commodities, yields, and sentiment.

### Step 3: Bubble Risk Assessment

Run the `trading-us-market-bubble-detector` skill:
1. Gather quantitative metrics (Put/Call, VIX, margin debt, breadth, IPO data)
2. Score on the Minsky/Kindleberger framework (0-15)
3. Determine risk phase: Normal → Caution → Elevated → Euphoria → Critical

### Step 4: Uptrend Health

Run the `trading-uptrend-analyzer` skill to diagnose market breadth health using uptrend ratio dashboard.

### Step 5: Weekly Summary

Synthesize all findings into a structured weekly report:
- Market cycle phase and sector positioning
- Macro environment assessment
- Bubble risk score and phase
- Uptrend breadth health
- Recommended portfolio adjustments
- Key risks to watch

Save to `outputs/reports/trading/weekly_review_YYYY-MM-DD.md`.

## Constraints

- All analysis in English
- No paid API keys required
- Include "This is not financial advice" disclaimer
