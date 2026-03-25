---
name: today
description: >-
  Run the daily data sync, fundamental collection, hot stock discovery,
  multi-factor screening, Turtle/Bollinger/Oscillator analysis, and Korean .docx
  report pipeline — check DB vs CSV freshness, backfill from Yahoo Finance,
  discover hot stocks from NASDAQ/KOSPI/KOSDAQ 100, screen (P/E, RSI, volume,
  MA crossovers, FCF yield), run SMA 20/55/200 + RSI/MACD/Stochastic/ADX,
  optionally fetch news (alphaear-news) and sentiment (alphaear-sentiment),
  generate buy/sell report via anthropic-docx, post to Slack #h-report,
  optionally run setup-doctor pre-flight and twitter-timeline-to-slack post-pipeline.
  Use when the user asks to run a daily pipeline, sync stock data, discover hot
  stocks, screen stocks, or generate a daily report.
  Do NOT use for weekly price updates only (use weekly-stock-update). Do NOT use
  for stock analysis without data sync (use daily-stock-check). Do NOT use for
  CSV downloads from investing.com (use stock-csv-downloader).
metadata:
  author: thaki
  version: "7.0.0"
  category: execution
---

# Today — Daily Data Sync, Screening, and Report Pipeline

Orchestrates a multi-phase pipeline: optional setup-doctor pre-flight, data freshness check, data sync, fundamental data collection (financial statements from yfinance), hot stock discovery, multi-factor stock screening (P/E, RSI, volume spikes, MA crossovers, earnings proximity, FCF yield, AI sentiment), technical analysis (SMA 20/55/200, Bollinger Bands, RSI/MACD/Stochastic/ADX oscillators), optional market context (alphaear-news + alphaear-sentiment), Korean expert report generation (.docx + optional Slack), and optional twitter-timeline-to-slack post-pipeline. Generates per-stock buy/sell recommendations using 3-way signal combination (Turtle + Bollinger + Oscillator) enhanced with fundamental screening scores and AI sentiment. Reuses `weekly-stock-update`, `daily-stock-check`, `financial-data-collector`, `stock-screener`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, `alphaear-sentiment`, `setup-doctor`, and `twitter-timeline-to-slack` skills internally. No API keys are required for Cursor-side execution.

## Prerequisites

- PostgreSQL running and migrated (`alembic upgrade head`)
- Stock CSV files exist in `data/latest/` (seed via `stock-csv-downloader` if empty)
- Python 3.11+ with backend dependencies installed
- Node.js with `docx` package installed locally (`cd outputs && npm install`) — for .docx report generation
- (Optional) Slack MCP server connected — only needed for posting to `#h-report`
- (Optional) `anthropic-docx` skill available — for .docx report generation; skip with `skip-docx`

> **Note**: No API keys (Claude, Slack, etc.) are required. API keys are only needed by the separate GitHub Actions pipeline.

## Workflow

### Natural language triggers

Map common utterances to flags and phase scope before executing. Do not skip dependency order.

| User intent (examples) | Execution |
| --- | --- |
| Full daily pipeline (`오늘의 파이프라인 전체 실행해줘`, `Run today's pipeline`) | Phases **0→6** with default flags (no `dry-run`). Run fundamentals (2.5), screener (3.5), news/sentiment (4.5), full report + Slack + quality gate + decisions unless user opts out. |
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

### Phase 1.5: Toss Daily Snapshot (Optional)

Archive the current Toss Securities account state for historical tracking. Skip with `skip-toss`.

**Step 1.5a — Check tossctl auth:**

```bash
tossctl auth status --output json
```

If session is active, proceed. If expired or `tossctl` not installed, skip Phase 1.5 and log a warning.

**Step 1.5b — Run snapshot:**

Follow the `toss-daily-snapshot` skill (`.cursor/skills/toss-daily-snapshot/SKILL.md`):

1. `tossctl account summary --output json` → save to `outputs/toss/summary-{date}.json`
2. `tossctl portfolio positions --output json` → save to `outputs/toss/positions-{date}.json`
3. `tossctl watchlist list --output json` → save to `outputs/toss/watchlist-{date}.json`

On failure: **Continue** — Toss snapshot is optional; the pipeline proceeds without it.

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

### Phase 5: Report and Post

**Step 5a — Generate report content (반드시 한국어로 작성):**

Use the `alphaear-reporter` skill workflow with the daily-stock-check JSON as input signals.
**모든 리포트 텍스트, 섹션 제목, 분석 내용, 요약은 반드시 한국어로 작성한다.** 종목 코드(ticker)와 고유명사(회사명 영문)만 영어를 허용한다.

1. **시그널 클러스터링**: 종목 시그널을 3–5개 테마로 그룹핑 (예: "기술주 모멘텀", "KRX 반등", "방어주 포지션")
2. **섹션 작성**: 각 테마별로 시그널 근거, 가격 맥락, 리스크 요인을 분석
3. **최종 조립**: 다음 섹션으로 리포트를 구성:
   - 날짜 및 시장 개요
   - 시그널 요약 (매수/중립/매도 종목 수)
   - 테마별 분석 (클러스터링된 시그널 기반)
   - 주요 종목 (가장 강한 매수/매도 시그널과 근거)
   - 리스크 노트 및 면책 조항

**Step 5b — Generate Korean .docx report (skip if `skip-docx` flag is set):**

1. Save analysis JSON to `outputs/analysis-{date}.json`, screener JSON to `outputs/screener-{date}.json`, and discovery JSON to `outputs/discovery-{date}.json`
2. Run the report generator:

```bash
cd outputs
node generate-report.js {date}
```

The generator also reads `outputs/news-{date}.json` for market context and `outputs/screener-{date}.json` for screening results (if available).
It produces a Korean expert report (`outputs/reports/daily-{date}.docx`) with:
   - 표지 (제목, 날짜, 분석 종목 수)
   - 요약 (시그널 분포표, 정배열 종목 수, 스퀴즈 종목, 골든/데스크로스, RSI 과매수/과매도, MACD 크로스)
   - 시장 동향 (alphaear-news 뉴스 헤드라인, if available)
   - **스크리너 결과** (STRONG BUY/BUY 종목 요약, composite score, 필터 통과 현황)
   - **펀더멘탈 스냅샷** (종목별 P/E, FCF Yield, ROE, Debt/Equity, Revenue Growth)
   - **거래량 분석** (RVOL, Volume Spike, OBV 추세)
   - 카테고리별 요약표
   - 주요 종목 상세 분석 (BUY/SELL 종목별 이동평균선·볼린저·오실레이터 분석 + 감성 점수 + 펀더멘탈 메트릭스 + 매매 판단 근거)
   - 전체 종목 시그널 일람표 (터틀/볼린저/오실레이터/스크리너/종합 5열)
   - **어닝 캘린더** (14일 내 실적 발표 예정 종목)
   - 핫 종목 (미추적 종목 발견 결과)
   - 기술적 지표 상세표 (이동평균선, 볼린저, 오실레이터 3개 테이블)
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

**Step 5c — Post to Slack (optional, skip if `dry-run` or `skip-slack`):**

1. Use `slack_search_channels` MCP tool to find `#h-report` channel ID (known: `C0AKHQWJBLZ`)
2. Post the **main message** with date, signal summary, top movers, hot stocks, and screener summary
3. Capture the `message_ts` from the response
4. **ALWAYS post a thread reply** using `thread_ts` = the main message's `message_ts`, containing:
   - `:mag: BUY 종목 상세 ({N}종목)` — grouped by category (한국 방산/전력/반도체, 미국 인프라/방산, 기타 등), each stock with name, price, change%, RSI, ADX (with 강한추세 label), and any warnings (과매수/과매도)
   - `:mag: SELL 종목 상세 ({N}종목)` — each stock with name, price, change%, RSI, RSI zone, MA alignment, ADX, Stochastic
   - `:warning:` notes for RSI extremes (과매수 80+, 과매도 30-)
   - `:bulb:` actionable insight for notable patterns (과매도 반등 가능, 과매수 조정 가능 등)

**Slack main message template:**

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

### Phase 5.5: Toss Signal Bridge + Risk Monitor (Optional)

Translate pipeline signals into tossctl order previews and run portfolio risk assessment. Skip with `skip-toss`.

**Step 5.5a — Signal Bridge (skip if no tossctl or `skip-toss`):**

Follow the `toss-signal-bridge` skill (`.cursor/skills/toss-signal-bridge/SKILL.md`):

1. Load today's `outputs/screener-{date}.json` and `outputs/analysis-{date}.json`
2. Filter to symbols tradeable on Toss Securities
3. Fetch current quotes via `tossctl quote get`
4. Check existing exposure via `tossctl portfolio positions --output json`
5. Apply position sizing logic with account buying power
6. Generate order previews (dry-run only — no execution)
7. Present ranked trade candidates in Korean

**Step 5.5b — Risk Monitor (skip if no tossctl or `skip-toss`):**

Follow the `toss-risk-monitor` skill (`.cursor/skills/toss-risk-monitor/SKILL.md`):

1. Run 6-dimension risk assessment (concentration, sector, buying power, drawdown, correlation, profit factor)
2. Generate composite risk scorecard (GREEN/YELLOW/RED)
3. If any RED conditions → auto-post alert to `#h-daily-stock-check`

**Step 5.5c — Include in Slack thread (if Phase 5c runs):**

Add a "Toss 실행 가능 시그널" section to the Slack thread reply containing:
- Top 3 trade candidates with signal strength and estimated cost
- Portfolio risk status summary
- Note: "실행하려면 tossinvest-trading 스킬을 사용하세요"

On failure: **Continue** — Toss integration is optional; log a warning and proceed.

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
| `skip-agent-desk` | off | Skip Phase 4.8, no multi-agent debate analysis | `/today skip-agent-desk` |
| `skip-docx` | off | Skip Step 5b `.docx` generation | `/today skip-docx` |
| `skip-quality-gate` | off | Skip Step 5b½ (`ai-quality-evaluator`) | `/today skip-quality-gate` |
| `skip-report` | off | Stop after Phase 3 (Phases 1+2+3); no 3.5 / 4 / 5 / 6 | `/today skip-report` |
| `skip-setup-doctor` | off | Skip Phase 0 | `/today skip-setup-doctor` |
| `skip-decisions` | off | Skip Step 5d (`decision-router`) | `/today skip-decisions` |
| `skip-toss` | off | Skip Phase 1.5 (snapshot) and Phase 5.5 (signal bridge + risk) | `/today skip-toss` |
| `skip-twitter` | off | Skip Phase 6 | `/today skip-twitter` |
| `twitter-only` | off | Phase 6 only | `/today twitter-only` |

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
7. **Phase 4.5** — `alphaear-news` + `alphaear-sentiment` (unless `skip-news` / `skip-sentiment`).
7.5. **Phase 4.8** — `AgentDesk.run()` multi-agent debate on top BUY/SELL tickers (unless `skip-agent-desk`).
8. **Phase 5a** — `alphaear-reporter` clustering and narrative sections.
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

Phase 4 — Reporting (depends on analysis):
  report_generation      → POST /reports/generate (depends on ai_news_correlation)
  pattern_refresh        → GET /patterns
  slack_notification     → Slack #h-report posting
```

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
- **DOCX generation**: `anthropic-docx` skill (docx-js, tables, formatting)
- **Report generator**: `outputs/generate-report.js`
- **Report prompt**: `.cursor/skills/today/references/report-prompt.md`
- **Report output**: `outputs/reports/daily-{date}.docx`
- **Analysis output**: `outputs/analysis-{date}.json`
- **Screener output**: `outputs/screener-{date}.json`
- **Discovery output**: `outputs/discovery-{date}.json`
- **News output**: `outputs/news-{date}.json` (optional, from alphaear-news)
- **Data directory**: `data/latest/`
- **DB models**: `backend/app/models/stock_price.py` (`Ticker`, `StockPrice`), `backend/app/models/llm_agents/models.py` (`FinancialStatement`)
- **Tracked tickers**: `backend/app/core/constants.py` (`DEFAULT_STOCKS`, `TICKER_CATEGORY_MAP`)
- **Slack channel**: `#h-report` (optional)
- **Slack decision channel**: `#효정-의사결정` (`C0ANBST3KDE`) — personal trading decisions (Step 5d)
- **Agent desk**: `backend/app/services/agent_desk/desk.py` (`AgentDesk`) — multi-agent debate pipeline (Phase 4.8)
- **Agent desk output**: `outputs/agent-desk/{date}/desk-decisions.json`
- **Related skills**: `weekly-stock-update`, `daily-stock-check`, `stock-csv-downloader`, `alphaear-reporter`, `anthropic-docx`, `alphaear-news`, `alphaear-sentiment`, `setup-doctor`, `twitter-timeline-to-slack`, `x-to-slack`, `decision-router`, `trading-agent-desk`, `toss-daily-snapshot`, `toss-signal-bridge`, `toss-risk-monitor`
- **Tab skills**: `tab-stock-sync`, `tab-event-detect`, `tab-fundamental-sync`, `tab-hot-stock-discovery`, `tab-technical-analysis`, `tab-turtle-refresh`, `tab-bollinger-refresh`, `tab-dualma-refresh`, `tab-screening`, `tab-llm-agents`, `tab-genai-features`, `tab-analysis-run`
- **GitHub Actions**: `.github/workflows/daily-today.yml` (independent pipeline, uses its own API keys via GitHub Secrets)
