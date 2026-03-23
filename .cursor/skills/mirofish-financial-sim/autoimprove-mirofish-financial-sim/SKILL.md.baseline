---
name: mirofish-financial-sim
description: Run financial market scenario simulations using MiroFish multi-agent engine — predict market reactions to Fed decisions, earnings surprises, geopolitical events, and macroeconomic shifts through swarm intelligence. Use when the user asks to "simulate market scenario", "predict Fed impact", "financial simulation", "earnings reaction prediction", "금융 시나리오 시뮬레이션", "시장 반응 예측", "Fed 영향 시뮬레이션", "mirofish-financial", or any request to simulate financial market reactions using AI agents. Do NOT use for static stock analysis without simulation (use daily-stock-check). Do NOT use for real-time market data only (use alphaear-stock). Do NOT use for general MiroFish operations (use mirofish).
---

# MiroFish Financial Scenario Simulation

## Overview

Specialized workflow for running financial market prediction simulations. Feeds market data and economic reports into MiroFish to create a digital financial world populated by investor agents, analyst agents, and institutional agents that react to injected market events.

## Prerequisites

Same as the `mirofish` skill. Verify: `curl -s http://localhost:5001/health`

## Workflow

### Step 1: Prepare Financial Seed Document

Combine relevant financial data into a seed document:

```python
seed_sources = [
    "Fed FOMC minutes or press conference transcript",
    "Company earnings reports (10-K, 10-Q)",
    "Macro indicators (CPI, unemployment, GDP)",
    "Financial news articles from alphaear-news",
    "Analyst reports and consensus estimates"
]
```

**Integration with existing skills:**
- Run `alphaear-news` first to gather current financial news
- Use `trading-market-environment-analysis` for macro context
- Pull `alphaear-sentiment` scores for baseline sentiment

### Step 2: Configure Financial Simulation

```bash
# Create simulation with financial parameters
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "<graph_id>",
    "prediction_requirement": "Predict market reactions if the Federal Reserve announces a 50bp rate cut. Simulate individual investors, institutional investors (hedge funds, pension funds), equity analysts, bond traders, and crypto traders. Focus on S&P 500, 10Y Treasury, BTC, and gold over 30 days.",
    "num_rounds": 25
  }'
```

### Step 3: God's Eye Financial Event Injection

Typical financial variables to inject mid-simulation:

| Round | Event | Expected Impact |
|-------|-------|-----------------|
| 5 | "Fed hints at rate cut in next meeting" | Build anticipation |
| 10 | "Fed announces 50bp emergency rate cut" | Immediate reaction |
| 15 | "Jobs report comes in stronger than expected" | Conflicting signal |
| 20 | "Major bank reports increased loan defaults" | Risk reassessment |

### Step 4: Analyze Results

After simulation completes:

1. **Sentiment timeline:** `GET /api/simulation/<id>/timeline` — track sentiment shifts at each injection point
2. **Agent positions:** Interview key agents about their portfolio decisions
3. **Consensus vs contrarian:** Ask ReportAgent to identify consensus trades and contrarian bets
4. **Generate actionable output:** Feed results into `alphaear-reporter` for a structured investment report

### Step 5: Cross-Reference

Compare MiroFish predictions with:
- `daily-stock-check` current signals
- `trading-scenario-analyzer` static analysis
- `alphaear-predictor` time-series forecasts
- Historical data from `weekly-stock-update`

## Pre-Built Financial Agent Profiles

MiroFish automatically generates these agent archetypes from financial seed data:

- **Retail investor** — emotional, momentum-following, social media influenced
- **Hedge fund manager** — contrarian, leverage-aware, macro-focused
- **Pension fund allocator** — conservative, long-term, regulatory-constrained
- **Equity analyst** — fundamental-focused, consensus-tracking, earnings-driven
- **Bond trader** — rate-sensitive, duration-focused, flight-to-safety aware
- **Crypto trader** — risk-on/risk-off, narrative-driven, high volatility tolerance
- **Financial journalist** — narrative-amplifying, breaking-news reactive

For a full financial scenario template with detailed steps, see the mirofish skill's [references/use-case-templates.md](../mirofish/references/use-case-templates.md) Template 1.

## Error Handling

| Error | Action |
|-------|--------|
| MiroFish backend unreachable | Start with `cd ~/thaki/MiroFish && npm run dev`. Verify: `curl -s http://localhost:5001/health` |
| Simulation create fails | Ensure `graph_id` is valid — list graphs with `GET /api/graph/project/list` |
| LLM API quota exceeded | Reduce `num_rounds` or switch to a lower-cost model (e.g., `qwen-plus`) |
| Zep Cloud rate limit | Start with ≤20 rounds. Monitor usage at app.getzep.com |
| No financial agents generated | Seed document may lack financial context. Add explicit stakeholder descriptions. |

## Examples

```
/mirofish-financial -- Simulate market reaction to NVIDIA 10:1 stock split announcement
/mirofish-financial -- Upload these Fed minutes and predict 30-day S&P 500 trajectory
/mirofish-financial -- What happens if China announces 500B RMB stimulus? Run 25-round simulation
/mirofish-financial -- Simulate impact of surprise CPI print at 5.2% vs 4.1% consensus
```
