---
description: "Translate natural-language stock screening requests into FINVIZ screener filters"
argument-hint: "Natural language query (e.g., 'high dividend large-cap value stocks with low P/E')"
---

# Trading FINVIZ Screener

## Skill Reference

Read and follow `.cursor/skills/trading-finviz-screener/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Interpret `$ARGUMENTS` as a natural-language stock screening request (English, Korean, or Japanese).

### Step 2: Map to FINVIZ Filters

Using the `trading-finviz-screener` skill:
1. Map the request to FINVIZ filter codes (500+ available)
2. Build the complete screener URL
3. Present the filter breakdown

### Step 3: Output

Present:
- Interpreted criteria
- FINVIZ filter codes applied
- Direct link to FINVIZ screener results
- Alternative filter suggestions

## Pre-built Recipes

If `$ARGUMENTS` matches a common pattern:
- "high dividend value" → Dividend yield > 3%, P/E < 20, P/B < 2
- "small-cap growth" → Market cap 300M-2B, EPS growth > 25%
- "oversold large-caps" → RSI < 30, Market cap > 10B
- "breakout candidates" → New high, volume surge
- "AI theme" → Technology sector, related industry filters

## Constraints

- No API key required for public FINVIZ screener
- FINVIZ Elite auto-detected from `$FINVIZ_API_KEY` if set
- Supports English, Korean, and Japanese input
