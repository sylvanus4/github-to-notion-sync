---
name: alphaear-orchestrator
description: >-
  3-layer AlphaEar intelligence pipeline orchestrating 8 skills across data
  collection (news, stock, search in parallel), analysis (sentiment,
  prediction, signal tracking in parallel), and report generation (reporter +
  optional visualizer). Replaces the ad-hoc separate AlphaEar invocations with
  a formal DAG. Use when the user asks for "alphaear intelligence", "alphaear
  analysis", "alphaear pipeline", "알파이어 분석", "알파이어 인텔리전스", "알파이어 파이프라인", or
  wants comprehensive AlphaEar- powered market intelligence. Do NOT use for
  individual AlphaEar skills (invoke them directly). Do NOT use for the daily
  pipeline (use today, which delegates to this orchestrator at Phase 3.5).
disable-model-invocation: true
---

# AlphaEar Intelligence Orchestrator

3-layer pipeline: parallel data collection → parallel analysis → sequential report generation.

## Usage

```
/alphaear-intel                          # Full AlphaEar pipeline
/alphaear-intel NVDA                     # Focus on specific ticker
/alphaear-intel --skip search,visualize  # Skip specific components
/alphaear-intel --visualize              # Include logic visualization
/alphaear-intel --dry-run                # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `news` | `alphaear-news` | included |
| `stock` | `alphaear-stock` | included |
| `search` | `alphaear-search` | included |
| `sentiment` | `alphaear-sentiment` | included |
| `predictor` | `alphaear-predictor` | included |
| `signal` | `alphaear-signal-tracker` | included |
| `reporter` | `alphaear-reporter` | included |
| `visualize` | `alphaear-logic-visualizer` | excluded (opt-in via `--visualize`) |

## Agent Team

| Layer | Agent | Skill | Execution | Output |
|-------|-------|-------|-----------|--------|
| Collection | News Collector | `alphaear-news` | Task (parallel) | `_workspace/alphaear/01_news.md` |
| Collection | Stock Collector | `alphaear-stock` | Task (parallel) | `_workspace/alphaear/01_stock.md` |
| Collection | Search Collector | `alphaear-search` | Task (parallel) | `_workspace/alphaear/01_search.md` |
| Analysis | Sentiment Analyst | `alphaear-sentiment` | Task (parallel) | `_workspace/alphaear/02_sentiment.md` |
| Analysis | Predictor | `alphaear-predictor` | Task (parallel) | `_workspace/alphaear/02_predictor.md` |
| Analysis | Signal Tracker | `alphaear-signal-tracker` | Task (parallel) | `_workspace/alphaear/02_signal.md` |
| Generation | Reporter | `alphaear-reporter` | Task (sequential) | `_workspace/alphaear/03_report.md` |
| Generation | Visualizer | `alphaear-logic-visualizer` | Task (sequential) | `_workspace/alphaear/03_diagram.drawio` |

## Temporal Context (AutoHedge P1)

Every subagent prompt in Phase 1 and Phase 2 MUST include the current timestamp as the first line after the role statement:

```
Current date and time: {ISO 8601 timestamp, e.g. 2026-04-14T09:30:00+09:00}
```

This prevents stale-date hallucinations and ensures all agents operate on the same temporal reference point. The orchestrator captures the timestamp once at pre-flight and passes it to every subagent.

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for ticker, `--skip`, `--visualize`, `--dry-run`.
2. Check `signal_flux.db` availability (optional — degrade gracefully).
3. `Shell: mkdir -p _workspace/alphaear`
4. If `--dry-run`, print the execution plan and stop.

### Phase 1: Data Collection (Fan-out — 3 parallel)

Launch up to 3 sub-agents via the Task tool in a single message.

**News Collector:**
```
You are a financial news aggregator.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-news/SKILL.md`.

## Task
Collect today's financial news. {If ticker: "Focus on news related to {ticker}."}
Write to SQLite daily_news table and output a summary.

## Output
Write summary to `_workspace/alphaear/01_news.md`.

## Completion
Return count of news items collected.
```

**Stock Collector:**
```
You are a market data collector.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-stock/SKILL.md`.

## Task
Collect OHLCV data for {ticker or broad market indices}.

## Output
Write data summary to `_workspace/alphaear/01_stock.md`.

## Completion
Return data point count and date range.
```

**Search Collector:**
```
You are a research aggregator.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-search/SKILL.md`.

## Task
Search local RAG index and web for relevant market intelligence.
{If ticker: "Focus on {ticker} and its sector."}

## Output
Write findings to `_workspace/alphaear/01_search.md`.

## Completion
Return count of relevant sources found.
```

Wait for all Phase 1 agents to complete.

### Phase 2: Analysis (Fan-out — 3 parallel)

Launch up to 3 sub-agents. Each reads relevant Phase 1 outputs.

**Sentiment Analyst:**
```
You are a sentiment analysis specialist.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-sentiment/SKILL.md`.

## Context
Read news data at `_workspace/alphaear/01_news.md`.

## Task
Analyze sentiment across collected news items using the following structured methodology checklist (AutoHedge P6):

1. **Source-level sentiment**: Score each news source individually (bullish/bearish/neutral with confidence 0-100)
2. **Entity extraction**: Identify companies, sectors, and macro themes mentioned — tag each with sentiment polarity
3. **Temporal weighting**: Weight recent news (< 4h) at 2x vs older items; flag breaking news separately
4. **Contradiction detection**: Flag cases where different sources report conflicting sentiment on the same entity
5. **Magnitude assessment**: Distinguish between routine sentiment (earnings beat) vs structural shifts (sector rotation, regulatory action)

Include a `methodology_compliance` section in output confirming each checklist dimension was evaluated.

## Output
Write sentiment analysis to `_workspace/alphaear/02_sentiment.md`.

## Completion
Return overall sentiment score (-100 to +100), direction (bullish/bearish/neutral), and confidence (0-100).
```

**Predictor:**
```
You are a market predictor.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-predictor/SKILL.md`.

## Context
Read stock data at `_workspace/alphaear/01_stock.md`.

## Task
Generate price predictions based on historical data patterns.

## Output
Write predictions to `_workspace/alphaear/02_predictor.md`.

## Completion
Return key prediction summary.
```

**Signal Tracker:**
```
You are a trading signal detector.
Current date and time: {ISO 8601 timestamp}

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-signal-tracker/SKILL.md`.

## Context
Read all collection outputs:
- `_workspace/alphaear/01_news.md`
- `_workspace/alphaear/01_stock.md`
- `_workspace/alphaear/01_search.md`

## Task
Identify and track trading signals across all data sources using the following structured methodology checklist (AutoHedge P6):

1. **Signal classification**: Categorize each signal as Technical (price/volume pattern), Fundamental (earnings/valuation shift), Sentiment (news/social momentum), or Macro (rate/policy/FX)
2. **Multi-source confirmation**: For each signal, check if it is confirmed by ≥ 2 independent data sources (news + stock data, search + news, etc.)
3. **Signal strength scoring**: Assign strength 0-100 based on historical reliability of the signal pattern and current market regime
4. **Directional consistency**: Verify signal direction aligns with the underlying price trend (trend-following) or explicitly flag counter-trend signals
5. **Decay assessment**: Flag signals older than 24h as potentially stale; mark signals from pre-market/after-hours data as provisional

Include a `methodology_compliance` section in output confirming each checklist dimension was evaluated.

## Output
Write signal analysis to `_workspace/alphaear/02_signal.md`.

## Completion
Return count of active signals, strongest signal summary, and overall directional bias.
```

Wait for all Phase 2 agents to complete.

### Phase 2.5: Consistency Validation Gate (AutoHedge P4)

Before proceeding to report generation, run a lightweight consistency check across Phase 2 outputs:

1. **Directional agreement**: Compare the directional bias from Sentiment (`02_sentiment.md`), Predictor (`02_predictor.md`), and Signal Tracker (`02_signal.md`). If all three agree on direction (all bullish or all bearish), mark consensus as `STRONG`.
2. **Contradiction detection**: If any two outputs disagree on direction (e.g., sentiment bullish but signals bearish), flag as `CONTRADICTION` and log the specific conflict.
3. **Confidence spread**: Calculate the spread between the highest and lowest confidence scores across the three analysts. If spread > 40 points, flag as `HIGH_VARIANCE`.
4. **Staleness check**: Verify that all Phase 1 data sources have timestamps within 24h of the pipeline run time. Flag any stale inputs.

**Action on findings:**
- `STRONG` consensus: Proceed directly to Phase 3 (fast-track).
- `CONTRADICTION` or `HIGH_VARIANCE`: Append a `## Consistency Notes` section to each Phase 2 output file documenting the conflicts before proceeding to Phase 3. The Reporter must address these conflicts in the final report.
- Stale inputs: Log a warning but do not block the pipeline.

Write validation results to `_workspace/alphaear/02_consistency.md`.

### Phase 3: Report Generation (Sequential)

**Reporter** (unless `--skip reporter`):

```
You are a financial intelligence reporter.

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-reporter/SKILL.md`.

## Context
Read ALL analysis outputs:
- `_workspace/alphaear/02_sentiment.md`
- `_workspace/alphaear/02_predictor.md`
- `_workspace/alphaear/02_signal.md`

## Task
Produce a comprehensive intelligence report synthesizing all analyses.

## Output
Write report to `_workspace/alphaear/03_report.md`.

## Completion
Return executive summary.
```

**Visualizer** (only if `--visualize` flag is set):

```
You are a logic visualization specialist.

## Skill Reference
Read and follow `.cursor/skills/alphaear/alphaear-logic-visualizer/SKILL.md`.

## Context
Read the report at `_workspace/alphaear/03_report.md`.

## Task
Create a visual diagram of the analysis logic and signal flow.

## Output
Write diagram to `_workspace/alphaear/03_diagram.drawio`.

## Completion
Return diagram description.
```

### Phase 4: Output

Copy final report to `outputs/alphaear/intel-{date}.md`.
If visualizer ran, copy diagram to `outputs/alphaear/intel-{date}.drawio`.

## Error Handling

| Failure | Action |
|---------|--------|
| 1 collector fails | Retry once. Proceed without that data source. Note in report. |
| 2+ collectors fail | Produce degraded report with available data. Warn user. |
| All collectors fail | Abort: "No data sources available." |
| 1 analyst fails | Retry once. Proceed without that analysis. Note in report. |
| Reporter fails | Return raw analysis outputs to user instead of formatted report. |
| Visualizer fails | Skip visualization. Non-critical. |

## Data Flow

```
Pre-flight (parse args, check signal_flux.db)
    │
    ▼ Phase 1: Collection (parallel)
    ├─► News Collector   ──► 01_news.md   ─┐
    ├─► Stock Collector  ──► 01_stock.md  ─┤
    └─► Search Collector ──► 01_search.md ─┘
                                            │
    ▼ Phase 2: Analysis (parallel)          │
    ├─► Sentiment (reads news) ──► 02_sentiment.md ─┐
    ├─► Predictor (reads stock) ──► 02_predictor.md ─┤
    └─► Signal Tracker (reads all) ──► 02_signal.md ─┘
                                                      │
    ▼ Phase 3: Generation (sequential)                │
    ├─► Reporter (reads all analysis) ──► 03_report.md
    └─► Visualizer (opt-in) ──► 03_diagram.drawio
                                          │
    ▼ Phase 4: Output                     │
    └─► outputs/alphaear/intel-{date}.md
```

## Integration with `today`

The `today` pipeline delegates to this orchestrator at Phase 3.5, consolidating the previously scattered AlphaEar invocations (news at Phase 2, sentiment at Phase 3, reporter at Phase 4) into a single orchestrator call.

## Examples

```
User: "알파이어 파이프라인 돌려줘"
→ 3-layer pipeline: news+stock+search → sentiment+predictor+signal → reporter

User: "alphaear intelligence --topic semiconductor"
→ Filters collection to semiconductor-related queries, full 3-layer execution

User: "알파이어 분석 --skip-visualizer"
→ Runs full pipeline, skips optional Phase 3b visualizer
```

## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
