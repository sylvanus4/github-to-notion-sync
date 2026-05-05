---
name: daily-stock-check
description: >-
  Analyze stocks from Turtle Trading (MA + Donchian) and Bollinger Bands
  perspectives, then post a buy/sell/neutral summary to Slack. Use when the user
  asks to run a daily stock check, analyze stock signals, or post trading
  analysis to Slack. Do NOT use for downloading historical stock CSVs or
  refreshing price data (use stock-csv-downloader). Do NOT use for updating
  recent stock prices in the database (use weekly-stock-update). Korean
  triggers: "주식", "체크", "분석", "데이터".
metadata:
  version: "1.1.0"
  category: "generation"
  author: "thaki"
---
# Daily Stock Check

Analyze tracked stocks from **CSV files** (`--dir`) or **PostgreSQL** (`--source db`) using Turtle Trading and Bollinger Bands, then post a formatted summary (root message + threaded details) to `#h-daily-stock-check` on Slack.

## Prerequisites

- **CSV mode (`--source csv`, default):** `*.csv` files exist under `--dir` (use `stock-csv-downloader` if missing)
- **DB mode (`--source db`):** PostgreSQL reachable via `DATABASE_URL`; prices loaded for tracked tickers (use `weekly-stock-update` if stale)
- Slack MCP server is connected
- Python 3.11+ available

## Quick Start

```bash
cd backend
python -m scripts.daily_stock_check --dir ../data/latest
```

PostgreSQL (tracked tickers in DB; requires `DATABASE_URL` and synced prices):

```bash
cd backend
python -m scripts.daily_stock_check --source db
```

## Analysis Methodology

### Turtle Trading Perspective

Evaluates trend-following signals using:

| Indicator | Period | Signal Logic |
|-----------|--------|-------------|
| SMA | 20, 50 | Price above = bullish, below = bearish |
| EMA | 20 | Trend direction confirmation |
| Donchian Channel | 20 | Price >= 20-high = BUY breakout, <= 20-low = SELL breakdown |
| ATR | 20 | Volatility context |

Scoring: SMA above = +1, SMA below = -1, Donchian breakout = +2, Donchian breakdown = -2.
- Score >= 3: STRONG_BUY
- Score >= 2: BUY
- Score <= -3: STRONG_SELL
- Score <= -2: SELL
- Otherwise: NEUTRAL

### Bollinger Bands Perspective

Evaluates mean-reversion and breakout signals using:

| Indicator | Params | Signal Logic |
|-----------|--------|-------------|
| Bollinger Bands | (20, 2σ) | Upper/Middle/Lower band levels |
| %B | - | Position within bands (0 = lower, 1 = upper) |
| BandWidth | - | Volatility measure |
| Squeeze | 20-bar low BW | Imminent breakout detection |

Signal rules:
- %B > 1.0 + Squeeze → STRONG_BUY (squeeze breakout up)
- %B > 1.0, no Squeeze → SELL (overextended)
- %B < 0.0 + Squeeze → STRONG_SELL (squeeze breakout down)
- %B < 0.0, no Squeeze → BUY (mean reversion candidate)
- %B 0.0–0.2 or 0.8–1.0 → NEUTRAL (near band edge)
- %B 0.2–0.8 → NEUTRAL (mid-range)

### Overall Signal

Combined score from Turtle + Bollinger signals (STRONG_BUY=+2, BUY=+1, NEUTRAL=0, SELL=-1, STRONG_SELL=-2).

## Script CLI Arguments

| Flag | Description | Default |
|------|-------------|---------|
| `--dir DIR` | Directory containing `*.csv` stock files (CSV mode only) | `data/latest` |
| `--tickers T` | Comma-separated tickers to analyze (empty = all) | *(all tickers)* |
| `--source MODE` | `csv` (read `*.csv` from `--dir`) or `db` (PostgreSQL OHLCV) | `csv` |

Examples:

```bash
# All CSVs under data/latest (default source=csv)
python -m scripts.daily_stock_check --dir ../data/latest

# Subset from CSVs
python -m scripts.daily_stock_check --dir ../data/latest --tickers AAPL,NVDA

# All stocks from DB (weekly-stock-update or equivalent must have populated prices)
python -m scripts.daily_stock_check --source db

# DB subset
python -m scripts.daily_stock_check --source db --tickers AAPL,NVDA
```

## Phase order (dependencies)

Execute strictly in this order. **Do not** call Slack tools until Step 1 completes and Step 1.5 is satisfied (or explicit partial-analysis path below).

1. **Step 1** — Run `daily_stock_check` → JSON on stdout
2. **Step 1.5** — Quality gate on that JSON
3. **Step 2** — Resolve `#h-daily-stock-check` channel ID
4. **Step 3** — Format mrkdwn (summary + threaded detail plan)
5. **Step 4** — Post to Slack (root + thread replies)

## Workflow

### Step 1: Run Analysis Script

```bash
cd backend
python -m scripts.daily_stock_check --dir ../data/latest
```

This outputs JSON with:
- `date`: analysis date
- `total_stocks`: number of stocks analyzed
- `results[]`: per-stock analysis with turtle, bollinger, overall signals
- `summary`: count of each signal type

### Step 1.5: Analysis Quality Gate

Before formatting for Slack, verify the analysis output:
- [ ] Analysis JSON contains `total_stocks >= 1`
- [ ] Each stock result has both Turtle and Bollinger analysis sections
- [ ] Data dates are within the last 3 trading days (skip this check on weekends/holidays)
- [ ] No script errors in stderr output
- [ ] Summary buckets (`strong_buy` + `buy` + `neutral` + `sell` + `strong_sell`) sum to `total_stocks`

**Halt (no Slack post):** If the script exits non-zero, prints an `error` key in JSON, stdout is not valid JSON, or `total_stocks == 0` — stop, report the failure to the user, and recommend prerequisites (refresh CSV/DB data). Do not post to Slack.

**Partial results:** If some requested tickers are missing but `total_stocks >= 1`, continue: include a `[부분 분석]` warning banner in the root Slack message listing missing tickers. See [assets/templates/slack-message.md](assets/templates/slack-message.md).

**Inline-only:** If the user asked for signals only with no Slack post, skip Steps 2–4 after Step 1.5 and return the JSON or a formatted summary in chat.

### Step 2: Find Slack Channel ID

Use `slack_search_channels` MCP tool to find `#h-daily-stock-check`:

```
query: "h-daily-stock-check"
```

If no channel is returned: widen the query, verify Slack MCP auth, then **halt** and tell the user the channel could not be resolved (do not post to an arbitrary channel).

### Step 3: Format for Slack (mrkdwn)

Format the JSON using the templates below. Plan a **root message** (header + summary counts) and **threaded detail** (per-signal sections) so the channel stays scannable.

### Slack message templates

**Root message (channel):** header, signal summary, disclaimer footer.

```
:chart_with_upwards_trend: *Daily Stock Check — {date}*
Analyzed {total_stocks} stocks | :green_circle: BUY {buy_count} | :white_circle: NEUTRAL {neutral_count} | :red_circle: SELL {sell_count}
_{data_source_line}_

_Turtle: SMA(20,50) + Donchian(20) | Bollinger: BB(20,2σ) + %B + Squeeze_
_This is not financial advice._
```

Set `{data_source_line}` to `Data source: CSV (--dir)` or `Data source: PostgreSQL (--source db)` as appropriate.

**Thread reply 1 — BUY / STRONG_BUY** (mrkdwn):

```
:large_green_circle: *BUY / STRONG_BUY*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*
(repeat per ticker)
```

**Thread reply 2 — NEUTRAL:**

```
:white_circle: *NEUTRAL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} | BB: {bb_signal}
```

**Thread reply 3 — SELL / STRONG_SELL:**

```
:red_circle: *SELL / STRONG_SELL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*
```

Formatting rules:
- Post the **root message** first; capture `thread_ts` from the response.
- Post each signal group as a **thread reply** (`thread_ts` = root message) using `scripts/slack_post_message.py --thread-ts`.
- Group stocks by overall signal within each thread block: BUY/STRONG_BUY, then NEUTRAL, then SELL/STRONG_SELL
- For NEUTRAL stocks, use a compact one-line format
- For BUY/SELL stocks, show full rationale details
- Use emoji indicators: :green_circle: for buy, :red_circle: for sell, :white_circle: for neutral
- If a single thread reply would exceed ~3500 characters, split that section into additional thread messages (same `thread_ts`)

### Step 4: Post to Slack

1. `python3 scripts/slack_post_message.py --channel <channel_id> --message "<root mrkdwn>"` — obtain `thread_ts` from stdout JSON.
2. On success, send thread replies with `python3 scripts/slack_post_message.py --channel <channel_id> --thread-ts <ts> --message "<reply mrkdwn>"`.
3. If `slack_post_message.py` fails: retry once after 2–3s; if it still fails, **halt**, surface the error to the user, and do not drop analysis silently.

## Error handling and fallbacks

| Step / call | On failure | Action |
|-------------|------------|--------|
| `python -m scripts.daily_stock_check` | Non-zero exit or stderr error | Halt; show stderr; suggest fixing CSV dir, `--source`, or DB connectivity |
| Script stdout | Invalid JSON or `"error"` key | Halt; propagate message; no Slack |
| Step 1.5 | `total_stocks == 0` | Halt; recommend `stock-csv-downloader` or `weekly-stock-update` |
| `slack_search_channels` | Empty / no match | Halt; verify MCP and channel name |
| `slack_post_message.py` | API error | Retry once; then halt and report |
| DB mode | Connection/query errors (from script) | Halt; verify `DATABASE_URL` and migrations |

## Data Requirements

| Indicator | Minimum Data Points |
|-----------|-------------------|
| SMA(20) | 20 |
| SMA(50) | 50 |
| Bollinger(20) | 20 |
| Donchian(20) | 21 |
| ATR(20) | 20 |

If CSVs have fewer than 20 rows, recommend running `stock-csv-download` first:
```
/stock-csv-download --all --gap-fill-from 2025-11-01
```

## Examples

### Example 1: Full pipeline (CSV → quality gate → Slack root + threads)

User says: "Run today's stock check and post to Slack" (same intent as Korean prompts like *오늘 주식 분석 돌려줘* or *일간 주식 분석*).

Actions (all phases, no skips):

1. `cd backend && python -m scripts.daily_stock_check --dir ../data/latest` (default `--source csv`)
2. Parse JSON; run **Step 1.5** checklist; halt if `total_stocks == 0` or invalid output
3. `slack_search_channels` → resolve `#h-daily-stock-check`
4. Build **root** mrkdwn (header + counts + disclaimer + data source line)
5. `python3 scripts/slack_post_message.py` root → obtain `thread_ts`
6. Post **thread reply** mrkdwn for BUY/STRONG_BUY block, then NEUTRAL, then SELL/STRONG_SELL (split if oversized)

Result: Channel shows summary in the main message; full per-stock detail in threads.

### Example 2: Specific tickers (CSV), optional Slack

User says: *AAPL, NVDA 시그널만 확인해줘* / "Check AAPL and NVDA only"

```bash
cd backend
python -m scripts.daily_stock_check --dir ../data/latest --tickers AAPL,NVDA
```

Actions:
1. Run command above; Step 1.5 on JSON
2. If user did **not** ask for Slack: return formatted summary or raw JSON in chat (**skip Steps 2–4**)
3. If user also wants Slack: continue from Example 1 Step 3 with this JSON

Result: Focused analysis for requested tickers.

### Example 3: Explicit Slack post

User says: *주식 체크 결과 슬랙에 올려줘* / "Post stock check results to Slack"

Actions: Same as Example 1 after Step 1 (always complete Steps 2–4 with threading unless Step 1.5 halts).

### Example 4: DB source (CLI parity)

User says: `daily stock check --source db` or requests analysis from the database.

```bash
cd backend
python -m scripts.daily_stock_check --source db
python -m scripts.daily_stock_check --source db --tickers AAPL,NVDA
```

Actions: Prerequisites (DB + `DATABASE_URL`); then same quality gate and Slack flow as Example 1; root template uses `Data source: PostgreSQL (--source db)`.

### Example 5: Weekend / holiday note

If Step 1.5 date-freshness check is skipped (weekend/holiday), still require valid JSON and `total_stocks >= 1` before Slack; document in thread if data is last session only.

## Troubleshooting

### CSVs missing or insufficient data
Cause: data/latest/ empty or rows fewer than 21 (Donchian needs 21)
Solution: Recommend stock-csv-downloader to fetch/refresh data before running daily check

### Slack channel not found
Cause: Channel name changed or MCP not connected
Solution: Use slack_search_channels with query "h-daily-stock-check"; verify Slack MCP server is enabled

## Integration

Script: `backend/scripts/daily_stock_check.py` | Indicators: `backend/app/services/technical_indicator_service.py` | Data: `data/latest/` | Slack: `#h-daily-stock-check`
