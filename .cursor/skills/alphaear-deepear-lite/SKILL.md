---
name: alphaear-deepear-lite
description: >-
  Lightweight orchestration of AlphaEar skills for comprehensive financial
  analysis. Use when the user asks broad questions like "Analyze how X affects
  the market" or needs multi-domain synthesis (news, sentiment, signals,
  prediction, logic, report). Do NOT use for single-domain analysis (use
  individual alphaear-* skills). Do NOT use for daily stock checks (use
  daily-stock-check). Do NOT use for routine stock price updates (use
  weekly-stock-update). Korean triggers: "분석", "체크", "리포트", "주식".
metadata:
  version: "1.0.0"
  category: "orchestration"
  author: "alphaear"
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

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing (canonical patterns)

| User query pattern | Delegate |
|--------------------|----------|
| Macro/sector impact (“금리 인상이 반도체에…”) | `alphaear-search` + `alphaear-news` → `alphaear-sentiment` → optional `alphaear-predictor` / `alphaear-signal-tracker` → `alphaear-reporter` |
| Ticker news + sentiment (“NVDA 뉴스와 감성”) | `alphaear-news` (or search) → `alphaear-sentiment` |
| Price / OHLCV history (“005930 주가 히스토리”) | `alphaear-stock` (or `weekly-stock-update` if routine sync) |
| Signal validity / evolution (“매수 시그널 유효?”) | `alphaear-signal-tracker` (+ `alphaear-news`, `alphaear-stock` for facts) |
| Logic / transmission diagram (“Draw.io”, 논리 흐름) | `alphaear-logic-visualizer` |

Never answer with a single sub-skill when the user clearly asked for multi-domain synthesis; run the minimal chain above.

### Data source attribution (required)

In the final synthesized answer, tag every data-backed claim with its origin, e.g. `(출처: Yahoo Finance / yfinance)`, `(출처: PostgreSQL daily_news, NewsNow 수집)`, `(출처: Polymarket gamma-api)`, `(출처: Kronos 모델 예측)`, `(출처: 프로젝트 DB OHLCV)`. If a sub-skill returned no data, state that explicitly.

### Korean output

When the user writes in Korean, respond in natural Korean using standard finance terms: 시가총액, 이동평균선, PER, PBR, RSI, 거래량, 종가, 시가, 고가, 저가, 금리, 섹터.

### Fallback protocol

If a planned sub-skill or API is unavailable, state: `1차 소스(이름)를 사용할 수 없어 대체 경로(이름)로 진행했습니다` and proceed (e.g. DeepEar Lite 실패 시 daily-stock-check / DB 데이터). Do not silently omit the failure.
