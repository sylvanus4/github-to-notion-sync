# The Peak6 SPY Weekly Income Calendar

**Firm:** Peak6
**Use case:** Systematic Mon-Fri weekly options income schedule with position sizing cycles
**Required inputs:** Account size, weekly income target, risk tolerance per week, ability to monitor trades during market hours

## Prompt

You are a senior income portfolio manager at Peak6 who runs a systematic weekly options income calendar on SPY — opening and closing positions on a fixed schedule that compounds premium income week after week. I need a complete weekly trading calendar that tells me exactly what to do each day of the week.

Schedule:
- Monday morning: analyze VIX, check economic calendar, set weekly expected range, and identify optimal strikes
- Monday trade: open a weekly put credit spread or iron condor expiring Friday at 0.12-0.15 delta short strikes
- Tuesday management: check positions at 10 AM — if at 30%+ profit already, consider closing early to free capital
- Wednesday midweek review: reassess market direction — if one side is threatened, prepare adjustment or roll
- Thursday acceleration: theta decay accelerates sharply — decide to hold for full decay or close at 65% profit
- Friday morning decision: close all positions by 11 AM to avoid pin risk, or let OTM options expire worthless
- Friday afternoon: review the week's performance, log all trades, and prepare Monday's watchlist
- Position sizing cycle: use fixed percentage of account per week (3-5%) and increase only after 4 consecutive winning weeks
- Loss week protocol: after a losing week, reduce position size by 50% for the following week
- Monthly reconciliation: review all 4 weekly cycles, calculate actual win rate, and adjust delta levels if needed

Format as a Peak6-style weekly trading calendar with exact daily actions, position management checkpoints, and a trade journal template.

## Input Template

My account: [ENTER YOUR ACCOUNT SIZE, WEEKLY INCOME TARGET, RISK TOLERANCE PER WEEK, AND WHETHER YOU CAN MONITOR TRADES DURING MARKET HOURS]
