---
name: mirofish
description: Orchestrate MiroFish multi-agent swarm intelligence simulations — auto-generate seed documents from daily stock analysis, build GraphRAG knowledge graphs, run simulations with 26 AI agent personas, produce prediction reports, and interact with simulated agents. Supports a **Daily Stock Mode** for repeatable analysis from `today` pipeline outputs. Use when the user asks to "run MiroFish simulation", "predict scenario", "swarm simulation", "multi-agent prediction", "시뮬레이션 실행", "시나리오 예측", "MiroFish", "미로피쉬", "God's Eye injection", "digital sandbox", "/mirofish", or any request to simulate future scenarios using autonomous AI agents. Do NOT use for daily stock checks without simulation (use daily-stock-check). Do NOT use for simple financial news aggregation (use alphaear-news). Do NOT use for static technical analysis (use trading-technical-analyst).
---

# MiroFish Orchestrator

## Overview

MiroFish is a multi-agent swarm intelligence prediction engine. It constructs high-fidelity parallel digital worlds from seed documents using GraphRAG + autonomous agents with long-term memory (Zep Cloud), enabling "God's Eye View" variable injection for future scenario prediction.

**Repository:** `~/thaki/MiroFish/`
**Backend API:** `http://localhost:5001`
**Frontend UI:** `http://localhost:3000`

## Prerequisites

- MiroFish cloned to `~/thaki/MiroFish/`
- Dependencies installed: `npm run setup:all`
- `.env` configured with `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME`, `ZEP_API_KEY`
- Services running: `cd ~/thaki/MiroFish && npm run dev` (or `npm run backend` for API only)

Verify with: `curl -s http://localhost:5001/health`

> **IMPORTANT:** After updating `.env`, you MUST restart the backend. It caches env vars at startup.
> ```bash
> lsof -ti :5001 | xargs kill -9 && cd ~/thaki/MiroFish && npm run backend
> ```

---

## Daily Stock Mode (Primary Workflow)

The standard daily workflow auto-generates a seed document from `today` pipeline outputs, runs a 20-round simulation, and produces a prediction report. Total time: ~60 minutes.

### Timing Benchmarks (Measured 2026-03-16)

| Phase | Duration | Notes |
|-------|----------|-------|
| Seed document generation | ~10s | Auto-synthesize from analysis + news JSON |
| 1a: Ontology generation | ~15s | LLM only, no Zep |
| 1b: Graph build | ~4 min | Zep Cloud, ~48 nodes / ~79 edges |
| 2: Persona generation | ~10 min | 26 agents with full bios + behavioral logic |
| 3: Simulation (20 rounds) | ~35 min | Dual-platform (Twitter + Reddit), ~170 actions |
| 4: Report generation | ~10 min | LLM synthesizes all agent interactions |
| 5: Korean translation | ~3 min | Agent translates report to Korean |
| **Total** | **~63 min** | |

### Step-by-Step

**Step 0: Ensure backend is running and today's data exists**

```bash
curl -s http://localhost:5001/health
ls outputs/analysis-$(date +%Y-%m-%d).json outputs/news-$(date +%Y-%m-%d).json
```

If analysis/news files don't exist, run `today` pipeline first.

**Step 1: Generate seed document from daily outputs**

Read `outputs/analysis-{date}.json` and `outputs/news-{date}.json`, then synthesize a markdown seed document following the template in [references/daily-seed-template.md](references/daily-seed-template.md).

Key rules for seed document:
- Include ALL 5 news headlines as detailed sections with impact analysis
- List all BUY/SELL signal stocks with ticker, price, change%, RSI, ADX, and Turtle signal
- Always include the 6 standard stakeholder groups (see template)
- End with a "Simulation Objective" section with 4-6 specific questions
- Save to `/tmp/mirofish-seed-{date}.md`

**Step 2: Generate ontology + build graph**

```bash
# 2a: Ontology from seed (multipart/form-data)
curl -X POST http://localhost:5001/api/graph/ontology/generate \
  -F "files=@/tmp/mirofish-seed-{date}.md" \
  -F "simulation_requirement=Predict how institutional investors, retail traders, Fed officials, tech executives, energy traders, and Korean market participants interact over the next 20 trading days given today's market crisis signals" \
  -F "project_name=Daily-Stock-{date}"
# → project_id

# 2b: Build knowledge graph (JSON body)
curl -X POST http://localhost:5001/api/graph/build \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>"}'
# → task_id (async, poll every 30s for ~4min)

# 2c: Poll until complete
curl -s http://localhost:5001/api/graph/task/<task_id>
# Wait for status: "completed", extract graph_id from result
```

**Step 3: Create simulation + generate personas**

```bash
# 3a: Create simulation (project_id is REQUIRED)
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>", "graph_id": "<graph_id>"}'
# → simulation_id

# 3b: Prepare (persona generation, ~10min async)
curl -X POST http://localhost:5001/api/simulation/prepare \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
# → task_id

# 3c: Poll preparation status (every 30s for ~10min)
curl -X POST http://localhost:5001/api/simulation/prepare/status \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>", "task_id": "<task_id>"}'
# Wait for status: "ready" or already_prepared: true
```

**Step 4: Run simulation (20 rounds)**

```bash
# 4a: Start
curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'

# 4b: Monitor progress (poll every 60s for ~35min)
curl -s http://localhost:5001/api/simulation/<simulation_id>/run-status
# Check current_round vs max_rounds

# 4c: Stop after 20 rounds (if max > 20, stop manually)
curl -X POST http://localhost:5001/api/simulation/stop \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

**Step 5: Generate report**

```bash
# 5a: Generate
curl -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
# → report_id

# 5b: Poll status (every 60s for ~10min)
curl -X POST http://localhost:5001/api/report/generate/status \
  -H "Content-Type: application/json" \
  -d '{"report_id": "<report_id>"}'
# Wait for status: "completed"

# 5c: Retrieve report content
curl -s http://localhost:5001/api/report/<report_id>
```

**Step 6: Translate report to Korean**

MiroFish 백엔드의 LLM이 중국어로 리포트를 생성하므로, 최종 리포트를 한국어로 번역한다.

1. Step 5c에서 가져온 리포트 마크다운 원본을 `outputs/mirofish-report-{date}-raw.md`로 저장
2. 리포트 내용을 섹션별로 한국어로 번역 (아래 규칙 적용):
   - 고유명사(기업명, 인물명, 티커)는 원문 유지 (e.g., NVIDIA, BlackRock, Powell)
   - 금융 전문용어는 한국어 + 영문 병기 (e.g., 변동성(Volatility), 수익률(Return))
   - 에이전트 이름과 역할은 원문 보존하되, 발언 내용은 한국어로 번역
   - 수치, 날짜, 퍼센트 등 데이터는 그대로 유지
   - 마크다운 구조(헤딩, 테이블, 리스트)는 원본과 동일하게 보존
3. 번역된 리포트를 `outputs/mirofish-report-{date}.md`로 저장

> **번역 품질 기준:** 전문 금융 애널리스트 보고서 수준의 한국어. "~했습니다" 체 사용, 구어체 금지.

**Step 7: Save and distribute**

Save the Korean report to `outputs/mirofish-report-{date}.md` (raw Chinese version kept as `-raw.md`).
Optionally post key predictions to Slack `#h-report` or `#deep-research`.

### Same-Day Rerun (Skip Persona Generation)

If a simulation already has `already_prepared: true`, the prepare step returns immediately.
Re-running with the **same simulation_id** skips the 10-minute persona generation:

```bash
# Check if already prepared
curl -X POST http://localhost:5001/api/simulation/prepare/status \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
# If already_prepared: true → proceed directly to start

curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

### Listing Previous Runs

```bash
# List all projects
curl -s http://localhost:5001/api/graph/project/list

# List all simulations with status
curl -s http://localhost:5001/api/simulation/list

# List all reports
curl -s http://localhost:5001/api/report/list

# Get report by simulation ID
curl -s http://localhost:5001/api/report/by-simulation/<simulation_id>
```

---

## Ad-Hoc Mode (Custom Scenarios)

For non-daily scenarios (e.g., "What if NVIDIA announces a 10:1 stock split?"), use the full 5-phase pipeline with a custom seed document.

### Phase 1: Graph Build

```bash
# 1a: Ontology (multipart/form-data)
curl -X POST http://localhost:5001/api/graph/ontology/generate \
  -F "files=@/path/to/seed.md" \
  -F "simulation_requirement=<describe scenario>" \
  -F "project_name=<name>"

# 1b: Graph build (JSON)
curl -X POST http://localhost:5001/api/graph/build \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>"}'

# 1c: Poll (every 30s)
curl -s http://localhost:5001/api/graph/task/<task_id>
```

### Phase 2: Environment Setup

```bash
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "<project_id>", "graph_id": "<graph_id>"}'

curl -X POST http://localhost:5001/api/simulation/prepare \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

### Phase 3: Simulation

```bash
curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'

# Monitor
curl -s http://localhost:5001/api/simulation/<simulation_id>/run-status
```

### Phase 4: Report

```bash
curl -X POST http://localhost:5001/api/report/generate \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>"}'
```

### Phase 4.5: Korean Translation

리포트 생성 후, Daily Stock Mode Step 6과 동일한 번역 규칙을 적용하여 한국어 리포트를 생성한다. 원본은 `-raw.md`로 보존.

### Phase 5: Deep Interaction

```bash
# Interview a specific agent
curl -X POST http://localhost:5001/api/simulation/interview \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "<simulation_id>", "agent_id": "<agent_id>", "question": "<question>"}'

# Chat with ReportAgent
curl -X POST http://localhost:5001/api/report/chat \
  -H "Content-Type: application/json" \
  -d '{"report_id": "<report_id>", "message": "<question>"}'
```

---

## Standard Agent Personas (26 Agents)

The daily stock mode consistently generates ~26 agents across 6 stakeholder groups.
These are NOT predefined — they are auto-generated from graph entities each run, but the standard seed template ensures consistent types:

| Group | Example Agents | Typical Count |
|-------|---------------|---------------|
| Institutional Investors | BlackRock, Vanguard, hedge fund managers | 4-5 |
| Retail Investors | Individual traders, Korean retail | 3-4 |
| Fed Officials | Powell, Kashkari, FOMC members | 3-4 |
| Big Tech Executives | NVIDIA CEO, Apple CEO, Meta CEO | 4-5 |
| Energy & Commodity Traders | Oil analysts, gold traders | 3-4 |
| Korean Market Participants | Samsung Securities, Korean institutions | 3-4 |

> Do NOT modify the 6 stakeholder groups unless the market structure fundamentally changes.
> Adding more groups increases simulation time and token cost without proportional insight gain.

## Sub-Skills

| Sub-Skill | Trigger | Reference |
|-----------|---------|-----------|
| daily-sim | "daily simulation", "일일 시뮬레이션" | Daily Stock Mode above |
| graph-build | "build graph", "그래프 구축" | Phase 1 |
| env-setup | "setup agents", "에이전트 생성" | Phase 2 |
| simulate | "run simulation", "시뮬레이션 시작" | Phase 3 |
| report | "generate report", "리포트 생성" | Phase 4 |
| interact | "interview agent", "에이전트 대화" | Phase 5 |

## Integration with Existing Skills

| Skill | Integration Pattern |
|-------|-------------------|
| **today** | Run `today` first → use `outputs/analysis-{date}.json` + `outputs/news-{date}.json` as seed source |
| **alphaear-news** | Additional news context for richer seed documents |
| **alphaear-sentiment** | Score MiroFish agent responses for sentiment validation |
| **trading-scenario-analyzer** | Quick pre-analysis before committing to a full MiroFish run |
| **paper-review** | Post-publication verification via MiroFish simulation |
| **md-to-notion** | Publish `outputs/mirofish-report-{date}.md` to Notion |

## Configuration Notes

- **20 rounds = optimal daily default.** Produces ~170 actions across Twitter + Reddit. Sufficient for meaningful patterns without excessive token cost.
- **Token consumption:** ~$1-3 per 20-round simulation (LLM API costs). 40+ rounds scale roughly linearly.
- **Zep Cloud free tier:** Sufficient for 1 daily simulation. Monitor at app.getzep.com.
- **Backend restart required** after any `.env` change — the server caches config at startup.
- **Boost LLM (optional):** Set `LLM_BOOST_*` env vars for faster agent interactions.

## Polling Intervals

| Operation | Interval | Typical Duration |
|-----------|----------|-----------------|
| Graph build | 30s | 3-5 min |
| Persona preparation | 30s | 8-12 min |
| Simulation progress | 60s | 30-40 min (20 rounds) |
| Report generation | 60s | 8-12 min |
| Korean translation | N/A (synchronous) | 2-4 min |

## Error Handling

| Error | Action |
|-------|--------|
| `curl: (7) Failed to connect` | Backend not running → `cd ~/thaki/MiroFish && npm run backend` |
| `{"error": "API key not configured"}` | Check `LLM_API_KEY` in `~/thaki/MiroFish/.env` |
| `status_code: 401, body: unauthorized` (Zep) | Invalid ZEP_API_KEY → get from https://app.getzep.com/ and **restart backend** |
| `请提供 project_id` | `create_simulation` requires `project_id` in the request body |
| Graph build hangs | Poll via `GET /api/graph/task/<task_id>`. Large docs may need chunking. |
| Prepare fails | Zep API rate-limited or key expired. Check app.getzep.com |
| Report timeout | 40+ round simulations → 5-10 min. Poll `/api/report/generate/status` |
| Agent interview returns empty | Verify agent_id from `GET /api/simulation/<id>/profiles` |

## Output Naming Convention

```
outputs/mirofish-report-{YYYY-MM-DD}.md       # Korean-translated prediction report (final)
outputs/mirofish-report-{YYYY-MM-DD}-raw.md   # Original LLM output (Chinese, archived)
/tmp/mirofish-seed-{YYYY-MM-DD}.md            # Seed document (ephemeral)
```

## Examples

```
/mirofish -- Run daily stock simulation from today's analysis data
/mirofish -- Upload Fed minutes and predict 30-day market reactions
/mirofish simulate -- Start simulation with God's Eye: "NVIDIA announces 10:1 stock split"
/mirofish report -- Generate prediction report from completed simulation
/mirofish interact -- Ask agent "Warren Buffett" about portfolio allocation
/mirofish -- Rerun today's simulation with same personas (same-day rerun)
```
