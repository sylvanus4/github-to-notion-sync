---
name: today
description: >-
  Run the daily data sync, fundamental collection, hot stock discovery,
  multi-factor screening, Turtle/Bollinger/Oscillator analysis, and Korean .docx
  report pipeline — check DB vs CSV freshness, backfill from Yahoo Finance,
  discover hot stocks from NASDAQ/KOSPI/KOSDAQ 100, screen (P/E, RSI, volume,
  MA crossovers, FCF yield), run SMA 20/55/200 + RSI/MACD/Stochastic/ADX,
  optionally fetch news (alphaear-news) and sentiment (alphaear-sentiment),
  generate buy/sell report via anthropic-docx, run 7-strategy backtested
  strategy engine outputting top 10 strategy cards, post pipeline summary
  and strategy cards to Slack #h-report via native API (no MCP required),
  optionally run setup-doctor pre-flight and twitter-timeline-to-slack post-pipeline,
  and ingest daily outputs into the trading-daily Knowledge Base for compound growth.
  Optionally cross-validates screener and TA results against TradingView MCP
  servers (--with-tradingview) and generates Pine Script v5 indicators for top
  stocks (--with-pine).
  Use when the user asks to run a daily pipeline, sync stock data, discover hot
  stocks, screen stocks, or generate a daily report.
  Do NOT use for weekly price updates only (use weekly-stock-update). Do NOT use
  for stock analysis without data sync (use daily-stock-check). Do NOT use for
  CSV downloads from investing.com (use stock-csv-downloader).
metadata:
  author: thaki
  version: "7.1.0"
  category: execution
---

# Today — Daily Data Sync, Screening, and Report Pipeline

Orchestrates a multi-phase pipeline: optional setup-doctor pre-flight, data freshness check, data sync, fundamental data collection (financial statements from yfinance), hot stock discovery, multi-factor stock screening (P/E, RSI, volume spikes, MA crossovers, earnings proximity, FCF yield, AI sentiment), technical analysis (SMA 20/55/200, Bollinger Bands, RSI/MACD/Stochastic/ADX oscillators), optional market context (alphaear-news + alphaear-sentiment), Korean expert report generation (.docx + optional Slack), and optional twitter-timeline-to-slack post-pipeline. Generates per-stock buy/sell recommendations using 3-way signal combination (Turtle + Bollinger + Oscillator) enhanced with fundamental screening scores and AI sentiment. Reuses `weekly-stock-update`, `daily-stock-check`, `financial-data-collector`, `stock-screener`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, `alphaear-sentiment`, `setup-doctor`, and `twitter-timeline-to-slack` skills internally. No API keys are required for Cursor-side execution.

## Prerequisites

- PostgreSQL running and migrated (`alembic upgrade head`)
- Stock CSV files exist in `data/latest/` (seed via `stock-csv-downloader` if empty)
- Python 3.11+ with backend dependencies installed
- Node.js with `docx` package installed locally (`cd outputs && npm install`) — for .docx report generation
- (Optional) Slack MCP server connected — only needed for Cursor-side posting to `#h-report`
- (Optional) `anthropic-docx` skill available — for .docx report generation; skip with `skip-docx`

> **Note**: No API keys are required for Cursor-side execution. The GitHub Actions pipeline (`daily-today.yml`) uses its own secrets (`SLACK_BOT_TOKEN`, `OPENAI_API_KEY`, etc.) and posts to Slack natively via the `pipeline_orchestrator.py` `slack_notification` stage — no MCP needed.

### Environment Variables (for GitHub Actions / API pipeline)

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SLACK_BOT_TOKEN` | For Slack | — | Bot token with `chat:write` + `channels:read` scopes |
| `SLACK_CHANNEL` | No | `h-report` | Target Slack channel name (resolved via `conversations.list`) |
| `SLACK_CHANNEL_ID` | No | — | Direct channel ID (skips name resolution lookup) |
| `OPENAI_API_KEY` | For LLM | — | Used by LLM agent stages |
| `ANTHROPIC_API_KEY` | For LLM | — | Used by quality evaluator |
| `FRED_API_KEY` | For macro | — | Federal Reserve economic data |

## Pipeline Output Protocol

All intermediate results are persisted to `outputs/today/{date}/` with a manifest file tracking completion status. The report generation phase (Phase 5) reads **exclusively** from these files — never from in-context conversation history. This prevents context window degradation from causing incomplete reports.

### Output Directory Structure

```
outputs/today/{date}/
  manifest.json                # pipeline status tracker
  phase-0-doctor.json          # Phase 0 output (setup-doctor)
  phase-1-freshness.json       # Phase 1 output
  phase-1.5-toss-monitor.json  # Phase 1.5 output (toss snapshot)
  phase-2-sync.json            # Phase 2 output
  phase-2.5-fundamentals.json  # Phase 2.5 output
  phase-3-discovery.json       # Phase 3 output
  phase-3.5-screener.json      # Phase 3.5 output
  phase-4-analysis.json        # Phase 4 main analysis
  phase-4.2-regime.json        # Phase 4.2 market regime
  phase-4.3-top-risk.json      # Phase 4.3 market top risk
  phase-4.5-alphaear.json      # Phase 4.5 AlphaEar intelligence
  phase-4.6-market-env.json    # Phase 4.6 market environment
  phase-4.8-agent-desk.json    # Phase 4.8 agent desk decisions
  phase-5a-dq.json             # Phase 5a-DQ data quality
  phase-5.1-edge.json          # Phase 5.1 edge candidates
  phase-5-report-content.json  # Phase 5 structured report sections for DOCX
  phase-5.5-toss-signal.json   # Phase 5.5 toss signal bridge
  phase-tv-screener.json       # TV screener cross-check (optional, --with-tradingview)
  phase-tv-ta.json             # TV TA cross-validation (optional, --with-tradingview)
  phase-pine-scripts.json      # Pine Script generation manifest (optional, --with-pine)
```

### Manifest Schema

```json
{
  "pipeline": "today",
  "date": "2026-04-01",
  "started_at": "2026-04-01T07:00:00Z",
  "completed_at": null,
  "phases": [
    {
      "id": "phase-1",
      "label": "data-freshness",
      "status": "completed",
      "output_file": "phase-1-freshness.json",
      "started_at": "2026-04-01T07:00:05Z",
      "elapsed_ms": 5200,
      "summary": "52 tickers checked, 3 stale gaps found"
    },
    {
      "id": "phase-4.2",
      "label": "market-regime",
      "status": "skipped",
      "skip_reason": "skip-regime flag set",
      "output_file": null
    }
  ],
  "flags": ["skip-twitter", "dry-run"],
  "overall_status": "completed_with_warnings",
  "warnings": ["Phase 4.3 skipped: FMP_API_KEY not set"]
}
```

### Manifest Update Pattern (apply after every phase)

After each phase completes:
1. Read the current manifest (create with pipeline metadata if Phase 0/1 is the first phase)
2. Append or update the phase entry with `status`, `output_file`, `elapsed_ms`, `summary`
3. Write back the manifest

### Subagent Return Contract

When a phase runs as a Task subagent, instruct it:
> "Save full results to `outputs/today/{date}/{output_file}`. Return ONLY: `{ status, file_path, one_line_summary }`"

This keeps the main orchestrator's context lean — detailed data lives on disk, not in conversation memory.

### Backward Compatibility — Legacy File Copies

After writing phase output files, also copy to legacy paths so existing scripts (`generate-report.js`, `daily-db-sync`) continue to work:
- `phase-4-analysis.json` → `outputs/analysis-{date}.json`
- `phase-3.5-screener.json` → `outputs/screener-{date}.json`
- `phase-3-discovery.json` → `outputs/discovery-{date}.json`
- `phase-4.2-regime.json` → `outputs/market-regime-{date}.json`
- `phase-4.3-top-risk.json` → `outputs/top-risk-{date}.json`
- `phase-4.6-market-env.json` → `outputs/market-env-{date}.json`
- `phase-5a-dq.json` → `outputs/dq-{date}.json`
- `phase-5.1-edge.json` → `outputs/edge-candidates/{date}/anomalies.json`

## Workflow

### Natural language triggers

Map common utterances to flags and phase scope before executing. Do not skip dependency order.

| User intent (examples) | Execution |
| --- | --- |
| Full daily pipeline (`오늘의 파이프라인 전체 실행해줘`, `Run today's pipeline`) | Phases **0→7** with default flags (no `dry-run`). Run fundamentals (2.5), screener (3.5), news/sentiment (4.5), full report + Slack + quality gate + decisions + KB ingest unless user opts out. |
| `today dry-run skip-twitter` | Full pipeline **except**: no Slack post (`dry-run`); no Phase 6 (`skip-twitter`). Still generate `.docx` unless `skip-docx`. |
| `today status` | **Phase 1 only** — stop after gap report (`status` / Step 1c). No writes. |
| Stock data sync only (`주식 데이터 동기화만 해줘`, sync prices only) | **Phases 1, 2, and 2.5** then stop: `skip-discover skip-screener skip-report` (skips Phases 3, 3.5, 4, 4.5, 5, 6). |
| Morning routine (`아침 루틴 시작`, `morning ship`) | **Do not run `today` alone** — invoke the `morning-ship` skill (Google briefing + `today` + consolidated Slack). If user insists on stock-only, run `today` full or with their flags. |

### Error recovery by step

| Step / call | On failure |
| --- | --- |
| Phase 0 (setup-doctor) | **Halt** if critical (DB unreachable, missing packages); **continue** with warnings if only optional gaps. |
| `weekly_stock_update.py` / `import_csv.py` | **Report** stderr; **retry once** after 30–60s if rate limit; if still failing, **continue** with warning and list tickers still stale (do not fake data). |
| `financial_data_collector.py` | **Log** per-ticker failures; **continue** pipeline — screener/report mark fundamentals N/A where missing. |
| `discover_hot_stocks.py` | **Continue** — empty discovery is expected on weekends/holidays; document in summary. |
| `stock_screener.py` | **Continue** without screener file if script errors; note in report/Slack that screening was skipped. |
| `daily_stock_check --source db` | **Halt** — Phase 4 output is required for Phase 5; user must fix DB/script error. |
| `alphaear-news` / `alphaear-sentiment` | **Continue** — already specified: missing JSON, report shows N/A. |
| `node generate-report.js` | **Halt** Step 5b; report `.docx` missing — offer `skip-docx` path only if user accepts no file. |
| `ai-quality-evaluator` | **Continue** with warning if skill unavailable; otherwise follow Step 5b½ thresholds (halt on FAIL when score is below 6.0). |
| Slack MCP (`slack_search_channels`, post, thread) | On post failure under `dry-run`, N/A; otherwise **retry once**, then **report** failure to user without claiming posted. |
| Phase 6 (`run_pipeline.js`, x-to-slack) | **Skip** Phase 6 if `TWITTER_COOKIE` missing or fetch fails after one retry; **log** warning. |

### Phase 0: Setup Doctor Pre-flight (Optional)

Run a quick diagnostic of the `core-platform` capability group to verify all prerequisites are available before starting the pipeline. Skip with `skip-setup-doctor`.

**Step 0a — Run targeted setup check:**

Read the `setup-doctor` skill and run Phase 1-3 checks for `--group core-platform` only. This verifies:
- PostgreSQL and Redis are running
- Python backend packages are installed
- `DATABASE_URL` is set and reachable

**Step 0b — Report and decide:**

- If all checks pass → proceed to Phase 1
- If critical items fail (DB connection, missing packages) → report the failures and halt
- If only warnings (optional items missing) → report and proceed

**Step 0c — Persist & manifest:** Save check results to `outputs/today/{date}/phase-0-doctor.json`. Create the initial `manifest.json` with pipeline metadata and this phase entry.

### Phase 1.5: Toss Snapshot + Monitoring (Optional — via toss-ops-orchestrator)

Delegates to `toss-ops-orchestrator` (`.cursor/skills/trading/toss-ops-orchestrator/SKILL.md`) for the snapshot and monitoring phases. Skip with `skip-toss`.

**Step 1.5a — Invoke toss-ops-orchestrator (Phase 1+2 only):**

Launch a Task with `toss-ops-orchestrator` using `--mode monitor-only` to run:
1. Account snapshot → `outputs/toss/summary-{date}.json`
2. Parallel monitoring (FX, risk, portfolio recon, watchlist sync)

The orchestrator handles tossctl availability checks internally — if tossctl is unavailable, it returns gracefully.

On failure: **Continue** — Toss operations are optional; the pipeline proceeds without them.

**Step 1.5b — Persist & manifest:** Save toss monitoring results to `outputs/today/{date}/phase-1.5-toss-monitor.json`. Update `manifest.json`.

### Phase 1: Data Freshness Check

Check current state of DB and CSV data to identify gaps.

**Step 1a — DB coverage:**

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

Capture the output table. Note the `Last` date column for each ticker.

**Step 1b — CSV freshness:**

For each CSV in `data/latest/`, read the first data row (most recent date). Compare against the DB `Last` date for the same ticker.

**Step 1c — Gap report:**

Produce a summary showing:
- Tickers where CSV has newer data than DB (CSV-ahead gap)
- Tickers where DB is missing yesterday's trading data (stale gap)
- Tickers that are up-to-date (no action needed)

If the `status` flag is set, stop here and report.

**Step 1d — Persist & manifest:** Save the gap report to `outputs/today/{date}/phase-1-freshness.json` (tickers with status, gap type, days stale). Update `manifest.json`.

### Phase 2: Data Sync

Fill identified gaps to ensure the DB has the freshest possible data.

**Step 2a — Import CSV data (if CSV-ahead gaps exist):**

```bash
cd backend
python scripts/import_csv.py ../data/latest --directory
```

This imports all CSVs; the upsert prevents duplicates.

**Step 2b — Fetch recent data from Yahoo Finance (if stale gaps exist):**

```bash
cd backend
python scripts/weekly_stock_update.py --days 3
```

The 3-day lookback covers weekends and short holidays. For longer gaps (>3 trading days), increase `--days` accordingly.

**Step 2c — Verify sync:**

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

Confirm `Last` dates have advanced. Report any tickers that still have gaps (market closed, delisted, etc.).

**Step 2d — Persist & manifest:** Save sync results to `outputs/today/{date}/phase-2-sync.json` (tickers synced, remaining gaps). Update `manifest.json`.

### Phase 2.5: Fundamental Data Sync

Collect financial statements and fundamental metrics for all tracked tickers. Skip with `skip-fundamentals`.

**Step 2.5a — Yahoo Finance fundamentals:**

```bash
cd backend
python scripts/financial_data_collector.py --all
```

This fetches quarterly income statements, balance sheets, and cash flow statements from yfinance, computes derived metrics (P/E, FCF yield, ROE, debt/equity, margins), and upserts into the `financial_statements` table.

**Step 2.5b — Verify fundamental coverage:**

```bash
cd backend
python scripts/financial_data_collector.py --status
```

Confirm financial data coverage. Report any tickers without fundamental data.

**Step 2.5c — Persist & manifest:** Save fundamental sync results to `outputs/today/{date}/phase-2.5-fundamentals.json`. Update `manifest.json`.

### Phase 3: Hot Stock Discovery

Discover the hottest untracked stocks from major indices. Skip this phase if the `skip-discover` flag is set.

**Step 3a — Run discovery script:**

```bash
cd backend
python scripts/discover_hot_stocks.py
```

This fetches constituents from NASDAQ 100 (Wikipedia), KOSPI 100, and KOSDAQ 100 (pykrx), filters out already-tracked tickers, and ranks by turnover (volume x close price). Returns JSON with the top 1 untracked stock per index.

**Step 3b — Fetch recent data for discovered tickers:**

For each discovered ticker, fetch 30 days of price data via yfinance:

```bash
cd backend
python scripts/weekly_stock_update.py --ticker {TICKER} --days 30
```

For Korean tickers, pass the 6-digit code (e.g., `003670`). The script auto-appends `.KS` or `.KQ`.

**Step 3c — Report discovery summary:**

Present the discovered hot stocks:
- Index name, ticker symbol, company name
- Yesterday's close price, change %, and turnover
- Suggested category (mapped from GICS sector)

The discovered stocks are included in the Phase 5 report but are NOT permanently added to the tracked ticker list.

**Step 3d — Persist & manifest:** Save discovery results to `outputs/today/{date}/phase-3-discovery.json`. Update `manifest.json`.

### Phase 3.5: Multi-Factor Screening (NEW)

Run institutional-grade screening on all tracked tickers. Skip with `skip-screener`.

**Step 3.5a — Run screener:**

```bash
cd backend
python scripts/stock_screener.py --all --json > ../outputs/screener-$(date +%Y-%m-%d).json
```

Runs by default with AI sentiment scoring (70% technical + 30% sentiment). Use `--no-sentiment` to skip sentiment. Applies 7 screening filters:
1. P/E ratio (0–50): eliminates overvalued / no-earnings stocks
2. RSI sweet spot (30–70): avoids overbought/oversold extremes
3. Volume spike (>1.5x 20-day avg): detects institutional flow
4. Trend confirmation (price > 50-day SMA): uptrend filter
5. Golden cross (20 SMA > 50 SMA): bullish crossover signal
6. Free Cash Flow yield (>0%): value filter from fundamental data
7. Earnings proximity (within 14 days): flags upcoming catalysts

**Step 3.5b — Skip sentiment (optional):** Use `--no-sentiment` if you want to run without AI sentiment. The default run includes sentiment.

**Step 3.5c — Report screener summary:**

Present screener results:
- Total stocks passing all filters
- STRONG BUY / BUY / NEUTRAL / CAUTION / AVOID distribution
- Top 5 stocks by composite score with key metrics

**Step 3.5d — Persist & manifest:** Save screener results to `outputs/today/{date}/phase-3.5-screener.json`. Update `manifest.json`.

### Phase 4: Analysis

Run technical analysis on all DB-tracked tickers using three indicator groups: Turtle Trading (SMA 20/55/200, Donchian), Bollinger Bands (20,2σ), and Oscillators (RSI, MACD, Stochastic, ADX).

```bash
cd backend
python -m scripts.daily_stock_check --source db
```

This analyzes all tickers stored in PostgreSQL (52+) instead of just CSV-mapped tickers. The JSON output includes:
- `date`: analysis date
- `total_stocks`: number of stocks analyzed
- `results[]`: per-stock signals including:
  - `category`: stock category from `TICKER_CATEGORY_MAP` (e.g., `ai_semiconductor`, `defense`)
  - `turtle`: SMA20, SMA55, SMA200, MA alignment (정배열/역배열/혼조), golden/death cross, Donchian channel, ATR
  - `bollinger`: upper/middle/lower bands, %B, bandwidth, squeeze detection
  - `oscillators`: RSI(14) with zone (과매수/과매도/중립), MACD(12,26,9) with cross detection, Stochastic(14,3) with zone, ADX(14) with trend strength
  - `overall_signal`: 3-way combined signal (STRONG_BUY/BUY/NEUTRAL/SELL/STRONG_SELL) from turtle + bollinger + oscillator scores
- `summary`: signal distribution counts

**Step 4b — Persist & manifest:** Save the full analysis JSON to `outputs/today/{date}/phase-4-analysis.json`. Update `manifest.json`.

#### Post-Analysis Parallel Fan-Out (Phases 4.2 / 4.3 / 4.5 / 4.6)

After Phase 4 stock analysis completes, launch the following four optional phases as **parallel subagents** (max 4 concurrent). Each is independent and produces its own output artifact. If any subagent fails, the others continue unaffected.

| Subagent | Phase | Output (file-first) | Skip Flag |
|----------|-------|--------|-----------|
| Regime Diagnosis | 4.2 | `outputs/today/{date}/phase-4.2-regime.json` | `skip-regime` |
| Top Risk Overlay | 4.3 | `outputs/today/{date}/phase-4.3-top-risk.json` | `skip-top-risk` |
| AlphaEar Intelligence | 4.5 | `outputs/today/{date}/phase-4.5-alphaear.json` | `skip-news` / `skip-sentiment` |
| Market Environment | 4.6 | `outputs/today/{date}/phase-4.6-market-env.json` | `skip-market-env` |

**Each subagent must**: save its output to the corresponding phase file under `outputs/today/{date}/`, and return only `{ status, file, summary }` to keep the orchestrator's context lean.

Wait for all four subagents to complete (or be skipped) before proceeding to Phase 4.8 (Agent Trading Desk) and Phase 5 (Report).

### Phase 4.2: Market Regime Diagnosis (Optional — parallel fan-out)

Diagnose the macro market environment before interpreting individual stock signals. Runs 3 independent analyses in parallel using free TraderMonty CSV data (no API key required). Skip with `skip-regime`.

**Step 4.2a — Launch parallel regime subagents:**

Launch 3 parallel Task subagents (model: fast):

1. **Breadth Health** — read the `trading-market-breadth-analyzer` skill and run:

```bash
python3 .cursor/skills/trading/trading-market-breadth-analyzer/scripts/analyze_market_breadth.py --json --save
```

Output: `outputs/breadth-{date}.json` (6-component score, 0-100, higher = healthier)

2. **Uptrend Ratios** — read the `trading-uptrend-analyzer` skill and run:

```bash
python3 .cursor/skills/trading/trading-uptrend-analyzer/scripts/analyze_uptrend.py --json --save
```

Output: `outputs/uptrend-{date}.json` (5-component score, 0-100, higher = healthier)

3. **Sector Rotation** — read the `trading-sector-analyst` skill and run:

```bash
python3 .cursor/skills/trading/trading-sector-analyst/scripts/analyze_sector_rotation.py --json --save
```

Output: `outputs/sector-rotation-{date}.json` (sector rankings, cyclical/defensive ratio, market cycle phase)

**Step 4.2b — Synthesize regime summary:**

After all 3 subagents complete, compute the Market Regime Summary:
- Composite regime score = breadth (40%) + uptrend (30%) + sector cyclical/defensive tilt (30%)
- Classification: **RISK-ON** (70+) / **CAUTIOUS** (40–69) / **RISK-OFF** (0–39)
- Exposure guidance: `full` / `reduced` / `defensive`

Save to `outputs/market-regime-{date}.json`:

```json
{
  "date": "2026-04-01",
  "breadth_score": 72,
  "uptrend_score": 65,
  "sector_phase": "mid-cycle",
  "cyclical_defensive_ratio": 1.4,
  "composite_regime_score": 68,
  "regime": "CAUTIOUS",
  "exposure_guidance": "reduced",
  "summary_ko": "시장 브레드스 72점, 업트렌드 65점으로 참여도 양호하나 섹터 순환 중기 단계. 익스포저 소폭 축소 권장."
}
```

On failure: **Continue** — regime data is optional. If any subagent fails, use available scores only. If all fail, report shows "N/A" for regime.

**Step 4.2c — Persist & manifest:** Save regime summary to `outputs/today/{date}/phase-4.2-regime.json`. Update `manifest.json`.

### Phase 4.3: Market Top Risk Overlay (Optional — conditional on FMP_API_KEY)

Detect whether a market top is forming using the O'Neil/Minervini/Monty methodology. Skip with `skip-top-risk`. Auto-skipped if `FMP_API_KEY` is not set in `.env`.

**Step 4.3a — Check API key availability:**

Verify `FMP_API_KEY` exists in the environment or `.env` file. If missing, log "FMP_API_KEY not set, skipping market top detection" and skip this phase entirely.

**Step 4.3b — Run top detector:**

Read the `trading-market-top-detector` skill and execute the 6-component scoring system:
1. Distribution Day accumulation (O'Neil methodology)
2. Leading stock deterioration (Minervini pattern)
3. Defensive sector rotation (Monty signal)
4. Volume distribution analysis
5. Breadth divergence detection
6. VIX term structure assessment

Save to `outputs/top-risk-{date}.json`:

```json
{
  "date": "2026-04-01",
  "top_probability": 35,
  "risk_level": "MODERATE",
  "distribution_day_count": 3,
  "leadership_deterioration": false,
  "defensive_rotation_active": false,
  "action": "monitor",
  "summary_ko": "천정 확률 35% — 분배일 3일 누적, 선도주 건재. 모니터링 유지."
}
```

On failure: **Continue** — top risk detection is optional. Report shows "N/A" if unavailable.

**Step 4.3c — Persist & manifest:** Save top risk results to `outputs/today/{date}/phase-4.3-top-risk.json`. Update `manifest.json`.

### Phase 4.5: AlphaEar Intelligence (Optional — via alphaear-orchestrator)

Delegates to `alphaear-orchestrator` (`.cursor/skills/alphaear/alphaear-orchestrator/SKILL.md`) for comprehensive market context. Skip with `skip-news` and/or `skip-sentiment`.

**Step 4.5a — Invoke alphaear-orchestrator:**

Launch a Task with `alphaear-orchestrator` to run the full 3-layer pipeline:
1. Data collection (news, stock data, search) — parallel
2. Analysis (sentiment, prediction, signal tracking) — parallel
3. Report generation

The orchestrator consolidates the previously separate `alphaear-news`, `alphaear-sentiment`, and `alphaear-reporter` calls into a single coordinated pipeline with proper data flow between layers.

Skip flags are forwarded: `skip-news` → `--skip news`, `skip-sentiment` → `--skip sentiment`.

Output: `outputs/alphaear/intel-{date}.md` and individual artifacts in `_workspace/alphaear/`.

On failure: **Continue** — AlphaEar is optional. The report shows "N/A" for market context if the orchestrator fails.

**Step 4.5b — Persist & manifest:** Save AlphaEar intelligence summary to `outputs/today/{date}/phase-4.5-alphaear.json`. Update `manifest.json`.

### Phase 4.6: Market Environment Context (Optional)

Collect a global market snapshot (US indices, VIX, FX, commodities, Treasury yields) to provide macro context for the report narrative. Uses web search — no API key required. Skip with `skip-market-env`.

**Step 4.6a — Collect global market data:**

Read the `trading-market-environment-analysis` skill. Run the web-search-based data collection covering:
1. US indices: S&P 500, NASDAQ Composite, Dow Jones
2. Volatility: VIX level and term structure
3. FX: USD/JPY, EUR/USD, USD/KRW
4. Commodities: WTI crude oil, Gold
5. Yields: US 2Y and 10Y Treasury yields
6. Risk sentiment classification: risk-on / risk-off / mixed

**Step 4.6b — Structure and save:**

Save to `outputs/market-env-{date}.json`:

```json
{
  "date": "2026-04-01",
  "us_markets": {
    "sp500": { "level": 5250, "change_pct": 0.3 },
    "nasdaq": { "level": 16500, "change_pct": 0.5 },
    "dow": { "level": 39800, "change_pct": 0.1 }
  },
  "vix": 18.5,
  "risk_sentiment": "risk-on",
  "fx": { "usd_jpy": 150.2, "eur_usd": 1.08, "usd_krw": 1350 },
  "commodities": { "wti": 82.5, "gold": 2350 },
  "yields": { "us_2y": 4.6, "us_10y": 4.2 },
  "summary_ko": "S&P 500 소폭 상승, VIX 18.5로 안정적. 원달러 1350원대. 유가·금 보합. 리스크온 분위기."
}
```

On failure: **Continue** — market environment data is optional. Report shows "N/A" for global context.

**Step 4.6c — Persist & manifest:** Save market environment data to `outputs/today/{date}/phase-4.6-market-env.json`. Update `manifest.json`.

### Phase 4.8: Agent Trading Desk (Optional)

Run a multi-agent debate-based analysis on top BUY/SELL signal stocks. Skip with `skip-agent-desk`.

**Step 4.8a — Select candidates:**

From the Phase 4 analysis output, select up to 5 stocks with the strongest BUY or SELL signals (highest absolute signal scores). These become candidates for the agent desk.

**Step 4.8b — Run Agent Desk pipeline:**

Use `backend/app/services/agent_desk/desk.py` `AgentDesk.run()`:
1. 4 Analyst agents (Technical, Fundamental, Sentiment, News) run in parallel using quick model
2. Bull/Bear debate runs for 2 rounds using deep model with BM25 memory injection
3. Research Manager synthesizes the debate into a BUY/SELL/HOLD decision with confidence
4. Risk Evaluator applies position sizing and risk-adjusted scoring

Output saved to `outputs/agent-desk/{date}/desk-decisions.json`.

**Step 4.8c — Merge into report:**

Agent desk decisions are included in the Phase 5 report as an "Agent Trading Desk 분석" section, showing the debate-synthesized consensus alongside the technical/quantitative signals.

On failure: **Continue** — agent desk is optional; the pipeline proceeds without desk decisions.

**Step 4.8d — Persist & manifest:** Save agent desk decisions to `outputs/today/{date}/phase-4.8-agent-desk.json`. Update `manifest.json`.

### Phase TV-SC: TradingView Screener Cross-Check (Optional — requires `--with-tradingview`)

Cross-checks the native multi-factor screener results against TradingView MCP screener data. Only runs when `--with-tradingview` flag is set and the `tradingview-mcp-server` npm MCP is available.

**Step TV-SC.a — Run screener cross-check:**

The `tv_screener_crosscheck` pipeline stage (registered in `pipeline_orchestrator.py`) loads the native screener output from `outputs/screener-{date}.json`, queries the TradingView MCP screener for the "most_volatile" strategy (top 50), and computes the overlap.

Output: `outputs/tv-screener-crosscheck-{date}.json` with `overlap` (tickers in both), `tv_only_highlights` (blind spots), and counts.

On failure: **Continue** — gracefully degrades if the TradingView MCP server is unavailable.

**Step TV-SC.b — Persist & manifest:** Save to `outputs/today/{date}/phase-tv-screener.json`. Update `manifest.json`.

### Phase TV-TA: TradingView TA Cross-Validation (Optional — requires `--with-tradingview`)

Cross-validates native TA signals against TradingView MCP TA data for the top 15 screened stocks. Only runs when `--with-tradingview` flag is set and the `tradingview_mcp` Python MCP is available.

**Step TV-TA.a — Run TA cross-validation:**

The `tv_ta_validation` pipeline stage loads analysis output from `outputs/analysis-{date}.json`, calls `TradingViewTAService.batch_analysis()` for the top 15 symbols, and runs `cross_validate_signals()` comparing RSI zones, MACD direction, trend alignment, and Bollinger position.

Output: `outputs/tv-ta-validation-{date}.json` with per-symbol confidence scores (HIGH/MEDIUM/LOW) and an overall agreement ratio.

On failure: **Continue** — gracefully degrades if the TradingView MCP server is unavailable.

**Step TV-TA.b — Persist & manifest:** Save to `outputs/today/{date}/phase-tv-ta.json`. Update `manifest.json`.

### Phase PS: Pine Script Generation (Optional — requires `--with-pine`)

Generates Pine Script v5 code for the top 5 screened stocks' indicator configurations. Runs locally — no external MCP dependency. Only runs when `--with-pine` flag is set.

**Step PS.a — Generate scripts:**

The `pine_script_generation` pipeline stage calls `generate_composite_script()` for overlay indicators (SMA, EMA, Bollinger, Donchian) and `generate_pine_script()` for each oscillator (RSI, MACD, ADX, Stochastic) per symbol.

Output: `outputs/pine-scripts/{SYMBOL}-{indicator}-{date}.pine` files plus `manifest-{date}.json`.

On failure: Per-symbol errors are logged and skipped; other symbols continue.

**Step PS.b — Persist & manifest:** Save generation manifest to `outputs/today/{date}/phase-pine-scripts.json`. Update `manifest.json`.

### Phase 5: Report and Post

**Step 5a — Generate report content (File-First — 반드시 한국어로 작성):**

**Data Source**: Read all inputs from `outputs/today/{date}/` phase files. Do NOT rely on in-context conversation memory for any data used in report generation.

Load the following files from `outputs/today/{date}/`:
- `phase-4-analysis.json` — main stock analysis (required)
- `phase-3.5-screener.json` — screening results (optional)
- `phase-4.2-regime.json` — market regime (optional)
- `phase-4.3-top-risk.json` — top risk overlay (optional)
- `phase-4.6-market-env.json` — global market environment (optional)
- `phase-4.5-alphaear.json` — AlphaEar news/sentiment (optional)
- `phase-4.8-agent-desk.json` — agent desk decisions (optional)
- `phase-5.1-edge.json` — edge candidates (optional)
- `phase-3-discovery.json` — hot stock discovery (optional)

For each file: if it exists, parse and integrate its data into the report. If it is missing or `status` in the manifest is `"skipped"`, omit that section with a brief note (e.g., "시장 체제 데이터: N/A").

Use the `alphaear-reporter` skill workflow with the loaded phase-4-analysis JSON as input signals.
**모든 리포트 텍스트, 섹션 제목, 분석 내용, 요약은 반드시 한국어로 작성한다.** 종목 코드(ticker)와 고유명사(회사명 영문)만 영어를 허용한다.

1. **시그널 클러스터링**: 종목 시그널을 3–5개 테마로 그룹핑 (예: "기술주 모멘텀", "KRX 반등", "방어주 포지션")
2. **섹션 작성**: 각 테마별로 시그널 근거, 가격 맥락, 리스크 요인을 분석
3. **최종 조립**: 다음 섹션으로 리포트를 구성:
   - 날짜 및 시장 개요
   - 시그널 요약 (매수/중립/매도 종목 수)
   - **시장 체제 대시보드** (from `phase-4.2-regime.json`, 없으면 생략): 복합 체제 점수(0-100), 체제 분류(RISK-ON/CAUTIOUS/RISK-OFF), 브레드스·업트렌드·섹터 로테이션 하위 점수, 1-2줄 체제 내러티브
   - **시장 천정 리스크** (from `phase-4.3-top-risk.json`, 없으면 생략): 천정 확률(%), 리스크 레벨(LOW/MODERATE/HIGH/CRITICAL), 분배일 수, 핵심 경고 사항
   - **글로벌 시장 스냅샷** (from `phase-4.6-market-env.json`, 없으면 생략): 미국 지수(S&P/NASDAQ/Dow), VIX, 주요 환율(USD/KRW 포함), 원자재, 국채 수익률, 리스크 센티먼트
   - 테마별 분석 (클러스터링된 시그널 기반)
   - 주요 종목 (가장 강한 매수/매도 시그널과 근거)
   - **엣지 후보 리서치 티켓** (from `phase-5.1-edge.json`, 없으면 생략): 발견된 이상 징후 요약, 심각도별 분류, 후속 조사 워치리스트
   - 리스크 노트 및 면책 조항

4. **Save structured report content**: Write the assembled report sections to `outputs/today/{date}/phase-5-report-content.json`:
```json
{
  "date": "2026-04-01",
  "sections": {
    "signal_summary": { "buy": 12, "neutral": 30, "sell": 10, "total": 52 },
    "regime_dashboard": { ... },
    "top_risk": { ... },
    "global_snapshot": { ... },
    "theme_analyses": [ ... ],
    "key_stocks": { "buy": [...], "sell": [...] },
    "edge_candidates": [ ... ]
  },
  "report_narrative_ko": "... full Korean report text ..."
}
```
5. **Update manifest**: Append phase-5 entry to `manifest.json`

**Step 5a-DQ — Data Quality Check (automatic, skip if `skip-dq`):**

Before generating the report, validate data consistency across all analysis outputs:

1. **Date alignment**: Verify all output files reference the same trading date.
2. **Price consistency**: Cross-check that ticker prices in `analysis-{date}.json` match `screener-{date}.json` within ±1% tolerance.
3. **Signal coherence**: Flag contradictions (e.g., a stock marked BUY in screener but SELL in analysis without an explanation).
4. **Stale data detection**: If any ticker's latest price is >2 trading days old, flag as potentially stale.
5. **Completeness**: Ensure all tracked tickers appear in the analysis output.

Read the `trading-data-quality-checker` skill for validation methodology.

Save to `outputs/dq-{date}.json`:

```json
{
  "date": "2026-04-01",
  "checks_passed": 4,
  "checks_failed": 1,
  "warnings": ["AAPL price stale by 3 days"],
  "errors": [],
  "overall": "PASS_WITH_WARNINGS"
}
```

If `overall` is `FAIL` (errors found): halt report generation and notify user.
If `overall` is `PASS_WITH_WARNINGS`: continue but include warnings in the report appendix.
If `overall` is `PASS`: continue normally.

**Persist & manifest:** Save DQ results to `outputs/today/{date}/phase-5a-dq.json`. Update `manifest.json`.

**Step 5b — Generate Korean .docx report (skip if `skip-docx` flag is set):**

1. **Legacy file copies** (backward compatibility for `generate-report.js` and `daily-db-sync`):
   - Copy `outputs/today/{date}/phase-4-analysis.json` → `outputs/analysis-{date}.json`
   - Copy `outputs/today/{date}/phase-3.5-screener.json` → `outputs/screener-{date}.json`
   - Copy `outputs/today/{date}/phase-3-discovery.json` → `outputs/discovery-{date}.json`
   - Copy `outputs/today/{date}/phase-4.2-regime.json` → `outputs/market-regime-{date}.json` (if exists)
   - Copy `outputs/today/{date}/phase-4.3-top-risk.json` → `outputs/top-risk-{date}.json` (if exists)
   - Copy `outputs/today/{date}/phase-4.6-market-env.json` → `outputs/market-env-{date}.json` (if exists)
   - Copy `outputs/today/{date}/phase-5a-dq.json` → `outputs/dq-{date}.json` (if exists)
   - Copy `outputs/today/{date}/phase-5.1-edge.json` → `outputs/edge-candidates/{date}/anomalies.json` (if exists)
2. Run the report generator:

```bash
cd outputs
node generate-report.js {date}
```

The generator also reads `outputs/news-{date}.json` for market context, `outputs/screener-{date}.json` for screening results, `outputs/market-regime-{date}.json` for regime data, `outputs/top-risk-{date}.json` for top risk data, `outputs/market-env-{date}.json` for global market context, and `outputs/edge-candidates/{date}/anomalies.json` for edge candidates (all optional — sections omitted when data unavailable).
It produces a Korean expert report (`outputs/reports/daily-{date}.docx`) with:
   - 표지 (제목, 날짜, 분석 종목 수)
   - 요약 (시그널 분포표, 정배열 종목 수, 스퀴즈 종목, 골든/데스크로스, RSI 과매수/과매도, MACD 크로스)
   - **시장 체제 대시보드** (복합 점수, 체제 분류, 하위 점수 테이블, 체제 내러티브 — `market-regime-{date}.json` 사용)
   - **시장 천정 리스크** (천정 확률, 리스크 레벨, 분배일 수, 핵심 경고 — `top-risk-{date}.json` 사용)
   - **글로벌 시장 스냅샷** (미국 지수, VIX, 환율, 원자재, 국채, 리스크 센티먼트 — `market-env-{date}.json` 사용)
   - 시장 동향 (alphaear-news 뉴스 헤드라인, if available)
   - **스크리너 결과** (STRONG BUY/BUY 종목 요약, composite score, 필터 통과 현황)
   - **펀더멘탈 스냅샷** (종목별 P/E, FCF Yield, ROE, Debt/Equity, Revenue Growth)
   - **거래량 분석** (RVOL, Volume Spike, OBV 추세)
   - 카테고리별 요약표
   - 주요 종목 상세 분석 (BUY/SELL 종목별 이동평균선·볼린저·오실레이터 분석 + 감성 점수 + 펀더멘탈 메트릭스 + 매매 판단 근거)
   - 전체 종목 시그널 일람표 (터틀/볼린저/오실레이터/스크리너/종합 5열)
   - **어닝 캘린더** (14일 내 실적 발표 예정 종목)
   - **엣지 후보 리서치 티켓** (이상 징후 요약, 심각도 분류, 워치리스트 — `edge-candidates/{date}/anomalies.json` 사용)
   - 핫 종목 (미추적 종목 발견 결과)
   - 기술적 지표 상세표 (이동평균선, 볼린저, 오실레이터 3개 테이블)
   - 데이터 품질 부록 (DQ 경고가 있는 경우 — `dq-{date}.json` 사용)
   - 리스크 노트 및 면책 조항

**Step 5b½ — Quality Gate (Evaluator-Optimizer, skip if `skip-quality-gate`):**

Evaluate the generated report before posting. Uses the `ai-quality-evaluator` skill as the evaluator in an evaluator-optimizer loop.

1. Score the report content on 5 dimensions: accuracy, hallucination detection, data consistency, coverage completeness, and actionability
2. Compute the overall quality score (weighted average)
3. Apply quality decision:
   - **Score >= 8.0** → PASS — proceed to Slack posting
   - **Score 6.0–7.9** → REFINE — feed evaluator feedback back to `alphaear-reporter`, regenerate the weak sections, re-score (max 2 refinement iterations)
   - **Score < 6.0** → FAIL — halt pipeline, do not post, notify user with the score breakdown and specific failures
4. Stopping criteria for refinement loop:
   - Score reaches >= 8.0
   - Max 2 iterations reached (post with best-scoring version and note the quality score)
   - No improvement between iterations (score delta < 0.5)

If `ai-quality-evaluator` skill is not available, log a warning and skip the gate (proceed to posting).

**Step 5c — Post to Slack (File-First — optional, skip if `dry-run` or `skip-slack`):**

**Data Source**: Read all Slack content from `outputs/today/{date}/` phase files and `manifest.json`. Do NOT compose Slack messages from in-context memory.

Load and parse:
- `manifest.json` — pipeline status, phase summaries, warnings
- `phase-5-report-content.json` — structured report sections (signal summary, key stocks, regime, etc.)
- `phase-4-analysis.json` — per-stock signals for thread detail
- `phase-4.2-regime.json` — regime badge/score (if available)
- `phase-4.3-top-risk.json` — top risk badge/level (if available)
- `phase-4.6-market-env.json` — market environment data (if available)
- `phase-3-discovery.json` — hot stocks (if available)
- `phase-5.1-edge.json` — edge candidates (if available)

1. Use `slack_search_channels` MCP tool to find `#h-report` channel ID (known: `C0AKHQWJBLZ`)
2. Populate the main message template using data loaded from the phase files above
3. Post the **main message** with date, signal summary, top movers, hot stocks, and screener summary
4. Capture the `message_ts` from the response
5. **ALWAYS post a thread reply** using `thread_ts` = the main message's `message_ts`, containing:
   - `:mag: BUY 종목 상세 ({N}종목)` — grouped by category (한국 방산/전력/반도체, 미국 인프라/방산, 기타 등), each stock with name, price, change%, RSI, ADX (with 강한추세 label), and any warnings (과매수/과매도)
   - `:mag: SELL 종목 상세 ({N}종목)` — each stock with name, price, change%, RSI, RSI zone, MA alignment, ADX, Stochastic
   - `:warning:` notes for RSI extremes (과매수 80+, 과매도 30-)
   - `:bulb:` actionable insight for notable patterns (과매도 반등 가능, 과매수 조정 가능 등)

**Slack main message template:**

```
:newspaper: *일간 분석 보고서 — {date}*
{total_stocks}개 종목 분석 | :green_circle: 매수 {buy_count} | :white_circle: 중립 {neutral_count} | :red_circle: 매도 {sell_count}
{regime_badge} {regime_label} (점수 {regime_score}/100) | {top_risk_badge} 천정 리스크 {top_risk_level}

---

:globe_with_meridians: *시장 환경*
> S&P {sp500_change}% | NASDAQ {nasdaq_change}% | VIX {vix} | USD/KRW {usdkrw} | 센티먼트: {risk_sentiment}

:chart_with_upwards_trend: *주요 매수 종목*
> :large_green_circle: *{ticker}* `{price}` (+{change}%) — {korean_rationale}

:chart_with_downwards_trend: *주요 매도 종목*
> :red_circle: *{ticker}* `{price}` ({change}%) — {korean_rationale}

---

:fire: *핫 종목 (미추적)*
> :us: *NASDAQ 100*: *{ticker}* `${close}` — 거래대금 ${turnover}
> :kr: *KOSPI 100*: *{ticker}* `₩{close}` — 거래대금 ₩{turnover}
> :kr: *KOSDAQ 100*: *{ticker}* `₩{close}` — 거래대금 ₩{turnover}

---

:page_facing_up: 상세 보고서: `outputs/reports/daily-{date}.docx`
_분석 기준: 이동평균선(20/55/200일) + 볼린저 밴드(%B/스퀴즈) + 오실레이터(RSI/MACD/Stoch/ADX) | 본 보고서는 투자 권유가 아닙니다._
```

**Slack main message dynamic fields (from new phases — omit entire line/section if data unavailable):**
- `{regime_badge}`: `:large_green_circle:` RISK-ON / `:large_orange_circle:` CAUTIOUS / `:red_circle:` RISK-OFF (from `outputs/today/{date}/phase-4.2-regime.json`)
- `{regime_label}`, `{regime_score}`: regime classification and composite score
- `{top_risk_badge}`: `:white_check_mark:` LOW / `:warning:` MODERATE / `:rotating_light:` HIGH / `:no_entry:` CRITICAL (from `outputs/today/{date}/phase-4.3-top-risk.json`)
- `{top_risk_level}`: top risk classification string
- Market environment fields (`sp500_change`, `nasdaq_change`, `vix`, `usdkrw`, `risk_sentiment`): from `outputs/today/{date}/phase-4.6-market-env.json`

**Slack thread reply template (MUST always post):**

```
:mag: *BUY 종목 상세 ({buy_count}종목 전체)*

{category_group_header} (정배열 집중)
> {name}({ticker}) {currency}{price} ({change}%) — RSI {rsi}, ADX {adx} {adx_strength}
...

:warning: {과매수_종목}은 RSI 80+ 과매수 구간으로 단기 조정 가능성 있음

---

:mag: *SELL 종목 상세 ({sell_count}종목)*
> {name} ${price} ({change}%) — RSI {rsi} {rsi_zone}, {ma_alignment} 배열{, ADX {adx}}
...

:bulb: {과매도_종목}는 RSI {rsi}로 과매도 구간, 반등 가능성 모니터링 필요

---

:dart: *엣지 후보 ({edge_count}건)* _(Phase 5.1 결과, 없으면 생략)_
> :small_orange_diamond: [{severity}] *{ticker}* — {anomaly_type}: {description}
...

---

_본 스레드 및 본 분석은 투자 권유가 아니며 참고용입니다._
```

**Step 5d — Trading Decision Extraction (skip if `skip-decisions`):**

After posting to Slack, scan the analysis results for decision-worthy trading signals using the `decision-router` skill rules. All trading decisions go to `#효정-의사결정` (`C0ANBST3KDE`) as personal scope.

Detection criteria:
- STRONG_BUY signal with composite score >= 8 → post as position entry decision (urgency: HIGH)
- STRONG_SELL signal with high confidence → post as exit decision (urgency: HIGH)
- Multiple correlated BUY signals in same sector → post as sector rebalancing decision (urgency: MEDIUM)
- RSI extreme (> 80 or < 20) with ADX > 25 → post as risk alert decision (urgency: MEDIUM)
- Screener STRONG BUY stocks not currently in portfolio → post as new position decision (urgency: MEDIUM)
- Market regime shift detected (RISK-ON → CAUTIOUS or CAUTIOUS → RISK-OFF) → post as exposure adjustment decision (urgency: HIGH) — from `outputs/today/{date}/phase-4.2-regime.json`
- Market top probability >= 60% → post as risk reduction decision (urgency: HIGH) — from `outputs/today/{date}/phase-4.3-top-risk.json`
- Edge candidate with severity HIGH or CRITICAL → post as investigation decision (urgency: MEDIUM) — from `outputs/today/{date}/phase-5.1-edge.json`

For each detected signal, format using the DECISION template:

```
*[DECISION]* {urgency_badge} | 출처: today

*{Ticker} {signal_type} 검토*

*배경*
{Signal details: composite score, RSI, ADX, MA alignment, Bollinger position}

*판단 필요 사항*
{Position entry/exit/rebalancing decision}

*옵션*
A. {action option} — {rationale with metrics}
B. {wait option} — {rationale}
C. 보류 / 추가 조사 필요

*추천*
{recommended option with technical rationale}

*긴급도*: {HIGH / MEDIUM / LOW}
*원본*: outputs/reports/daily-{date}.docx
```

Post each decision as a separate message (not threaded) to `#효정-의사결정`.

### Phase 5.1: Edge Candidate Discovery (Optional)

After all analysis is complete, automatically detect anomalies and generate research tickets for potential new trading edges. Converts daily observations into a persistent research pipeline. Skip with `skip-edge`.

**Step 5.1a — Feed analysis data:**

Collect inputs from earlier phases (read from `outputs/today/{date}/`):
- Phase 4 analysis JSON (`phase-4-analysis.json`) — individual stock signals
- Phase 4.2 regime data (`phase-4.2-regime.json`, if available) — macro context
- Phase 3 discovery JSON (`phase-3-discovery.json`, if available) — hot stocks

**Step 5.1b — Run edge candidate detection:**

Read the `trading-edge-candidate-agent` skill. Run in daily auto-detect mode:
1. Scan for volume anomalies (RVOL > 3x with no news catalyst)
2. Detect unusual price action (gap > 2% against sector direction)
3. Identify sector divergences from Phase 4.2 data
4. Flag cross-market correlation breaks

**Step 5.1c — Save research tickets:**

Output to `outputs/edge-candidates/{date}/`:
- `daily_report.md` — human-readable summary of anomalies
- `anomalies.json` — structured anomaly list with severity scores
- `watchlist.csv` — tickers warranting follow-up research

Log the count of new edge candidates in the pipeline summary.

On failure: **Continue** — edge candidate discovery is optional. The pipeline proceeds without research tickets.

**Step 5.1d — Persist & manifest:** Save edge candidate summary to `outputs/today/{date}/phase-5.1-edge.json`. Update `manifest.json`.

### Phase 5.5: Toss Signal Bridge + Reporting (Optional — via toss-ops-orchestrator)

Delegates to `toss-ops-orchestrator` (`.cursor/skills/trading/toss-ops-orchestrator/SKILL.md`) for the signal bridge and reporting phases. Skip with `skip-toss`.

**Step 5.5a — Invoke toss-ops-orchestrator (Phase 3+4 only):**

Launch a Task with `toss-ops-orchestrator` using `--skip snapshot,fx,risk,recon,watchlist` to run only:
1. Signal bridge (reads screener + analysis outputs, generates dry-run order previews)
2. Trade journal (log recent trades)
3. Morning briefing (consolidated Slack post to `#h-daily-stock-check`)

The orchestrator uses the snapshot data from Phase 1.5 (if available) and the screener/analysis outputs from Phases 3.5/4.

**Step 5.5b — Include in Slack thread (if Phase 5c runs):**

Add a "Toss 실행 가능 시그널" section to the Slack thread reply containing:
- Top 3 trade candidates with signal strength and estimated cost
- Portfolio risk status summary
- Note: "실행하려면 tossinvest-trading 스킬을 사용하세요"

On failure: **Continue** — Toss integration is optional; log a warning and proceed.

**Step 5.5c — Persist & manifest:** Save toss signal bridge results to `outputs/today/{date}/phase-5.5-toss-signal.json`. Update `manifest.json`.

### Phase 5½: Report Quality Gate

Before posting to Slack or proceeding to Phase 6, verify report quality:

- [ ] **Data consistency** — All tickers in the report have matching DB data (no stale or missing prices)
- [ ] **Signal accuracy** — Buy/sell signals match the underlying indicator calculations (SMA crossovers, RSI thresholds, Bollinger position)
- [ ] **Report completeness** — All tracked tickers appear in the report; no ticker silently dropped
- [ ] **Date correctness** — Report date matches the latest trading date in the DB, not today's calendar date

If ANY criterion fails, log the discrepancy in the report's appendix and flag it in the Slack message. Do NOT suppress the report — post it with warnings attached.

### Phase 6: Twitter Timeline to Slack (Optional)

Fetch the user's latest tweets and post to classified Slack channels. Skip with `skip-twitter`.

**Step 6a — Fetch and classify tweets:**

Read the `twitter-timeline-to-slack` skill. Run the fetch pipeline for the default screen name (`hjguyhan`):

```bash
cd scripts/twitter && node run_pipeline.js --fetch-only
```

**Step 6b — Post unposted tweets:**

For each unposted tweet (excluding thread members), execute the full x-to-slack workflow:
1. FxTwitter API enrichment
2. WebSearch (2-3 queries per tweet)
3. 3-message Slack thread (title → detailed summary → topic insights)
4. Media upload if photo/video exists
5. Update `tweets.json` with posting status
6. Rate limit: 10-15s between tweets

**Step 6c — Report:**

Report the number of tweets fetched, classified, and posted with channel distribution.

**Prerequisite:** `TWITTER_COOKIE` must be set in `.env`. If missing, skip Phase 6 and log a warning.

**Step 6d — Persist & manifest:** Save twitter pipeline results to `outputs/today/{date}/phase-6-twitter.json` (tweet count, channels, post status). Update `manifest.json`. Finalize `manifest.json` with `completed_at` and `overall_status`.

### Phase 7: Knowledge Base Accumulation (Optional — Compound Growth Loop)

Two-path knowledge accumulation for long-term compound growth. Path A writes to Karpathy-style markdown KBs; Path B feeds Cognee KG via `knowledge_daily_aggregator.py`. Skip with `skip-kb`.

**Step 7a — KB ingest (trading-daily raw source):**

```bash
python scripts/kb_daily_ingest.py --date {date}
```

Reads phase output files from `outputs/today/{date}/` or `outputs/daily/{date}/`, condenses into a single markdown with YAML frontmatter, saves to `knowledge-bases/trading-daily/raw/daily-{date}.md`.

**Step 7b — KB multi-topic router:**

```bash
python scripts/kb_daily_router.py --date {date}
```

Scans all `outputs/` directories, classifies artifacts by topic (trading-daily, ai-research, tech-trends, project-ops), and routes each to its `knowledge-bases/{topic}/raw/` directory. Auto-initializes new KB directories. Deduplicates against existing raw files.

**Step 7c — Incremental compile (optional, skip if `skip-kb-compile`):**

If accumulated raw sources exceed 7 since last compile, trigger LLM wiki compilation:

```bash
python scripts/kb_compile.py {topic}
```

Uses Claude to transform raw sources into structured wiki articles with YAML frontmatter, wikilinks, and navigation files (`_index.md`, `_summary.md`, `_glossary.md`, `_concept-map.md`).

**Step 7d — Persist & manifest:** Save KB results to `outputs/today/{date}/phase-7-kb-ingest.json`:

```json
{
  "date": "2026-04-01",
  "raw_file": "knowledge-bases/trading-daily/raw/daily-2026-04-01.md",
  "topics_routed": {"trading-daily": 2, "ai-research": 6, "tech-trends": 12},
  "compiled": false,
  "status": "completed"
}
```

Update `manifest.json`.

On failure: **Continue** — KB accumulation is optional; the pipeline succeeds without it.

## CLI Arguments

| Argument | Default | Description | Example |
|---|---|---|---|
| (none) | Full pipeline | Run Phases 0–6 (optional phases per flags below) | `/today` |
| `status` | off | Phase 1 only — show data freshness report | `/today status` |
| `dry-run` | off | Run all phases but skip Slack posting (still generates `.docx` unless `skip-docx`) | `/today dry-run` |
| `skip-slack` | off | Skip Step 5c only (no main or thread Slack post); unlike `dry-run`, intent is Slack-specific | `/today skip-slack` |
| `skip-sync` | off | Skip Phase 2, run analysis on existing DB data | `/today skip-sync` |
| `skip-fundamentals` | off | Skip Phase 2.5, no fundamental data collection | `/today skip-fundamentals` |
| `skip-discover` | off | Skip Phase 3, no hot stock discovery | `/today skip-discover` |
| `skip-screener` | off | Skip Phase 3.5, no multi-factor screening | `/today skip-screener` |
| `skip-news` | off | Skip Phase 4.5a, no market news context | `/today skip-news` |
| `skip-sentiment` | off | Skip Phase 4.5b, no sentiment scoring | `/today skip-sentiment` |
| `skip-regime` | off | Skip Phase 4.2, no market regime diagnosis | `/today skip-regime` |
| `skip-top-risk` | off | Skip Phase 4.3, no market top risk overlay | `/today skip-top-risk` |
| `skip-market-env` | off | Skip Phase 4.6, no global market environment context | `/today skip-market-env` |
| `skip-agent-desk` | off | Skip Phase 4.8, no multi-agent debate analysis | `/today skip-agent-desk` |
| `skip-edge` | off | Skip Phase 5.1, no edge candidate discovery | `/today skip-edge` |
| `skip-dq` | off | Skip Phase 5a-DQ, no data quality check | `/today skip-dq` |
| `skip-docx` | off | Skip Step 5b `.docx` generation | `/today skip-docx` |
| `skip-quality-gate` | off | Skip Step 5b½ (`ai-quality-evaluator`) | `/today skip-quality-gate` |
| `skip-report` | off | Stop after Phase 3 (Phases 1+2+3); no 3.5 / 4 / 5 / 6 | `/today skip-report` |
| `skip-setup-doctor` | off | Skip Phase 0 | `/today skip-setup-doctor` |
| `skip-decisions` | off | Skip Step 5d (`decision-router`) | `/today skip-decisions` |
| `skip-toss` | off | Skip Phase 1.5 (snapshot) and Phase 5.5 (signal bridge + risk) | `/today skip-toss` |
| `skip-twitter` | off | Skip Phase 6 | `/today skip-twitter` |
| `skip-kb` | off | Skip Phase 7, no KB ingest | `/today skip-kb` |
| `skip-kb-compile` | off | Skip Phase 7b incremental compile | `/today skip-kb-compile` |
| `twitter-only` | off | Phase 6 only | `/today twitter-only` |
| `--with-tradingview` | off | Enable TradingView MCP cross-validation (Phases TV-SC + TV-TA) | `/today --with-tradingview` |
| `--with-pine` | off | Enable Pine Script v5 generation (Phase PS) | `/today --with-pine` |

**Combined flags:** Multiple tokens stack (e.g. `dry-run` + `skip-twitter`). Example: `/today dry-run skip-twitter` — full analysis and `.docx`, no Slack, no Twitter phase.

**Sync-only preset:** After Phases 1 + 2 + 2.5, stop using `skip-discover skip-screener skip-report` (see Natural language triggers).

## Examples

### Example 1: Full daily pipeline (every phase end-to-end)

User says: "Run today's pipeline" or `오늘의 파이프라인 전체 실행해줘`

Actions (execute in order; each depends on the previous completing successfully unless error recovery says otherwise):

0. **Phase 0** — `setup-doctor` core-platform pre-flight (unless `skip-setup-doctor`).
0.5. **Phase 1.5** — `toss-daily-snapshot` archive (unless `skip-toss` or tossctl unavailable).
1. **Phase 1** — DB `--status` + CSV freshness + gap report (halt here if `status`).
2. **Phase 2** — `import_csv` (if needed) + `weekly_stock_update.py --days 3` + verify `--status`.
3. **Phase 2.5** — `financial_data_collector.py --all` + `--status` (unless `skip-fundamentals`).
4. **Phase 3** — `discover_hot_stocks.py` + per-ticker price fetch (unless `skip-discover`).
5. **Phase 3.5** — `stock_screener.py --all --json` → `outputs/screener-{date}.json` (unless `skip-screener`; optional `--no-sentiment` on script).
6. **Phase 4** — `daily_stock_check --source db`.
7. **Phase 4.2–4.6** — Parallel fan-out: market regime (`skip-regime`), top risk (`skip-top-risk`), AlphaEar (`skip-news`/`skip-sentiment`), market environment (`skip-market-env`).
7.5. **Phase 4.8** — `AgentDesk.run()` multi-agent debate on top BUY/SELL tickers (unless `skip-agent-desk`).
8. **Phase 5a** — `alphaear-reporter` clustering and narrative sections.
8.1. **Phase 5.1** — `trading-edge-candidate-agent` anomaly discovery (unless `skip-edge`).
8.2. **Phase 5a-DQ** — `trading-data-quality-checker` validation (unless `skip-dq`; FAIL → halt report).
9. **Phase 5b** — Persist JSON artifacts + `node generate-report.js` (unless `skip-docx`).
10. **Phase 5b½** — `ai-quality-evaluator` loop (unless `skip-quality-gate` or evaluator unavailable → warn and continue).
11. **Phase 5½** — Manual checklist (data consistency, signals, completeness, date) — flag discrepancies in Slack if any fail.
12. **Phase 5c** — Slack main + **mandatory thread** (unless `dry-run`, `skip-slack`, or no MCP).
13. **Phase 5d** — `decision-router` posts (unless `skip-decisions`).
13.5. **Phase 5.5** — `toss-signal-bridge` order previews + `toss-risk-monitor` assessment (unless `skip-toss` or tossctl unavailable).
14. **Phase 6** — `twitter-timeline-to-slack` (unless `skip-twitter` or missing `TWITTER_COOKIE`).

Result: All default phases complete; `.docx` at `outputs/reports/daily-{date}.docx`; analysis/screener/discovery JSON under `outputs/`; `#h-report` main + threaded BUY/SELL detail; optional decisions and Twitter distribution.

### Example 1b: Full pipeline, no Slack, no Twitter

User says: `today dry-run skip-twitter` (or natural-language equivalent with same flags)

Actions: Same as Example 1 through Phase 5d (Slack skipped for 5c because of `dry-run`). **Phase 6 skipped** entirely. `.docx` and local JSON outputs still produced unless `skip-docx`.

Result: Full analysis artifact without public Slack post or Twitter phase.

### Example 2: Check data freshness only

User says: "today status"

Actions:
1. Run `weekly_stock_update.py --status` for DB coverage
2. Scan `data/latest/` CSVs for latest dates
3. Report gap summary

Result: Table showing each ticker's DB date, CSV date, and gap status. No data modification.

### Example 3: Sync data without report

User says: "today skip-report"

Actions:
1. Check data freshness (Phase 1)
2. Import CSVs and fetch from Yahoo Finance (Phase 2)
3. Discover hot stocks (Phase 3)
4. Stop — no analysis or report generated

Result: Database updated with latest available data; hot stocks identified but no Slack message posted.

### Example 4: Pipeline without hot stock discovery

User says: "today skip-discover"

Actions:
1. Check data freshness (Phase 1)
2. Sync data (Phase 2)
3. Skip Phase 3
4. Run analysis (Phase 4)
5. Generate report and post (Phase 5)

Result: Standard pipeline without hot stock discovery section in the report.

### Example 5: Lightweight pipeline — skip all new market intelligence phases

User says: "today skip-regime skip-top-risk skip-market-env skip-edge skip-dq"

Actions:
1. Check data freshness (Phase 1)
2. Sync data (Phase 2)
3. Discover hot stocks (Phase 3)
4. Run stock analysis (Phase 4)
5. Skip Phases 4.2, 4.3, 4.6, 5.1, 5a-DQ
6. Run AlphaEar news + sentiment (Phase 4.5) — still active unless separately skipped
7. Generate report and post (Phase 5) — regime/top-risk/environment/edge sections show "N/A"

Result: Faster pipeline equivalent to the pre-enhancement baseline, useful when market intelligence APIs are down or during weekends/holidays.

### Example 6: Full pipeline with regime and edge, no trading desk debate

User says: "today skip-agent-desk"

Actions:
1. Check data freshness (Phase 1)
2. Sync data (Phase 2)
3. Discover hot stocks (Phase 3)
4. Run stock analysis (Phase 4)
5. Parallel fan-out: market regime (4.2) + top risk (4.3) + AlphaEar (4.5) + market environment (4.6)
6. Skip Phase 4.8 (agent desk)
7. Edge candidate discovery (Phase 5.1)
8. Data quality check (Phase 5a-DQ)
9. Generate report with all market intelligence sections and post (Phase 5)

Result: Complete market intelligence pipeline without the computationally expensive multi-agent debate phase. Report includes regime dashboard, top risk, global market snapshot, and edge candidates.

## Troubleshooting

### No CSV files in data/latest/

Cause: First-time setup or directory cleared.

Solution: Run `stock-csv-downloader` first: `/stock-csv-download --all --import`

### Yahoo Finance returns no data

Cause: Market closed (weekend/holiday) or rate limiting.

Solution: Check if yesterday was a trading day. If rate limited, retry with `--delay 2`. For persistent issues, use `stock-csv-downloader` as fallback.

### Slack channel not found

Cause: `#h-report` channel doesn't exist or Slack MCP not connected.

Solution: Create the channel in Slack, then verify MCP connection via `slack_search_channels` with query `h-report`.

### Hot stock discovery returns empty results

Cause: pykrx not installed, market closed, or Wikipedia table format changed.

Solution: Install pykrx (`pip install pykrx`). If Wikipedia parsing fails, the script logs a warning and skips NASDAQ 100. For Korean indices, check that pykrx can reach the KRX API. Use `--index nasdaq` or `--index kospi` to test individual indices.

### DB connection failure

Cause: PostgreSQL not running or `DATABASE_URL` misconfigured.

Solution: Check `docker compose up -d db` or verify `DATABASE_URL` in `.env`.

## Tab Automation Pipeline (API-Driven)

The `today` skill also drives a fully automated pipeline via the `PipelineOrchestrator` backend service. Each stage maps to one of the 12 tab automation skills. The orchestrator handles dependency ordering, retries, and parallel execution.

### Dependency Graph

```
Phase 1 — Data Collection (parallel):
  tab-stock-sync        → POST /stock-prices/fetch-latest
  tab-event-detect      → POST /events/detect
  tab-fundamental-sync  → POST /financial-statements/sync
  tab-hot-stock-discovery → POST /admin/discover-hot-stocks

Phase 2 — Computation (depends on data_sync):
  tab-technical-analysis → POST /technical-analysis/batch-compute
  tab-turtle-refresh     → POST /turtle/indicators/daily-refresh
  tab-bollinger-refresh  → POST /bollinger-bands/daily-refresh
  tab-dualma-refresh     → scripts/daily_stock_check.py --source db
  tab-screening          → POST /admin/screen-stocks (depends on fundamental_sync too)
  tab-market-breadth     → POST /market-breadth/refresh
  tab-sentiment          → POST /sentiment/batch-analyze (depends on news_fetch)
  tab-dualma-backtest    → POST /dualma/backtest (depends on dualma_refresh + hot_stock_discovery)

Phase 3 — Analysis (depends on computation):
  tab-ai-news-corr       → AI model news correlation (depends on event_detection + data_sync)
  tab-analysis-run       → POST /analysis/run + POST /reports/generate + GET /patterns
  tab-llm-agents         → POST /llm-agents/run + POST /llm-agents/macro/refresh
  tab-genai-features     → POST /genai-features/generate

Phase 4 — Strategy + Reporting (depends on analysis):
  strategy_engine        → scripts/daily_strategy_engine.py (7 strategies, backtest, top 10 cards)
  report_generation      → Template-based multi-format reports (MD, DOCX, PPTX, XLSX via build_spec + renderers)
  pattern_refresh        → GET /patterns
  slack_notification     → Slack #h-report posting (Jinja2 templates + strategy cards thread)
```

### Strategy Engine Stage

The `strategy_engine` stage runs `scripts/daily_strategy_engine.py` which:
1. Reads all tracked tickers from the DB
2. Detects signals across 7 strategies (Turtle Breakout, Golden Cross, Bollinger Squeeze, RSI Reversal, MACD Cross, Momentum Burst, Overnight Dip-Buy)
3. Backtests each signal against 60 days of historical data with commission modeling
4. Ranks by risk-adjusted return (Sharpe ratio)
5. Outputs the top 10 strategy cards to `outputs/strategy-cards-{date}.json`

Each strategy card contains: ticker, strategy name, signal direction (BUY/SELL/HOLD), entry/exit prices, stop-loss, risk:reward ratio, backtest win rate, and a `toss_cmd` field for Toss Securities execution.

### Report Generation Stage (Template-Based)

The `report_generation` stage generates reports in 4 formats using the template system in `scripts/report_templates/`:

1. **build_spec.py** reads daily JSON outputs (analysis, screener, strategy-cards, etc.) into a unified `report_spec` dict
2. **render_md.py** renders a Markdown report via `templates/daily-report.md.j2` (Jinja2)
3. **render_docx.py** populates `templates/daily-report.docx` with data (python-docx)
4. **render_pptx.py** populates `templates/daily-slides.pptx` with data (python-pptx)
5. **render_xlsx.py** populates `templates/stock-tracker.xlsx` with per-ticker data (openpyxl)

All renderers handle `None`/missing data gracefully. Each has a fallback path — if templates fail, legacy `generate_daily_report.py` produces a minimal Markdown report.

Outputs: `outputs/reports/daily-{date}.md`, `.docx`, `.pptx`, `stock-tracker-{date}.xlsx`

### Slack Notification Stage (Template-Based)

The `slack_notification` stage posts to Slack using Jinja2 templates:
1. `render_slack.py` reads the `report_spec` and renders `templates/slack-main.txt.j2`, `slack-thread.txt.j2`, `slack-strategy.txt.j2`
2. Falls back to legacy `generate_daily_report` functions if templates unavailable
3. Posts main message + BUY/SELL thread + strategy cards thread to `#h-report`

### Running the Full Pipeline via API

```bash
curl -X POST http://localhost:4567/api/v1/pipeline/run-daily
```

This triggers `PipelineOrchestrator.run()` which executes all 20 stages with proper dependency ordering and retry logic.

### Running Individual Tab Skills

Each tab skill can be run independently via its trigger command (see Phase 6 commands):
- `/tab-stock-sync` — sync stock prices only
- `/tab-event-detect` — detect events only
- `/tab-screening` — run stock screener only
- etc.

## Integration

- **Pipeline Orchestrator**: `backend/app/services/pipeline_orchestrator.py` (20-stage DAG with retries)
- **DB status script**: `backend/scripts/weekly_stock_update.py`
- **CSV import script**: `backend/scripts/import_csv.py`
- **Fundamental data collector**: `backend/scripts/financial_data_collector.py` (yfinance → financial_statements table)
- **Stock screener**: `backend/scripts/stock_screener.py` (multi-factor screening + AI sentiment)
- **Discovery script**: `backend/scripts/discover_hot_stocks.py`
- **Analysis script**: `backend/scripts/daily_stock_check.py` (Turtle + Bollinger + Oscillators)
- **Indicator engine**: `backend/app/services/technical_indicator_service.py` (RSI, MACD, Stochastic, ADX, etc.)
- **Volume metrics**: `backend/app/services/llm_agents/data/financial_data_service.py` (RVOL, OBV, Volume SMA)
- **Report workflow**: `alphaear-reporter` skill (Cluster → Write → Assemble)
- **Template system**: `scripts/report_templates/` (build_spec, render_md, render_docx, render_pptx, render_xlsx)
- **Template files**: `templates/daily-report.docx`, `templates/daily-slides.pptx`, `templates/stock-tracker.xlsx`, `templates/daily-report.md.j2`, `templates/slack-*.txt.j2`
- **Report outputs**: `outputs/reports/daily-{date}.md`, `.docx`, `.pptx`, `stock-tracker-{date}.xlsx`
- **DOCX generation (legacy)**: `anthropic-docx` skill — fallback when template renderer fails
- **Report prompt**: `.cursor/skills/pipeline/today/references/report-prompt.md`
- **Analysis output**: `outputs/analysis-{date}.json`
- **Screener output**: `outputs/screener-{date}.json`
- **Discovery output**: `outputs/discovery-{date}.json`
- **News output**: `outputs/news-{date}.json` (optional, from alphaear-news)
- **Data directory**: `data/latest/`
- **DB models**: `backend/app/models/stock_price.py` (`Ticker`, `StockPrice`), `backend/app/models/llm_agents/models.py` (`FinancialStatement`)
- **Tracked tickers**: `backend/app/core/constants.py` (`DEFAULT_STOCKS`, `TICKER_CATEGORY_MAP`)
- **Strategy engine**: `scripts/daily_strategy_engine.py` (7 strategies, backtest, top-10 card output)
- **Strategy cards output**: `outputs/strategy-cards-{date}.json`
- **Pipeline runner**: `scripts/today_pipeline_runner.py` (`--dry-run` supported)
- **Makefile targets**: `make run-today` (full pipeline), `make run-today-dry` (dry-run)
- **Slack channel**: `#h-report` (optional for Cursor; native posting in API pipeline)
- **Slack decision channel**: `#효정-의사결정` (`C0ANBST3KDE`) — personal trading decisions (Step 5d)
- **Agent desk**: `backend/app/services/agent_desk/desk.py` (`AgentDesk`) — multi-agent debate pipeline (Phase 4.8)
- **Agent desk output**: `outputs/agent-desk/{date}/desk-decisions.json`
- **Related skills**: `weekly-stock-update`, `daily-stock-check`, `stock-csv-downloader`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, `alphaear-sentiment`, `setup-doctor`, `twitter-timeline-to-slack`, `x-to-slack`, `decision-router`, `trading-agent-desk`, `toss-ops-orchestrator` (delegates to 8 toss-* skills), `alphaear-orchestrator` (delegates to 8 alphaear-* skills)
- **Tab skills**: `tab-stock-sync`, `tab-event-detect`, `tab-fundamental-sync`, `tab-hot-stock-discovery`, `tab-technical-analysis`, `tab-turtle-refresh`, `tab-bollinger-refresh`, `tab-dualma-refresh`, `tab-screening`, `tab-llm-agents`, `tab-genai-features`, `tab-analysis-run`
- **GitHub Actions**: `.github/workflows/daily-today.yml` (independent pipeline, uses its own API keys via GitHub Secrets)

## Coordinator Synthesis

When delegating to subagents:

- **Never use lazy delegation.** Provide specific inputs (file paths, data, context) to every subagent — not "based on your findings, do X."
- **Purpose statement required:** Every subagent prompt must include why the task matters and how its output is used downstream — e.g., "This work feeds the daily Korean DOCX report and Slack #h-report; downstream steps must read artifacts under `outputs/today/{date}/` (and legacy `outputs/analysis-{date}.json` / `outputs/screener-{date}.json` where applicable), not chat memory."
- **Continue vs Spawn decision:**
  - Continue (resume) when worker context overlaps with the next task or fixing a previous failure
  - Spawn fresh when verifying another worker's output or when previous approach was fundamentally wrong
- Use `model: "fast"` for exploration/read-only subagents; default model for generation/analysis

## Honest Reporting

- Report phase outcomes faithfully: if a phase fails, say so with the error output
- Never claim "pipeline complete" when phases were skipped or failed
- Never suppress failing phases to manufacture a green summary
- When a phase succeeds, state it plainly without unnecessary hedging
- The Slack summary must accurately reflect what happened — not what was hoped

## Subagent Contract

Subagent prompts must include:
- Always use absolute file paths (subagent cwd may differ)
- Return `{ status, file, summary }` for orchestrator context efficiency
- Include code snippets only when exact text is load-bearing
- Do not recap files merely read — summarize findings
- Final response: concise report of what was done, key findings, files changed
- Do not use emojis

## Appendix: Skill Utilization Tiers (2026-04-05 Audit)

Full classification at `docs/skill-utilization-audit/tier-classification.md`.

### Tier A — Pipeline-Core (30 skills, already wired)

Every daily run exercises these through `PHASE_REGISTRY` in `scripts/today_pipeline_runner.py`:

- **Data**: `weekly-stock-update`, `tab-stock-sync`, `tab-fundamental-sync`
- **Discovery + Screening**: `tab-hot-stock-discovery`, `tab-screening`, `daily-stock-check`
- **Technical Analysis**: `tab-technical-analysis`, `tab-turtle-refresh`, `tab-bollinger-refresh`, `tab-dualma-refresh`
- **Market Context**: `tab-market-breadth`, `trading-market-breadth-analyzer`, `tab-news-fetch`, `alphaear-news`, `alphaear-sentiment`, `trading-market-news-analyst`, `tab-market-environment`, `trading-market-environment-analysis`
- **Deep Analysis**: `tab-analysis-run`, `tab-llm-agents`, `tab-genai-features`, `trading-agent-desk`, `trading-data-quality-checker`
- **Backtesting**: `tab-strategy-comparison`, `trading-backtest-expert`
- **Reporting**: Template renderers (`render_md`, `render_docx`, `render_pptx`, `render_xlsx`), `alphaear-reporter`, `tab-patterns`, `tab-report-generate`, `ai-quality-evaluator`

### Tier B — Pipeline-Ready (18 skills, integration candidates)

**Toss integration (9 skills)** — gated on `tossctl` availability, addressed in Phase 6:
`toss-daily-snapshot`, `toss-ops-orchestrator`, `toss-morning-briefing`, `toss-risk-monitor`, `toss-signal-bridge`, `toss-portfolio-recon`, `toss-fx-monitor`, `toss-watchlist-sync`, `toss-trade-journal`

**Future pipeline enrichment (9 skills)**:
- `trading-intel-orchestrator` → unified market intelligence (replace parallel fan-out)
- `alphaear-orchestrator` → already documented in Phase 4.5
- `alphaear-deepear-lite` → comprehensive mode on high-signal days
- `trading-uptrend-analyzer` → breadth enrichment for Phase 4.2
- `trading-edge-candidate-agent` → edge candidate generation for Phase 5.1
- `tab-dashboard-summary` → consolidated Slack dashboard for Phase 6
- `tab-event-detect` → RSS event detection for Phase 4.5+
- `trading-scenario-analyzer` → event-driven scenario analysis
- `alphaear-signal-tracker` → signal evolution tracking

### Tier C/D — On-Demand and Standalone (35 skills)

Not candidates for daily pipeline integration. Available for manual invocation:
- Tier C (21): ad-hoc analysis tools (options, FinViz, predictor, position sizer, etc.)
- Tier D (14): broker-specific (KIS), simulation (MiroFish), experimental

### Utilization Tracker

Run `python scripts/skill_utilization_tracker.py --days 14` to generate utilization reports:
- JSON: `outputs/skill-utilization/utilization-{date}.json`
- Markdown: `outputs/skill-utilization/utilization-{date}.md`
