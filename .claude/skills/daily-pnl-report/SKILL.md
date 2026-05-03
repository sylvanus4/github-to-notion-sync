---
name: daily-pnl-report
description: >-
  Generate a daily portfolio P&L report from Alpaca broker positions, compute
  equity curves, strategy-level win/loss stats, and drawdown metrics. Posts a
  formatted summary to Slack #h-report channel.
disable-model-invocation: true
---

# Daily P&L Report

## Description

Generate a daily portfolio P&L report from Alpaca broker positions, compute equity curves, strategy-level win/loss stats, and drawdown metrics. Posts a formatted summary to Slack #h-report channel.

## Triggers

Use when the user asks to:
- "daily P&L report", "portfolio report", "how did I do today"
- "equity curve", "drawdown report", "strategy performance"
- "daily-pnl-report", "오늘 수익", "포트폴리오 리포트", "손익 리포트"

Do NOT use for:
- Running the daily stock analysis pipeline (use `today`)
- Paper trading validation (use `paper-trading-validator`)
- Backtesting historical strategies (use `trading-backtest-expert`)
- Content performance metrics (use content-performance API)

## Procedure

### 1. Generate P&L snapshot

```bash
cd backend
python -c "
from app.services.broker import AlpacaBroker
from app.services.portfolio_tracker import generate_pnl_report

broker = AlpacaBroker(paper=True)
report = generate_pnl_report(broker, days=7)

snap = report['current_snapshot']
print(f\"=== Daily P&L Report ===\")
print(f\"Equity: \${snap['equity']:,.2f}\")
print(f\"Unrealized P&L: \${snap['unrealized_pnl']:+,.2f} ({snap['unrealized_pnl_pct']:+.1f}%)\")
print(f\"Positions: {snap['total_positions']} ({snap['winners']}W / {snap['losers']}L)\")
print(f\"Max Drawdown: {report['metrics']['max_drawdown_pct']:.1f}%\")
print()

for strat, stats in report.get('strategy_stats', {}).items():
    print(f\"Strategy '{strat}': {stats}\")
"
```

### 2. Post to Slack

Format the report as a Slack message and post to `#h-report` using the Slack MCP `slack_send_message` tool:

```
📊 Daily P&L Report — {date}

💰 Equity: ${equity}
📈 Unrealized P&L: ${pnl} ({pnl_pct}%)
📉 Max Drawdown: {drawdown}%

Positions: {count} ({winners}W / {losers}L)

Best: {best_symbol} +{best_pnl}%
Worst: {worst_symbol} {worst_pnl}%
```

### 3. Check alerts

Flag if:
- Daily loss exceeds 2% → reduce exposure
- Drawdown exceeds 5% → halt new entries
- Win rate below 40% over 20 days → review strategy

## Output

- `outputs/portfolio/snapshot-{date}.json` — Daily snapshot
- `outputs/portfolio/pnl-report-{date}.json` — Full P&L report with equity curve
- Slack message to `#h-report`
