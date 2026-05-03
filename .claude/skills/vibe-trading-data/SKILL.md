---
name: vibe-trading-data
description: >-
  Fetch multi-market OHLCV data via Vibe-Trading's get_market_data MCP tool.
  Supports US/HK equities (yfinance), China A-shares (tushare), and crypto
  (OKX) with automatic source detection from symbol format. Use when the user
  asks to "fetch stock data via vibe", "get crypto OHLCV", "vibe-trading
  data", "vibe market data", "바이브 시세 조회", "바이브 트레이딩 데이터", or needs OHLCV data
  through the Vibe-Trading MCP. Do NOT use for Yahoo Finance data via the
  project's own weekly-stock-update. Do NOT use for AlphaEar stock search (use
  alphaear-stock). Do NOT use for setup (use vibe-trading-setup).
---

# Vibe-Trading Data Fetching

## Overview

Fetch OHLCV (Open, High, Low, Close, Volume) data for any symbol across 3 markets
using a single MCP tool: `get_market_data` on the `user-vibe-trading` server.

## Symbol Format & Auto-Detection

When `source="auto"` (default), the tool detects the data source from the symbol format:

| Market | Format | Source | API Key Required |
|--------|--------|--------|-----------------|
| US equities | `AAPL.US`, `MSFT.US` | yfinance | No |
| HK equities | `700.HK`, `9988.HK` | yfinance | No |
| China A-shares | `000001.SZ`, `600519.SH` | tushare | Yes (`TUSHARE_TOKEN`) |
| Crypto | `BTC-USDT`, `ETH-USDT` | OKX | No |

Mixed-market queries are supported -- the tool groups symbols by detected source
and fetches each group independently.

## Usage

### Single Market

```
CallMcpTool
  server: user-vibe-trading
  toolName: get_market_data
  arguments:
    codes: ["AAPL.US", "MSFT.US", "GOOGL.US"]
    start_date: "2024-01-01"
    end_date: "2024-12-31"
    source: "auto"
    interval: "1D"
```

### Cross-Market (Mixed Symbols)

```
CallMcpTool
  server: user-vibe-trading
  toolName: get_market_data
  arguments:
    codes: ["AAPL.US", "BTC-USDT", "000001.SZ"]
    start_date: "2024-06-01"
    end_date: "2024-12-31"
```

### Intraday Data

```
CallMcpTool
  server: user-vibe-trading
  toolName: get_market_data
  arguments:
    codes: ["BTC-USDT"]
    start_date: "2024-12-01"
    end_date: "2024-12-31"
    interval: "1H"
```

Supported intervals: `1m`, `5m`, `15m`, `30m`, `1H`, `4H`, `1D`.

## Response Format

JSON object keyed by symbol. Each value is an array of OHLCV records:

```json
{
  "AAPL.US": [
    {
      "date": "2024-01-02",
      "open": 187.15,
      "high": 188.44,
      "low": 183.89,
      "close": 185.64,
      "volume": 82488700
    }
  ]
}
```

## Integration with Other Vibe-Trading Skills

| Downstream Skill | How Data Feeds In |
|------------------|-------------------|
| vibe-trading-backtest | Write OHLCV to `run_dir/` or let backtest fetch internally via `config.json` |
| vibe-trading-quant | Pass codes + dates to `factor_analysis` or `pattern_recognition` |
| vibe-trading-swarm | Swarm agents fetch data internally; use `get_market_data` for pre-analysis |

## Integration with Existing Project Skills

| Project Skill | Relationship |
|--------------|--------------|
| weekly-stock-update | Project's own Yahoo Finance sync to PostgreSQL -- use for DB-backed analysis |
| alphaear-stock | AlphaEar A-Share/HK/US stock search and OHLCV -- narrower scope, different API |
| daily-stock-check | Project's native Turtle/Bollinger analysis pipeline -- uses DB data |

Use `vibe-trading-data` when you specifically need Vibe-Trading's multi-source
fallback chain or cross-market mixed queries.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Empty data for A-shares | Missing `TUSHARE_TOKEN` | Set token in `~/thaki/Vibe-Trading/agent/.env` |
| Symbol not found | Incorrect format | Check symbol format table above |
| Timeout | Large date range + intraday | Reduce date range or use `1D` interval |
