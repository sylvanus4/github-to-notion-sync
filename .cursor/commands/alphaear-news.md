---
description: "Fetch real-time financial news from 10+ sources and Polymarket prediction market data"
---

# AlphaEar News

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-news/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a source name (e.g., "wallstreetcn", "weibo", "cls"), use it as `source_id`
- If `$ARGUMENTS` contains a number, use it as `count`
- If `$ARGUMENTS` mentions "polymarket" or "prediction", run `PolymarketTools.get_market_summary`
- If `$ARGUMENTS` mentions "unified" or "trends", run `get_unified_trends`
- If `$ARGUMENTS` is empty, fetch unified trends from default finance sources (cls, wallstreetcn, xueqiu)

### Step 2: Execute

Follow the workflow in the skill:

1. Initialize `DatabaseManager` and `NewsNowTools`
2. Run the appropriate method based on Step 1
3. For US/KR market news, supplement with `parallel-web-search` for Reuters/Bloomberg/CNBC

### Step 3: Report

Present results as a formatted summary with:
- Source attribution
- Headline list with URLs where available
- Timestamp of fetch
