---
description: "Market prediction using Kronos time-series model with news-aware adjustments"
---

# AlphaEar Predictor

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear/alphaear-predictor/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a ticker, use it for prediction
- If `$ARGUMENTS` contains a horizon (e.g., "7d", "5 days"), set `pred_len` accordingly
- If `$ARGUMENTS` mentions "news" or "adjusted", include news context in forecast
- If `$ARGUMENTS` is empty, ask user for ticker and forecast horizon

### Step 2: Execute

Follow the workflow in the skill:

1. Load OHLCV data from PostgreSQL or backend services
2. Generate base forecast via `KronosPredictorUtility.get_base_forecast`
3. If news-aware: apply Forecast Adjustment prompt from `references/PROMPTS.md`

### Step 3: Report

Present results with:
- Base forecast (OHLCV table for predicted days)
- Adjusted forecast (if news context applied)
- Rationale for adjustments
- Disclaimer: "This is a model prediction, not financial advice"
