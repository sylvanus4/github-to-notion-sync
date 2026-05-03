---
name: vibe-trading-backtest
description: >-
  Run vectorized backtests via Vibe-Trading MCP: prepare config.json and
  signal_engine.py, execute the backtest tool, and interpret 15+ performance
  metrics. Supports US/HK (yfinance), A-shares (tushare), and crypto (OKX).
  Use when the user asks to "backtest with vibe", "vibe-trading backtest",
  "run vibe backtest", "바이브 백테스트", "바이브 트레이딩 백테스트", or wants to validate a
  strategy through the Vibe-Trading engine. Do NOT use for the project's
  native Turtle/DualMA/Bollinger backtests (use tab-strategy-comparison or
  daily-strategy-engine). Do NOT use for KIS backtesting (use kis-backtester).
  Do NOT use for setup (use vibe-trading-setup).
---

# Vibe-Trading Backtest

## Overview

Vibe-Trading provides a cross-market vectorized backtest engine accessible via the
`backtest` MCP tool. The workflow:

1. Create a `run_dir` with `config.json` and `code/signal_engine.py`
2. Call the `backtest` tool
3. Parse returned metrics and artifact paths

## Step 1: Prepare config.json

```json
{
  "source": "auto",
  "codes": ["AAPL.US"],
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "initial_cash": 1000000,
  "commission": 0.001
}
```

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | `"auto"`, `"yfinance"`, `"okx"`, `"tushare"` |
| `codes` | list[str] | Symbols to trade |
| `start_date` | string | YYYY-MM-DD |
| `end_date` | string | YYYY-MM-DD |
| `initial_cash` | number | Starting capital |
| `commission` | number | Commission rate (0.001 = 0.1%) |

## Step 2: Write signal_engine.py

The signal engine must define a `signal(df)` function that receives a DataFrame
with OHLCV columns and returns it with an added `signal` column:

- `1` = BUY
- `-1` = SELL
- `0` = HOLD

```python
def signal(df):
    """Dual moving average crossover strategy."""
    df["sma20"] = df["close"].rolling(20).mean()
    df["sma60"] = df["close"].rolling(60).mean()
    df["signal"] = 0
    df.loc[df["sma20"] > df["sma60"], "signal"] = 1
    df.loc[df["sma20"] < df["sma60"], "signal"] = -1
    return df
```

## Step 3: Create Files & Run

Use the Vibe-Trading MCP `write_file` tool to create the run directory:

```
1. CallMcpTool server=user-vibe-trading toolName=write_file
   arguments={"path": "/tmp/vt-run/config.json", "content": "<config JSON>"}

2. CallMcpTool server=user-vibe-trading toolName=write_file
   arguments={"path": "/tmp/vt-run/code/signal_engine.py", "content": "<signal code>"}

3. CallMcpTool server=user-vibe-trading toolName=backtest
   arguments={"run_dir": "/tmp/vt-run"}
```

## Step 4: Interpret Results

The backtest returns 15+ metrics:

| Metric | Description | Good Threshold |
|--------|-------------|---------------|
| `total_return` | Cumulative return | > benchmark |
| `annual_return` | Annualized CAGR | > 15% |
| `sharpe_ratio` | Risk-adjusted return | > 1.0 |
| `max_drawdown` | Largest peak-to-trough decline | < 20% |
| `win_rate` | Percentage of winning trades | > 50% |
| `profit_factor` | Gross profits / gross losses | > 1.5 |
| `calmar_ratio` | Annual return / max drawdown | > 1.0 |
| `sortino_ratio` | Return / downside deviation | > 1.5 |
| `total_trades` | Number of round-trip trades | context-dependent |

Results also include artifact paths for equity curve CSVs and trade logs.

## Strategy Templates

### RSI Mean Reversion

```python
def signal(df):
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))
    df["signal"] = 0
    df.loc[df["rsi"] < 30, "signal"] = 1
    df.loc[df["rsi"] > 70, "signal"] = -1
    return df
```

### Bollinger Bands Breakout

```python
def signal(df):
    df["sma"] = df["close"].rolling(20).mean()
    df["std"] = df["close"].rolling(20).std()
    df["upper"] = df["sma"] + 2 * df["std"]
    df["lower"] = df["sma"] - 2 * df["std"]
    df["signal"] = 0
    df.loc[df["close"] < df["lower"], "signal"] = 1
    df.loc[df["close"] > df["upper"], "signal"] = -1
    return df
```

### Crypto Momentum (OKX)

```python
def signal(df):
    df["ret_5"] = df["close"].pct_change(5)
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(20).mean()
    df["signal"] = 0
    df.loc[(df["ret_5"] > 0.03) & (df["vol_ratio"] > 1.5), "signal"] = 1
    df.loc[df["ret_5"] < -0.05, "signal"] = -1
    return df
```

## Chaining with Pattern Recognition

After backtest, run pattern recognition on the generated OHLCV artifacts:

```
CallMcpTool server=user-vibe-trading toolName=pattern_recognition
arguments={"run_dir": "/tmp/vt-run"}
```

This overlays chart pattern detection on the same data used for backtesting.

## Comparison with Project's Native Backtesting

| Feature | Vibe-Trading Backtest | Project Native (tab-strategy-comparison) |
|---------|----------------------|------------------------------------------|
| Markets | US, HK, A-shares, Crypto | US, KR (via Yahoo/DB) |
| Strategy definition | Python `signal_engine.py` | Predefined Turtle/DualMA/Bollinger |
| Custom strategies | Any Python logic | Fixed 7 strategies |
| Metrics | 15+ | 15+ |
| Data persistence | File-based artifacts | PostgreSQL |
| Best for | Exploration, custom strategies | Daily operational signals |
