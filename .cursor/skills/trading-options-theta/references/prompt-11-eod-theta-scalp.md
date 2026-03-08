# The Optiver End-of-Day Theta Scalper

**Firm:** Optiver
**Use case:** Accelerated theta decay capture in the final 90 minutes of trading on 0DTE options
**Required inputs:** Underlying (SPX, SPY, QQQ), account size, ability to actively trade the final 90 minutes

## Prompt

You are a senior market maker at Optiver who specializes in capturing accelerated theta decay in the final 90 minutes of the trading day — when time decay on 0DTE options reaches its maximum velocity. I need a complete end-of-day theta scalping strategy for 0DTE options.

Scalp:
- Entry window: open positions between 2:30-3:00 PM when theta acceleration enters its steepest curve
- Strike selection: sell credit spreads at the nearest OTM strike with 0.08-0.12 delta for high probability
- Premium target: collect minimum $0.30-$0.50 per spread with 90 minutes to expiration
- Rapid decay math: calculate exactly how much premium will decay in each 15-minute block until 4:00 PM
- Gamma awareness: this close to expiration, delta can swing wildly — keep positions small
- Hard stop-loss: if the spread moves to 1.5x credit received, close immediately with no exceptions
- Scaling strategy: start with 1-2 contracts and add only after 3 consecutive winning sessions
- Market-on-close risk: be fully closed by 3:50 PM to avoid settlement surprises
- Daily P&L log: track every trade with entry time, premium, close time, and profit or loss
- Win rate tracking: maintain a rolling 20-trade win rate — if it drops below 70%, pause and reassess

Format as an Optiver-style intraday scalping playbook with a minute-by-minute timeline, entry criteria, and a risk management checklist.

## Input Template

My setup: [ENTER THE UNDERLYING (SPX, SPY, QQQ), YOUR ACCOUNT SIZE, AND WHETHER YOU CAN ACTIVELY TRADE THE FINAL 90 MINUTES]
