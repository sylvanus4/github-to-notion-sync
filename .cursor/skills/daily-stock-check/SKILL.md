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
  version: "1.0.0"
  category: "generation"
  author: "thaki"
---
# Daily Stock Check

Analyze all stocks in `data/latest/` using Turtle Trading and Bollinger Bands methodologies, then post a formatted summary to `#h-daily-stock-check` on Slack.

## Prerequisites

- Stock CSV files exist in `data/latest/` (download using `stock-csv-downloader` skill if missing)
- Slack MCP server is connected
- Python 3.11+ available

## Quick Start

```bash
cd backend
python -m scripts.daily_stock_check --dir ../data/latest
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

```
--dir DIR      CSV directory (default: data/latest)
--tickers T    Comma-separated tickers to filter (default: all)
```

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

### Step 2: Find Slack Channel ID

Use `slack_search_channels` MCP tool to find `#h-daily-stock-check`:

```
query: "h-daily-stock-check"
```

### Step 3: Format and Post to Slack

Format the JSON output as a Slack mrkdwn message. Use the template below.

### Slack Message Template

```
:chart_with_upwards_trend: *Daily Stock Check — {date}*
Analyzed {total_stocks} stocks | :green_circle: BUY {buy_count} | :white_circle: NEUTRAL {neutral_count} | :red_circle: SELL {sell_count}

---

:large_green_circle: *BUY / STRONG_BUY*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*

---

:white_circle: *NEUTRAL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} | BB: {bb_signal}

---

:red_circle: *SELL / STRONG_SELL*

> *{ticker}* `{price}` ({change_pct}%)
> Turtle: {turtle_signal} — {turtle_rationale}
> Bollinger: {bb_signal} — {bb_rationale}
> Overall: *{overall_signal}*

---

_Turtle: SMA(20,50) + Donchian(20) | Bollinger: BB(20,2σ) + %B + Squeeze_
_Data source: data/latest/ CSVs | This is not financial advice._
```

Formatting rules:
- Group stocks by overall signal: BUY/STRONG_BUY first, then NEUTRAL, then SELL/STRONG_SELL
- For NEUTRAL stocks, use a compact one-line format
- For BUY/SELL stocks, show full rationale details
- Use emoji indicators: :green_circle: for buy, :red_circle: for sell, :white_circle: for neutral
- If Slack message exceeds 4000 characters, split into multiple messages (header + body + footer)

### Step 4: Post to Slack

Use `slack_send_message` MCP tool:
- `channel_id`: the channel ID from Step 2
- `message`: formatted mrkdwn content from Step 3

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

### Example 1: Full daily check run
User says: "Run today's stock check and post to Slack"
Actions:
1. Execute daily_stock_check script with data/latest
2. Find #h-daily-stock-check channel via slack_search_channels
3. Format JSON as mrkdwn, group by signal (BUY/NEUTRAL/SELL)
4. Post via slack_send_message
Result: Slack message with analysis summary and per-stock signals posted to channel

### Example 2: Analysis for specific tickers
User says: "Check AAPL and NVDA signals only"
Actions:
1. Run script with --tickers AAPL,NVDA
2. Output per-stock turtle, bollinger, overall signals
3. Optionally post to Slack or return inline
Result: Focused analysis for requested tickers

## Troubleshooting

### CSVs missing or insufficient data
Cause: data/latest/ empty or rows fewer than 21 (Donchian needs 21)
Solution: Recommend stock-csv-downloader to fetch/refresh data before running daily check

### Slack channel not found
Cause: Channel name changed or MCP not connected
Solution: Use slack_search_channels with query "h-daily-stock-check"; verify Slack MCP server is enabled

## Integration

Script: `backend/scripts/daily_stock_check.py` | Indicators: `backend/app/services/technical_indicator_service.py` | Data: `data/latest/` | Slack: `#h-daily-stock-check`
