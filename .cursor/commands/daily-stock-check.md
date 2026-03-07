---
description: "Run daily stock analysis (Turtle Trading + Bollinger Bands) and post results to #h-daily-stock-check Slack channel"
---

# Daily Stock Check

## Skill Reference

Read and follow the skill at `.cursor/skills/daily-stock-check/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains specific tickers (e.g., "AAPL,NVDA"), pass them via `--tickers`
- If `$ARGUMENTS` is empty or "all", analyze all stocks
- If `$ARGUMENTS` contains "dry-run" or "test", skip the Slack posting step

### Step 2: Run Analysis

Run the analysis script from the `backend` directory:

```bash
cd backend
python -m scripts.daily_stock_check --dir ../data/latest [--tickers TICKERS]
```

Capture the JSON output. If the script reports 0 stocks or an error:
1. Check if `data/latest/` has CSV files
2. If empty, suggest running `/stock-csv-download --all` first
3. If CSVs exist but have too few rows, suggest `/stock-csv-download --all --gap-fill-from 2025-11-01`

### Step 3: Format Slack Message

Using the JSON output, format a Slack mrkdwn message following the template in the skill:

1. Header with date and summary counts
2. Group stocks by signal: BUY/STRONG_BUY → NEUTRAL → SELL/STRONG_SELL
3. BUY/SELL stocks get detailed view with rationale
4. NEUTRAL stocks get compact one-line view
5. Footer with methodology note and disclaimer

### Step 4: Post to Slack

1. Use `slack_search_channels` to find the channel ID for `h-daily-stock-check`
2. Use `slack_send_message` to post the formatted message to the channel
3. If the message is too long (>4000 chars), split into multiple messages

### Step 5: Report

Summarize what was posted:
- Number of stocks analyzed
- Signal distribution (BUY/NEUTRAL/SELL counts)
- Any stocks that were skipped and why
- Confirm the Slack message was posted successfully

## Constraints

- Always run the Python script first; do not manually compute indicators
- Use the Slack MCP tools for channel lookup and message posting
- Do not post to Slack if `dry-run` or `test` is in the arguments
- Include the disclaimer: "This is not financial advice"
- If no BUY or SELL signals exist, still post the NEUTRAL summary
