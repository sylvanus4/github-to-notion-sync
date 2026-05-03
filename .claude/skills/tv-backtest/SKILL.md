---
name: tv-backtest
description: >-
  Backtest trading strategies against Yahoo Finance historical data via
  TradingView MCP (`backtest_strategy`, `compare_strategies`,
  `walk_forward_backtest_strategy`). Supports 6 built-in strategies: rsi,
  bollinger, macd, ema_cross, supertrend, donchian.
---

# TV Backtest

Backtest trading strategies against Yahoo Finance historical data via TradingView MCP (`backtest_strategy`, `compare_strategies`, `walk_forward_backtest_strategy`). Supports 6 built-in strategies: rsi, bollinger, macd, ema_cross, supertrend, donchian.

## Triggers

Use when the user asks to "backtest via TradingView", "TV backtest", "compare strategies via MCP", "walk-forward backtest", "TradingView 백테스트", "TV 전략 비교", "walk-forward 검증", "tv-backtest", or wants MCP-powered backtesting with commission and slippage modeling.

Do NOT use for the project's native Turtle/DualMA/Bollinger backtesting (use `tab-strategy-comparison`). Do NOT use for KIS strategy backtesting via QuantConnect (use `kis-backtester`). Do NOT use for daily stock signals (use `daily-stock-check`).

## Adapter

`backend/app/services/tradingview_mcp_adapter.py` — `TradingViewBacktestService` singleton: `backtest_service`

## Workflow

### Mode 1: Single Strategy Backtest

1. Call `backtest_service.backtest(symbol, strategy, period, initial_capital, commission_pct, slippage_pct, interval, include_trade_log, include_equity_curve)`
2. Present results: total return, CAGR, max drawdown, Sharpe ratio, win rate, trade count
3. Optionally include trade log and equity curve if requested

### Mode 2: Strategy Comparison

1. Call `backtest_service.compare_strategies(symbol, period, initial_capital, interval)`
2. All 6 strategies run on the same symbol with identical parameters
3. Present ranked leaderboard sorted by risk-adjusted return

### Mode 3: Walk-Forward Validation

1. Call `backtest_service.walk_forward(symbol, strategy, period, n_splits, train_ratio, initial_capital, interval)`
2. Splits data into train/test windows to detect overfitting
3. Compare in-sample vs out-of-sample performance for robustness assessment

## Strategies

| ID | Name | Key Parameters |
|---|---|---|
| `rsi` | RSI Mean Reversion | RSI period, overbought/oversold thresholds |
| `bollinger` | Bollinger Bands | BB period, std deviation multiplier |
| `macd` | MACD Crossover | Fast/slow/signal periods |
| `ema_cross` | EMA Crossover | Short/long EMA periods |
| `supertrend` | SuperTrend | ATR period, multiplier |
| `donchian` | Donchian Channel | Lookback period |

## Defaults

- `period`: 1y
- `initial_capital`: 10,000
- `commission_pct`: 0.1%
- `slippage_pct`: 0.05%
- `interval`: 1d

## Output Format

Report results in Korean with:
- Strategy name and parameters
- Return metrics (total, CAGR, max drawdown)
- Risk metrics (Sharpe, Sortino if available)
- Trade statistics (count, win rate, avg profit/loss)
- Comparison table when multiple strategies tested
