---
name: trading-market-news-analyst
description: >-
  Analyze recent market-moving news events and their impact on equity markets
  and commodities. Use when the user asks to "analyze market news", "FOMC
  impact", "geopolitical commodity correlations", "mega-cap earnings review",
  "시장 뉴스 분석", "FOMC 영향", "지정학적 상품 상관관계", or needs impact-ranked analysis of
  major financial news from the past 10 days. Do NOT use for AlphaEar news
  aggregation (use alphaear-news). Do NOT use for AlphaEar sentiment analysis
  (use alphaear-sentiment). Do NOT use for general web search (use WebSearch
  directly).
---

# Market News Analyst

## Overview

Comprehensive analysis of market-moving news from the past 10 days. WebSearch/WebFetch for collection; evaluate impact magnitude; analyze market reactions; produce structured English reports ranked by impact. US equities and commodities focus.

## When to Use

- Recent major market news analysis (past 10 days)
- Event-specific impact (FOMC, earnings, geopolitical)
- Market news summary with impact assessment
- News-commodity correlations
- Central bank policy effects on markets

## Analysis Workflow

### Step 1: News Collection

**Search categories:** Monetary policy (FOMC, ECB, BOJ), Inflation/Economic (CPI, NFP, GDP), Mega-cap earnings (AAPL, MSFT, NVDA, etc.), Geopolitical, Commodities, Corporate.

**Sources:** Official (FederalReserve.gov, SEC, Treasury, BLS), Tier 1 (Bloomberg, Reuters, WSJ, FT), Specialized (CNBC, MarketWatch, S&P Platts). See [references/trusted_news_sources.md](references/trusted_news_sources.md).

**Filter:** Tier 1 market-moving events per [references/market_event_patterns.md](references/market_event_patterns.md). Exclude minor stock news.

### Step 2: Load Knowledge Base

**Always:** `market_event_patterns.md`, `trusted_news_sources.md`
**If monetary policy:** Central Bank section of market_event_patterns
**If geopolitical:** [references/geopolitical_commodity_correlations.md](references/geopolitical_commodity_correlations.md)
**If mega-cap earnings:** [references/corporate_news_impact.md](references/corporate_news_impact.md)
**If commodities:** geopolitical_commodity_correlations

### Step 3: Impact Magnitude Assessment

For scoring framework (Asset Price Impact, Breadth Multiplier, Forward-Looking Modifier), see [references/impact_scoring_framework.md](references/impact_scoring_framework.md). Rank events by Impact Score descending.

### Step 4: Market Reaction Analysis

For each event (Score >5): Immediate reaction (direction, magnitude, timing), multi-asset response (equities, bonds, commodities, currencies, derivatives). Compare against expected pattern (Consistent/Amplified/Dampened/Inverse). Flag anomalies.

### Step 5: Correlation and Causation

Assess: Reinforcing vs offsetting events, sequential causation, coincidental timing. Use geopolitical_commodity_correlations for commodity impact analysis. Trace transmission: Direct, Indirect, Sentiment channels.

### Step 6: Report Generation

Use [references/report_template.md](references/report_template.md) for structure. Output: `outputs/reports/trading/market_news_analysis_[START]_to_[END].md`. Objective, quantified, cited, causation-disciplined.

**Mandatory add-ons to every report:**

1. **Impact-ranked event table** — Columns: `Event` | `Impact score` | `Key numeric fact` | `Source` | `Date (as-of)` (minimum **3** rows when ≥3 major events exist; if fewer events, explain why).
2. **Market reaction metrics** — For top events, quote **≥3** market numbers (index % move, VIX change, yield bps, commodity %) **only** from collected sources; include citation.
3. **Forward playbook (Actionable)** — Final section with **stance** (risk-on/off/neutral), **primary trade expression** (e.g., favor duration, quality, energy hedges—not specific stock picks unless sourced), and **monitoring checklist**.
4. **Risks & invalidation** — At least one scenario where the narrative breaks (data revision, policy surprise, positioning unwind).
5. **No fabricated prints** — If reaction data unavailable, write `Reaction: N/A (data gap)` instead of guessing.

English remains the default output language unless the user requests otherwise.

## Key Principles

1. Impact over noise
2. Multi-asset perspective
3. Pattern recognition vs historical precedents
4. Causation discipline
5. Forward-looking emphasis
6. Quantification (%, bps)
7. Source credibility
8. English throughout

## Common Pitfalls

- Over-attribution; Recency bias; Hindsight bias; Single-factor analysis; Ignoring magnitude

## Resources

| Reference | Purpose |
|-----------|---------|
| [market_event_patterns.md](references/market_event_patterns.md) | Central bank, inflation, geopolitical, earnings patterns |
| [geopolitical_commodity_correlations.md](references/geopolitical_commodity_correlations.md) | Energy, metals, agriculture correlations |
| [corporate_news_impact.md](references/corporate_news_impact.md) | Mega-cap impact framework |
| [trusted_news_sources.md](references/trusted_news_sources.md) | Source credibility tiers |
| [impact_scoring_framework.md](references/impact_scoring_framework.md) | Scoring formula and thresholds |
| [report_template.md](references/report_template.md) | Report structure |

## Important Notes

- All analysis and output in English
- WebSearch and WebFetch for collection
- Target: past 10 days; US equities + commodities
- FOMC/central bank highest priority
- Quantify all reactions

## Examples

### Example 1: Weekly market news summary
**User:** "What moved the market this week?"
**Action:** WebSearch for FOMC, earnings, geopolitical events from past 7 days. Score each by impact formula. Rank and analyze multi-asset reactions.
**Output:** Impact-ranked report with top 5 events, scores, market reactions, and forward implications saved to `outputs/reports/trading/`.

### Example 2: FOMC impact analysis
**User:** "Analyze the impact of last week's FOMC decision"
**Action:** Collect FOMC statement, dot plot changes, press conference highlights. Assess rate path implications. Analyze equity, bond, FX, and commodity reactions.
**Output:** FOMC-specific impact report with policy transmission analysis and sector positioning implications.

## Error Handling

| Error | Action |
|-------|--------|
| WebSearch returns no results | Broaden search terms, try alternative news sources from trusted_news_sources.md |
| Conflicting news sources | Weight by source credibility tier (Official > Tier 1 > Specialized) |
| No significant market-moving events found | Report "quiet period" with notable non-events and upcoming catalysts |
| Unable to quantify market reaction | Note the data gap and provide qualitative assessment with explicit uncertainty |
