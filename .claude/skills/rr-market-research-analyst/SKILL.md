---
name: rr-market-research-analyst
description: >-
  Role Replacement Case Study: Market Research Analyst / Quant Trader —
  orchestrates the full daily market intelligence lifecycle from data sync
  through multi-strategy backtesting, multi-agent debate, quality gate, and
  broker integration. Thin harness composing today, daily-strategy-engine,
  trading-agent-desk, ai-quality-evaluator, toss-ops-orchestrator, and
  pine-script-generator into a single market-analyst role pipeline with
  MemKraft-powered decision memory and adversarial quality validation.
---

# Role Replacement: Market Research Analyst / Quant Trader

## What This Replaces

A human Market Research Analyst / Quant Trader who:
- Arrives at 7 AM, checks overnight market moves across US/KR/Asia
- Runs technical screens (SMA, RSI, MACD, Bollinger, Donchian) across 50+ tickers
- Backtests 7 strategies against 16 blue-chip stocks with commission modeling
- Conducts dialectical analysis (bull vs bear case) for top candidates
- Validates report quality before distribution
- Generates Pine Script indicators for TradingView monitoring
- Interfaces with the brokerage for signal-to-order translation
- Maintains a decision journal and reflects on past calls

This skill replaces the full daily cycle of a quantitative market analyst, compressing
8+ hours of research, analysis, and reporting into a single automated pipeline with
memory-driven context continuity.

## Prerequisites

| Requirement | Check |
|-------------|-------|
| `today` pipeline prerequisites | `python scripts/weekly_stock_update.py --status` returns OK |
| PostgreSQL with price data | `DATABASE_URL` env var set; prices synced |
| Slack MCP connected | `slack_send_message` available |
| MemKraft directories exist | `memory/memkraft/` directory present |
| `ai-context-router` operational | Can query both MemKraft and LLM Wiki |
| Python 3.11+ | `python --version` >= 3.11 |
| `python-docx` installed | For DOCX report generation |

Optional (enhance output quality):
- TradingView MCP servers (`fiale-plus`, `atilaahmettaner`) for cross-validation
- Toss Securities `tossctl` CLI for broker integration
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` for agent-desk debate

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           rr-market-research-analyst                     │
│           (Thin Harness Orchestrator)                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phase 0: MemKraft Context Pre-load                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │ ai-context-router → retrieve:                     │  │
│  │   HOT: yesterday's decisions, active positions    │  │
│  │   WARM: strategy performance patterns, lessons    │  │
│  │   KB: market regime history, sector correlations  │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 1: Full Pipeline Execution                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │ today (16-phase):                                 │  │
│  │   DB sync → fundamentals → hot stock discovery →  │  │
│  │   screening → analysis (SMA/RSI/MACD/ADX) →       │  │
│  │   news + sentiment → DOCX report → Slack          │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 2: Strategy Engine                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │ daily-strategy-engine:                            │  │
│  │   7 strategies × 16 tickers → 112 evaluations →   │  │
│  │   commission-aware ranking → Top 10 cards          │  │
│  │   + OvernightDipBuy with paired limit orders       │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 3: Agent Desk Debate (top 3-5 signals)           │
│  ┌───────────────────────────────────────────────────┐  │
│  │ trading-agent-desk:                               │  │
│  │   4 Analysts (parallel) → Bull/Bear Debate →      │  │
│  │   Research Manager → Risk Evaluator →              │  │
│  │   DeskDecision per symbol                          │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 4: Quality Gate                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ ai-quality-evaluator:                             │  │
│  │   6 dimensions (Accuracy, Consistency, Coverage,   │  │
│  │   Actionability, External Consensus, Tone) →       │  │
│  │   PASS (≥8.0) / REVIEW (6.0-7.9) / FAIL (<6.0)   │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 5: Broker Integration (conditional)              │
│  ┌───────────────────────────────────────────────────┐  │
│  │ toss-ops-orchestrator:                            │  │
│  │   snapshot → FX → risk → signal bridge →           │  │
│  │   order previews (NO auto-execution)               │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 6: Pine Script Generation (optional)             │
│  ┌───────────────────────────────────────────────────┐  │
│  │ pine-script-generator:                            │  │
│  │   Generate TradingView indicators for top BUY      │  │
│  │   stocks from strategy cards                       │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ▼                               │
│  Phase 7: MemKraft Write-back & Daily Digest            │
│  ┌───────────────────────────────────────────────────┐  │
│  │ memkraft-ingest:                                  │  │
│  │   Store today's decisions, strategy outcomes,      │  │
│  │   debate conclusions, quality score to HOT tier    │  │
│  │ + Consolidated Slack digest to #h-report           │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Pipeline Output Protocol

All phases persist structured output following `pipeline-skill-intermediate-persistence.mdc`:

```
outputs/rr-market-analyst/{date}/
├── manifest.json                    # Phase status tracker
├── phase-0-memkraft-context.json    # Pre-loaded context summary
├── phase-1-pipeline-summary.json    # today pipeline output summary
├── phase-2-strategy-cards.json      # Top 10 backtested strategy cards
├── phase-3-desk-decisions.json      # Agent desk debate outcomes
├── phase-4-quality-report.md        # Quality gate evaluation
├── phase-5-broker-preview.json      # Toss order previews (if applicable)
├── phase-6-pine-scripts/            # Generated Pine Script files
│   ├── {SYMBOL}_composite.pine
│   └── ...
└── phase-7-daily-digest.md          # Consolidated summary
```

### manifest.json Schema

```json
{
  "skill": "rr-market-research-analyst",
  "date": "2026-04-15",
  "started_at": "2026-04-15T07:00:00+09:00",
  "phases": {
    "memkraft_preload": { "status": "completed", "file": "phase-0-memkraft-context.json" },
    "pipeline": { "status": "completed", "file": "phase-1-pipeline-summary.json" },
    "strategy_engine": { "status": "completed", "file": "phase-2-strategy-cards.json" },
    "agent_desk": { "status": "completed", "file": "phase-3-desk-decisions.json" },
    "quality_gate": { "status": "completed", "file": "phase-4-quality-report.md", "score": 8.4 },
    "broker": { "status": "skipped", "reason": "tossctl unavailable" },
    "pine_scripts": { "status": "completed", "file": "phase-6-pine-scripts/" },
    "writeback": { "status": "completed", "file": "phase-7-daily-digest.md" }
  }
}
```

## Execution Steps

### Phase 0: MemKraft Context Pre-load

Before any analysis, retrieve yesterday's market context to avoid cold-start:

1. Query `ai-context-router` with topics: `["market decisions", "strategy outcomes", "position changes", "market regime"]`
2. Retrieve from MemKraft HOT tier:
   - Yesterday's top BUY/SELL decisions and their post-decision outcomes
   - Active positions from `toss-daily-snapshot`
   - Agent desk debate conclusions
3. Retrieve from MemKraft WARM tier:
   - Strategy win-rate trends (rolling 30-day)
   - Recurring sector rotation patterns
   - Past false-signal patterns to watch for
4. Retrieve from KB tier:
   - Market regime classification (bull/bear/sideways) from `market-environment`
   - Sector correlation data
5. Persist to `phase-0-memkraft-context.json` with provenance tags

**Context injection**: The pre-loaded context is passed to Phase 3 (Agent Desk) as additional input, enabling debate agents to reference past lessons and avoid repeating mistakes.

### Phase 1: Full Pipeline Execution

Delegate to `today` skill with default parameters:

```
today --with-tradingview (default)
```

This runs the full 16-phase pipeline:
- DB vs CSV freshness check + multi-provider backfill
- Hot stock discovery from NASDAQ/KOSPI/KOSDAQ 100
- Multi-factor screening (P/E, RSI, volume, MA crossovers, FCF yield)
- SMA 20/55/200 + RSI/MACD/Stochastic/ADX analysis
- News fetch (alphaear-news) + sentiment (alphaear-sentiment)
- DOCX report generation via `anthropic-docx`
- Slack posting to `#h-report`
- TradingView cross-validation stages

**Error handling**: If `today` fails at any phase, log the failure phase, persist partial results, and continue to Phase 2 with whatever data is available. Do NOT abort the entire pipeline for a single phase failure.

Extract from `today` outputs:
- `outputs/analysis-{date}.json` → signals per ticker
- `outputs/screener-{date}.json` → screening results
- `outputs/reports/daily-{date}.docx` → generated report

### Phase 2: Strategy Engine

Delegate to `daily-strategy-engine`:

```bash
python scripts/daily_strategy_engine.py --date {date}
```

Input: Phase 1 analysis and screener outputs
Output: `outputs/strategy-cards-{date}.json` with Top 10 cards

Key outputs per card:
- Symbol, strategy name, signal direction
- Entry/stop-loss/target prices
- Commission-aware Sharpe, win rate, total return
- Risk assessment (VaR, stress scenario, correlation, concentration)
- Execution guidance (optimal window, volume threshold, slippage)
- TradingView consensus (agree/disagree/no_data)
- OvernightDipBuy cards include `sell_limit_price` for paired orders

Copy strategy cards to `phase-2-strategy-cards.json`.

### Phase 3: Agent Desk Debate

Select the **top 3-5 BUY signals** from strategy cards (by composite score) and run `trading-agent-desk` for each:

1. **4 Analysts** (parallel, quick model):
   - Technical: Consumes `analysis-{date}.json`
   - Fundamental: Consumes screener data
   - Sentiment: Consumes alphaear-sentiment outputs
   - News: Consumes alphaear-news outputs

2. **Bull/Bear Debate** (2 rounds, deep model):
   - Both receive analyst reports + Phase 0 MemKraft context
   - BM25 memory retrieval of similar past situations
   - Consensus fast-track if all analysts agree (>70 or <30)

3. **Research Manager Synthesis** → BUY/SELL/HOLD + confidence + Korean rationale

4. **Risk Evaluator** → position size + VaR + stress scenarios + compliance gate

Persist `DeskDecision` per symbol to `phase-3-desk-decisions.json`.

**Adversarial critique**: The MemKraft context from Phase 0 feeds into the Bear Researcher, enabling it to cite past false signals and strategy drawdowns as counter-arguments. This is the key differentiator from running `trading-agent-desk` standalone.

### Phase 4: Quality Gate

Delegate to `ai-quality-evaluator` on the generated DOCX report:

Evaluation inputs:
- `outputs/reports/daily-{date}.docx`
- `outputs/analysis-{date}.json`
- Ground truth from `weekly_stock_update.py --status`
- TradingView cross-validation files (if available)

6 dimensions scored (0-10, weighted):
| Dimension | Weight |
|-----------|--------|
| Accuracy | 25% |
| Consistency | 15% |
| Coverage | 15% |
| Actionability | 20% |
| External Consensus | 15% |
| Tone | 10% |

Gate decisions:
- **PASS (≥ 8.0)**: Continue to Phase 5
- **REVIEW (6.0-7.9)**: Log issues, continue with warnings appended to digest
- **FAIL (< 6.0)**: Halt broker integration, post failure notice to Slack, recommend re-generation

Persist evaluation to `phase-4-quality-report.md`.

### Phase 5: Broker Integration (Conditional)

**Prerequisites**: `tossctl` CLI available and authenticated.

If quality gate is PASS or REVIEW, delegate to `toss-ops-orchestrator`:
1. Daily snapshot (positions, account summary)
2. FX rate derivation (USD/KRW for US stock sizing)
3. Risk monitor (concentration, drawdown, sector exposure)
4. Signal bridge: translate strategy cards to `tossctl` order previews
5. Portfolio reconciliation (signals vs actual holdings)

**CRITICAL**: This phase generates **order previews only**. No orders are auto-executed. The user must explicitly approve via `tossinvest-trading` with the 7-layer Safety Model.

If `tossctl` is unavailable, skip this phase with `status: "skipped"` in manifest.

### Phase 6: Pine Script Generation (Optional)

For the top BUY stocks from strategy cards, delegate to `pine-script-generator`:

Generate composite TradingView indicators including:
- SMA 20/55/200 overlay
- RSI + MACD panel
- Bollinger Bands with %B
- Donchian Channel
- ADX/Stochastic panel

Output Pine Script v5 files to `phase-6-pine-scripts/{SYMBOL}_composite.pine`.

Skip if `--skip-pine` flag is set or no BUY signals exist.

### Phase 7: MemKraft Write-back & Daily Digest

1. **MemKraft Ingest** (HOT tier):
   - Today's desk decisions with confidence scores
   - Quality gate score and any issues flagged
   - Strategy cards that passed the quality gate
   - Broker preview results (if available)
   - New patterns identified during debate

2. **Consolidated Digest**: Build a markdown summary covering:
   - Market overview (from Phase 1)
   - Top strategy cards (from Phase 2)
   - Debate outcomes with conviction levels (from Phase 3)
   - Quality score (from Phase 4)
   - Broker status (from Phase 5, if run)
   - Pine Script generation status (from Phase 6)

3. **Slack Distribution**: Post digest as a thread reply to the `#h-report` root message posted by Phase 1, with structure:
   - Reply 1: Strategy cards summary (top 5 with scores)
   - Reply 2: Agent desk debate outcomes (conviction + rationale)
   - Reply 3: Quality gate result + broker preview status

## Memory Configuration

| Tier | Content | TTL | Source |
|------|---------|-----|--------|
| HOT | Today's decisions, active signals, quality scores | 7 days | Phase 3, 4, 5 outputs |
| WARM | Strategy win-rate trends, sector rotation patterns, false signal history | 90 days | Rolling aggregation from HOT |
| Knowledge | Market regime history, correlation matrices, commission models | Persistent | `trading-daily` KB topic |

### Decision Memory Store

The agent desk maintains its own BM25-indexed memory at `outputs/agent-desk/memory/trade_memory.json`. This skill ensures:
- New decisions are appended after Phase 3
- Reflection runs after market close (comparing decisions to actual outcomes)
- Memory is queried during Phase 0 pre-load for similar historical situations

## Error Recovery

| Phase | Failure | Action |
|-------|---------|--------|
| 0 (MemKraft) | Context retrieval fails | Continue with empty context; log warning |
| 1 (Pipeline) | `today` fails at any sub-phase | Persist partial results; continue with available data |
| 1 (Pipeline) | No analysis JSON produced | Abort Phases 2-3; skip to Phase 7 with error digest |
| 2 (Strategy) | Script fails or empty cards | Skip Phase 3 debate; proceed to Phase 4 with pipeline report only |
| 3 (Debate) | LLM API timeout or rate limit | Retry once with 30s backoff; on second failure, skip with warning |
| 3 (Debate) | Cost exceeds $5 budget | Halt debate, use strategy cards directly |
| 4 (Quality) | Evaluation errors | Default to REVIEW gate; append error to digest |
| 5 (Broker) | `tossctl` unavailable | Skip with `status: "skipped"` in manifest |
| 6 (Pine) | Generation fails | Skip; non-critical output |
| 7 (Write-back) | MemKraft ingest fails | Log warning; digest posted to Slack regardless |

## Security Rules

- **No auto-execution**: Phase 5 produces order PREVIEWS only. Live orders require explicit user approval through `tossinvest-trading` with signal strength ≥ 0.5
- **Cost cap**: Phase 3 agent desk debate is capped at $5 per run (~30 symbol analyses)
- **No credential exposure**: API keys, account numbers, and access tokens are never logged or included in outputs
- **Disclaimer**: All Slack posts include "투자 권유가 아닙니다" (not financial advice)
- **Account masking**: Toss account numbers are masked in all output files

## Honest Reporting

- Report outcomes faithfully — never claim all phases passed when any failed
- Never suppress errors, partial results, or skipped phases
- Surface unexpected findings even if they complicate the narrative
- If a phase produces no actionable output, say so explicitly

## Coordinator Synthesis

- Do not reconstruct phase outputs from chat context — always read from persisted files
- Each phase dispatch includes a purpose statement explaining the expected transformation
- File paths and line numbers must be specific, not inferred
- Never delegate with vague instructions like "analyze this" — provide concrete specs

## Subagent Contract

Every subagent dispatch MUST include:
1. **Purpose statement** — one sentence explaining why this subagent exists
2. **Absolute file paths** — all input/output paths as absolute paths
3. **Return contract** — subagent must return JSON: `{"status": "ok|error", "file": "<output_path>", "summary": "<1-line>"}`
4. Load-bearing outputs must be written to disk, not passed via chat context

## Operational Runbook

### Daily Operation (07:00 KST)

```
1. Trigger: /rr-market-research-analyst or scheduled via daily-am-orchestrator
2. Phase 0: MemKraft pre-loads yesterday's decisions (30s)
3. Phase 1: today pipeline runs (5-10 min)
4. Phase 2: Strategy engine generates cards (2-3 min)
5. Phase 3: Agent desk debates top signals (3-5 min, $0.80-$1.60)
6. Phase 4: Quality gate evaluates report (1-2 min)
7. Phase 5: Broker preview if tossctl available (1 min)
8. Phase 6: Pine Script generation for top BUY stocks (30s)
9. Phase 7: MemKraft write-back + Slack digest (30s)
Total: 15-25 minutes
```

### Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Phase 1 produces no analysis | DB prices stale | Run `weekly-stock-update` first |
| Phase 2 empty strategy cards | Insufficient price history (<60 days) | Backfill via `stock-csv-downloader` |
| Phase 3 debate inconclusive | Low analyst agreement, extreme market | Check MemKraft for regime context |
| Phase 4 FAIL score | Hallucinated prices or signals | Verify DB freshness; re-run Phase 1 |
| Phase 5 skipped repeatedly | `tossctl` auth expired | Run `tossinvest-setup` to re-authenticate |

### Weekend/Holiday Handling

- Phase 1 uses last trading day's data (date check skipped)
- Phase 2 strategy cards are labeled with the last valid trading date
- Phase 5 broker integration is skipped on non-trading days
- Phase 7 digest notes "비거래일 분석" in the header

## Comparison: Human Analyst vs This Skill

| Dimension | Human Analyst | rr-market-research-analyst |
|-----------|---------------|---------------------------|
| Coverage | 15-30 tickers manually | 50+ tickers across KR/US markets |
| Strategies tested | 2-3 favorite strategies | 7 strategies × 16 tickers = 112 evaluations |
| Backtesting | Approximate mental models | Commission-aware simulation with VaR |
| Debate quality | Internal bias, confirmation risk | Structured 4-analyst + bull/bear dialectic |
| Quality validation | Self-review (blind spots) | 6-dimension automated quality gate |
| Decision memory | Informal notes/journal | BM25-indexed memory with reflection |
| Reproducibility | Low (mood, fatigue dependent) | Deterministic pipeline, same inputs = same outputs |
| Time to report | 4-8 hours | 15-25 minutes |
| Cost | $400-800/day salary | ~$2-5/day (LLM API + compute) |

### What This Skill Does NOT Replace

- **Discretionary judgment**: Novel macro events (war, pandemic) require human override
- **Client relationships**: Institutional analyst roles with client-facing responsibilities
- **Regulatory compliance**: Fiduciary duty, licensing, and compliance sign-off
- **Market making**: High-frequency or latency-sensitive execution strategies

## Examples

```
User: 마켓 리서치 분석 전체 파이프라인 돌려줘
Agent: rr-market-research-analyst 실행:
  Phase 0: MemKraft에서 어제 NVDA BUY 결정 + SK Hynix 오버나이트 결과 로드
  Phase 1: today 파이프라인 16단계 실행 (48개 종목 분석)
  Phase 2: 7전략 × 16종목 = 112개 평가 → Top 10 카드 생성
    1. NVDA Turtle BUY @ $850, Sharpe 1.8, TV consensus: agree
    2. 005930 Bollinger I BUY @ ₩78,500, Sharpe 1.4
    3. 000660 OvernightDipBuy @ ₩185,000 → 매도호가 ₩188,500
    ...
  Phase 3: Top 3 (NVDA, 005930, 000660) → Agent Desk 토론
    NVDA: BUY 유지 (신뢰도 82%, Bear 반론: 밸류에이션 부담)
    005930: BUY (신뢰도 75%, 반도체 사이클 상승 합의)
    000660: HOLD 변경 (신뢰도 55%, 오버나이트 리스크 vs 리워드 불충분)
  Phase 4: 품질 게이트 8.2/10 → PASS
  Phase 5: Toss 주문 미리보기 2건 생성 (실행 없음)
  Phase 6: NVDA_composite.pine, 005930_composite.pine 생성
  Phase 7: MemKraft에 결정 저장 + #h-report 쓰레드 3건 게시

User: 퀀트 트레이더 자동화 — 오늘 오버나이트 전략만 집중
Agent: Phase 2에서 OvernightDipBuy 필터링 →
  000660 SK Hynix: Dip Score 0.72, 평균 수익 0.45%
  012450 한화에어: Dip Score 0.55, 평균 수익 0.38%
  Phase 3 debate → 000660만 통과 (012450 볼륨 부족 리스크)
  Phase 5: 매수 ₩185,000 + 매도 지정가 ₩188,500 미리보기

User: 어제 결정 복기 결과 알려줘
Agent: MemKraft HOT tier 조회:
  어제 NVDA BUY @ $850 → 오늘 종가 $862 (+1.4%) ✅
  어제 005930 BUY @ ₩78,500 → 오늘 종가 ₩77,800 (-0.9%) ⚠️
  Agent desk reflection: 005930 결정 시 Bear의 외국인 매도 경고 무시됨
  → WARM tier에 "외국인 순매도 3일 연속 시 005930 BUY 재고" 패턴 저장
```
