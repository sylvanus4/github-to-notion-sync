# The Citadel Monthly Performance Dashboard

**Firm:** Citadel
**Use case:** Monthly performance tracking with Sharpe ratio, profit factor, equity curve, and strategy attribution
**Required inputs:** Monthly trades including date, strategy, premium collected, close price, and P&L for each trade

## Prompt

You are the head of portfolio analytics at Citadel who builds performance dashboards tracking every metric that matters for options income strategies — because you can't improve what you don't measure. I need a complete monthly performance tracking system for my theta income strategy.

Track:
- Total monthly premium collected: gross income from all short options positions before adjustments
- Total monthly realized P&L: net profit after winning trades, losing trades, and adjustments
- Win rate: percentage of trades that were profitable out of total trades placed
- Average winner vs average loser: ratio between typical winning trade and typical losing trade in dollars
- Profit factor: total dollars won divided by total dollars lost (above 1.5 is professional grade)
- Maximum drawdown: largest peak-to-trough decline during the month
- Sharpe ratio estimate: risk-adjusted return measuring consistency of daily income
- Theta harvested vs realized: how much theta income was available vs how much I actually captured
- Best and worst trade analysis: what made the best trade work and what went wrong on the worst trade
- Strategy-level breakdown: P&L separated by strategy type (0DTE spreads, weekly iron condors, earnings plays)
- Equity curve: running account balance plotted day by day showing growth trajectory and drawdowns
- Next month adjustment plan: based on this month's data, what to change for better results next month

Format as a Citadel-style monthly performance report with metrics dashboard, equity curve description, and strategy-level attribution analysis.

## Input Template

My monthly data: [ENTER YOUR TRADES FOR THE MONTH INCLUDING DATE, STRATEGY, PREMIUM COLLECTED, CLOSE PRICE, AND PROFIT OR LOSS FOR EACH TRADE]
