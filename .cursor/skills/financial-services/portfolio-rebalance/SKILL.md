# Portfolio Rebalance — Wealth Management Portfolio Optimization

Analyze current portfolio allocation, identify drift from target, generate rebalancing recommendations with tax-aware trade lists and compliance checks.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `wealth-management` vertical plugin.

## Triggers

Use when the user asks to "rebalance portfolio", "portfolio optimization", "asset allocation review", "drift analysis", "tactical rebalance", "strategic rebalance", "포트폴리오 리밸런싱", "자산 배분 검토", "포트폴리오 최적화", "드리프트 분석", "전술적 리밸런스", or needs to realign a portfolio to target allocations.

Do NOT use for single-stock position sizing (use trading-position-sizer). Do NOT use for portfolio risk monitoring only (use toss-risk-monitor). Do NOT use for initial portfolio construction without existing holdings.

## Rebalancing Approaches

### 1. Calendar Rebalance
- Fixed schedule (monthly, quarterly, annually)
- Simple to implement, predictable turnover

### 2. Threshold / Drift Rebalance
- Triggered when allocation drifts beyond tolerance bands
- Typical bands: +/- 5% absolute or 25% relative

### 3. Tactical Overlay
- Active tilt based on market conditions
- Overlay on strategic allocation with risk budget

## Workflow

### Step 1: Current State Analysis

Gather current holdings:
- Position-by-position holdings with quantities and market values
- Calculate current allocation percentages by:
  - Asset class (equity, fixed income, alternatives, cash)
  - Geography (US, international developed, EM)
  - Sector
  - Individual position concentration

### Step 2: Target Allocation Comparison

| Asset Class | Target (%) | Current (%) | Drift (%) | Status |
|-------------|-----------|------------|----------|--------|
| US Equity | 40 | 45 | +5.0 | Over |
| Intl Equity | 20 | 17 | -3.0 | Under |
| Fixed Income | 30 | 28 | -2.0 | Within |
| Alternatives | 5 | 5 | 0.0 | On Target |
| Cash | 5 | 5 | 0.0 | On Target |

Flag positions where drift exceeds tolerance band.

### Step 3: Rebalancing Trade List

Generate specific trades to return to target:

| Action | Security | Shares | Est. Amount | Purpose |
|--------|----------|--------|-------------|---------|
| SELL | SPY | 50 | $25,000 | Reduce US equity overweight |
| BUY | VXUS | 200 | $12,000 | Increase intl equity |
| BUY | AGG | 100 | $10,000 | Increase fixed income |

### Step 4: Tax Impact Analysis

For taxable accounts:
- **Tax lot review**: Identify lots with short-term vs. long-term gains
- **Loss harvesting**: Flag positions with unrealized losses for harvesting
- **Wash sale check**: Verify no wash sale violations
- **Estimated tax impact**: Calculate expected capital gains/losses

```
Tax Impact Summary:
- Short-term gains realized: $X,XXX (taxed at ordinary income rate)
- Long-term gains realized: $X,XXX (taxed at LTCG rate)
- Losses available for harvest: $X,XXX
- Net tax impact estimate: $X,XXX
```

### Step 5: Compliance Checks

- [ ] No single position exceeds concentration limit (default: 10%)
- [ ] Sector exposure within policy bands
- [ ] Cash reserve meets minimum requirement
- [ ] No prohibited securities in trade list
- [ ] Round lots where practical (minimize odd lots)
- [ ] ADV check: trade size vs. average daily volume

### Step 6: Execution Plan

- Priority ordering (most out-of-band positions first)
- Market vs. limit order recommendations
- Staging for large rebalances (multi-day execution)
- Settlement date awareness (T+1 equity, T+1 fixed income)

## Output Format

```
## Portfolio Rebalance Report
Date: [YYYY-MM-DD]
Account: [Account Name/ID]
Portfolio Value: $X,XXX,XXX

### Drift Summary
[Asset class drift table]

### Recommended Trades
[Trade list with rationale]

### Tax Considerations
[Tax lot analysis and harvesting opportunities]

### Compliance Check
[All items pass/fail]

### Execution Notes
[Timing, order type, staging recommendations]
```

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Peer assessment for individual holdings |
| `parallel-web-search` | Current market conditions, tax law updates |
| `anthropic-xlsx` | Trade list export |
| `anthropic-docx` | Client-facing rebalance report |
