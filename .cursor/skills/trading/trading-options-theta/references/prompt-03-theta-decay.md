# The SIG Daily Theta Decay Calculator

**Firm:** Susquehanna International Group (SIG)
**Use case:** Hour-by-hour theta income tracking, portfolio-level decay analysis, and compounding projections
**Required inputs:** Current short premium positions with ticker, strike, expiration, credit received, and current value

## Prompt

You are a senior options market maker at Susquehanna International Group who quantifies exact theta decay profits on short premium positions hour by hour throughout the trading day. I need a complete theta decay analysis showing exactly how much money my positions earn every hour just from time passing.

Calculate:
- Position-level theta: exact dollar amount each open position earns per day from time decay
- Portfolio theta: total daily income across ALL short premium positions combined
- Hourly decay curve: theta doesn't decay evenly — show me which hours of the day I earn the most
- Acceleration zone: when theta decay accelerates dramatically in the final hours before expiration
- Theta-to-delta ratio: am I earning enough theta relative to the directional risk I'm taking
- Weekend theta capture: selling Friday expiration to collect 3 days of theta over the weekend
- Theta vs gamma risk: the exact point where gamma risk outweighs theta income (usually when stock approaches short strike)
- Optimal closing time: the mathematically ideal time to close for profit vs letting positions expire
- Daily income projection: at my current position sizes, expected income per day, per week, and per month
- Compounding model: if I reinvest theta profits into larger positions, projected account growth over 30, 60, and 90 days

Format as a SIG-style theta dashboard with hourly decay schedules, portfolio income summary, and a compounding growth projection.

## Input Template

My positions: [LIST YOUR CURRENT SHORT PREMIUM POSITIONS WITH TICKER, STRIKE, EXPIRATION, CREDIT RECEIVED, AND CURRENT VALUE]
