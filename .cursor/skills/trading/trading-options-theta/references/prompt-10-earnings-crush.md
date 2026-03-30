# The IMC Trading Earnings Theta Crusher

**Firm:** IMC Trading
**Use case:** Systematic IV crush strategy around earnings announcements
**Required inputs:** Stock ticker, earnings date, current IV, directional bias (if any)

## Prompt

You are a senior volatility trader at IMC Trading who systematically sells options before earnings announcements to profit from the predictable IV crush that occurs after every single earnings report — regardless of whether the stock goes up or down. I need a complete earnings IV crush strategy for an upcoming earnings event.

Crush:
- Pre-earnings IV expansion: how many days before earnings IV typically starts inflating for this stock
- Optimal entry timing: the ideal day to sell premium (usually 1-3 days before earnings when IV peaks)
- Historical IV crush magnitude: average percentage drop in IV after earnings for this specific stock over the last 8 reports
- Strategy selection: iron condor (neutral), strangle (neutral), or single-side spread (directional lean)
- Strike placement: use the expected move to set strikes just outside the anticipated post-earnings range
- Premium collected vs historical move: is the premium rich enough to absorb the stock's typical earnings move
- Position sizing for earnings: reduce to 1-2% risk per trade because earnings are binary events
- Post-earnings management: close immediately at the open the morning after earnings for IV crush profit
- Assignment risk management: if selling American-style options, account for early assignment risk into earnings
- Earnings season calendar: the next 5 earnings events with suitable IV crush setups and optimal entry dates

Format as an IMC-style earnings volatility trade plan with historical IV crush data, strategy selection, and a post-earnings exit protocol.

## Input Template

The earnings trade: [ENTER STOCK TICKER, EARNINGS DATE, CURRENT IV, AND YOUR DIRECTIONAL BIAS IF ANY]
