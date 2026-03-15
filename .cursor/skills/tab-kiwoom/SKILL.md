---
description: "Interface with Kiwoom Securities brokerage API for real-time Korean stock quotes, order placement, and account management. Use when interacting with Kiwoom, '키움 증권', 'tab-kiwoom', 'Kiwoom API'. Do NOT use for Yahoo Finance stock data (use tab-stock-sync), daily stock analysis (use daily-stock-check), or US stock analysis (use trading-us-stock-analysis)."
---

# tab-kiwoom

## Purpose

Interface with Kiwoom Securities brokerage API for Korean market (KOSPI/KOSDAQ) operations: real-time quotes, order management, account balance, and position tracking.

## When to Use

- Kiwoom API interaction
- 키움 증권 연동
- tab-kiwoom
- real-time Korean stock quotes
- place order on KOSPI/KOSDAQ

## When NOT to Use

- Yahoo Finance data sync — use tab-stock-sync
- Daily stock analysis — use daily-stock-check
- US stock analysis — use trading-us-stock-analysis
- Strategy backtesting — use tab-strategy-comparison

## Status

**PLANNED** — This skill is a placeholder for future Kiwoom Securities API integration. The endpoints below are designed but not yet implemented.

## Planned Endpoints

- `POST /api/v1/kiwoom/connect` — establish connection to Kiwoom OpenAPI
- `GET /api/v1/kiwoom/account` — fetch account info and balance
- `GET /api/v1/kiwoom/positions` — list current positions
- `GET /api/v1/kiwoom/quote/{symbol}` — real-time quote for a Korean ticker
- `POST /api/v1/kiwoom/order` — place market/limit order (body: symbol, side, qty, price, order_type)
- `GET /api/v1/kiwoom/orders` — list pending/filled orders
- `DELETE /api/v1/kiwoom/order/{order_id}` — cancel pending order

## Dependencies

- Kiwoom Open API+ SDK (Windows-only, requires wine or VM on macOS)
- KRX market hours (09:00-15:30 KST)

## Output

Real-time Korean market data, order execution, and position management.
