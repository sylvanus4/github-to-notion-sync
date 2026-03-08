---
description: "Deep-dive individual stock research: fundamentals + technicals + peer comparison"
argument-hint: "TICKER (e.g., AAPL, NVDA, TSLA)"
---

# Trading Stock Research

## Skill References

Read and follow these skills:
1. `.cursor/skills/trading-us-stock-analysis/SKILL.md`
2. `.cursor/skills/trading-technical-analyst/SKILL.md` (if chart image provided)

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- Extract the ticker symbol(s) from `$ARGUMENTS`
- If chart images are attached, plan to run technical analysis
- If "compare" or "vs" is in the arguments, run peer comparison mode

### Step 2: Fundamental Analysis

Run the `trading-us-stock-analysis` skill for the target ticker:
1. Analyze financial metrics, valuation ratios, growth trajectories
2. Assess competitive positioning
3. Generate bull/bear cases

### Step 3: Technical Analysis (if chart provided)

If chart image is attached, run `trading-technical-analyst`:
1. Identify trends, support/resistance levels
2. Assess chart patterns and momentum
3. Generate scenario-based probability assessments

### Step 4: Investment Memo

Generate a structured investment memo:
- Company overview and thesis
- Key financial metrics
- Technical setup (if chart analyzed)
- Bull/bear cases with probabilities
- Risk assessment
- Recommendation with conviction level

Save to `outputs/reports/trading/stock_research_[TICKER]_YYYY-MM-DD.md`.

## Constraints

- Output in English
- Include "This is not financial advice" disclaimer
- Use data provided by user or gathered via WebSearch
