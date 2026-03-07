---
name: alphaear-stock
description: Search A-Share/HK/US stock tickers and retrieve OHLCV price history. Use when the user asks about stock codes, recent price changes, specific company stock info, or ad-hoc historical price queries. Do NOT use for routine weekly price updates (use weekly-stock-update). Do NOT use for CSV downloads from investing.com (use stock-csv-downloader). Do NOT use for technical indicator analysis (use daily-stock-check).
metadata:
  version: "1.0.0"
  category: data-collection
  author: alphaear
---

# AlphaEar Stock

## Overview

Search A-Share, HK, and US stock tickers by code or name, and retrieve historical OHLCV price data. Optimized for ad-hoc lookups and historical queries. The project also tracks 21 tickers in `data/latest/` and PostgreSQL — for routine updates, use `weekly-stock-update`; for CSV imports from investing.com, use `stock-csv-downloader`.

## Prerequisites

- Python 3.10+
- `pandas`, `requests`, `akshare`, `yfinance`
- `scripts/database_manager.py` (PostgreSQL or SQLite for local cache)
- Network access for akshare/yfinance

## Workflow

1. **Initialize**: Create `DatabaseManager`, then `StockTools(db)`.
2. **Search ticker**: Call `StockTools.search_ticker(query)` — fuzzy search by code (e.g. "600519") or name (e.g. "Moutai", "宁德时代").
3. **Get price**: Call `StockTools.get_stock_price(ticker, start_date, end_date)` with dates in `YYYY-MM-DD` format.
4. **Routine updates**: For the 21 tracked tickers, prefer `weekly-stock-update` skill instead of this skill.
5. **CSV downloads**: For investing.com historical CSVs and gap-fill, use `stock-csv-downloader` skill.

## Examples

| Trigger | Action | Result |
|--------|--------|--------|
| "Search for Moutai" | `search_ticker("Moutai")` | `[{code: "600519", name: "贵州茅台"}]` |
| "Price history of 600519" | `get_stock_price("600519", "2025-01-01", "2025-02-28")` | DataFrame with date, open, close, high, low, volume, change_pct |
| "Recent AAPL prices" | `get_stock_price("AAPL", end_date=today)` | Last ~90 days (default) OHLCV |
| "宁德时代 最近30天" | `get_stock_price("300750", ...)` | 30-day OHLCV |

## Integration with Project

- **21 tickers**: Tracked in `data/latest/` and PostgreSQL; routine sync via `weekly-stock-update`.
- **Ad-hoc queries**: This skill — ticker search + historical OHLCV for any A/H share.
- **Bulk CSV import**: `stock-csv-downloader` for investing.com downloads and DB import.

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Unknown ticker | Empty list / empty DataFrame | Verify code with `search_ticker`; check A/H vs US format |
| Network/proxy error | Retries with proxy disabled | Ensure akshare/yfinance reachable |
| Date out of range | Returns available data | Adjust start/end to trading days |
| DB empty | Auto fetches from network | First request may be slower |

## Troubleshooting

- **No results for US ticker**: This skill focuses on A-Share/HK via akshare; US tickers may need `yfinance` path — check `stock_tools.py` implementation.
- **Proxy issues**: Script uses `temporary_no_proxy()` context to retry when proxy blocks akshare.
- **Stale data**: `get_stock_price` auto-syncs when DB is >2 days behind requested end_date.
