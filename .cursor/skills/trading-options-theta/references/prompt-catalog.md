# Options Theta Prompt Catalog

Quick-reference table for all 12 prompts. Each prompt file contains the full text and required inputs.

## Prompt Index

| # | File | Strategy | Firm | Category | Timing |
|---|------|----------|------|----------|--------|
| 01 | [prompt-01-0dte-credit-spread.md](prompt-01-0dte-credit-spread.md) | 0DTE SPX Credit Spread Scanner | Tastytrade | Trade Setup | Intraday (9:45-10:30 AM) |
| 02 | [prompt-02-market-regime.md](prompt-02-market-regime.md) | Market Regime Classifier | Citadel | Pre-Trade Analysis | Pre-market |
| 03 | [prompt-03-theta-decay.md](prompt-03-theta-decay.md) | Daily Theta Decay Calculator | SIG | Position Management | Any time |
| 04 | [prompt-04-strike-selection.md](prompt-04-strike-selection.md) | Probability-Based Strike Selection | Two Sigma | Trade Setup | Pre-trade |
| 05 | [prompt-05-iron-condor.md](prompt-05-iron-condor.md) | Iron Condor Income Machine | D.E. Shaw | Trade Setup | Market open |
| 06 | [prompt-06-pre-market-edge.md](prompt-06-pre-market-edge.md) | Pre-Market Edge Analyzer | Jane Street | Pre-Trade Analysis | 8 AM pre-market |
| 07 | [prompt-07-risk-management.md](prompt-07-risk-management.md) | Risk Management System | Wolverine Trading | Risk Management | Before/during session |
| 08 | [prompt-08-volatility-skew.md](prompt-08-volatility-skew.md) | Volatility Skew Exploiter | Akuna Capital | Advanced Strategy | Pre-trade |
| 09 | [prompt-09-weekly-income.md](prompt-09-weekly-income.md) | SPY Weekly Income Calendar | Peak6 | Weekly Workflow | Mon-Fri schedule |
| 10 | [prompt-10-earnings-crush.md](prompt-10-earnings-crush.md) | Earnings Theta Crusher | IMC Trading | Event-Driven | 1-3 days pre-earnings |
| 11 | [prompt-11-eod-theta-scalp.md](prompt-11-eod-theta-scalp.md) | End-of-Day Theta Scalper | Optiver | Trade Setup | 2:30-4:00 PM |
| 12 | [prompt-12-monthly-dashboard.md](prompt-12-monthly-dashboard.md) | Monthly Performance Dashboard | Citadel | Performance Review | End of month |

## Category Grouping

### Pre-Trade Analysis (run first)
- **02** Market Regime Classifier — determines GREEN/YELLOW/RED verdict
- **06** Pre-Market Edge Analyzer — 8 AM morning briefing

### Trade Setup (run after analysis)
- **01** 0DTE SPX Credit Spread Scanner — morning credit spreads
- **04** Probability-Based Strike Selection — statistical strike placement
- **05** Iron Condor Income Machine — dual-side premium collection
- **08** Volatility Skew Exploiter — skew-based advanced strategies
- **11** End-of-Day Theta Scalper — final 90-minute scalping

### Position Management (run during session)
- **03** Daily Theta Decay Calculator — track hourly income
- **07** Risk Management System — enforce loss limits

### Weekly/Periodic Workflows
- **09** SPY Weekly Income Calendar — Mon-Fri schedule
- **10** Earnings Theta Crusher — event-driven IV crush
- **12** Monthly Performance Dashboard — end-of-month review

## Recommended Daily Workflow

1. **Pre-market (8 AM):** Run prompt 06 (Jane Street Pre-Market Edge)
2. **Market open assessment:** Run prompt 02 (Citadel Market Regime)
3. **Trade setup (9:30-10:30 AM):** Run prompt 01 or 05 based on regime
4. **Strike selection:** Run prompt 04 (Two Sigma Probability)
5. **Risk check:** Run prompt 07 (Wolverine Risk Management)
6. **During session:** Run prompt 03 (SIG Theta Decay) to monitor
7. **EOD opportunity (2:30 PM):** Run prompt 11 (Optiver EOD Scalp)
8. **End of month:** Run prompt 12 (Citadel Dashboard)
