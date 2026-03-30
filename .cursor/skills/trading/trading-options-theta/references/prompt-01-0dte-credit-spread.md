# The Tastytrade 0DTE SPX Credit Spread Scanner

**Firm:** Tastytrade
**Use case:** Daily 0DTE credit spread setup with exact strikes and risk parameters on SPX
**Required inputs:** Today's date, current SPX price, VIX level, major economic events scheduled today

## Prompt

You are a senior options trader at Tastytrade who specializes in 0DTE (zero days to expiration) SPX credit spreads — the strategy professional theta traders use to generate daily income from time decay on the S&P 500 index. I need a complete 0DTE trade setup for today's market session with exact strikes and risk parameters.

Scan:
- Market conditions check: is today's VIX level, overnight futures action, and economic calendar suitable for selling premium
- SPX expected move: calculate today's implied expected range using current ATM straddle pricing
- Put credit spread setup: short put strike at 0.10-0.15 delta and long put 5-10 points below for protection
- Call credit spread setup: short call strike at 0.10-0.15 delta and long call 5-10 points above for protection
- Iron condor combination: if conditions favor it, combine both sides for double premium collection
- Premium target: minimum $0.50-$1.00 credit collected per spread to justify the risk-reward
- Risk-reward ratio: maximum loss vs premium collected with a minimum 1:3 reward-to-risk target
- Entry timing: optimal time of day to enter (typically 9:45-10:30 AM after opening volatility settles)
- Stop-loss rules: close the trade if spread reaches 2x the premium collected or if SPX breaches short strike
- Exit strategy: let expire worthless for full profit, or close at 50% profit if reached before 2 PM

Format as a Tastytrade-style 0DTE trade ticket with exact strikes, entry price, max profit, max loss, and time-based exit rules.

## Input Template

Today's setup: [ENTER TODAY'S DATE, CURRENT SPX PRICE, VIX LEVEL, AND ANY MAJOR ECONOMIC EVENTS SCHEDULED TODAY]
