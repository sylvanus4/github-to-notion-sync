---
name: axis-investment
description: >-
  Axis 2 of the 6-Axis Personal Assistant. Market intelligence, portfolio
  management, trading signals, and investment content creation. Thin
  orchestrator wrapping the existing `today` pipeline and adding content
  distribution, broker operations, and EOD summary. Use when the user asks for
  "axis investment", "investment axis", "투자 축", "market axis",
  "axis-investment", or wants the full investment intelligence cycle including
  content generation. Do NOT use for running the today pipeline directly (use
  today). Do NOT use for weekly price sync only (use weekly-stock-update). Do
  NOT use for broker operations only (use toss-ops-orchestrator or kis-team
  directly).
---

# Axis 2: Investment + Content

Orchestrates the full investment intelligence cycle: market data sync, screening,
technical analysis, trading signals, broker monitoring, content generation, and
distribution. Wraps the existing `today` pipeline as its core engine and adds
content distribution and broker operations layers.

## Principles

- **Single Responsibility**: Only investment and market intelligence
- **Context Isolation**: Reads/writes exclusively to `outputs/axis/investment/{date}/`
  and delegates to `outputs/daily/{date}/` via the `today` sub-pipeline
- **Failure Isolation**: Errors in this axis do not affect other axes
- **File-First Data Bus**: All inter-phase data flows through files, never context

## Phase Guard Protocol

Before running a wrapped sub-pipeline, check if today's output already exists.
If it does, SKIP the phase and reuse existing outputs. This prevents duplicate
API calls, Slack posts, and compute when `today` or other pipelines were
already invoked separately.

| Phase | Guard File | Skip Condition |
|-------|-----------|----------------|
| 1 (today) | `outputs/daily/{date}/daily_report_{date}.docx` | File exists with today's date |
| 2 (Toss ops) | `outputs/axis/investment/{date}/toss-ops.json` | File exists |

Pass `--force` to bypass all guards and re-run from scratch.
When a phase is skipped, log `REUSED — {guard_file}` in the dispatch manifest.

## Composed Skills

### Data Layer
- `tab-stock-sync`, `tab-fundamental-sync`, `weekly-stock-update`, `stock-csv-downloader`

### Screening
- `tab-screening`, `tab-hot-stock-discovery`, `tab-tradingview-screener`

### Analysis
- `daily-stock-check`, `tab-technical-analysis`, `tab-tradingview-ta`
- `trading-technical-analyst`, `trading-market-environment-analysis`

### Signals
- `tab-turtle-refresh`, `tab-bollinger-refresh`, `tab-dualma-refresh`, `daily-strategy-engine`

### Intelligence
- `alphaear-orchestrator` (8 sub-skills), `trading-intel-orchestrator` (4 parallel analysts)
- `mirofish` (swarm simulation, on-demand)

### Broker
- `tossinvest-*` (8 skills via `toss-ops-orchestrator`), `kis-*` (5 skills via `kis-team`), `tab-kiwoom`

### Risk
- `toss-risk-monitor`, `toss-portfolio-recon`, `trading-position-sizer`

### Reports
- `tab-report-generate`, `ai-quality-evaluator`, `anthropic-docx`

### Content
- `stock-content-printer`, `content-repurposing-engine`, `hook-generator`, `video-script-generator`

### Research
- `alphaear-news`, `alphaear-sentiment`, `hf-trending-intelligence`

## Workflow

### Morning Run (triggered by `axis-dispatcher` ~07:30)

```
Phase 1: today pipeline         → outputs/daily/{date}/  (full pipeline)
Phase 2: Toss operations        → outputs/axis/investment/{date}/toss-ops.json
Phase 3: Content generation     → outputs/axis/investment/{date}/content/
Phase 4: Summary + distribution → outputs/axis/investment/{date}/morning-summary.json
```

**Phase 1 — Market Intelligence Pipeline** *(guarded)*
Check Phase Guard: if `outputs/daily/{date}/daily_report_{date}.docx` exists,
SKIP this phase and read existing outputs. Otherwise invoke the `today` skill
as-is. All outputs land in `outputs/daily/{date}/`.
Do NOT duplicate today's logic. Treat it as a black box.

**Phase 2 — Broker Operations** *(guarded)*
Check Phase Guard: if `outputs/axis/investment/{date}/toss-ops.json` exists,
SKIP. Otherwise run `toss-ops-orchestrator` for portfolio snapshot, risk check,
signal bridge, and watchlist sync. Write results to
`outputs/axis/investment/{date}/toss-ops.json`.

**Phase 3 — Content Generation** (Level 1+: skip at Level 0)
Read `outputs/daily/{date}/phase-5-report.json` and generate:
- Twitter thread draft via `content-repurposing-engine`
- LinkedIn post via `content-repurposing-engine`
- Video script outline via `video-script-generator` (if top signal strength > 0.7)
Write to `outputs/axis/investment/{date}/content/`.

**Phase 4 — Summary**
Compile morning summary from Phase 1-3 outputs. Write to
`outputs/axis/investment/{date}/morning-summary.json` with:
- Top 3 signals with confidence
- Portfolio health (from Toss)
- Pending decisions for `decision-router`
- Content pieces generated

### Evening Run (triggered by `axis-dispatcher` ~17:00)

```
Phase E1: EOD market summary    → outputs/axis/investment/{date}/eod-summary.json
Phase E2: Strategy card review  → outputs/axis/investment/{date}/strategy-review.json
```

**Phase E1 — EOD Summary**
Read latest market data, daily P&L from Toss, and compile EOD summary.

**Phase E2 — Strategy Review**
Review today's strategy cards against actual market close. Score prediction accuracy.
Append to `outputs/axis/investment/{date}/strategy-review.json`.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `outputs/daily/{date}/*` | Full today pipeline (delegated) |
| 2 | `outputs/axis/investment/{date}/toss-ops.json` | Broker operations |
| 3 | `outputs/axis/investment/{date}/content/*.md` | Generated content pieces |
| 4 | `outputs/axis/investment/{date}/morning-summary.json` | Consolidated summary |
| E1 | `outputs/axis/investment/{date}/eod-summary.json` | EOD market summary |
| E2 | `outputs/axis/investment/{date}/strategy-review.json` | Strategy accuracy |

## Slack Channels

- `#h-report` — trading signals and daily report (via today pipeline)
- `#효정-의사결정` — trade decisions requiring approval (via decision-router)

## Automation Level

Tracked centrally in `outputs/axis/automation-levels.json`.
Full protocol: `axis-dispatcher/references/automation-levels.md`.

- **Level 0 (current)**: Report only — human reviews signals and acts
- **Level 1**: Suggest trades + human confirms before execution
- **Level 2**: Post signals to Slack, generate reports autonomously

Trade execution NEVER auto-executes (safety constraint) — stays Level 1 max.

## Error Recovery

Follow the protocol in `axis-dispatcher/references/failure-alerting.md`.

If Phase 1 (today) fails, the axis reports the failure to `#효정-할일` with
the error context and skips Phases 2-4. The today pipeline's own checkpoint
files in `outputs/daily/{date}/` enable partial re-runs.

Write errors to `outputs/axis/investment/{date}/errors.json` using the
standard error record format (severity S1-S4, phase, impact, recovery).

## Gotchas

- The `today` pipeline already posts to Slack; avoid double-posting by NOT
  re-posting signals from Phase 1
- Toss operations require `tossctl` CLI to be authenticated; if auth fails,
  skip Phase 2 gracefully and note in summary
- Content generation at Level 0 is skipped entirely — enable at Level 1+
