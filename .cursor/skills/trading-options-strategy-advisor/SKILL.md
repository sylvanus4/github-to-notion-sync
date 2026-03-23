---
name: trading-options-strategy-advisor
description: >-
  Options trading strategy analysis and simulation tool. Provides Black-Scholes theoretical pricing, Greeks calculation, strategy P/L simulation, and risk management guidance. Use when the user asks for "options strategy", "covered call", "protective put", "iron condor", "bull call spread", "options Greeks", "옵션 전략", "커버드콜", "옵션 P/L 분석", "Greeks 계산", or earnings-based options recommendations. Educational focus with practical trade simulation. Do NOT use for stock-only analysis (use trading-us-stock-analysis).
metadata:
  author: tradermonty
  version: "1.0.0"
  category: execution
  source: claude-trading-skills
  api_required: fmp
---

# Options Strategy Advisor

## Overview

Comprehensive options strategy analysis using theoretical pricing. Black-Scholes pricing, Greeks, P/L simulation, earnings strategies, risk management. FMP API for prices/HV; user provides IV from broker when available.

**Core Capabilities:** Black-Scholes pricing, strategy simulation, earnings strategies, risk management, educational focus.

## When to Use

- Options strategy questions ("What's a covered call?", "How does an iron condor work?")
- Strategy P/L simulation ("Max profit on bull call spread?")
- Greeks analysis ("Delta exposure?")
- Earnings strategies ("Straddle before NVDA earnings?")
- Strategy comparison ("Covered call vs protective put?")
- Position sizing, volatility ("Is IV high?")

## Supported Strategies

For full strategy descriptions, see [references/strategies_guide.md](references/strategies_guide.md).

**Summary:** Income (Covered Call, Cash-Secured Put, Poor Man's Covered Call), Protection (Protective Put, Collar), Directional (Bull/Bear Call/Put Spreads), Volatility (Long/Short Straddle/Strangle), Range-Bound (Iron Condor, Iron Butterfly), Advanced (Calendar, Diagonal, Ratio Spread).

## Analysis Workflow

### Step 1: Gather Input

**Required:** Ticker, strategy type, strikes, expiration(s), contracts. **Optional:** IV (default: HV), risk-free rate (~5.3%).

**FMP:** Stock price, historical prices (HV), dividend yield, earnings date.

### Step 2: Historical Volatility (if IV not provided)

90-day log returns, annualize with √252. Note: "Consider using broker IV for accuracy." Script accepts `--iv 28.0`.

### Step 3: Black-Scholes Pricing

```
Call = S*N(d1) - K*e^(-r*T)*N(d2)
Put = K*e^(-r*T)*N(-d2) - S*N(-d1)
d1 = [ln(S/K) + (r + σ²/2)*T] / (σ√T), d2 = d1 - σ√T
```

Adjust dividends for calls. Use `scripts/black_scholes.py` for implementation.

### Step 4: Greeks

For formulas and interpretation, see [references/greeks_explained.md](references/greeks_explained.md). Position Greeks = sum across legs (long +, short -).

### Step 5: P/L Simulation

Generate price range (±30%), compute intrinsic value at expiration per leg. Output: Max profit/loss, breakeven(s), profit probability.

### Step 6: P/L Diagram

ASCII chart of P/L vs stock price. Legend: █ Profit, ░ Loss, ─ Breakeven, │ Current price.

### Step 7: Strategy-Specific Analysis

Load [references/strategies_guide.md](references/strategies_guide.md) for Covered Call, Protective Put, Iron Condor details, earnings strategies, exit rules.

### Step 8: Earnings Strategy Integration

Fetch earnings date (Earnings Calendar). Pre-earnings: Long straddle/strangle (IV crush risk); Short iron condor (IV crush benefit). See strategies_guide.md.

### Step 9: Risk Management

**Position Sizing:** Risk per trade = account × tolerance (e.g. 2%). Max contracts = max_risk / max_loss_per_contract.

**Portfolio Greeks:** Delta -10 to +10; Theta positive; Vega monitored. See [references/greeks_explained.md](references/greeks_explained.md).

## Output Format

Report: Strategy setup, leg table, P/L analysis, ASCII diagram, Greeks, risk assessment, trade management, suitability, alternatives. Save as `options_analysis_[TICKER]_[STRATEGY]_[DATE].md`.

### Required Section Headers (Eval-Aligned)

The written report **must** include these **markdown headings** in order:

1. `## Setup` — Ticker, strategy name, expiries, strikes, contracts, **S₀** (spot), **r**, **σ or IV**, **T** (years) — every parameter shown as a **number** where known.
2. `## Legs` — Table: leg, type, strike, qty, mid/theo price (numeric).
3. `## P/L & Breakevens` — Max profit ($), max loss ($), breakeven(s) with **numeric** prices.
4. `## Greeks` — Net delta, gamma, theta, vega (numbers or “N/A” with reason).
5. `## Scenario Table` — At least 3 rows: stock price scenarios with P/L **numbers** (from model, not guessed).
6. `## Recommendation` — **One** primary action (open / skip / adjust strike) with rationale.
7. `## Risks & Invalidation` — Assignment risk, gap risk, IV crush, early exercise; **stop or roll trigger** as price level or % move when possible.
8. `## Data Provenance` — Label each figure: `FMP API`, `user-provided`, `Black-Scholes (scripts/black_scholes.py)`, or `UNKNOWN`.

**Hallucination guard:** If FMP fails, use user-supplied **S₀** and IV; never fabricate live quotes. For “AAPL 커버드콜” without numbers, **ask** for spot, short-call strike, expiry, and IV or accept HV default and state it.

**Closing:** Single-sentence **trade decision** (do / don’t / conditional).

## Key Principles

**Black-Scholes Limits:** European-style, constant vol, no costs. Real: bid-ask, American early exercise, liquidity. Use for education; get broker quotes before trading.

**Volatility:** See [references/volatility_guide.md](references/volatility_guide.md) for HV vs IV, IV percentile guidance.

## Integration

- **Earnings Calendar:** Fetch dates, suggest earnings strategies
- **Technical Analyst:** Support/resistance for strikes
- **US Stock Analysis:** Fundamentals for LEAPS
- **Bubble Detector:** High risk → protective puts

## Resources

- [references/strategies_guide.md](references/strategies_guide.md) — All 18+ strategies, earnings plays, exit rules
- [references/greeks_explained.md](references/greeks_explained.md) — Greeks formulas and interpretation
- [references/volatility_guide.md](references/volatility_guide.md) — HV vs IV, IV percentile
- `scripts/black_scholes.py` — Pricing engine

## Important Notes

- All analysis in English; educational focus
- Theoretical pricing; user IV optional (default HV)
- FMP Free tier sufficient; Python 3.8+, numpy, scipy, pandas

## Examples

### Example 1: Bull call spread analysis
**User:** "Analyze a $180/$185 bull call spread on AAPL, 30 days to expiration, 10 contracts."
**Action:** Fetches AAPL price from FMP, calculates HV or uses user IV, prices both legs via Black-Scholes, computes Greeks and P/L simulation.
**Output:** Report with leg details, max profit/loss, breakeven, P/L diagram, Greeks, and risk management guidance.

### Example 2: Earnings straddle vs iron condor
**User:** "Should I trade a straddle or iron condor before NVDA earnings?"
**Action:** Fetches earnings date, estimates IV and IV crush risk, compares long straddle (IV crush risk) vs short iron condor (IV crush benefit).
**Output:** Side-by-side analysis with breakevens, IV crush impact, and recommendation based on expected move vs implied move.

### Example 3: Covered call income
**User:** "I own 100 AAPL at $180. What covered call should I sell for income?"
**Action:** Fetches price, suggests ATM or OTM strikes, calculates premium, max profit, assignment risk, and when to use.
**Output:** Strategy setup with strike recommendation, Greeks (delta/theta), and exit plan.

## Error Handling

| Error | Action |
|-------|--------|
| IV not available | Use HV as proxy; note to user; suggest getting IV from broker (TOS, TastyTrade) |
| Negative option price | Verify strike vs stock price; check for deep ITM numerical edge cases |
| FMP API fails (price/data) | Request user to provide current stock price; proceed with theoretical analysis |
| Greeks seem wrong | Confirm T in years, sigma annualized, r as decimal; check annual vs daily units |
