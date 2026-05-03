---
name: tab-strategy-comparison
description: >-
  Run unified cross-strategy backtest comparison via POST
  /strategy-comparison/run for Turtle, DualMA, and Bollinger strategies. Use
  when comparing strategies, '전략 비교', 'tab-strategy-comparison', 'strategy
  comparison'. Do NOT use for single-strategy backtesting (use POST
  /turtle/backtest/run or /dualma/backtest/run or /bollinger-bands/backtest),
  daily stock analysis (use daily-stock-check), or stock price sync (use
  tab-stock-sync).
---

# tab-strategy-comparison

## Purpose

Run a unified comparison across multiple trading strategies (Turtle, DualMA, Bollinger I-IV) for a given symbol and period. Returns normalized metrics for side-by-side comparison.

## When to Use

- compare strategies
- 전략 비교
- tab-strategy-comparison
- strategy comparison run
- which strategy is best for AAPL

## When NOT to Use

- Single-strategy backtest — use POST /turtle/backtest/run, /dualma/backtest/run, or /bollinger-bands/backtest
- Daily stock signals — use daily-stock-check
- Stock price sync — use tab-stock-sync

## Workflow

1. Call `GET /api/v1/strategy-comparison/strategies` to list available strategies and their parameters
2. Call `POST /api/v1/strategy-comparison/run` with symbol, optional strategy selection, and date range
3. Review returned metrics: total_return_pct, max_drawdown_pct, sharpe_ratio, win_rate_pct, profit_factor
4. Identify best_strategy from the response

## Endpoints Used

- `GET /api/v1/strategy-comparison/strategies` — list available strategies with default params
- `POST /api/v1/strategy-comparison/run` — run cross-strategy comparison (body: symbol, strategies, start_date, end_date, initial_equity, days)
- `GET /api/v1/strategy-comparison/results` — list past comparison runs
- `GET /api/v1/strategy-comparison/results/{comparison_id}` — retrieve saved comparison result

## Request Example

```json
{
  "symbol": "AAPL",
  "strategies": [
    {"strategy_type": "turtle"},
    {"strategy_type": "dualma"},
    {"strategy_type": "bollinger_i"}
  ],
  "days": 365,
  "initial_equity": 10000000
}
```

## Dependencies

- Requires backend server running on port 4567
- Requires PostgreSQL with stock price data for the requested symbol

## Output

Normalized comparison result with per-strategy metrics and best strategy identification.
