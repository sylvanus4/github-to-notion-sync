---
name: kis-backtester
description: "Validate KIS trading strategies against historical data using the kis-backtest MCP server with Docker-based QuantConnect Lean engine. Run 10 presets or custom .kis.yaml strategies, interpret BacktestResult metrics (total return, CAGR, max drawdown, Sharpe ratio), perform Grid/Random parameter optimization, batch strategy comparison, portfolio analysis, and HTML report generation. Use when the user asks to 'backtest', 'run backtest', 'strategy validation', 'performance analysis', 'parameter optimization', 'check returns', 'check Sharpe', 'check max drawdown', '백테스팅', '백테스트 해줘', '전략 검증', '성과 분석', '파라미터 최적화', '수익률 확인'. Do NOT use for strategy design (use kis-strategy-builder). Do NOT use for live order execution (use kis-order-executor). Do NOT use for full pipeline orchestration (use kis-team). Do NOT use for existing project backtesting via tab-strategy-comparison API (use tab-strategy-comparison for Turtle/DualMA/Bollinger comparisons)."
---

# [Step 2] KIS Backtesting

## Purpose

Validate strategy performance against historical data using the backtester system.
Run 10 presets or custom `.kis.yaml` from Step 1 to verify returns, Sharpe ratio, and max drawdown.
Supports parameter optimization and HTML report generation.
When the user does not specify dates, default `end_date` to today and `start_date` to 1 year ago.

## Prerequisites (required — cannot run without these)

- **Docker running** (`quantconnect/lean:latest`) — the backtest engine runs in Docker containers
- KIS auth completed (`/kis-auth vps` or `/kis-auth prod`)

```bash
docker ps
# If lean image is missing:
docker pull quantconnect/lean:latest
```

## Server Startup

```bash
# MCP server (port 3846)
cd $CLAUDE_PROJECT_DIR/backtester && bash scripts/start_mcp.sh
# → http://127.0.0.1:3846/mcp

# (Optional) Backend REST API (port 8002)
cd $CLAUDE_PROJECT_DIR/backtester && uv run uvicorn backend.main:app --reload --port 8002

# (Optional) Frontend
cd $CLAUDE_PROJECT_DIR/backtester/frontend && pnpm dev
# → http://localhost:3001
```

## Workflow

### 0. Pre-Run Validation (custom YAML)

For custom YAML (not presets), confirm parameters with the user before execution:

```
📋 Backtest Parameters

| Item | Value |
|------|-------|
| Strategy | Samsung Electronics Swing |
| Symbol | 005930 (Samsung Electronics) |
| Period | 2024-02-25 ~ 2026-02-25 (1 year) |
| Capital | 10,000,000 KRW |
| Indicators | EMA(20,60), RSI(14), ATR(14) |
| Entry | EMA golden cross AND RSI < 40 |
| Exit | EMA dead cross OR RSI > 70 |
| Stop/Profit | 4.0% / 12.0% |

이 조건으로 백테스트를 실행할까요?
```

**YAML pre-validation**:
- `validate_yaml_tool` for syntax check
- Replace `$param_name` variables with their default values
- Reject non-numeric `value` fields

### 1. Strategy Selection

- **Preset ID**: `"sma_crossover"`, `"momentum"`, etc.
  ```
  Tool: list_presets_tool
  Tool: get_preset_yaml_tool  # { "strategy_id": "sma_crossover" }
  ```
- **Custom YAML**: Use the `.kis.yaml` from Step 1
  ```
  Tool: validate_yaml_tool    # { "yaml_content": "..." } — run first
  Tool: run_backtest_tool      # yaml_content for direct execution
  ```
- **Indicator reference**:
  ```
  Tool: list_indicators_tool   # 80 indicators + 57 candlestick parameter definitions
  ```

### 2. Parameter Configuration

```
Tool: list_presets_tool     # Check param schema (type, min, max, default)
Tool: get_preset_yaml_tool  # { "strategy_id": "sma_crossover", "param_overrides": {"fast_period": 50} }
```

### 3. Execution

**Preset execution** — `start_date`/`end_date` omitted defaults to 1 year back to today:
```
Tool: run_preset_backtest_tool {
  "strategy_id": "sma_crossover",
  "symbols": ["005930", "000660"],
  "initial_capital": 10000000,
  "param_overrides": { "fast_period": 5, "slow_period": 20 }
}
→ { job_id, status: "running" }
```

**Custom YAML execution**:
```
Tool: run_backtest_tool {
  "yaml_content": "<.kis.yaml content>",
  "symbols": ["005930"]
}
→ { job_id, status: "running" }
```

**Result retrieval** (default: waits for completion, no polling needed):
```
Tool: get_backtest_result_tool { "job_id": "<job_id>" }
→ Server waits internally up to 5 minutes
→ Completed: { status: "completed", result: { metrics, equity_curve, ... } }
→ Failed: { status: "failed", error: "..." }
→ Timeout: { status: "running", message: "timeout..." }

# Immediate status check (no wait):
Tool: get_backtest_result_tool { "job_id": "<job_id>", "wait": false }
```

### 4. Result Interpretation

`BacktestResult` fields:

| Field | Meaning |
|-------|---------|
| `total_return_pct` | Total return (%) |
| `cagr` | Compound annual growth rate |
| `sharpe_ratio` | Risk-adjusted return (1.0+ is good) |
| `sortino_ratio` | Downside risk-adjusted return |
| `max_drawdown` | Maximum drawdown (lower is better) |
| `win_rate` | Win rate (%) |
| `profit_factor` | Total profit / total loss |
| `total_trades` | Total number of trades |

### 4b. Retry on Failure

For transient errors like EGW00201 (rate limit exceeded):
```
Tool: retry_backtest_tool { "job_id": "<failed_job_id>" }
→ { new_job_id, status: "running" }
```

### 5. Parameter Optimization (optional)

```
Tool: optimize_strategy_tool {
  "strategy_id": "sma_crossover",
  "symbols": ["005930"],
  "parameters": [
    {"name": "fast_period", "min": 2, "max": 20, "step": 3},
    {"name": "slow_period", "min": 10, "max": 60, "step": 10}
  ],
  "search_type": "grid",
  "target": "sharpe_ratio"
}
→ { job_id, total_combinations: 12, status: "running" }
```

### 5b. Batch Backtest — Compare Multiple Strategies (optional)

```
Tool: run_batch_backtest_tool {
  "items": [
    {"strategy_id": "sma_crossover", "symbols": ["005930"]},
    {"strategy_id": "golden_cross", "symbols": ["005930"], "param_overrides": {"fast_period": 50}},
    {"yaml_content": "<custom YAML>", "symbols": ["000660"]}
  ]
}
→ { completed, comparison: { by_sharpe, by_return, by_drawdown }, runs, job_ids }
```

### 6. Portfolio Analysis (optional)

Run multiple symbols in a single backtest for portfolio effects:
```
Tool: run_preset_backtest_tool {
  "symbols": ["005930", "000660", "035420"],
  "initial_capital": 30000000
}
```

### 7. HTML Report Generation

```
Tool: get_report_tool { "job_id": "<job_id>", "format": "html" }
Tool: get_report_tool { "job_id": "<job_id>", "format": "json" }
```

## 10 Preset IDs

| ID | Name | Category | Key Parameters |
|----|------|----------|---------------|
| `sma_crossover` | SMA Golden/Dead Cross | trend | fast_period, slow_period |
| `momentum` | Momentum | momentum | lookback, threshold |
| `trend_filter_signal` | Trend Filter + Signal | composite | trend_period |
| `week52_high` | 52-Week High Breakout | trend | lookback, stop_loss_pct |
| `ma_divergence` | MA Disparity | mean_reversion | period, buy_ratio, sell_ratio |
| `false_breakout` | False Breakout | trend | lookback |
| `short_term_reversal` | Short-term Reversal | mean_reversion | period, threshold_pct |
| `strong_close` | Strong Close | momentum | close_ratio, stop_loss_pct |
| `volatility_breakout` | Volatility Breakout | volatility | atr_period, lookback |
| `consecutive_moves` | Consecutive Moves | momentum | up_days, down_days |

## Interpretation Guidelines

| Metric | Threshold | Assessment |
|--------|-----------|------------|
| Sharpe Ratio | > 1.5 excellent / 1.0-1.5 good / < 1.0 needs improvement |
| Max Drawdown | < 10% excellent / < 20% acceptable / > 20% risky |
| Win Rate | > 55% good (interpret with Profit Factor) |
| Profit Factor | > 1.5 good / > 2.0 excellent |

## Troubleshooting

- **MCP server not running** → `curl http://127.0.0.1:3846/health` then `bash backtester/scripts/start_mcp.sh`
- **Docker not running** → `docker ps` then start Docker Desktop (required)
- **No data** → Check KIS auth with `/kis-auth`
- **Port 8002 conflict** → `lsof -i :8002`
- **Slow optimization** → Reduce parameter ranges or test with 1 symbol first

## Next Steps

- **[Step 3]** `kis-order-executor` — Execute verified strategies in live/paper trading
- **[Step 1]** `kis-strategy-builder` — Modify strategy if performance is insufficient
