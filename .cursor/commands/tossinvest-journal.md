---
description: "Trade journal analytics — view logged trades, monthly P&L, win rate, strategy breakdown, and generate performance reports"
---

# Tossinvest Trade Journal

## Skill Reference

Read and follow the skill at `.cursor/skills/toss-trade-journal/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run trade journal analytics based on $ARGUMENTS:

### Default (no arguments): Current Month Summary
1. Load `outputs/toss/journal-{YYYY-MM}.json` for the current month
2. Compute: total trades, win rate, average win/loss, profit factor, average holding period
3. Break down by strategy and sector
4. Present Korean summary

### With "log" argument: Log a New Trade
1. Ask for trade details (symbol, side, quantity, price) or parse from $ARGUMENTS
2. Optionally fetch market context from Toss via `tossctl account summary --output json`
3. Ask for thesis/reasoning
4. Append to `outputs/toss/journal-{YYYY-MM}.json`
5. Confirm with Korean summary

### With month argument (e.g., "2026-02"): Historical Month Analysis
1. Load the specified month's journal file
2. Compute all analytics for that period
3. Present Korean summary with month-over-month comparison if prior month exists

### With "report" argument: Generate DOCX Report
1. Run full analytics for the target month
2. Generate `.docx` via anthropic-docx with executive summary, trade log table, win/loss analysis, and strategy comparison
3. Save to `outputs/toss/journal-report-{YYYY-MM}.docx`

### With "close" argument: Close a Position
1. Parse symbol from $ARGUMENTS
2. Find the matching open entry in the journal
3. Fetch current price via `tossctl quote get <symbol> --output json`
4. Update the journal entry with exit data (price, P&L, holding days, exit reason)
5. Confirm with Korean summary

## Constraints

- Journal files are append-only (no retroactive modification of logged entries)
- Duplicate order_id entries are rejected
- Present all output in Korean
