---
name: rr-investment-trader
version: 1.0.0
description: >-
  Role Replacement Case Study: Investment Research Trader — full-cycle daily
  investment intelligence pipeline replacing a dedicated trader/analyst who
  manually syncs market data, screens stocks, runs technical/fundamental analysis,
  conducts multi-agent debate-based trade evaluation, manages broker operations
  (Toss Securities), generates backtested strategy cards, validates report quality,
  creates investment content, monitors portfolio risk, and maintains a trade
  journal. Thin harness composing axis-investment, today, toss-ops-orchestrator,
  trading-agent-desk, daily-strategy-engine, ai-quality-evaluator, and
  content-repurposing-engine into a unified Investment Trader role pipeline with
  MemKraft-powered trading memory, 7-layer safety model enforcement, and
  multi-channel Slack distribution.
tags: [role-replacement, harness, trading, investment, broker, strategy, risk]
triggers:
  - rr-investment-trader
  - investment trader replacement
  - trading automation
  - full trading pipeline
  - investment research trader
  - daily trading lifecycle
  - 투자 트레이더 대체
  - 투자 연구 자동화
  - 트레이딩 파이프라인
  - 일일 투자 라이프사이클
  - 투자 분석 자동화
do_not_use:
  - Running the today pipeline directly (use today)
  - Weekly price sync only (use weekly-stock-update)
  - Broker operations only (use toss-ops-orchestrator or kis-team)
  - Single stock technical analysis (use trading-technical-analyst)
  - Agent desk debate only (use trading-agent-desk)
  - Strategy card generation only (use daily-strategy-engine)
  - Report quality check only (use ai-quality-evaluator)
  - Content repurposing without trading context (use content-repurposing-engine)
composes:
  - axis-investment
  - today
  - toss-ops-orchestrator
  - trading-agent-desk
  - daily-strategy-engine
  - ai-quality-evaluator
  - content-repurposing-engine
  - toss-morning-briefing
  - toss-trade-journal
  - toss-risk-monitor
  - toss-signal-bridge
  - decision-router
  - memkraft
  - ai-context-router
---

# Role Replacement: Investment Research Trader

## Human Role Being Replaced

An Investment Research Trader who manually:
- Syncs market data from Yahoo Finance / Polygon / Tiingo across 60+ tracked tickers every morning
- Runs multi-factor stock screening (P/E, RSI, volume, MA crossovers, FCF yield) across NASDAQ 100, KOSPI 100, KOSDAQ 100
- Discovers hot untracked stocks and adds promising ones to the watchlist
- Performs 3-layer technical analysis: Turtle Trading (SMA 20/55/200 + Donchian), Bollinger Bands (4 methods), Oscillators (RSI/MACD/Stochastic/ADX)
- Conducts multi-agent debate (bull vs. bear) with 4 analyst perspectives (technical, fundamental, sentiment, news) before making trade decisions
- Generates 10 backtested strategy cards from 7 strategies across 16 blue-chip stocks with commission-aware P&L
- Validates AI-generated reports across 6 quality dimensions (accuracy, consistency, coverage, actionability, external consensus, tone) before publishing
- Manages Toss Securities operations: daily snapshots, FX monitoring, risk assessment, portfolio reconciliation, watchlist sync, signal bridging, trade journaling
- Enforces the 7-layer safety model before any live trade execution (Paperclip governance → signal strength gate → mode disclosure → position sizing → concentration check → compliance gate → user confirmation)
- Creates investment content (Twitter threads, LinkedIn posts, video scripts) from trading insights
- Posts structured reports to Slack (#h-report for signals, #효정-의사결정 for trade approvals)
- Maintains a persistent trade journal with cumulative P&L, win rate, and strategy performance tracking
- Compares prediction accuracy against actual market close (EOD strategy review)
- Cross-validates native TA signals against TradingView MCP data for consensus scoring

This skill replaces 3-4 hours of daily manual trading work (1.5-2h morning analysis + 1-1.5h broker management + 0.5-1h EOD review) into a single automated pipeline.

## Architecture

```
Morning Pipeline (triggered ~07:30 or on-demand)
  Phase 0: MemKraft Context Pre-load
    └─ ai-context-router → trading memory, yesterday's decisions, open positions,
       signal accuracy history, risk patterns, market regime

  Phase 1: Market Intelligence (today pipeline — guarded)
    └─ 8 sequential stages: DB freshness check → multi-provider data sync →
       hot stock discovery → multi-factor screening → 3-layer TA analysis →
       strategy card generation → DOCX report → Slack distribution
    Guard: outputs/daily/{date}/daily_report_{date}.docx exists → SKIP

  Phase 2: Broker Operations (toss-ops-orchestrator — guarded)
    └─ 4 phases: snapshot → parallel monitoring (FX, risk, recon, watchlist) →
       signal bridge → reporting (journal + morning briefing)
    Guard: outputs/axis/investment/{date}/toss-ops.json exists → SKIP

  Phase 3: Agent Desk Debate (trading-agent-desk — conditional)
    └─ 4 phases: 4 parallel analysts → bull/bear debate (2 rounds) →
       research manager synthesis → risk evaluator gate
    Condition: Run only for top 3-5 stocks from Phase 1 screener with
       ambiguous signals (no unanimous BUY/SELL consensus)
    MemKraft Enhancement: Inject prior decisions for same tickers from
       trade memory into debate context for learning continuity

  Phase 4: Quality Gate (ai-quality-evaluator)
    └─ 6-dimension scoring: accuracy, consistency, coverage, actionability,
       external consensus, tone
    Gate: PASS (≥8.0) → proceed to distribution
          REVIEW (6.0-7.9) → flag issues, append warnings to report
          FAIL (<6.0) → halt distribution, alert #효정-의사결정

  Phase 5: Content Generation (conditional, Level 1+)
    └─ content-repurposing-engine → Twitter thread, LinkedIn post
    └─ hook-generator → attention hooks for top signal
    └─ video-script-generator → video outline if signal strength > 0.7
    Condition: Skip at Level 0 (report-only mode)

  Phase 6: Distribution & Reporting
    ├─ Slack #h-report → daily report + strategy cards thread
    ├─ Slack #효정-의사결정 → trade decisions requiring approval (via decision-router)
    ├─ MemKraft write-back → trading patterns, signal accuracy, market regime
    └─ Trade journal update → toss-trade-journal

Evening Pipeline (triggered ~17:00 or on-demand)
  Phase E1: EOD Market Summary
    └─ Read latest market close data, compute daily P&L from Toss
    Guard: outputs/axis/investment/{date}/eod-summary.json exists → SKIP

  Phase E2: Strategy Accuracy Review
    └─ Compare morning strategy cards against actual market close
    └─ Score prediction accuracy per strategy type
    └─ Append to trading-agent-desk BM25 memory for learning

  Phase E3: MemKraft Write-back
    └─ Store EOD patterns: which strategies worked, signal accuracy,
       regime persistence, notable market moves
```

## MemKraft Trading Memory Configuration

### HOT Tier (session-critical, loaded every run)
- Open positions and unrealized P&L
- Today's pending orders and watchlist alerts
- Current market regime classification (risk-on/risk-off/transitional)
- Yesterday's strategy card accuracy scores

### WARM Tier (cross-session patterns, loaded on-demand)
- Signal accuracy history per strategy type (30-day rolling)
- Recurring sector rotation patterns
- Ticker-specific decision history (last 5 decisions per symbol)
- FX rate trend and impact on USD positions
- Agent desk debate outcomes vs. actual returns (learning loop)

### Knowledge Tier (persistent, KB-compiled)
- KB topic: `trading-daily` — daily pipeline outputs compiled into wiki
- KB topic: `competitive-intel` — broker fee structures, alternative platforms
- Backtest parameter history — which parameters worked in which regimes

### Pre-load Query

```
ai-context-router query:
  "Retrieve: (1) current open positions and pending orders,
   (2) yesterday's strategy card accuracy scores,
   (3) 7-day signal accuracy trend per strategy type,
   (4) current market regime classification,
   (5) any unresolved trading decisions from prior sessions"
```

### Write-back Schema

```json
{
  "tier": "HOT",
  "entries": [
    {
      "type": "trading_session",
      "date": "{date}",
      "market_regime": "{bull|bear|sideways|transitional}",
      "signals_generated": "{count}",
      "quality_gate_score": "{score}/10",
      "strategy_accuracy": {
        "turtle": "{win_rate}",
        "dualma": "{win_rate}",
        "bollinger": "{win_rate}",
        "overnight_dip": "{win_rate}"
      },
      "top_decision": "{symbol} {BUY|SELL|HOLD} confidence:{score}",
      "portfolio_pnl_daily": "{amount}",
      "risk_status": "{GREEN|YELLOW|RED}"
    }
  ]
}
```

## Phase Guard Protocol

Before running a wrapped sub-pipeline, check if today's output already exists.
If it does, SKIP the phase and reuse existing outputs. This prevents duplicate
API calls, Slack posts, and compute.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (today) | `outputs/daily/{date}/daily_report_{date}.docx` | File exists with today's date |
| 2 (Toss ops) | `outputs/axis/investment/{date}/toss-ops.json` | File exists |
| 3 (Agent desk) | `outputs/agent-desk/{date}/desk-decisions.json` | File exists |
| E1 (EOD) | `outputs/axis/investment/{date}/eod-summary.json` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.

## Composed Skills Reference

### Core Pipeline
| Skill | Role in Pipeline | Phase |
|-------|-----------------|-------|
| `today` | Full daily pipeline (data sync → screening → TA → report) | 1 |
| `daily-strategy-engine` | 7-strategy × 16-stock backtested cards | 1 (internal) |
| `toss-ops-orchestrator` | 8-skill broker operations composite | 2 |
| `toss-morning-briefing` | Portfolio morning briefing to Slack | 2 (internal) |

### Decision Layer
| Skill | Role in Pipeline | Phase |
|-------|-----------------|-------|
| `trading-agent-desk` | 4-analyst + bull/bear debate + risk gate | 3 |
| `ai-quality-evaluator` | 6-dimension report quality scoring | 4 |
| `decision-router` | Route trade decisions to appropriate Slack channel | 6 |

### Risk & Execution
| Skill | Role in Pipeline | Phase |
|-------|-----------------|-------|
| `toss-risk-monitor` | Portfolio risk scorecard (GREEN/YELLOW/RED) | 2 (internal) |
| `toss-signal-bridge` | Convert strategy cards to order previews | 2 (internal) |
| `toss-trade-journal` | Log trades with context and track P&L | 6 |

### Content & Distribution
| Skill | Role in Pipeline | Phase |
|-------|-----------------|-------|
| `content-repurposing-engine` | Transform signals into platform-specific content | 5 |
| `hook-generator` | Attention hooks for top trading signal | 5 |

### Memory
| Skill | Role in Pipeline | Phase |
|-------|-----------------|-------|
| `memkraft` | Trading memory read/write | 0, 6, E3 |
| `ai-context-router` | Cross-layer memory retrieval with provenance | 0 |

## Execution Instructions

### Morning Pipeline

1. **Phase 0 — MemKraft Context Pre-load**
   - Invoke `ai-context-router` with the pre-load query above
   - Extract: open positions, yesterday's accuracy, market regime, unresolved decisions
   - Store in session context for downstream phases

2. **Phase 1 — Market Intelligence (guarded)**
   - Check guard: `outputs/daily/{date}/daily_report_{date}.docx`
   - If exists → log `REUSED — Phase 1 today pipeline` and skip
   - If not → invoke `today` skill as-is (treat as black box)
   - Key outputs consumed downstream:
     - `outputs/analysis-{date}.json` — TA signals per ticker
     - `outputs/screener-{date}.json` — multi-factor screening results
     - `outputs/strategy-cards-{date}.json` — 10 backtested strategy cards
     - `outputs/discovery-{date}.json` — hot stock discoveries

3. **Phase 2 — Broker Operations (guarded)**
   - Check guard: `outputs/axis/investment/{date}/toss-ops.json`
   - If exists → log `REUSED — Phase 2 toss-ops` and skip
   - If not → invoke `toss-ops-orchestrator`
   - Pre-flight: verify `tossctl` availability; if unavailable, skip gracefully
   - Key outputs: portfolio snapshot, risk scorecard, signal previews, FX rates

4. **Phase 3 — Agent Desk Debate (conditional)**
   - Read `outputs/screener-{date}.json` and `outputs/analysis-{date}.json`
   - Identify top 3-5 stocks with ambiguous signals (not unanimous BUY/SELL)
   - For each ambiguous stock, invoke `trading-agent-desk` with:
     - 4 analyst reports from Phase 1 data
     - MemKraft injection: prior decisions for same ticker from trade memory
     - Debate rounds: 2 (default), 1 if consensus fast-track triggers
   - Save results to `outputs/agent-desk/{date}/desk-decisions.json`
   - If all screened stocks have clear consensus → skip with log

5. **Phase 4 — Quality Gate**
   - Invoke `ai-quality-evaluator` on Phase 1 report
   - Score across 6 dimensions with TradingView cross-validation
   - Gate decision:
     - PASS (≥8.0): proceed to distribution
     - REVIEW (6.0-7.9): append warnings, flag for human review
     - FAIL (<6.0): halt distribution, post alert to #효정-의사결정

6. **Phase 5 — Content Generation (Level 1+ only)**
   - Check automation level in `outputs/axis/automation-levels.json`
   - If Level 0 → skip content generation entirely
   - If Level 1+:
     - Read Phase 1 top signals and Phase 3 desk decisions
     - Generate Twitter thread + LinkedIn post via `content-repurposing-engine`
     - Generate attention hook via `hook-generator`
     - If top signal strength > 0.7: generate video script via `video-script-generator`
   - Write to `outputs/axis/investment/{date}/content/`

7. **Phase 6 — Distribution & Reporting**
   - Build consolidated morning summary from phase outputs (file-first)
   - Slack #h-report: daily report + strategy cards as threaded reply
   - Route trade decisions to #효정-의사결정 via `decision-router`
   - Update trade journal via `toss-trade-journal`
   - MemKraft write-back: trading session record (schema above)
   - Write `outputs/axis/investment/{date}/morning-summary.json`

### Evening Pipeline

1. **Phase E1 — EOD Market Summary**
   - Read latest market close data
   - Compute daily P&L from Toss snapshot comparison
   - Write `outputs/axis/investment/{date}/eod-summary.json`

2. **Phase E2 — Strategy Accuracy Review**
   - Load morning strategy cards from `outputs/strategy-cards-{date}.json`
   - Compare predicted signals against actual close prices
   - Score prediction accuracy per strategy type
   - Append accuracy data to `trading-agent-desk` BM25 memory store
   - Write `outputs/axis/investment/{date}/strategy-review.json`

3. **Phase E3 — MemKraft Write-back**
   - Store EOD patterns: strategy accuracy, regime persistence, notable moves
   - Update WARM tier: rolling signal accuracy per strategy

## Safety Model (7 Layers)

Any path from analysis to live trade execution MUST pass all 7 layers:

| Layer | Gate | Enforcement |
|-------|------|-------------|
| L0 | Paperclip governance | Budget check (if Paperclip active) |
| L1 | Signal strength ≥ 0.5 | Auto-skip if below threshold |
| L2 | Mode disclosure | Display VPS/prod mode before any order |
| L3 | Position sizing | `trading-position-sizer` validates allocation |
| L4 | Concentration check | Single position ≤ 15% of portfolio |
| L5 | Compliance gate | Wash-sale, slippage, timing checks |
| L6 | User confirmation | Explicit approval for prod orders with symbol/qty/amount |

Trade execution NEVER auto-executes — stays Level 1 max (suggest + confirm).

## Automation Levels

Tracked in `outputs/axis/automation-levels.json`, protocol in `axis-dispatcher/references/automation-levels.md`.

| Level | Behavior | Current |
|-------|----------|---------|
| 0 | Report only — human reviews signals and acts | ✅ Active |
| 1 | Suggest trades + content + human confirms | Target |
| 2 | Post signals and reports autonomously | Future |

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 0 | (session context) | MemKraft pre-loaded trading memory |
| 1 | `outputs/daily/{date}/*` | Full today pipeline (delegated) |
| 1 | `outputs/strategy-cards-{date}.json` | 10 backtested strategy cards |
| 2 | `outputs/axis/investment/{date}/toss-ops.json` | Broker operations |
| 3 | `outputs/agent-desk/{date}/desk-decisions.json` | Agent desk decisions |
| 4 | `outputs/axis/investment/{date}/quality-gate.md` | Quality evaluation |
| 5 | `outputs/axis/investment/{date}/content/*.md` | Generated content |
| 6 | `outputs/axis/investment/{date}/morning-summary.json` | Consolidated summary |
| E1 | `outputs/axis/investment/{date}/eod-summary.json` | EOD market summary |
| E2 | `outputs/axis/investment/{date}/strategy-review.json` | Strategy accuracy |

## Slack Channels

| Channel | Content | Phase |
|---------|---------|-------|
| `#h-report` | Daily report + strategy cards thread | 1, 6 |
| `#효정-의사결정` | Trade decisions requiring approval | 6 |
| `#효정-할일` | Pipeline execution summary | 6 |

## Error Handling

| Failure | Phase | Action |
|---------|-------|--------|
| Data sync fails (all providers) | 1 | Abort pipeline, alert #효정-할일 |
| tossctl unavailable | 2 | Skip broker ops, note in summary |
| Agent desk fails | 3 | Skip debate, rely on Phase 1 signals only |
| Quality gate FAIL | 4 | Halt distribution, alert #효정-의사결정 |
| Content generation fails | 5 | Skip content, non-critical |
| Slack posting fails | 6 | Retry once; if fails, write to local file |
| EOD data unavailable | E1 | Skip with warning, defer to next morning |

For all errors, write to `outputs/axis/investment/{date}/errors.json` using
standard error record format (severity S1-S4, phase, impact, recovery).

## Gaps Addressed vs. Existing Implementation

| Gap | How This Skill Addresses It |
|-----|---------------------------|
| No unified morning-to-evening trading lifecycle | Single pipeline orchestrates both morning and evening cycles |
| Agent desk debate lacks historical context | MemKraft injects prior decisions for same tickers into debate context |
| Quality gate disconnected from distribution | Phase 4 gates Phase 6; FAIL halts Slack posting |
| Strategy accuracy not tracked systematically | Phase E2 scores predictions against actuals, feeds BM25 memory |
| Content generation not integrated with signals | Phase 5 reads signal strength to conditionally generate content |
| Risk monitor runs independently | Phase 2 integrates risk assessment into unified broker operations |
| Trade decisions lack provenance | MemKraft stores full decision context with phase references |

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

## Examples

**Standard morning dispatch:**
User: "rr-investment-trader" or "투자 트레이더 대체"
→ Runs full pipeline Phases 0-7: data sync → screening → TA → agent desk → strategies → quality gate → Slack

**Error recovery after Phase 3 failure:**
User: "rr-investment-trader" after toss-ops-orchestrator timeout
→ Phase Guard detects manifest with Phase 2 complete, resumes from Phase 3 (broker ops)

## Operational Runbook

### Daily Execution
```
07:30  Morning pipeline auto-triggered by axis-dispatcher
       or manual: "rr-investment-trader" / "투자 트레이더 대체"
17:00  Evening pipeline auto-triggered by axis-dispatcher
       or manual: "rr-investment-trader --evening"
```

### Manual Overrides
```
--force              Bypass all phase guards, re-run from scratch
--skip-toss          Skip Phase 2 broker operations
--skip-debate        Skip Phase 3 agent desk debate
--skip-content       Skip Phase 5 content generation
--evening            Run evening pipeline only (E1-E3)
--morning            Run morning pipeline only (Phases 0-6)
--symbols NVDA,AAPL  Override stock universe for agent desk debate
```

### Troubleshooting
| Symptom | Check | Fix |
|---------|-------|-----|
| No strategy cards | `outputs/strategy-cards-{date}.json` missing | Re-run `today` with `--force` |
| Toss data stale | `tossctl auth status` shows expired | Run `tossinvest-setup` for re-auth |
| Agent desk timeout | Debate rounds taking >5 min per symbol | Reduce to `--debate-rounds 1` |
| Quality gate always REVIEW | Consistently 6.0-7.9 scores | Check TA data freshness, validate DB sync |
| MemKraft empty on pre-load | No prior trading sessions found | First run bootstraps — expected on initial use |
