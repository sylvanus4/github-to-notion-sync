---
name: trading-position-sizer
description: >-
  Calculate risk-based position sizes for long stock trades using Fixed
  Fractional, ATR-Based, or Kelly Criterion methods. Supports stop-loss
  distance calculation, volatility scaling, and sector concentration checks.
  Use when the user asks to "position size", "how many shares to buy", "risk
  per trade", "Kelly criterion", "ATR-based sizing", "포트폴리오 리스크 배분", "포지션
  사이징", "몇 주 살까", or wants portfolio risk allocation guidance. Do NOT use for
  stock analysis (use daily-stock-check or trading-technical-analyst).
---

# Position Sizer

## Overview

Calculate the optimal number of shares to buy for a long stock trade based on risk management principles. Supports three sizing methods:

- **Fixed Fractional**: Risk a fixed percentage of account equity per trade (default: 1%)
- **ATR-Based**: Use Average True Range to set volatility-adjusted stop distances
- **Kelly Criterion**: Calculate mathematically optimal risk allocation from historical win/loss statistics

All methods apply portfolio constraints (max position %, max sector %) and output a final recommended share count with full risk breakdown.

## When to Use

- User asks "how many shares should I buy?"
- User wants to calculate position size for a specific trade setup
- User mentions risk per trade, stop-loss sizing, or portfolio allocation
- User asks about Kelly Criterion or ATR-based position sizing
- User wants to check if a position fits within portfolio concentration limits

## Prerequisites

- No API keys required
- Python 3.9+ with standard library only

## Workflow

### Step 1: Gather Trade Parameters

Collect from the user:
- **Required**: Account size (total equity)
- **Mode A (Fixed Fractional)**: Entry price, stop price, risk percentage (default 1%)
- **Mode B (ATR-Based)**: Entry price, ATR value, ATR multiplier (default 2.0x), risk percentage
- **Mode C (Kelly Criterion)**: Win rate, average win, average loss; optionally entry and stop for share calculation
- **Optional constraints**: Max position % of account, max sector %, current sector exposure

If the user provides a stock ticker but not specific prices, use available tools to look up the current price and suggest entry/stop levels based on technical analysis.

### Step 2: Execute Position Sizer Script

Run the position sizing calculation:

```bash
# Fixed Fractional (most common)
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --output-dir outputs/reports/trading/

# ATR-Based
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --atr 3.20 \
  --atr-multiplier 2.0 \
  --risk-pct 1.0 \
  --output-dir outputs/reports/trading/

# Kelly Criterion (budget mode - no entry)
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir outputs/reports/trading/

# Kelly Criterion (shares mode - with entry/stop)
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir outputs/reports/trading/
```

### Step 3: Load Methodology Reference

Read `references/sizing_methodologies.md` to provide context on the chosen method, risk guidelines, and portfolio constraint best practices.

### Step 4: Calculate Multiple Scenarios

If the user has not specified a single method, run multiple scenarios for comparison:
- Fixed Fractional at 0.5%, 1.0%, and 1.5% risk
- ATR-based at 1.5x, 2.0x, and 3.0x multipliers
- Present a comparison table showing shares, position value, and dollar risk for each

### Step 5: Apply Portfolio Constraints and Determine Final Size

Add constraints if the user has portfolio context:

```bash
python3 .cursor/skills/trading-position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --max-position-pct 10 \
  --max-sector-pct 30 \
  --current-sector-exposure 22 \
  --output-dir outputs/reports/trading/
```

Explain which constraint is binding and why it limits the position.

### Step 6: Generate Position Report

Present the final recommendation including:
- Method used and rationale
- Exact share count and position value
- Dollar risk and percentage of account
- Stop-loss price
- Any binding constraints
- Risk management reminders (portfolio heat, loss-cutting discipline)

## Mandatory Output Contract (Quality Gate)

All human-facing outputs (chat or markdown report) MUST use this structure:

1. **Parameters** — Account size, entry, stop (or ATR inputs), method, risk %, optional constraints.
2. **Method & rationale** — One paragraph: why Fixed Fractional / ATR / Kelly.
3. **Numeric results** — Table: `Shares` | `Position $` | `$ risk` | `% account risk` | `Stop price` | `Risk per share`.
4. **Binding constraint** — State `None` or which cap reduced size (position %, sector %, Kelly cap).
5. **Recommendation** — Single explicit line: "Buy **N** shares at assumed entry **$X** with stop **$Y**."
6. **Risks** — At least one bullet: gap risk, model risk (if prices assumed), or portfolio heat.

**No fabricated prices**: If the user omits entry/stop, **fetch** via web/tools when possible. If still unknown, print clearly tagged **ASSUMED:** values and rerun or label results as illustrative only—never present assumed numbers as live quotes.

**Minimum numerics**: Final output must show **≥3** numbers (e.g., shares, entry, stop, $ risk) before completion.

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "mode": "shares",
  "parameters": {
    "entry_price": 155.0,
    "account_size": 100000,
    "stop_price": 148.50,
    "risk_pct": 1.0
  },
  "calculations": {
    "fixed_fractional": {
      "method": "fixed_fractional",
      "shares": 153,
      "risk_per_share": 6.50,
      "dollar_risk": 1000.0,
      "stop_price": 148.50
    },
    "atr_based": null,
    "kelly": null
  },
  "constraints_applied": [],
  "final_recommended_shares": 153,
  "final_position_value": 23715.0,
  "final_risk_dollars": 994.50,
  "final_risk_pct": 0.99,
  "binding_constraint": null
}
```

### Markdown Report

Generated automatically alongside the JSON report. Contains:
- Parameters summary
- Calculation details for the active method
- Constraints analysis (if any)
- Final recommendation with shares, value, and risk

Reports are saved to `outputs/reports/trading/` with filenames `position_sizer_YYYY-MM-DD_HHMMSS.json` and `.md`.

## Resources

- `references/sizing_methodologies.md`: Comprehensive guide to Fixed Fractional, ATR-based, and Kelly Criterion methods with examples, comparison table, and risk management principles
- `scripts/position_sizer.py`: Main calculation script (CLI interface)

## Key Principles

1. **Survival first**: Position sizing is about surviving losing streaks, not maximizing winners
2. **The 1% rule**: Default to 1% risk per trade; never exceed 2% without exceptional reason
3. **Round down**: Always round shares down to whole numbers (never round up)
4. **Strictest constraint wins**: When multiple limits apply, the tightest one determines final size
5. **Half Kelly**: Never use full Kelly in practice; half Kelly captures 75% of growth with far less risk
6. **Portfolio heat**: Total open risk should not exceed 6-8% of account equity
7. **Asymmetry of losses**: A 50% loss requires a 100% gain to recover; size accordingly

## Examples

### Example 1: Fixed fractional sizing
**User:** "Account $100k, buying at $155, stop at $148.50. How many shares with 1% risk?"
**Action:** Runs `position_sizer.py --account-size 100000 --entry 155 --stop 148.50 --risk-pct 1.0`.
**Output:** Report with recommended shares (~153), dollar risk (~$1,000), position value, and stop price.

### Example 2: ATR-based stop
**User:** "Use 2x ATR for my stop. Entry $155, ATR $3.20. Size for 1% risk."
**Action:** Runs script with `--atr 3.20 --atr-multiplier 2.0`; stop = 155 - 2*3.20 = $148.60.
**Output:** Shares, volatility-adjusted stop, and risk breakdown.

### Example 3: Portfolio constraints
**User:** "Max 10% per position, 30% per sector. I already have 22% in tech. Size this trade."
**Action:** Runs with `--max-position-pct 10`, `--max-sector-pct 30`, `--current-sector-exposure 22`.
**Output:** Final shares (possibly reduced by sector constraint), binding constraint explanation, and rationale.

## Error Handling

| Error | Action |
|-------|--------|
| Entry <= stop (negative risk) | Swap if user reversed values; stop must be below entry for long |
| Risk pct too high (>2%) | Warn; recommend 1% default; explain survival impact |
| Kelly outputs extreme size | Use half-Kelly; cap at max-position-pct or sensible limit |
| Script path wrong | Use `.cursor/skills/trading-position-sizer/scripts/position_sizer.py` |
