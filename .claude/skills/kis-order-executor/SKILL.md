---
name: kis-order-executor
description: >-
  Execute KIS strategy signals and place orders on Korea Investment &
  Securities. Selects symbols, runs strategies to generate BUY/SELL/HOLD
  signals with strength (0-1), and executes paper (VPS) or live (prod) orders.
  Enforces safety rules: signal strength < 0.5 auto-skips, prod orders require
  explicit user confirmation with symbol/quantity/amount details, and current
  mode (VPS/prod) must be disclosed before any order. Use when the user asks
  to 'execute strategy', 'check signals', 'run strategy on symbol', 'any buy
  signals?', 'sell timing', 'live trading', 'auto trade', 'place order with
  this strategy', '전략 실행해줘', '신호 확인', '종목 돌려봐줘', '매수 신호 있어?', '매도 타이밍', '실시간
  매매', '자동매매'. Do NOT use for strategy design (use kis-strategy-builder). Do
  NOT use for backtesting (use kis-backtester). Do NOT use for full pipeline
  orchestration (use kis-team). Do NOT use for Toss Securities orders (use
  tossinvest-trading). Do NOT use for Kiwoom Securities (use tab-kiwoom).
---

# [Step 3] KIS Strategy Execution & Signal-Based Orders

## Purpose

Select symbols, run a strategy to generate BUY/SELL/HOLD signals, and execute paper (VPS) or live (prod) orders based on signal strength.

> **Important**: This is NOT direct order placement. The flow is:
> symbol selection → strategy execution → signal generation → order (if signal is strong enough).

## Safety Rules

- **Prod orders**: Must show symbol, quantity, and estimated amount, then get explicit user confirmation
- **Pre-order**: Always disclose current mode (VPS/prod)
- **Signal strength < 0.5**: Automatically skip the order

## Prerequisites

- KIS auth completed: `/kis-auth vps` (paper) or `/kis-auth prod` (live)
- strategy_builder backend running (port 8000)

## Server Startup

```bash
# Backend
cd $CLAUDE_PROJECT_DIR/strategy_builder && uv run uvicorn backend.main:app --reload --port 8000

# Frontend
cd $CLAUDE_PROJECT_DIR/strategy_builder/frontend && pnpm dev
# → http://localhost:3000/execute
```

## Trading Hours (reference — actual availability determined by KIS API)

| Session | Time (KST) | Order Type |
|---------|-----------|------------|
| Pre-market | 08:00 ~ 09:00 | Limit only |
| Regular | 09:00 ~ 15:30 | Market & limit |
| After-hours | 15:40 ~ 18:00 | Limit only |

> These are reference values for Korean equities. The KIS API makes the final determination.

## Workflow

### 1. Check Auth Status

```bash
/kis-auth   # Verify current mode (VPS/prod) and token expiry
```

### 2. Select Symbols

```bash
codes: ["005930", "000660", "035420"]

# Symbol search
GET /api/symbols/search?q=삼성
GET /api/symbols/search?q=하이닉스
```

### 3. Select Strategy

```bash
GET /api/strategies         # Preset list
GET /api/strategies/custom  # Custom YAML strategies
```

### 4. Execute Strategy → Generate Signals

```bash
POST /api/strategies/execute
Body: {
  "strategy_id": "golden_cross",
  "codes": ["005930", "000660"],
  "params": { "fast_period": 50, "slow_period": 200 }
}
```

Response (`SignalResult`):
```json
[
  { "code": "005930", "name": "삼성전자", "action": "BUY", "strength": 0.85, "reason": "RSI 28.3 < 30" },
  { "code": "000660", "name": "SK하이닉스", "action": "HOLD", "strength": 0.3, "reason": "RSI 45.2 in range" }
]
```

### 5. Interpret Signals

| Strength | Meaning | Order Type |
|----------|---------|------------|
| 0.8 ~ 1.0 | Strong signal | Market order |
| 0.5 ~ 0.8 | Medium signal | Limit order |
| < 0.5 | Weak signal | No order |

> Strength < 0.5 → order is skipped. Strength exactly 0.5 → treated as "medium" and limit order is possible.

### 6. Execute Order (after signal confirmation)

**For prod mode** — display details and require user confirmation:
```
종목: 삼성전자 (005930)
수량: 10주
예상금액: 약 730,000원
모드: 실전투자 (prod)
→ 실행하시겠습니까?
```

```bash
POST /api/orders
Body: {
  "code": "005930",
  "action": "BUY",
  "quantity": 10,
  "order_type": "market"
  # For limit orders: add "price" field
  # Buy limit: at or below current price
  # Sell limit: at or above current price
}
```

**For VPS mode** — can execute directly.

### 7. Monitor Results

```bash
GET /api/account/holdings    # Current holdings
GET /api/orders/history      # Order history
```

## Troubleshooting

- **Auth error** → Run `/kis-auth` to check status, re-authenticate with `/kis-auth vps` or `/kis-auth prod`
- **Order rejected** → Insufficient balance or outside trading hours (regular: 09:00-15:30)
- **No signals (HOLD only)** → Strategy conditions not met. Adjust parameters or try a different strategy
- **Execute error** → Verify strategy_builder backend is running (`lsof -i :8000`)

## Next Steps

- **[Step 1]** `kis-strategy-builder` — Modify strategy if signals don't match expectations
- **[Step 2]** `kis-backtester` — Re-validate performance before execution
