---
name: tab-llm-agents
description: >-
  Run LLM agent pipeline via POST /llm-agents/run and refresh macro data via
  POST /llm-agents/macro/refresh. Use when running LLM agents, 'LLM 에이전트 실행',
  'tab-llm-agents'. Do NOT use for GenAI features (use tab-genai-features),
  stock price sync (use tab-stock-sync), or daily stock check (use
  daily-stock-check).
---

# tab-llm-agents

## Purpose

Runs the LLM agents pipeline and refreshes macro economic data. Calls `POST /llm-agents/run` to trigger the agent pipeline (predictions, portfolio analysis, sentiment) and `POST /llm-agents/macro/refresh` to update macroeconomic indicators.

## When to Use

- run llm agents
- LLM 에이전트 실행
- tab-llm-agents
- agent pipeline run

## When NOT to Use

- GenAI feature generation (use tab-genai-features)
- Stock price sync (use tab-stock-sync)
- Daily stock check (use daily-stock-check)

## Workflow

1. Ensure backend server and PostgreSQL are running
2. Call `POST /api/v1/llm-agents/run` to trigger the agent pipeline
3. Call `POST /api/v1/llm-agents/macro/refresh` to update macroeconomic indicators
4. Wait for pipeline completion

## API Endpoints Used

- `POST /api/v1/llm-agents/run` — Triggers agent pipeline (predictions, portfolio analysis, sentiment)
- `POST /api/v1/llm-agents/macro/refresh` — Updates macroeconomic indicators

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock data

## Output

Updated LLM agent outputs (predictions, portfolio analysis, sentiment) and refreshed macroeconomic indicator data
