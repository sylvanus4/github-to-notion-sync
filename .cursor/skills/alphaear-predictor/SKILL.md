---
name: alphaear-predictor
description: Market prediction using Kronos time-series model with news-aware adjustments. Use when user needs finance market time-series forecasting, multi-day price predictions, or news-informed forecast adjustments. Do NOT use for technical indicator analysis like SMA/Bollinger (use daily-stock-check). Do NOT use for backtesting strategies (use backtest service).
metadata:
  version: "1.0.0"
  category: analysis
  author: alphaear
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
