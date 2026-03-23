---
name: alphaear-predictor
description: >-
  Market prediction using Kronos time-series model with news-aware adjustments.
  Use when user needs finance market time-series forecasting, multi-day price
  predictions, or news-informed forecast adjustments. Do NOT use for technical
  indicator analysis like SMA/Bollinger (use daily-stock-check). Do NOT use for
  backtesting strategies (use backtest service). Korean triggers: "테스트", "체크",
  "주식", "시장".
metadata:
  version: "1.0.0"
  category: "analysis"
  author: "alphaear"
---
# AlphaEar Predictor

## Overview

Uses the Kronos model to generate time-series forecasts (OHLCV K-line points) and optionally adjusts them based on news context via an LLM. The agent orchestrates: (1) base technical forecast from `scripts/kronos_predictor.py`, (2) subjective/news-aware adjustment using prompts in `references/PROMPTS.md`.

## Prerequisites

- Python 3.10+
- `torch`, `transformers`, `sentence-transformers`, `pandas`, `numpy`, `scikit-learn`
- Stock data from project PostgreSQL (via existing backend services or `scripts/utils/database_manager.py`)
- Model weights at `scripts/predictor/exports/models/kronos_news_v1_20260101_0015.pt` (~1.2MB)
- Env vars: `EMBEDDING_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`), `KRONOS_MODEL_PATH` (optional override)

## Workflow

1. **Load OHLCV data**: Fetch from PostgreSQL via project backend or `scripts/utils/database_manager.py` — ensure DataFrame has columns `date`, `open`, `high`, `low`, `close`, `volume`.
2. **Generate base forecast**: Call `KronosPredictorUtility.get_base_forecast(df, lookback, pred_len, news_text)` from `scripts/kronos_predictor.py`. Returns `List[KLinePoint]`.
3. **Adjust with news**: Use the **Forecast Adjustment** prompt from `references/PROMPTS.md` — agent applies LLM to adjust technical forecast based on latest intelligence/news.
4. **Return adjusted forecast**: Combine base + adjusted points and rationale for downstream use.

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "7-day forecast for 600519" | `get_base_forecast(df, 20, 7)` | List of 7 `KLinePoint` (date, open, high, low, close, volume) |
| "Forecast 600519 with latest news" | `get_base_forecast(..., news_text=news)` + LLM adjustment | Adjusted OHLCV + rationale |
| "Multi-day prediction Moutai" | Load DF from DB → run predictor | JSON or K-line list |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Insufficient data | Returns empty list, logs warning | Ensure `len(df) >= lookback` (default 20) |
| Model not loaded | Returns `[]`, logs error | Check model path, `KRONOS_MODEL_PATH`, download Kronos base if needed |
| News encoding fails | Proceeds without news emb | Falls back to base technical forecast |
| LLM adjustment fails | Use base forecast only | Retry with smaller news context or skip adjustment |

## Troubleshooting

- **No trained news weights**: If `news_proj_state_dict` missing in `.pt`, model runs in base-only mode.
- **CUDA/MPS**: Predictor auto-selects device (cuda > mps > cpu).
- **PostgreSQL integration**: Reference project's stock services for OHLCV; ensure date range covers required `lookback` days.

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Multi-day OHLCV forecast / Kronos + 뉴스 반영 | **This skill** |
| SMA/Bollinger/RSI rules | `daily-stock-check` |
| Backtest | dedicated backtest service — **not** this skill |
| Broad multi-domain report | `alphaear-deepear-lite` |

### Data source attribution (required)

State: historical input `(출처: PostgreSQL OHLCV / 프로젝트 DB)`, base forecast `(출처: Kronos 모델, 가중치 경로 명시)`, adjustment `(출처: LLM 뉴스 반영 조정)` or `조정 생략(뉴스 없음)`.

### Korean output

Korean users: explain 구간 예측, 변동성, 전제 조건 in natural Korean; use 시가, 고가, 저가, 종가, 거래량.

### Fallback protocol

Insufficient rows → `lookback 미충족 — 예측 불가`. Model load fail → `Kronos 가중치 로드 실패 — 기술적 예측 생략`. LLM adjustment fail → `뉴스 조정 실패 — Kronos 기본 예측만 제공` 명시.
