---
name: vibe-trading-mcp
description: >-
  Reference guide for all 16 Vibe-Trading MCP tools with parameter schemas,
  return formats, and chaining patterns. Use when the user asks to "list vibe
  trading tools", "vibe-trading MCP reference", "vibe MCP tools", "what tools
  does vibe-trading have", "바이브 트레이딩 MCP 도구", "바이브 MCP 참조", or needs to
  understand which MCP tool to call for a specific finance task. Do NOT use
  for setup/installation (use vibe-trading-setup). Do NOT use for orchestrated
  workflows (use vibe-trading-orchestrator).
---

# Vibe-Trading MCP Tool Reference

**MCP Server**: `user-vibe-trading` | **Transport**: stdio | **16 Tools**

All tools are called via `CallMcpTool` with `server: "user-vibe-trading"`.

---

## Category 1: Skill Discovery (2 tools)

### `list_skills`

List all available finance skills with names and descriptions.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| _(none)_ | | | |

**Returns**: JSON array of `{name, description}` for 67+ skills.

```
CallMcpTool server=user-vibe-trading toolName=list_skills arguments={}
```

### `load_skill`

Load full documentation for a named finance skill.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Skill name from `list_skills` output |

**Returns**: `{status, skill, content}` with full markdown documentation.

```
CallMcpTool server=user-vibe-trading toolName=load_skill arguments={"name": "strategy-generate"}
```

---

## Category 2: Market Data (1 tool)

### `get_market_data`

Fetch OHLCV market data for stocks, crypto, or mixed symbols.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `codes` | list[str] | yes | | Symbol list (e.g. `["AAPL.US", "BTC-USDT"]`) |
| `start_date` | string | yes | | YYYY-MM-DD |
| `end_date` | string | yes | | YYYY-MM-DD |
| `source` | string | no | `"auto"` | `"auto"`, `"yfinance"`, `"okx"`, `"tushare"` |
| `interval` | string | no | `"1D"` | `1m/5m/15m/30m/1H/4H/1D` |

**Symbol format auto-detection** (`source="auto"`):

| Pattern | Detected Source | Example |
|---------|----------------|---------|
| `\d{6}.(SZ\|SH\|BJ)` | tushare | `000001.SZ` |
| `[A-Z]+.US` | yfinance | `AAPL.US` |
| `\d{3,5}.HK` | yfinance | `700.HK` |
| `[A-Z]+-USDT` | okx | `BTC-USDT` |

**Returns**: JSON object keyed by symbol, each value is an array of OHLCV records.

---

## Category 3: Backtesting (1 tool)

### `backtest`

Run a vectorized backtest using config.json and code/signal_engine.py.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_dir` | string | yes | Path to directory containing `config.json` and `code/signal_engine.py` |

**run_dir structure**:
```
run_dir/
  config.json          # source, codes, dates, initial_cash, commission
  code/
    signal_engine.py   # def signal(df) -> df with 'signal' column
```

**Returns**: JSON with metrics (Sharpe, total_return, max_drawdown, win_rate, etc.) and artifact paths.

---

## Category 4: Quantitative Analysis (3 tools)

### `factor_analysis`

Compute factor IC/IR analysis and layered backtest.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `codes` | list[str] | yes | | Stock codes |
| `factor_name` | string | yes | | Factor column (e.g. `"pe_ttm"`, `"pb"`, `"turnover_rate"`) |
| `start_date` | string | yes | | YYYY-MM-DD |
| `end_date` | string | yes | | YYYY-MM-DD |
| `source` | string | no | `"auto"` | Data source |
| `top_n` | int | no | `10` | Top-ranked stocks per period |
| `bottom_n` | int | no | `10` | Bottom-ranked stocks per period |

**Returns**: IC, IR, top/bottom quintile return spreads.

### `analyze_options`

Calculate Black-Scholes option price and Greeks.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `spot` | float | yes | | Current underlying price |
| `strike` | float | yes | | Strike price |
| `expiry_days` | int | yes | | Days until expiration |
| `risk_free_rate` | float | no | `0.03` | Annual risk-free rate |
| `volatility` | float | no | `0.25` | Annual volatility |
| `option_type` | string | no | `"call"` | `"call"` or `"put"` |

**Returns**: Price, Delta, Gamma, Theta, Vega.

### `pattern_recognition`

Detect technical chart patterns in OHLCV data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_dir` | string | yes | Path to run directory with `artifacts/ohlcv_*.csv` |

**Returns**: Detected patterns (head-and-shoulders, double top/bottom, triangles, wedges, channels).

---

## Category 5: Swarm Multi-Agent Teams (5 tools)

### `list_swarm_presets`

List available swarm team presets. No parameters.

**Returns**: JSON array of preset names, descriptions, agent counts, required variables.

### `run_swarm`

Run a swarm multi-agent team (blocking, polls up to 30 min).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `preset_name` | string | yes | Preset name from `list_swarm_presets` |
| `variables` | dict | yes | Required variables (e.g. `{"target": "AAPL.US", "market": "US"}`) |

**Returns**: `{status, preset, run_id, final_report, tasks[], token_counts}`.

### `get_swarm_status`

Poll a running swarm.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | string | yes | Run ID from `run_swarm` |

### `get_run_result`

Get final report and task summaries of a completed swarm.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `run_id` | string | yes | Run ID |

### `list_runs`

List recent swarm runs.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | int | no | `20` | Max runs to return |

---

## Category 6: File & Web I/O (4 tools)

### `read_url`

Fetch a web page and convert to clean markdown.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Target URL |

### `read_document`

Extract text from a PDF with OCR fallback.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | string | yes | Absolute path to PDF |

### `write_file`

Write content to a file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | yes | File path |
| `content` | string | yes | Content to write |

### `read_file`

Read a file's contents.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | yes | File path |

---

## Common Chaining Patterns

### Pattern 1: Research -> Strategy -> Backtest

```
1. list_skills -> find relevant strategy skill
2. load_skill("strategy-generate") -> read methodology
3. get_market_data(codes, start, end) -> fetch OHLCV
4. write_file("run/config.json", config) -> write backtest config
5. write_file("run/code/signal_engine.py", code) -> write strategy
6. backtest("run") -> execute and get metrics
```

### Pattern 2: Multi-Agent Research

```
1. list_swarm_presets -> find suitable team
2. run_swarm("investment_committee", {"target": "AAPL.US"}) -> team analysis
3. get_run_result(run_id) -> extract final report
```

### Pattern 3: Factor Screening -> Backtest Validation

```
1. factor_analysis(codes, "pe_ttm", start, end) -> identify factor
2. write_file(config + signal_engine based on factor) -> prepare backtest
3. backtest(run_dir) -> validate with backtest
4. pattern_recognition(run_dir) -> overlay chart patterns
```

### Pattern 4: Cross-Market Analysis

```
1. get_market_data(["AAPL.US", "BTC-USDT", "000001.SZ"], start, end) -> mixed markets
2. run_swarm("cross_market_desk", vars) -> multi-agent cross-market analysis
```
