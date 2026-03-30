---
name: trading-market-environment-analysis
description: >-
  Comprehensive market environment analysis and reporting. Analyzes global
  markets: US, European, Asian, forex, commodities, economic indicators. Use
  when the user asks "market analysis", "market environment", "global markets",
  "trading environment", "risk-on risk-off", "market conditions", "investment
  climate", "market sentiment", "相場環境", "市場分析", "マーケット状況", "投資環境". Do NOT use
  for daily stock signals (use daily-stock-check). Do NOT use for AlphaEar news
  aggregation (use alphaear-news). Korean triggers: "시장", "분석", "체크", "리포트".
metadata:
  author: "tradermonty"
  version: "1.0.0"
  category: "analysis"
  source: "claude-trading-skills"
  api_required: "none"
---
# Market Environment Analysis

Comprehensive analysis tool for understanding market conditions and creating professional market reports anytime.

## Core Workflow

### 1. Initial Data Collection
Collect latest market data using web_search tool:
1. Major stock indices (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. Forex rates (USD/JPY, EUR/USD, major currency pairs)
3. Commodity prices (WTI crude, Gold, Silver)
4. US Treasury yields (2-year, 10-year, 30-year)
5. VIX index (Fear gauge)
6. Market trading status (open/close/current values)

### 2. Market Environment Assessment
Evaluate the following from collected data:
- **Trend Direction**: Uptrend/Downtrend/Range-bound
- **Risk Sentiment**: Risk-on/Risk-off
- **Volatility Status**: Market anxiety level from VIX
- **Sector Rotation**: Where capital is flowing

### 3. Report Structure

#### Standard Report Format:
```
1. Executive Summary (3-5 key points)
2. Data Provenance & As-Of (required)
   - Table: Metric | Value | % change (if any) | Source | Timestamp (UTC or market date)
   - Every numeric quote in the report must appear in this table or be labeled INLINE with source+date
3. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
4. Forex & Commodities Trends
5. Key Events & Economic Indicators
6. Risk Factor Analysis (invalidation conditions required)
7. Investment Strategy Implications
8. Actionable Outlook (required)
   - 1-5 day bias: Risk-on / Risk-off / Mixed (pick one)
   - Primary playbook: add/trim risk, hedges, or wait—with **one** concrete trigger (level or event)
9. Summary
```

**Anti-hallucination**: Do not fabricate index levels, yields, or FX prints. If a number is unavailable after search, write `N/A` and omit it from narrative conclusions that depend on it.

**Numeric density**: Include **at least three** distinct numeric market datapoints (e.g., index level, VIX, yield, FX) tied to the provenance table.

**Actionable + risk**: **Actionable Outlook** must end with a clear stance; **Risk Factor Analysis** must include at least one **invalidation** (what data would prove the thesis wrong).

## Script Usage

### market_utils.py
Provides common functions for report creation:
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## Reference Documentation

### Key Indicators Interpretation (references/indicators.md)
Reference when you need:
- Important levels for each index
- Technical analysis key points
- Sector-specific focus areas

### Analysis Patterns (references/analysis_patterns.md)
Reference when analyzing:
- Risk-on/Risk-off criteria
- Economic indicator interpretation
- Inter-market correlations
- Seasonality and market anomalies

## Output Examples

### Quick Summary Version
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### Detailed Analysis Version
Start with executive summary, then analyze each section in detail.
Key clarifications:
1. Current market phase (Bullish/Bearish/Neutral)
2. Short-term direction (1-5 days outlook)
3. Risk events to monitor
4. Recommended position adjustments

## Output Location

Save reports to `outputs/reports/trading/` directory.

## Important Considerations

### Timezone Awareness
- Consider all major market timezones
- US markets: Evening to early morning (Asian time)
- European markets: Afternoon to evening (Asian time)
- Asian markets: Morning to afternoon (Local time)

### Economic Calendar Priority
Categorize by importance:
- ⭐⭐⭐ Critical (FOMC, NFP, CPI, etc.)
- ⭐⭐ Important (GDP, Retail Sales, etc.)
- ⭐ Reference level

### Data Source Priority
1. Official releases (Central banks, Government statistics)
2. Major financial media (Bloomberg, Reuters)
3. Broker reports
4. Analyst consensus estimates

## Troubleshooting

### Data Collection Notes
- Check market holidays (holiday calendars)
- Be aware of daylight saving time changes
- Distinguish between flash and final data

### Market Volatility Response
1. First organize the facts
2. Reference historical similar events
3. Verify with multiple sources
4. Maintain objective analysis

## Customization Options

Adjust based on user's investment style:
- **Day Traders**: Intraday charts, order flow focus
- **Swing Traders**: Daily/weekly technicals emphasis
- **Long-term Investors**: Fundamentals, macro economics focus
- **Forex Traders**: Currency correlations, interest rate differentials
- **Options Traders**: Volatility analysis, Greeks monitoring

## Examples

### Example 1: Quick market snapshot
**User:** "What's the current market environment? Give me a quick summary."
**Action:** Collects indices (S&P, Nasdaq, Nikkei, etc.), forex, commodities, VIX, yields via web search; assesses risk-on/risk-off and volatility.
**Output:** Short summary with key indices, FX, VIX level, dominant theme (e.g., Risk-On Continues), and upcoming events.

### Example 2: Detailed analysis for swing traders
**User:** "Market analysis for swing trading — what's the setup?"
**Action:** Gathers data, evaluates trend direction and volatility, references analysis_patterns.md and indicators.md, produces detailed report with 1–5 day outlook.
**Output:** Structured report with executive summary, global overview, forex/commodities, risk factors, and swing-trading positioning implications.

### Example 3: Risk event focus
**User:** "What critical events could move markets this week?"
**Action:** Identifies economic calendar items, prioritizes by importance (FOMC, NFP, CPI), and notes impact on risk sentiment.
**Output:** Prioritized event list with significance levels and suggested monitoring approach.

## Error Handling

| Error | Action |
|-------|--------|
| Market closed / no recent data | Note session status; use last available close; clarify timezone in report |
| Web search returns stale data | Prefer official sources (central banks, BLS); note data timestamps in report |
| Conflicting signals (e.g., risk-on indices, risk-off bonds) | Present both; synthesize into "Mixed" or dominant regime with caveats |
| VIX or yield data unavailable | Proceed with available data; note gaps in methodology section |
