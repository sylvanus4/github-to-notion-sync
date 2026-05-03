---
name: trading-backtest-expert
description: >-
  Expert guidance for systematic backtesting of trading strategies. Use when
  developing, testing, stress-testing, or validating quantitative trading
  strategies. Covers "beating ideas to death" methodology, parameter
  robustness testing, slippage modeling, bias prevention, and interpreting
  backtest results. Use for "backtesting", "strategy validation", "로버스트니스
  테스트", "백테스트", "전략 검증", "과적합 방지". Do NOT use for daily stock signals (use
  daily-stock-check). Do NOT use for AlphaEar analysis (use
  alphaear-deepear-lite). Do NOT use for weekly price updates (use
  weekly-stock-update).
---

# Backtest Expert

Systematic approach to backtesting trading strategies based on professional methodology that prioritizes robustness over optimistic results.

## Core Philosophy

**Goal**: Find strategies that "break the least", not strategies that "profit the most" on paper.

**Principle**: Add friction, stress test assumptions, and see what survives. If a strategy holds up under pessimistic conditions, it's more likely to work in live trading.

## When to Use This Skill

Use this skill when:
- Developing or validating systematic trading strategies
- Evaluating whether a trading idea is robust enough for live implementation
- Troubleshooting why a backtest might be misleading
- Learning proper backtesting methodology
- Avoiding common pitfalls (curve-fitting, look-ahead bias, survivorship bias)
- Assessing parameter sensitivity and regime dependence
- Setting realistic expectations for slippage and execution costs

## Prerequisites

- Python 3.9+ (for evaluation script)
- No API keys required
- No external data dependencies — metrics are user-provided

## Workflow

### 1. State the Hypothesis

Define the edge in one sentence.

**Example**: "Stocks that gap up >3% on earnings and pull back to previous day's close within first hour provide mean-reversion opportunity."

If you can't articulate the edge clearly, don't proceed to testing.

### 2. Codify Rules with Zero Discretion

Define with complete specificity:
- **Entry**: Exact conditions, timing, price type
- **Exit**: Stop loss, profit target, time-based exit
- **Position sizing**: Fixed $$, % of portfolio, volatility-adjusted
- **Filters**: Market cap, volume, sector, volatility conditions
- **Universe**: What instruments are eligible

**Critical**: No subjective judgment allowed. Every decision must be rule-based and unambiguous.

### 3. Run Initial Backtest

Test over:
- **Minimum 5 years** (preferably 10+)
- **Multiple market regimes** (bull, bear, high/low volatility)
- **Realistic costs**: Commissions + conservative slippage

Examine initial results for basic viability. If fundamentally broken, iterate on hypothesis.

### 4. Stress Test the Strategy

This is where 80% of testing time should be spent.

**Parameter sensitivity**:
- Test stop loss at 50%, 75%, 100%, 125%, 150% of baseline
- Test profit target at 80%, 90%, 100%, 110%, 120% of baseline
- Vary entry/exit timing by ±15-30 minutes
- Look for "plateaus" of stable performance, not narrow spikes

**Execution friction**:
- Increase slippage to 1.5-2x typical estimates
- Model worst-case fills (buy at ask+1 tick, sell at bid-1 tick)
- Add realistic order rejection scenarios
- Test with pessimistic commission structures

**Time robustness**:
- Analyze year-by-year performance
- Require positive expectancy in majority of years
- Ensure strategy doesn't rely on 1-2 exceptional periods
- Test in different market regimes separately

**Sample size**:
- Absolute minimum: 30 trades
- Preferred: 100+ trades
- High confidence: 200+ trades

### 5. Out-of-Sample Validation

**Walk-forward analysis**:
1. Optimize on training period (e.g., Year 1-3)
2. Test on validation period (Year 4)
3. Roll forward and repeat
4. Compare in-sample vs out-of-sample performance

**Warning signs**:
- Out-of-sample <50% of in-sample performance
- Need frequent parameter re-optimization
- Parameters change dramatically between periods

### 6. Evaluate Results

**Questions to answer**:
- Does edge survive pessimistic assumptions?
- Is performance stable across parameter variations?
- Does strategy work in multiple market regimes?
- Is sample size sufficient for statistical confidence?
- Are results realistic, not "too good to be true"?

**Decision criteria**:
- ✅ **Deploy**: Survives all stress tests with acceptable performance
- 🔄 **Refine**: Core logic sound but needs parameter adjustment
- ❌ **Abandon**: Fails stress tests or relies on fragile assumptions

Use the evaluation script for a structured, quantitative assessment:

```bash
python3 .cursor/skills/trading-backtest-expert/scripts/evaluate_backtest.py \
  --total-trades 150 \
  --win-rate 62 \
  --avg-win-pct 1.8 \
  --avg-loss-pct 1.2 \
  --max-drawdown-pct 15 \
  --years-tested 8 \
  --num-parameters 3 \
  --slippage-tested \
  --output-dir outputs/reports/trading/
```

The script scores across 5 dimensions (Sample Size, Expectancy, Risk Management, Robustness, Execution Realism), detects red flags, and outputs a Deploy/Refine/Abandon verdict.

## Key Testing Principles

### Punish the Strategy

Add friction everywhere:
- Commissions higher than reality
- Slippage 1.5-2x typical
- Worst-case fills
- Order rejections
- Partial fills

**Rationale**: Strategies that survive pessimistic assumptions often outperform in live trading.

### Seek Plateaus, Not Peaks

Look for parameter ranges where performance is stable, not optimal values that create performance spikes.

**Good**: Strategy profitable with stop loss anywhere from 1.5% to 3.0%
**Bad**: Strategy only works with stop loss at exactly 2.13%

Stable performance indicates genuine edge; narrow optima suggest curve-fitting.

### Test All Cases, Not Cherry-Picked Examples

**Wrong approach**: Study hand-picked "market leaders" that worked
**Right approach**: Test every stock that met criteria, including those that failed

Selective examples create survivorship bias and overestimate strategy quality.

### Separate Idea Generation from Validation

**Intuition**: Useful for generating hypotheses
**Validation**: Must be purely data-driven

Never let attachment to an idea influence interpretation of test results.

## Common Failure Patterns

Recognize these patterns early to save time:

1. **Parameter sensitivity**: Only works with exact parameter values
2. **Regime-specific**: Great in some years, terrible in others
3. **Slippage sensitivity**: Unprofitable when realistic costs added
4. **Small sample**: Too few trades for statistical confidence
5. **Look-ahead bias**: "Too good to be true" results
6. **Over-optimization**: Many parameters, poor out-of-sample results

See `references/failed_tests.md` for detailed examples and diagnostic framework.

## Standard Response Format (Every Engagement)

Unless the user only needs a one-line clarification, structure answers with these **labeled sections**:

1. **Hypothesis restatement** — One sentence rule set (entry/exit/universe).
2. **Test plan** — Data range, costs/slippage assumptions, parameter grid (if any).
3. **Results snapshot** — Table of key metrics the user supplied (trades, win%, avg W/L, max DD, years).
4. **Stress & robustness** — Bullet findings (parameter plateaus, regime split, OOS decay).
5. **Biases & caveats** — Look-ahead, survivorship, liquidity, corporate actions.
6. **Verdict** — **Deploy / Refine / Abandon** with one-sentence justification.
7. **Next experiments** — Numbered list of **actionable** follow-up tests (max 5).

**Actionable close**: Section 6 must give a **single** verdict label; Section 7 must list **at least one** concrete next step.

**Numeric grounding**: When discussing the user's backtest, quote **≥3** numeric inputs they provided (e.g., trade count, win rate %, drawdown %)—never invent backtest stats.

**Risk awareness**: Section 5 or 6 must mention **at least one** failure mode (e.g., "breaks if slippage > X bps" or "sample <30 trades").

## Output

- `outputs/reports/trading/backtest_eval_<timestamp>.json` — structured evaluation with per-dimension scores, red flags, and verdict
- `outputs/reports/trading/backtest_eval_<timestamp>.md` — human-readable report with dimension table, key metrics, and red flag details

## Resources

### Methodology Reference
**File**: `references/methodology.md`

**When to read**: For detailed guidance on specific testing techniques.

**Contents**:
- Stress testing methods
- Parameter sensitivity analysis
- Slippage and friction modeling
- Sample size requirements
- Market regime classification
- Common biases and pitfalls (survivorship, look-ahead, curve-fitting, etc.)

### Failed Tests Reference
**File**: `references/failed_tests.md`

**When to read**: When strategy fails tests, or learning from past mistakes.

**Contents**:
- Why failures are valuable
- Common failure patterns with examples
- Case study documentation framework
- Red flags checklist for evaluating backtests

## Critical Reminders

**Time allocation**: Spend 20% generating ideas, 80% trying to break them.

**Context-free requirement**: If strategy requires "perfect context" to work, it's not robust enough for systematic trading.

**Red flag**: If backtest results look too good (>90% win rate, minimal drawdowns, perfect timing), audit carefully for look-ahead bias or data issues.

**Tool limitations**: Understand your backtesting platform's quirks (interpolation methods, handling of low liquidity, data alignment issues).

**Statistical significance**: Small edges require large sample sizes to prove. 5% edge per trade needs 100+ trades to distinguish from luck.

## Discretionary vs Systematic Differences

This skill focuses on **systematic/quantitative** backtesting where:
- All rules are codified in advance
- No discretion or "feel" in execution
- Testing happens on all historical examples, not cherry-picked cases
- Context (news, macro) is deliberately stripped out

Discretionary traders study differently—this skill may not apply to setups requiring subjective judgment.

## Examples

### Example 1: Strategy stress test evaluation
**User:** "I backtested a gap-up mean reversion strategy: 150 trades, 62% win rate, 1.8% avg win, 1.2% avg loss, 15% max drawdown over 8 years. Run the evaluation script and tell me if it's deployable."
**Action:** Runs `evaluate_backtest.py` with the provided metrics, evaluates across 5 dimensions, checks for red flags, and produces Deploy/Refine/Abandon verdict.
**Output:** Structured JSON + Markdown report with per-dimension scores, red flag analysis, and actionable verdict with rationale.

### Example 2: Parameter sensitivity guidance
**User:** "My breakout strategy only works with stop loss at exactly 2.13%. Is that robust?"
**Action:** Applies "Seek Plateaus, Not Peaks" principle and explains why narrow optima suggest curve-fitting; guides user to test 50%/75%/100%/125%/150% of baseline stop to find stable performance ranges.
**Output:** Explanation of parameter robustness testing methodology and recommended next steps.

### Example 3: Out-of-sample validation
**User:** "My walk-forward backtest shows out-of-sample Sharpe is 40% of in-sample. What does that mean?"
**Action:** Interprets the degradation against the 50% threshold and explains warning signs (frequent re-optimization needed, regime dependence).
**Output:** Assessment of whether the strategy is likely overfit and guidance on whether to refine or abandon.

## Error Handling

| Error | Action |
|-------|--------|
| Evaluate script fails with missing args | Ensure `--total-trades`, `--win-rate`, `--avg-win-pct`, `--avg-loss-pct`, `--max-drawdown-pct`, `--years-tested` are all provided |
| Results look "too good to be true" (>90% win rate) | Audit for look-ahead bias, survivorship bias, or data alignment issues; add slippage/friction |
| Sample size &lt;30 trades | Do not proceed to deployment; run longer history or broaden universe to increase trade count |
| Python script not found | Verify path: `.cursor/skills/trading-backtest-expert/scripts/evaluate_backtest.py` |
