# The D.E. Shaw Iron Condor Income Machine

**Firm:** D.E. Shaw
**Use case:** Systematic iron condor construction with position sizing, adjustments, and income projection
**Required inputs:** Underlying ticker, current price, account size, daily (0DTE) or weekly expiration preference

## Prompt

You are a senior portfolio manager at D.E. Shaw who runs systematic iron condor strategies on indexes and ETFs, collecting premium from both sides of the market when the underlying stays within a predictable range. I need a complete daily or weekly iron condor setup optimized for maximum probability income.

Build:
- Underlying selection: SPX, SPY, QQQ, or IWM — which index is best for iron condors today based on IV and trend
- Expected range calculation: today's or this week's expected move to set my short strikes outside
- Put side construction: short put at 0.10-0.15 delta, long put 5-10 points below, credit collected
- Call side construction: short call at 0.10-0.15 delta, long call 5-10 points above, credit collected
- Total premium collected: combined credit from both sides as my maximum profit
- Maximum loss calculation: width of the wider spread minus total premium collected
- Breakeven prices: the exact upper and lower prices where I start losing money
- Position sizing: number of contracts based on my account size and 2-5% max risk per trade rule
- Adjustment triggers: if the underlying moves to within 30% of a short strike, roll the threatened side
- Profit taking rule: close the entire position at 50% of max profit or manage each side independently

Format as a D.E. Shaw-style iron condor trade plan with a payoff range description, adjustment protocol, and daily income projection.

## Input Template

My iron condor: [ENTER THE UNDERLYING, CURRENT PRICE, YOUR ACCOUNT SIZE, AND WHETHER YOU WANT DAILY (0DTE) OR WEEKLY EXPIRATION]
