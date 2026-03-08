---
description: "Run daily market monitoring: breadth analysis + market news + sector rotation"
---

# Trading Daily Market Monitoring

## Skill References

Read and follow these skills in order:
1. `.cursor/skills/trading-market-breadth-analyzer/SKILL.md`
2. `.cursor/skills/trading-market-news-analyst/SKILL.md`
3. `.cursor/skills/trading-sector-analyst/SKILL.md`

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains "breadth-only", run only market breadth analysis
- If `$ARGUMENTS` contains "news-only", run only market news analysis
- If `$ARGUMENTS` contains "sector-only", run only sector analysis
- If `$ARGUMENTS` is empty or "all", run all three in sequence

### Step 2: Market Breadth Analysis

Run the `trading-market-breadth-analyzer` skill:
1. Fetch CSV data from TraderMonty's GitHub
2. Calculate the 6-component breadth score (0-100)
3. Save report to `outputs/reports/trading/market_breadth_YYYY-MM-DD.md`

### Step 3: Market News Analysis

Run the `trading-market-news-analyst` skill:
1. Use WebSearch to gather news from the past 10 days
2. Rank events by impact score (Price Impact x Breadth x Forward Significance)
3. Save report to `outputs/reports/trading/market_news_analysis_YYYY-MM-DD.md`

### Step 4: Sector Rotation Analysis

Run the `trading-sector-analyst` skill:
1. Fetch sector uptrend ratio CSV data
2. Analyze cyclical vs defensive positioning
3. Identify market cycle phase
4. Save report to `outputs/reports/trading/sector_analysis_YYYY-MM-DD.md`

### Step 5: Synthesize

Provide a unified summary combining:
- Overall market health score (breadth)
- Top 3 market-moving events (news)
- Current sector rotation positioning
- Actionable implications

## Constraints

- All reports go to `outputs/reports/trading/`
- Output language: English
- Include disclaimers: "This is not financial advice"
- Do not require any paid API keys
