---
name: today
description: >-
  Run the daily data sync, hot stock discovery, multi-indicator analysis, and
  report pipeline — check DB vs CSV freshness gaps, backfill missing data from
  Yahoo Finance, discover the hottest untracked stocks from NASDAQ 100/KOSPI 100/
  KOSDAQ 100, run Turtle/Bollinger/Oscillator analysis (SMA 20/55/200, MA alignment,
  golden/death cross, RSI, MACD, Stochastic, ADX), optionally fetch market news
  context (alphaear-news) and sentiment scores (alphaear-sentiment), generate a
  Korean expert .docx report with per-stock buy/sell recommendations (via
  anthropic-docx), and optionally post a summary to Slack #h-report.
  Use when the user asks to run a daily pipeline, sync stock data, check data
  freshness, discover hot stocks, or generate a daily report.
  Do NOT use for weekly price updates only (use weekly-stock-update). Do NOT use
  for stock analysis without data sync (use daily-stock-check). Do NOT use for
  CSV downloads from investing.com (use stock-csv-downloader).
metadata:
  author: thaki
  version: "5.0.0"
  category: execution
---

# Today — Daily Data Sync and Report Pipeline

Orchestrates a multi-phase pipeline: data freshness check, data sync, hot stock discovery, technical analysis (SMA 20/55/200, Bollinger Bands, RSI/MACD/Stochastic/ADX oscillators), optional market context (alphaear-news + alphaear-sentiment), and Korean expert report generation (.docx + optional Slack). Generates per-stock buy/sell recommendations using 3-way signal combination (Turtle + Bollinger + Oscillator) with MA alignment, golden/death cross, Bollinger %B, RSI zones, and MACD cross analysis. Reuses `weekly-stock-update`, `daily-stock-check`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, and `alphaear-sentiment` skills internally. No API keys are required for Cursor-side execution.

## Prerequisites

- PostgreSQL running and migrated (`alembic upgrade head`)
- Stock CSV files exist in `data/latest/` (seed via `stock-csv-downloader` if empty)
- Python 3.11+ with backend dependencies installed
- Node.js with `docx` package installed locally (`cd outputs && npm install`) — for .docx report generation
- (Optional) Slack MCP server connected — only needed for posting to `#h-report`
- (Optional) `anthropic-docx` skill available — for .docx report generation; skip with `skip-docx`

> **Note**: No API keys (Claude, Slack, etc.) are required. API keys are only needed by the separate GitHub Actions pipeline.

## Workflow

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

### Phase 4.5: Market Context (Optional)

Fetch market news and sentiment to add qualitative context. Skip with `skip-news` and/or `skip-sentiment`.

**Step 4.5a — Market news (skip if `skip-news`):**

Use the `alphaear-news` skill to fetch latest financial news from multiple sources. Filter for news relevant to tracked tickers and categories. Save top 3-5 headlines as `outputs/news-{date}.json`. If the skill fails or times out, the pipeline continues — the report gracefully handles missing news data.

**Step 4.5b — Sentiment scoring (skip if `skip-sentiment`):**

Use the `alphaear-sentiment` skill to score news sentiment for stocks with BUY or SELL signals. Add sentiment score (-1.0 to 1.0) and summary to the analysis JSON. If the skill fails, the report shows "N/A" for sentiment.

### Phase 5: Report and Post

**Step 5a — Generate report content:**

Use the `alphaear-reporter` skill workflow with the daily-stock-check JSON as input signals:

1. **Cluster Signals**: Group the stock signals into 3–5 themes (e.g., "Tech momentum", "KRX recovery", "Defensive positions")
2. **Write Sections**: For each theme, write analysis covering signal rationale, price context, and risk factors
3. **Final Assembly**: Compile into a report with these sections:
   - Date and Market Overview
   - Signal Summary (BUY/NEUTRAL/SELL counts)
   - Theme Analysis (from clustered signals)
   - Top Movers (strongest BUY and SELL signals with rationale)
   - Risk Notes and Disclaimer

**Step 5b — Generate Korean .docx report (skip if `skip-docx` flag is set):**

1. Save analysis JSON to `outputs/analysis-{date}.json` and discovery JSON to `outputs/discovery-{date}.json`
2. Run the report generator:

```bash
cd outputs
node generate-report.js {date}
```

The generator also reads `outputs/news-{date}.json` for market context (if available).
It produces a Korean expert report (`outputs/reports/daily-{date}.docx`) with:
   - 표지 (제목, 날짜, 분석 종목 수)
   - 요약 (시그널 분포표, 정배열 종목 수, 스퀴즈 종목, 골든/데스크로스, RSI 과매수/과매도, MACD 크로스)
   - 시장 동향 (alphaear-news 뉴스 헤드라인, if available)
   - 카테고리별 요약표
   - 주요 종목 상세 분석 (BUY/SELL 종목별 이동평균선·볼린저·오실레이터 분석 + 감성 점수 + 매매 판단 근거)
   - 전체 종목 시그널 일람표 (터틀/볼린저/오실레이터/종합 4열)
   - 핫 종목 (미추적 종목 발견 결과)
   - 기술적 지표 상세표 (이동평균선, 볼린저, 오실레이터 3개 테이블)
   - 리스크 노트 및 면책 조항

**Step 5c — Post to Slack (optional, skip if `dry-run` or `skip-slack`):**

1. Use `slack_search_channels` MCP tool to find `#h-report` channel ID
2. If the report exceeds 4000 characters, split into a thread:
   - Main message: Date + Signal Summary + Top Movers
   - Thread reply: Full theme analysis and risk notes
3. Use `slack_send_message` MCP tool to post

**Slack message template:**

```
:newspaper: *일간 분석 보고서 — {date}*
{total_stocks}개 종목 분석 | :green_circle: 매수 {buy_count} | :white_circle: 중립 {neutral_count} | :red_circle: 매도 {sell_count}

---

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

## CLI Arguments

| Argument | Description | Example |
|---|---|---|
| (none) | Run full pipeline | `/today` |
| `status` | Phase 1 only — show data freshness report | `/today status` |
| `dry-run` | Run all phases but skip Slack posting (still generates .docx) | `/today dry-run` |
| `skip-sync` | Skip Phase 2, run analysis on existing data | `/today skip-sync` |
| `skip-discover` | Skip Phase 3, no hot stock discovery | `/today skip-discover` |
| `skip-news` | Skip Phase 4.5a, no market news context | `/today skip-news` |
| `skip-sentiment` | Skip Phase 4.5b, no sentiment scoring | `/today skip-sentiment` |
| `skip-docx` | Skip .docx report generation (Step 5b) | `/today skip-docx` |
| `skip-report` | Run Phase 1+2+3 only, no analysis or report | `/today skip-report` |

## Examples

### Example 1: Full daily pipeline

User says: "Run today's pipeline"

Actions:
1. Check DB status and CSV freshness (Phase 1)
2. Import CSV gaps and fetch from Yahoo Finance (Phase 2)
3. Discover hottest untracked stocks from NASDAQ 100, KOSPI 100, KOSDAQ 100 (Phase 3)
4. Run Turtle + Bollinger + Oscillator analysis (Phase 4)
5. Fetch market news context and sentiment scores (Phase 4.5)
6. Generate themed report content, produce .docx file, and post summary to `#h-report` (Phase 5)

Result: Data synced, hot stocks discovered, multi-indicator analysis complete, .docx report saved to `outputs/reports/daily-{date}.docx`, summary posted to Slack.

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

## Integration

- **DB status script**: `backend/scripts/weekly_stock_update.py`
- **CSV import script**: `backend/scripts/import_csv.py`
- **Discovery script**: `backend/scripts/discover_hot_stocks.py`
- **Analysis script**: `backend/scripts/daily_stock_check.py` (Turtle + Bollinger + Oscillators)
- **Indicator engine**: `backend/app/services/technical_indicator_service.py` (RSI, MACD, Stochastic, ADX, etc.)
- **Report workflow**: `alphaear-reporter` skill (Cluster → Write → Assemble)
- **DOCX generation**: `anthropic-docx` skill (docx-js, tables, formatting)
- **Report generator**: `outputs/generate-report.js`
- **Report prompt**: `.cursor/skills/today/references/report-prompt.md`
- **Report output**: `outputs/reports/daily-{date}.docx`
- **Analysis output**: `outputs/analysis-{date}.json`
- **Discovery output**: `outputs/discovery-{date}.json`
- **News output**: `outputs/news-{date}.json` (optional, from alphaear-news)
- **Data directory**: `data/latest/`
- **DB models**: `backend/app/models/stock_price.py` (`Ticker`, `StockPrice`)
- **Tracked tickers**: `backend/app/core/constants.py` (`DEFAULT_STOCKS`, `TICKER_CATEGORY_MAP`)
- **Slack channel**: `#h-report` (optional)
- **Related skills**: `weekly-stock-update`, `daily-stock-check`, `stock-csv-downloader`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, `alphaear-sentiment`
- **GitHub Actions**: `.github/workflows/daily-today.yml` (independent pipeline, uses its own API keys via GitHub Secrets)
