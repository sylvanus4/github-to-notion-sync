# TV Live Data

Fetch real-time stock prices and global market snapshots via TradingView MCP (`yahoo_price`, `market_snapshot`).

## Triggers

Use when the user asks to "get live price via TV", "TV live data", "market snapshot", "real-time price from MCP", "TradingView 실시간", "TV 시세", "글로벌 마켓 스냅샷", "tv-live-data", or wants MCP-powered real-time market data.

Do NOT use for Yahoo Finance DB sync (use `weekly-stock-update` or `tab-stock-sync`). Do NOT use for Toss Securities quotes (use `tossinvest-cli`). Do NOT use for AlphaEar stock OHLCV history (use `alphaear-stock`).

## Adapter

`backend/app/services/tradingview_mcp_adapter.py` — `TradingViewLiveDataService` singleton: `live_data_service`

## Workflow

### Mode 1: Single Price Quote

1. Call `live_data_service.get_price(symbol)`
2. Returns: current price, change, change %, volume, day high/low, 52-week high/low
3. Report in Korean with key metrics highlighted

### Mode 2: Batch Price Quotes

1. Call `live_data_service.batch_prices(symbols)`
2. Runs concurrent `yahoo_price` calls for all symbols
3. Present as a comparison table sorted by daily change %

### Mode 3: Global Market Snapshot

1. Call `live_data_service.market_snapshot()`
2. Returns overview of: major indices (S&P 500, NASDAQ, Dow, etc.), crypto, FX pairs, key ETFs
3. Summarize market regime (risk-on/risk-off) based on cross-asset signals

## Output Format

Report results in Korean with:
- Price data formatted with appropriate decimal places
- Change values color-coded (positive/negative indication)
- Timestamp of data retrieval
- Brief market context interpretation
