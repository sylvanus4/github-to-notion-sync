---
name: tab-genai-features
description: >-
  Generate AI-powered prediction features via POST /genai-features/generate
  for all tracked stocks. Use when generating GenAI features, 'GenAI 피처 생성',
  'tab-genai-features'. Do NOT use for LLM agent pipeline (use
  tab-llm-agents), stock analysis (use daily-stock-check), or event detection
  (use tab-event-detect).
---

# tab-genai-features

## Purpose

Generates AI-powered features and predictions. Calls `POST /genai-features/generate` to create prediction features, sentiment scores, and AI-powered analysis for all tracked stocks.

## When to Use

- generate genai features
- GenAI 피처 생성
- tab-genai-features
- AI feature generation

## When NOT to Use

- LLM agent pipeline (use tab-llm-agents)
- Stock analysis (use daily-stock-check)
- Event detection (use tab-event-detect)

## Workflow

1. Ensure backend server and PostgreSQL are running
2. Call `POST /api/v1/genai-features/generate` to trigger feature generation
3. Wait for generation job to complete
4. Receive prediction features and sentiment scores for all tracked stocks

## API Endpoints Used

- `POST /api/v1/genai-features/generate` — Creates prediction features, sentiment scores, and AI-powered analysis for all tracked stocks

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Prediction features, sentiment scores, and AI-powered analysis for all tracked stocks
