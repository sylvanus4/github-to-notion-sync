# Options Strategies Guide

Comprehensive descriptions for all 18+ supported strategies. Use for strategy-specific analysis and educational content.

## Strategy Categories

### Income Strategies
1. **Covered Call** - Own stock, sell call (generate income, cap upside)
2. **Cash-Secured Put** - Sell put with cash backing (collect premium, willing to buy stock)
3. **Poor Man's Covered Call** - LEAPS call + short near-term call (capital efficient)

### Protection Strategies
4. **Protective Put** - Own stock, buy put (insurance, limited downside)
5. **Collar** - Own stock, sell call + buy put (limited upside/downside)

### Directional Strategies
6. **Bull Call Spread** - Buy lower strike call, sell higher strike call (limited risk/reward bullish)
7. **Bull Put Spread** - Sell higher strike put, buy lower strike put (credit spread, bullish)
8. **Bear Call Spread** - Sell lower strike call, buy higher strike call (credit spread, bearish)
9. **Bear Put Spread** - Buy higher strike put, sell lower strike put (limited risk/reward bearish)

### Volatility Strategies
10. **Long Straddle** - Buy ATM call + ATM put (profit from big move either direction)
11. **Long Strangle** - Buy OTM call + OTM put (cheaper than straddle, bigger move needed)
12. **Short Straddle** - Sell ATM call + ATM put (profit from no movement, unlimited risk)
13. **Short Strangle** - Sell OTM call + OTM put (profit from no movement, wider range)

### Range-Bound Strategies
14. **Iron Condor** - Bull put spread + bear call spread (profit from range-bound movement)
15. **Iron Butterfly** - Sell ATM straddle, buy OTM strangle (profit from tight range)

### Advanced Strategies
16. **Calendar Spread** - Sell near-term option, buy longer-term option (profit from time decay)
17. **Diagonal Spread** - Calendar spread with different strikes (directional + time decay)
18. **Ratio Spread** - Unbalanced spread (more contracts on one leg)

---

## Detailed Strategy Analysis (Key Strategies)

### Covered Call
**Income Strategy:** Generate premium while capping upside

**Setup:**
- Own 100 shares @ stock price
- Sell 1x OTM call (30 DTE)

**Max Profit:** Stock gain to strike + premium received
**Max Loss:** Unlimited downside (stock ownership)
**Breakeven:** Cost basis - premium received

**Greeks:** Delta reduces stock exposure; Theta positive (time decay benefit)
**Assignment Risk:** Shares called away if stock above strike at expiration

**When to Use:** Neutral to slightly bullish, want income, willing to sell at strike
**Exit Plan:** Buy back call if strong rally; let expire if below strike; roll to next month to keep shares

---

### Protective Put
**Insurance Strategy:** Limit downside while keeping upside

**Setup:**
- Own 100 shares
- Buy 1x OTM put (30 DTE)

**Max Profit:** Unlimited (stock can rise infinitely)
**Max Loss:** Stock loss to strike + premium paid
**Breakeven:** Cost basis + premium paid

**Greeks:** Delta reduced; Theta negative (time decay cost)
**Protection:** Guaranteed sell price regardless of how far stock falls

**When to Use:** Own stock, worried about drop; earnings protection; alternative to stop-loss
**Cost:** Typically 1-3% of stock value (insurance premium)
**Exit Plan:** Let expire worthless if stock rises; exercise if below strike; sell put if want to keep shares after drop

---

### Iron Condor
**Range-Bound Strategy:** Profit from low volatility

**Setup:** Sell put spread + sell call spread (4 legs)
- Sell OTM put, buy further OTM put
- Sell OTM call, buy further OTM call
- Net credit received

**Max Profit:** Net credit (if stock stays in range)
**Max Loss:** Width of one spread minus credit
**Profit Range:** Between short strikes

**Greeks:** Delta ~0 (market neutral); Theta positive; Vega negative (short volatility)
**When to Use:** Expect range-bound; after big move consolidation; high IV (sell expensive options)
**Risk:** Unlimited if one side tested; use stop loss at 2x credit
**Adjustments:** Roll tested side out in time; close early at 50% max profit

---

## Earnings Strategies

### Long Straddle/Strangle
**Thesis:** Expect big move (>5%) but unsure of direction

**IV Crush Risk:** Critical - pre-earnings IV (e.g. 40%) drops post-earnings (e.g. 25%). Can lose significant value even if stock doesn't move.

**Implied Move:** √(DTE/365) × IV × Stock Price
**Recommendation:** Consider if expect >10% move (larger than implied); avoid if expect normal ~5% move

### Short Iron Condor (Earnings)
**Thesis:** Expect stock to stay range-bound
**IV Crush Benefit:** Short high IV before earnings; IV drop after = profit on vega
**Recommendation:** Good if expect normal earnings reaction (<8% move); benefit from IV crush regardless of direction
**Exit Plan:** Close next day if IV crushed; stop loss if one side tested (-2x credit)

---

## Exit Rules by Strategy

| Strategy | Profit Target | Loss Trigger | Time Management |
|----------|---------------|-------------|-----------------|
| Covered Call | 50-75% max profit | Stock -5%, buy back call | 7-10 DTE, roll to avoid assignment |
| Spreads | 50% max profit | 2x debit paid | 21 DTE, close or roll (avoid gamma risk) |
| Iron Condor | 50% credit | 2x credit lost if tested | Roll tested side out in time |
| Straddle/Strangle | Stock moved >breakeven | Theta eating, no move | Day after earnings (if earnings play) |

---

## Alternatives Comparison Table

| Strategy | Max Profit | Max Loss | Complexity | When Better |
|----------|-----------|----------|------------|-------------|
| Bull Call Spread | Limited | Debit | Medium | Moderately bullish |
| Long Call | Unlimited | Premium | Low | Very bullish |
| Covered Call | Strike gain + premium | Unlimited | Medium | Own stock already |
| Bull Put Spread | Credit | Spread width - credit | Medium | Want credit spread |
