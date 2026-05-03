---
name: paper-trading-validator
description: >-
  Validates trading signals against real market outcomes using Alpaca paper
  trading. Submits signals as paper trades, monitors fills, and compares
  predicted vs actual performance over rolling windows. Produces daily P&L
  snapshots and strategy-level win/loss statistics. Ensures only strategies
  with pro
---

# Paper Trading Validator

## Description

Validates trading signals against real market outcomes using Alpaca paper trading. Submits signals as paper trades, monitors fills, and compares predicted vs actual performance over rolling windows. Produces daily P&L snapshots and strategy-level win/loss statistics. Ensures only strategies with proven paper-trading track records graduate to live trading.

## Triggers

Use when the user asks to:
- "validate trading signals", "run paper trading", "paper trade validation"
- "paper-trading-validator", "test strategy on paper", "validate before live"
- "페이퍼 트레이딩", "모의 매매 검증", "전략 검증"

Do NOT use for:
- Running the daily stock analysis pipeline (use `today`)
- Live trading execution (use `trade-executor`)
- Backtesting historical data (use `trading-backtest-expert`)
- Strategy design or ideation (use `trading-trade-hypothesis-ideator`)

## Procedure

### 1. Load today's signals

```bash
cat outputs/screener-$(date +%Y-%m-%d).json | python -c "
import json, sys
data = json.load(sys.stdin)
signals = [s for s in (data if isinstance(data, list) else data.get('results', []))
           if s.get('signal','').upper() in ('BUY','STRONG_BUY','SELL','STRONG_SELL')]
print(f'{len(signals)} actionable signals found')
"
```

### 2. Execute paper trades

```bash
cd backend
python -c "
from app.services.broker import AlpacaBroker
from app.services.broker.signal_bridge import load_screener_signals, execute_signals, RiskLimits
from datetime import datetime

broker = AlpacaBroker(paper=True)
signals = load_screener_signals(datetime.now().strftime('%Y-%m-%d'))
limits = RiskLimits(max_position_pct=0.05, max_daily_loss_pct=0.02)

results = execute_signals(broker, signals, limits, dry_run=False)
for r in results:
    status = r.get('action', 'unknown')
    print(f\"  {r['side'].upper()} {r['symbol']}: {status}\")
"
```

### 3. Check positions and P&L

```bash
cd backend
python -c "
from app.services.broker import AlpacaBroker

broker = AlpacaBroker(paper=True)
acct = broker.get_account()
print(f\"Equity: \${acct.get('equity', 0):,.2f}\")
print(f\"Buying Power: \${acct.get('buying_power', 0):,.2f}\")

for p in broker.get_positions():
    pnl = p.get('unrealized_pl', 0)
    pnl_pct = p.get('unrealized_plpc', 0) * 100
    icon = '🟢' if pnl >= 0 else '🔴'
    print(f\"  {icon} {p['symbol']}: {p['qty']} shares, PnL: \${pnl:+,.2f} ({pnl_pct:+.1f}%)\")
"
```

### 4. Graduation criteria

A strategy graduates from paper to live when ALL conditions are met:

| Criterion | Threshold |
|-----------|-----------|
| Paper trading days | >= 20 |
| Win rate | >= 55% |
| Profit factor | >= 1.3 |
| Max drawdown | <= 10% |
| Sharpe ratio | >= 0.5 |

## Output

- `outputs/trades/executions-{date}.json` — Daily execution log
- `outputs/trades/paper-summary-{date}.json` — Rolling P&L summary
- Strategy graduation report when thresholds are met

## Integration

This skill is designed to run after the `today` pipeline completes.
Sequence: `today` → `paper-trading-validator` → (if graduated) `trade-executor`
