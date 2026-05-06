# NAV Calc — Net Asset Value Calculation

Calculate daily fund Net Asset Value (NAV) with full audit trail: position pricing, accruals, expense allocation, and per-share NAV derivation.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `fund-administration` vertical plugin.

## Triggers

Use when the user asks to "calculate NAV", "net asset value", "fund NAV", "daily NAV", "NAV per share", "fund valuation", "NAV 계산", "순자산가치", "펀드 NAV", "일일 NAV", "주당 NAV", "펀드 밸류에이션", or needs to compute the net asset value of a fund or portfolio.

Do NOT use for single-stock valuation (use dcf-model or comps-analysis). Do NOT use for portfolio rebalancing (use portfolio-rebalance). Do NOT use for accounting reconciliation (use reconciliation skill).

## NAV Calculation Framework

### Standard NAV Formula

```
NAV per Share = (Total Assets - Total Liabilities) / Shares Outstanding
```

### Component Breakdown

```
Total Assets
  + Equity positions (mark-to-market)
  + Fixed income positions (mark-to-market or fair value)
  + Cash and cash equivalents
  + Receivables (dividends, interest, subscriptions)
  + Prepaid expenses
  + Other assets

Total Liabilities
  + Management fees payable
  + Performance fees (crystallized + accrued)
  + Administration fees payable
  + Redemptions payable
  + Accrued expenses (audit, legal, custody)
  + Pending trades (unsettled purchases)
  + Other liabilities
```

## Workflow

### Step 1: Position Pricing

For each holding, determine the fair value:

| Asset Type | Pricing Source | Methodology |
|-----------|---------------|-------------|
| Listed equity | Exchange close | Last trade price |
| OTC equity | Dealer quotes | Mid of bid/ask |
| Govt bonds | Bloomberg/Reuters | Clean price + accrued interest |
| Corporate bonds | Dealer quotes / pricing service | Evaluated price |
| Derivatives | Valuation model | Black-Scholes / Monte Carlo |
| Private assets | Last round / appraisal | Most recent fair value |

**Stale price detection**: Flag any price older than 1 business day for listed securities. Report fair value hierarchy level (Level 1/2/3).

### Step 2: Accrual Calculations

| Accrual Type | Calculation |
|-------------|-------------|
| Dividend receivable | Ex-date passed, pay-date pending |
| Bond interest | Coupon rate x days since last payment / day count |
| Management fee | AUM x fee rate x days / 365 |
| Performance fee | (NAV - HWM) x perf rate, if positive |
| Expense accrual | Annual expense / 365 x days |

### Step 3: Trade Settlement

Check for unsettled trades:
- T+1 (equities): Trades from today and yesterday
- T+1 (fixed income): Same-day settlement
- Impact on cash position and holdings

### Step 4: NAV Computation

```
Gross Asset Value (GAV)
  = Sum(position_i x price_i) + cash + receivables

Net Asset Value (NAV)
  = GAV - management_fee_accrual - perf_fee_accrual - expenses - payables

NAV per Share
  = NAV / shares_outstanding

Daily Change
  = (NAV_today - NAV_yesterday) / NAV_yesterday x 100
```

### Step 5: Control Checks

| Check | Threshold | Action if Failed |
|-------|-----------|-----------------|
| NAV day-over-day change | > 5% | Flag for review |
| Pricing completeness | 100% of positions priced | Cannot publish with gaps |
| Cash reconciliation | Matches custodian | Investigate variance |
| Share count reconciliation | Matches transfer agent | Investigate variance |
| Expense ratio | Within TER budget | Alert if exceeding |

### Step 6: Report Generation

```
## Daily NAV Report
Fund: [Fund Name]
Date: [YYYY-MM-DD]
Currency: [USD/KRW]

### NAV Summary
| Metric | Value |
|--------|-------|
| Gross Assets | $XX,XXX,XXX |
| Total Liabilities | $X,XXX,XXX |
| Net Assets | $XX,XXX,XXX |
| Shares Outstanding | X,XXX,XXX |
| NAV per Share | $XX.XXXX |
| Daily Change | +X.XX% |

### Position Detail
[Top 10 holdings by weight]

### Accruals
[Management fee, performance fee, expenses]

### Control Checks
[All pass/fail with explanations]
```

## Pricing Hierarchy (IFRS 13 / ASC 820)

| Level | Description | Example |
|-------|------------|---------|
| Level 1 | Quoted prices in active markets | NYSE-listed equities |
| Level 2 | Observable inputs, not Level 1 | Corporate bond evaluated prices |
| Level 3 | Unobservable inputs | Private company valuations |

Report the percentage of GAV at each level.

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `reconciliation` | Cash and position reconciliation |
| `parallel-web-search` | Current market prices, corporate actions |
| `anthropic-xlsx` | NAV worksheet with formulas |
| `anthropic-docx` | Investor-facing NAV report |
