---
description: "Design and validate a trading strategy with systematic backtesting methodology"
argument-hint: "Strategy description (e.g., 'Turtle breakout on NASDAQ 100 stocks with 20-day Donchian channel')"
---

# Trading Backtest Expert

## Skill Reference

Read and follow `.cursor/skills/trading-backtest-expert/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Define Hypothesis

From `$ARGUMENTS`, define:
- Strategy name and type
- Entry and exit rules
- Universe of instruments
- Timeframe
- Expected edge (why this should work)

### Step 2: Design Backtest

Following the `trading-backtest-expert` skill methodology:
1. Define parameter ranges (not single values)
2. Set realistic assumptions (slippage, commissions, survivorship bias)
3. Design walk-forward testing windows
4. Define quality gates for each phase

### Step 3: Robustness Checks

Guide through:
- Parameter sensitivity analysis
- Out-of-sample validation
- Monte Carlo simulation considerations
- Regime analysis (bull/bear/sideways)

### Step 4: Report

Generate strategy validation report:
- Hypothesis definition
- Backtest design specification
- Expected metrics (Sharpe, max drawdown, win rate)
- Parameter robustness assessment
- Go/no-go recommendation
- Production deployment checklist

Save to `outputs/reports/trading/backtest_[STRATEGY]_YYYY-MM-DD.md`.

## Constraints

- Focus on methodology, not curve-fitting
- Include failed test post-mortems from references
- No API keys required
