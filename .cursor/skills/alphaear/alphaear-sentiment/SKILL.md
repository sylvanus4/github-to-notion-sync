---
name: alphaear-sentiment
description: >-
  Analyze financial text sentiment using LLM (default) or FinBERT (optional).
  Use when the user needs to determine sentiment (positive/negative/neutral) and
  score of financial text. Do NOT use for news aggregation (use alphaear-news).
  Do NOT use for trading signal generation (use daily-stock-check). Do NOT use
  for market prediction (use alphaear-predictor). Korean triggers: "감성 분석",
  "감성 점수", "긍정 부정", "FinBERT".
metadata:
  version: "1.1.0"
  last_updated: "2026-03-27"
  category: "analysis"
  author: "alphaear"
---
# AlphaEar Sentiment

## Overview

Analyze financial text sentiment with a score from -1.0 (negative) to 1.0 (positive). Default mode is LLM-only — no torch/transformers required. Optional FinBERT mode provides fast local batch analysis when `torch` and `transformers` are installed. Results are persisted to SQLite (`data/signal_flux.db`) via `scripts/database_manager.py`.

## Prerequisites

- **Minimal (LLM-only)**: `loguru`, `scripts/database_manager.py`, LLM API credentials.
- **Full (FinBERT)**: `torch`, `transformers`, plus minimal deps.
- SQLite (`data/signal_flux.db`) with `daily_news` table (auto-created by `DatabaseManager`).

## Workflow

1. **Initialize**: Create `DatabaseManager`, then `SentimentTools(db, mode="llm")` — use `"llm"` for default (no torch).
2. **Single analysis (LLM)**: Run the prompt below with your LLM; parse JSON; optionally call `update_single_news_sentiment(id, score, reason)` to save.
3. **Single analysis (FinBERT)**: If `mode="bert"` or `mode="auto"` with BERT available, call `analyze_sentiment(text)` — returns `{score, label, reason}`.
4. **Batch update**: Call `batch_update_news_sentiment(source, limit)` — uses FinBERT when available; otherwise no-op (use Agent + `update_single_news_sentiment` for LLM batch).
5. **Persistence**: `update_single_news_sentiment(news_id, score, reason)` writes to `daily_news.sentiment_score` and `meta_data.sentiment_reason`.

## LLM Prompt (Default Mode)

Use this prompt for sentiment analysis when FinBERT is not used:

```
Analyze the following financial text sentiment.
Return strict JSON: {"score": <float: -1.0 to 1.0>, "label": "<positive/negative/neutral>", "reason": "<brief reason>"}

Scoring: Positive (0.1-1.0): growth, support. Negative (-1.0 to -0.1): losses, sanctions. Neutral (-0.1 to 0.1): factual.

Text: {text}
```

## Examples

| Trigger | Action | Result |
|--------|--------|--------|
| "Sentiment of this headline" | Run LLM prompt → `update_single_news_sentiment(id, 0.6, "Profit growth reported")` | Score saved to DB |
| "Batch sentiment for wallstreetcn" | `batch_update_news_sentiment("wallstreetcn", 50)` | FinBERT: N items updated; LLM-only: 0 (use Agent loop) |
| "Analyze this text" | `analyze_sentiment(text)` (FinBERT mode) | `{score: 0.3, label: "positive", reason: "..."}` |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| BERT not installed | `analyze_sentiment` returns error dict | Use LLM prompt; or install torch, transformers |
| LLM parse failure | Returns `{score: 0.0, label: "error"}` | Retry with stricter JSON instruction |
| DB update failure | `update_single_news_sentiment` returns False | Check SQLite file access and `news_id` |
| Invalid score range | Depends on implementation | Clamp to [-1.0, 1.0] before persist |

## Troubleshooting

- **"BERT pipeline not initialized"**: Default is LLM-only; use the prompt above. For FinBERT, set `SENTIMENT_MODE=bert` and install transformers.
- **Batch returns 0**: In LLM-only mode, batch does nothing; run Agent loop with prompt + `update_single_news_sentiment` per item.
- **json_set**: SQLite uses `json_set` for updating JSONB-like fields in `meta_data`; check `database_manager` for exact SQL.

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Sentiment label/score for text or headlines | **This skill** |
| Fetching news lists | `alphaear-news` — **not** this skill |
| Trading buy/sell signals | `daily-stock-check` — **not** this skill |
| Price forecast | `alphaear-predictor` — **not** this skill |

### Data source attribution (required)

State engine per score: `(출처: LLM 감성 분석)`, `(출처: FinBERT 로컬 모델)`, or `(출처: daily_news.sentiment_score — DB 업데이트)`. If analyzing user-pasted text with no DB row, say `원문 기반 분석 (외부 DB 미연동)`.

### Korean output

Present `label`, `score`, `reason` in Korean for Korean users; use terms like 긍정/부정/중립, 감성 점수, 리스크 요인.

### Fallback protocol

If FinBERT unavailable: `FinBERT 미설치 — LLM 프롬프트 모드로 분석`. If LLM JSON parse fails: `감성 분석 재시도 중` and retry; if still failing, report 중립(0) and 오류 사유.
