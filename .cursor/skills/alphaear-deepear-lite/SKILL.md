---
name: alphaear-deepear-lite
description: Lightweight orchestration of AlphaEar skills for comprehensive financial analysis. Use when the user asks broad questions like "Analyze how X affects the market" or needs multi-domain synthesis (news, sentiment, signals, prediction, logic, report). Do NOT use for single-domain analysis (use individual alphaear-* skills). Do NOT use for daily stock checks (use daily-stock-check). Do NOT use for routine stock price updates (use weekly-stock-update).
metadata:
  version: "1.0.0"
  category: orchestration
  author: alphaear
---

# AlphaEar DeepEar Lite

## Overview

Coordinates alphaear-search, alphaear-news, alphaear-sentiment, alphaear-signal-tracker, alphaear-predictor, alphaear-logic-visualizer, alphaear-reporter, and project data sources (daily-stock-check, weekly-stock-update) into a single workflow for comprehensive finance queries.

## Prerequisites

- All 8 alphaear sub-skills available
- `scripts/deepear_lite.py` for orchestration logic
- No heavy runtime dependencies (orchestration only)

## Workflow

1. **Parse intent**: Analyze user query to identify needed domains (news, analysis, prediction, signals, diagrams, report).
2. **Delegate sequence**:
   - alphaear-search + alphaear-news for data gathering
   - alphaear-sentiment for sentiment scoring
   - alphaear-signal-tracker for signal analysis
   - alphaear-predictor for time-series forecasting
   - alphaear-logic-visualizer for transmission-chain diagrams
   - alphaear-reporter for final report assembly
3. **Synthesize**: Combine sub-skill outputs into a comprehensive response.

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "Analyze how X affects the market" | Full orchestration workflow | News + sentiment + signals + prediction + report |
| "Latest signals from DeepEar Lite" | `scripts/deepear_lite.py` `fetch_latest_signals()` | Signal titles, summaries, confidence, source links |
| "Comprehensive view on sector Y" | Delegate to alphaear-search, news, sentiment, reporter | Multi-domain synthesis |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Sub-skill unavailable | Skip or substitute | Fall back to available skills; report gaps |
| DeepEar Lite API down | `fetch_latest_signals` returns error/empty | Use project data (daily-stock-check) as fallback |
| Over-scoped query | Long-running orchestration | Suggest narrowing scope or splitting into sub-queries |

## Troubleshooting

- **Single-domain**: If the query is narrow (e.g. only sentiment, only stock price), call the specific alphaear-* skill instead.
- **Data freshness**: Combine DeepEar Lite signals with project daily-stock-check and weekly-stock-update for up-to-date inputs.
- **Report output**: Route final assembly to alphaear-reporter for structured report generation.
