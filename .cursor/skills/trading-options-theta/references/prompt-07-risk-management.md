# The Wolverine Trading Risk Management System

**Firm:** Wolverine Trading
**Use case:** Portfolio risk rules, circuit breakers, loss limits, and recovery protocols for theta strategies
**Required inputs:** Account size, current positions, daily income target, maximum acceptable drawdown

## Prompt

You are a senior risk manager at Wolverine Trading who monitors options portfolios in real-time and enforces strict risk rules that prevent catastrophic losses — because surviving bad days is more important than maximizing good ones. I need a complete risk management system for my daily theta income strategy.

Protect:
- Daily loss limit: the maximum dollar amount I'm allowed to lose in a single day before closing all positions
- Weekly loss limit: cumulative weekly threshold that triggers a trading pause until next Monday
- Position size cap: maximum number of contracts or dollar risk per individual trade (never exceed 2-5% of account)
- Correlation check: am I accidentally running the same directional bet in multiple positions simultaneously
- Tail risk protection: how to hedge against a 3+ standard deviation move that blows through all my short strikes
- VIX spike protocol: specific actions when VIX jumps 20%+ in a single day (close, hedge, or widen strikes)
- Buying power management: never use more than 50% of total buying power so I always have room to adjust
- Rolling vs closing decision tree: when to roll a losing position for recovery vs cutting the loss immediately
- Recovery protocol: after a max loss day, how to reduce size and rebuild confidence systematically
- Monthly drawdown circuit breaker: if monthly losses hit 10% of account, stop trading for the rest of the month

Format as a Wolverine-style risk management manual with hard rules, decision trees, and a daily risk checklist to review before every trading session.

## Input Template

My account: [ENTER YOUR ACCOUNT SIZE, CURRENT POSITIONS, DAILY INCOME TARGET, AND MAXIMUM ACCEPTABLE DRAWDOWN]
