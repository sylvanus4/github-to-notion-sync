---
name: mirofish-financial-sim
description: >-
  Run financial market scenario simulations using MiroFish multi-agent engine
  — predict market reactions to Fed decisions, earnings surprises,
  geopolitical events, and macroeconomic shifts through swarm intelligence.
  Use when the user asks to "simulate market scenario", "predict Fed impact",
  "financial simulation", "earnings reaction prediction", "금융 시나리오 시뮬레이션", "시장
  반응 예측", "Fed 영향 시뮬레이션", "mirofish-financial", or any request to simulate
  financial market reactions using AI agents. Do NOT use for static stock
  analysis without simulation (use daily-stock-check). Do NOT use for
  real-time market data only (use alphaear-stock). Do NOT use for general
  MiroFish operations (use mirofish).
---

# MiroFish Financial Scenario Simulation

## Overview

Specialized workflow for running financial market prediction simulations. Feeds market data and economic reports into MiroFish to create a digital financial world populated by investor agents, analyst agents, and institutional agents that react to injected market events.

## Prerequisites

Same as the `mirofish` skill. Verify: `curl -s http://localhost:5001/health`

**Backend base URL:** `http://localhost:5001` — all routes below are under `/api/...` as documented in the main `mirofish` skill.

## Quality Contract (aligned with simulation evals)

### EVAL 1 — Financial seed document

Before ontology generation, produce a markdown seed with:

| Element | Requirement |
|--------|-------------|
| Title | H1: e.g. `# Fed Rate Cut Scenario — {YYYY-MM-DD}` |
| Date | ISO date in metadata or title |
| Sections | ≥3 `##` blocks: Macro context, Key instruments/actors, Hypothesis & shock, Stakeholders |
| Entities | ≥5 named entities (Fed officials, indices, tickers, banks, policy names) |

Map user prompts to content:

- *Fed 금리 인하* → FOMC path, yields, USD, risk assets, bank EPS
- *NVDA 실적* → guidance, data-center revenue, supply chain, semis basket

Integrate optional context from `alphaear-news`, `trading-market-environment-analysis`, `alphaear-sentiment`.

### EVAL 2 — Simulation parameters (defaults + overrides)

State for the user before starting long-running steps:

| Parameter | Default | When to override |
|-----------|---------|------------------|
| Topic | User’s scenario text → `simulation_requirement` (multipart field for ontology) | Narrow if graph is too broad |
| Agents | ~26 after prepare (from graph) | Richer seed with more institutions → more personas |
| Rounds | 20 (standard); 25 for multi-leg macro narratives | Stop via `/api/simulation/stop` after N rounds if backend max is higher |
| `project_name` | `Financial-{short-slug}-{date}` | User-requested label |

### EVAL 3 — Report output structure

After report generation and optional Korean translation, ensure the user sees:

1. **Primary prediction** (equities, rates, FX, or cross-asset as relevant)
2. **Confidence** (high/medium/low + rationale)
3. **≥3 key factors** (data, positioning, policy, flows)
4. **Consensus vs divergence** across agent groups (institutional vs retail, bond vs equity, etc.)

### EVAL 4 — API sequence (do not invent paths)

Use the same canonical MiroFish HTTP API as `mirofish` (not `POST /graph` or `POST /simulation/run` shorthand):

1. `POST /api/graph/ontology/generate` (multipart: `files`, `simulation_requirement`, `project_name`) → `project_id`
2. `POST /api/graph/build` with `{"project_id": "..."}` → `task_id`; poll `GET /api/graph/task/<task_id>` until completed → `graph_id`
3. `POST /api/simulation/create` with `{"project_id": "<project_id>", "graph_id": "<graph_id>"}` → `simulation_id`
4. `POST /api/simulation/prepare` → poll `POST /api/simulation/prepare/status` until ready
5. `POST /api/simulation/start` with `{"simulation_id": "<simulation_id>"}`; monitor `GET /api/simulation/<simulation_id>/run-status`
6. `POST /api/report/generate` → poll `POST /api/report/generate/status` → `GET /api/report/<report_id>`

God’s Eye–style mid-run injections follow the main `mirofish` skill and product UI if available; do not assume a non-documented `prediction_requirement` field on `simulation/create`.

## Workflow

### Step 1: Prepare Financial Seed Document

Combine relevant financial data into a seed document:

```text
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

Save seed to e.g. `/tmp/mirofish-financial-seed-{date}.md` and verify the EVAL 1 table.

### Step 2: Ontology + graph build

```bash
curl -X POST http://localhost:5001/api/graph/ontology/generate \
  -F "files=@/tmp/mirofish-financial-seed-{date}.md" \
  -F "simulation_requirement=<concise scenario objective>" \
  -F "project_name=Financial-{slug}-{date}"

curl -X POST http://localhost:5001/api/graph/build \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>"}'

curl -s http://localhost:5001/api/graph/task/<task_id>
```

### Step 3: Create simulation, prepare, run

```bash
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>", "graph_id": "<graph_id>"}'

curl -X POST http://localhost:5001/api/simulation/prepare \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'

# Poll prepare/status every 30s until ready

curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'

curl -s http://localhost:5001/api/simulation/<simulation_id>/run-status
```

### Step 4: God’s Eye financial event injection (optional)

Typical financial variables to inject mid-simulation (when the product supports variable injection):

| Round | Event | Expected Impact |
|-------|-------|-----------------|
| 5 | Fed hints at rate cut in next meeting | Build anticipation |
| 10 | Fed announces 50bp emergency rate cut | Immediate reaction |
| 15 | Jobs report stronger than expected | Conflicting signal |
| 20 | Major bank reports increased loan defaults | Risk reassessment |

### Step 5: Report + structured summary

```bash
curl -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

After retrieval, map content to **EVAL 3** bullets. Translate to Korean per `mirofish` Step 6 rules when needed.

### Step 6: Cross-reference

After the report is ready, optionally inspect run dynamics:

1. **Sentiment timeline:** `GET /api/simulation/<simulation_id>/timeline` (when the deployment exposes it) — track shifts at injection points
2. **Agent positions:** use `mirofish` Phase 5 interview endpoints for key personas
3. **Consensus vs contrarian:** ask ReportAgent via `/api/report/chat`

Compare MiroFish predictions with:

- `daily-stock-check` current signals
- `trading-scenario-analyzer` static analysis
- `alphaear-predictor` time-series forecasts
- Historical data from `weekly-stock-update`

## Pre-Built Financial Agent Profiles

MiroFish automatically generates agent archetypes from financial seed data (examples):

- **Retail investor** — emotional, momentum-following, social media influenced
- **Hedge fund manager** — contrarian, leverage-aware, macro-focused
- **Pension fund allocator** — conservative, long-term, regulatory-constrained
- **Equity analyst** — fundamental-focused, consensus-tracking, earnings-driven
- **Bond trader** — rate-sensitive, duration-focused, flight-to-safety aware
- **Crypto trader** — risk-on/risk-off, narrative-driven, high volatility tolerance
- **Financial journalist** — narrative-amplifying, breaking-news reactive

For a full financial scenario template with detailed steps, see the mirofish skill’s [references/use-case-templates.md](../mirofish/references/use-case-templates.md) Template 1.

## Error Handling

| Error | Action |
|-------|--------|
| MiroFish backend unreachable | Start with `cd ~/thaki/MiroFish && npm run dev`. Verify: `curl -s http://localhost:5001/health` |
| Simulation create fails | Confirm `project_id` + `graph_id` from ontology/build; list projects via `GET /api/graph/project/list` |
| LLM API quota exceeded | Reduce monitored rounds or switch to a lower-cost model in `.env` |
| Zep Cloud rate limit | Prefer ≤20 rounds; monitor usage at app.getzep.com |
| No financial agents generated | Seed document may lack financial context. Add explicit stakeholder descriptions (EVAL 1). |

## Examples

```
/mirofish-financial -- Simulate market reaction to NVIDIA 10:1 stock split announcement
/mirofish-financial -- Upload these Fed minutes and predict 30-day S&P 500 trajectory
/mirofish-financial -- What happens if China announces 500B RMB stimulus? Run 25-round simulation
/mirofish-financial -- Simulate impact of surprise CPI print at 5.2% vs 4.1% consensus
```
