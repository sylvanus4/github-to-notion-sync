---
description: "Run daily data sync, hot stock discovery, analysis, and report pipeline — check DB/CSV gaps, backfill missing data, discover trending stocks, run stock analysis, generate .docx report, and optionally post to #h-report"
---

# Today — Daily Pipeline

## Skill Reference

Read and follow the skill at `.cursor/skills/today/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **mode** from user input:

- **status / check / freshness**: keywords → run Phase 1 only (data freshness report)
- **dry-run / test / preview**: keywords → run all phases, generate .docx, but skip Slack posting
- **skip-sync**: keyword → skip Phase 2 (use existing DB data)
- **skip-discover**: keyword → skip Phase 3 (no hot stock discovery)
- **skip-docx**: keyword → skip .docx report generation (Step 6b)
- **skip-slack**: keyword → skip Slack posting (Step 6c)
- **skip-news**: keyword → skip Phase 4.5a (market context from alphaear-news)
- **skip-sentiment**: keyword → skip Phase 4.5b (sentiment scoring for BUY/SELL stocks)
- **skip-report**: keyword → run Phase 1 + 2 + 3 only (no analysis or report)
- **No arguments**: run the full pipeline

### Step 2: Data Freshness Check (Phase 1)

1. Run DB status check:

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

2. Scan CSV files in `data/latest/` — for each CSV, read the first data row to get the latest date
3. Compare DB `Last` date vs CSV latest date per ticker
4. Report the gap summary:
   - CSV-ahead: CSV has newer data than DB
   - Stale: DB is missing recent trading data
   - Up-to-date: no gap

If mode is `status`, stop here and present the gap report.

### Step 3: Data Sync (Phase 2)

Skip if `skip-sync` is set.

1. If any CSV-ahead gaps exist, import CSVs:

```bash
cd backend
python scripts/import_csv.py ../data/latest --directory
```

2. If any stale gaps exist, fetch from Yahoo Finance:

```bash
cd backend
python scripts/weekly_stock_update.py --days 3
```

3. Verify by re-running status:

```bash
cd backend
python scripts/weekly_stock_update.py --status
```

### Step 4: Hot Stock Discovery (Phase 3)

Skip if `skip-discover` is set.

1. Run the discovery script to find the hottest untracked stock from each index:

```bash
cd backend
python scripts/discover_hot_stocks.py
```

2. Capture the JSON output. For each discovered ticker, fetch recent data:

```bash
cd backend
python scripts/weekly_stock_update.py --ticker {DISCOVERED_TICKER} --days 30
```

3. Present the discovery summary: index, ticker, name, close price, change %, turnover, and suggested category.

If mode is `skip-report`, stop here and present the sync + discovery results.

### Step 5: Analysis (Phase 4)

Run technical analysis (Turtle Trading + Bollinger Bands + Oscillators):

```bash
cd backend
python -m scripts.daily_stock_check --source db
```

Capture the JSON output with per-stock signals. The output now includes `oscillators` (RSI, MACD, Stochastic, ADX) alongside `turtle` and `bollinger` signals. The `overall_signal` is a 3-way combination of all three signal groups.

### Step 5.5: Market Context (Phase 4.5) — Optional

Skip entirely if `skip-news` AND `skip-sentiment` are set. Each sub-step is independent and optional.

**Step 5.5a — Market news context (skip if `skip-news`):**

1. Read the `alphaear-news` skill at `.cursor/skills/alphaear-news/SKILL.md`
2. Fetch latest financial news headlines from multiple sources
3. Filter for news relevant to tracked tickers and active categories
4. Save the top 3-5 headlines as `outputs/news-{date}.json` in format: `{ "headlines": [{ "title": "...", "source": "...", "summary": "..." }] }`
5. If the skill fails or times out, continue — the report gracefully handles missing news data

**Step 5.5b — Sentiment scoring (skip if `skip-sentiment`):**

1. Read the `alphaear-sentiment` skill at `.cursor/skills/alphaear-sentiment/SKILL.md`
2. For each stock with BUY or SELL signal, gather recent news context
3. Run sentiment analysis to score each stock's news sentiment (-1.0 to 1.0)
4. Merge sentiment scores into the analysis JSON results: add `"sentiment": { "score": 0.72, "summary": "..." }` to each scored stock
5. Save updated analysis JSON back to `outputs/analysis-{date}.json`
6. If the skill fails, continue — the report shows "N/A" for sentiment

### Step 6: Report and Post (Phase 5)

**Step 6a — Generate report content:**

1. Read the `alphaear-reporter` skill at `.cursor/skills/alphaear-reporter/SKILL.md`
2. Use the daily-stock-check JSON as input signals
3. Follow the reporter workflow: Cluster Signals → Write Sections → Final Assembly
4. Include the Hot Stocks discovery results in the report (use the template from the skill)

**Step 6b — Generate Korean .docx report (skip if `skip-docx` is set):**

1. Save analysis JSON to `outputs/analysis-{date}.json`
2. Save discovery JSON to `outputs/discovery-{date}.json`
3. Run the report generator:

```bash
cd outputs
node generate-report.js {date}
```

This produces a Korean expert report with per-stock MA/Bollinger/Oscillator analysis at `outputs/reports/daily-{date}.docx`. The generator also reads `outputs/news-{date}.json` for market context (if available).

**Step 6c — Post to Slack (skip if `dry-run` or `skip-slack`):**

1. Format the report for Slack using the template in the today skill
2. Use `slack_search_channels` to find `#h-report` channel ID (known: `C0AKHQWJBLZ`)
3. Use `slack_send_message` to post the **main message** (date, signal summary, top movers, hot stocks, screener)
4. Capture the `message_ts` from the main message response
5. **ALWAYS post a thread reply** using `thread_ts` = the main message's `message_ts`, containing:
   - `:mag: BUY 종목 상세 ({N}종목 전체)` — grouped by category, each with name, ticker, price, change%, RSI, ADX (강한추세 label), 과매수/과매도 warnings
   - `:mag: SELL 종목 상세 ({N}종목)` — each with name, price, change%, RSI, RSI zone, MA alignment, ADX, Stochastic
   - `:warning:` for RSI extremes (80+ 과매수, 30- 과매도)
   - `:bulb:` actionable insight (과매도 반등, 과매수 조정 등)

### Step 7: Summary

Summarize what was done:
- Phase 1: Gap summary (CSV-ahead / stale / up-to-date counts)
- Phase 2: Records imported and fetched (if run)
- Phase 3: Hot stocks discovered (index, ticker, turnover) — or skipped
- Phase 4: Stocks analyzed with Turtle + Bollinger + Oscillator signals, signal distribution
- Phase 4.5a: Market news context fetched (or skipped)
- Phase 4.5b: Sentiment scoring for BUY/SELL stocks (or skipped)
- Phase 5a: Report content generated
- Phase 5b: .docx report saved to `outputs/reports/daily-{date}.docx` (or skipped)
- Phase 5c: Summary posted to Slack (or skipped if dry-run)

## Constraints

- Always run Phase 1 (data freshness check) regardless of mode
- Never skip Phase 1 — it provides the context for all subsequent phases
- Use existing Python scripts for data operations; do not manually compute indicators
- No API keys are needed for Cursor-side execution — API keys are only for the GitHub Actions pipeline
- Use Slack MCP tools for channel lookup and message posting (optional)
- Do not post to Slack if `dry-run` or `test` is in the arguments
- Include the disclaimer: "This is not financial advice"
- If the DB or CSVs are empty, recommend running `/stock-csv-download --all --import` first
- Hot stock discoveries are report-only — do NOT modify `constants.py` or `TICKER_SLUG_MAP`
