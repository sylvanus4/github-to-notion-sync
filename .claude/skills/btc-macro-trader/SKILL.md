---
name: btc-macro-trader
description: >-
  Analyze BTC/crypto positions using the bwjoke 6-year trading dataset
  patterns: macro-cycle timing, leverage drawdown recovery, portfolio
  concentration evolution, and withdrawal-adjusted performance. Use when the
  user asks to "BTC macro analysis", "crypto cycle timing", "BTC position
  sizing", "leverage drawdown assessment", "BTC 매크로 분석", "암호화폐 사이클", "BTC
  포지션", "레버리지 드로다운", "btc-macro-trader", or wants crypto trading decisions
  grounded in real 6-year performance data. Do NOT use for spot-only stock
  analysis (use daily-stock-check). Do NOT use for options strategies (use
  trading-options-strategy-advisor). Do NOT use for general market environment
  without crypto focus (use trading-market-environment-analysis).
---

# BTC Macro Trader

Crypto trading analysis grounded in the bwjoke dataset: 6 years (2020-05 → 2026-04),
43k+ orders, 52.39x return, 66 XBT withdrawn, across BitMEX derivatives.

## Source Dataset

- **Repo**: `github.com/bwjoke/BTC-Trading-Since-2020`
- **Baseline**: 1.84 XBT (2020-05-01)
- **Final**: 96.4 XBT adjusted wealth (52.39x multiple)
- **CAGR**: 93.4% (full 6-year), 207.8% (in-dataset 3.2 years)
- **Max Drawdown**: 80.6% (2020-06 → 2020-07, early leverage period)

## Core Framework: 4-Phase Cycle Model

The dataset reveals a clear 4-phase evolution pattern. Use this to assess where a trader
currently sits and what comes next.

### Phase 1 — Exploration (Year 1)
- **Signature**: 20+ instruments, high symbol diversity, frequent small trades
- **Dataset evidence**: 2020 had 24 instruments, 32% BTC-related, active in ETHUSD/XRPUSD/LINKUSDT
- **Risk**: Scattered focus, transaction-cost drag, inconsistent sizing
- **Guidance**: Track win rate per instrument. Drop anything below 45% win rate after 50+ trades.

### Phase 2 — Aggressive Leverage (Year 1-2)
- **Signature**: Large PnL swings, 50%+ drawdowns, high RealisedPNL transaction count
- **Dataset evidence**: 80.6% drawdown in Q3 2020 (peak 2.83x → trough 0.55x)
- **Risk**: Account wipeout. The dataset survived; most don't.
- **Guidance**: If current drawdown exceeds 40%, reduce position size by 50% immediately.
  Never allocate >25% of equity to a single leveraged position.

### Phase 3 — Concentration + Scaling (Year 2-4)
- **Signature**: 5-10 instruments, >80% BTC-focused, growing equity curve
- **Dataset evidence**: 2021 had 16 instruments (84% BTC), 2022 had 17 (73% BTC).
  Equity grew from 5.73x (end-2020) → 22.54x (end-2021) → 7.13x (end-2022 post-crash)
- **Risk**: Concentration without hedging during regime shifts
- **Guidance**: Maintain 1-2 hedge instruments (stablecoin pairs, inverse perps).
  Use trailing stops at 2x ATR on concentrated positions.

### Phase 4 — Harvest + Preservation (Year 4+)
- **Signature**: Regular withdrawals, <10 instruments, stable or declining leverage
- **Dataset evidence**: 66 XBT total withdrawals, 2023 had 9 instruments (99% BTC-focused),
  final multiple 38.64x (in-dataset) / 52.39x (full period)
- **Risk**: Leaving too much on the exchange; not securing realized gains
- **Guidance**: Withdraw 20-30% of realized profits quarterly to cold storage.
  Keep exchange balance ≤ 50% of total crypto wealth.

## Drawdown Recovery Playbook

From the dataset's 5 major drawdown events:

| Period | Peak → Trough | Drawdown | Recovery Time |
|--------|---------------|----------|---------------|
| 2020-Q3 | 2.83x → 0.55x | -80.6% | ~6 months |
| 2021-Q2 | 22.07x → 10.99x | -50.2% | ~3 months |
| 2022-H1 | 22.54x → 7.13x | -68.4% | ~8 months |
| 2021-Q1 | 13.23x → 8.89x | -32.8% | ~2 months |
| 2020-Q4 | 5.73x → 4.42x | -22.9% | ~1 month |

**Recovery rules derived from data**:
1. Drawdowns >50% take 3-8 months to recover — reduce size, don't chase
2. Drawdowns <30% recover within 1-2 months — hold positions, tighten stops
3. The trader never added to losing positions — no "averaging down" observed

## Position Sizing Formula

Based on the dataset's risk-adjusted behavior:

```
MaxPositionBTC = AccountEquity × RiskFactor × CycleMultiplier

RiskFactor:
  - Phase 1 (Exploration): 0.05 (5% per trade)
  - Phase 2 (Aggressive): 0.10 (10% per trade, only if track record >6 months)
  - Phase 3 (Concentration): 0.15 (15% per trade)
  - Phase 4 (Harvest): 0.08 (8% per trade)

CycleMultiplier:
  - Bull (BTC above 200-day MA): 1.5
  - Neutral (within 10% of 200-day MA): 1.0
  - Bear (BTC below 200-day MA): 0.5
```

## Macro Cycle Timing Indicators

The dataset's equity milestones correlate with BTC macro cycles:

- **2020-Q4**: 5.73x — post-halving accumulation (BTC $10k → $30k)
- **2021-Q2**: 22.07x — bull peak before summer crash
- **2021-Q4**: 22.54x — second peak, lower growth rate = distribution signal
- **2022-Q4**: 7.13x — bear bottom, survived with 66% drawdown
- **2023-Q3**: 38.64x — recovery confirmed, concentrated BTC longs

**Timing signals to monitor**:
1. **Halving cycle**: BTC halvings (2020, 2024) precede 12-18 month bull runs
2. **MA crossover**: 50-day crossing above 200-day = aggressive entry window
3. **Funding rate**: Sustained negative funding = accumulation opportunity
4. **Exchange reserve**: Declining exchange BTC reserves = supply squeeze setup

## Analysis Workflow

When the user asks for BTC macro analysis:

1. **Identify current phase**: Map user's trading history to the 4-phase model
2. **Assess drawdown status**: Compare current drawdown to the recovery playbook
3. **Calculate position size**: Apply the sizing formula with current cycle multiplier
4. **Check macro signals**: Evaluate halving cycle, MA crossover, funding rate
5. **Generate recommendation**: Combine phase + drawdown + sizing + macro into
   a BUY/HOLD/REDUCE/EXIT verdict with confidence level (1-10)

## Integration Points

- **daily-stock-check**: Cross-reference BTC signals with broader equity market
- **trading-technical-analyst**: Use for chart-level BTC analysis (RSI, MACD, Bollinger)
- **trading-position-sizer**: Validate position sizes against portfolio-level risk
- **alphaear-sentiment**: Gauge crypto market sentiment from news sources
- **trading-market-environment-analysis**: Check global risk-on/risk-off context

## Key Constraints

- This framework is based on ONE trader's 6-year track record on BitMEX derivatives
- Past performance does not predict future results
- The 80.6% early drawdown would have wiped out most accounts — survival bias applies
- Leverage amplifies both gains and losses — never exceed 10x on BTC, 5x on altcoins
- Always maintain a cold-storage reserve separate from exchange trading capital
