# Reconciliation — Financial Operations Reconciliation

Systematic reconciliation workflows for trade matching, position reconciliation, cash reconciliation, and break resolution in financial operations.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-operations` vertical plugin.

## Triggers

Use when the user asks to "reconcile positions", "trade reconciliation", "cash reconciliation", "break resolution", "position matching", "settlement reconciliation", "exception management", "포지션 대사", "거래 대사", "현금 대사", "불일치 해결", "정산 대사", or needs to match and verify financial data across systems.

Do NOT use for portfolio rebalancing (use portfolio-rebalance). Do NOT use for NAV calculation (use nav-calc). Do NOT use for financial statement reconciliation (use kwp-finance-reconciliation).

## Reconciliation Types

### 1. Position Reconciliation

Compare holdings across systems:

| Source A | Source B | Fields to Match |
|----------|----------|----------------|
| Internal books | Custodian records | Security, quantity, market value |
| Fund admin | Prime broker | Positions, collateral |
| Front office | Back office | Trade captures |

### 2. Cash Reconciliation

```
Internal Cash Balance (expected)
  = Opening balance
  + Settled buy/sell proceeds
  + Dividends/coupons received
  + Subscriptions received
  - Redemptions paid
  - Fees paid
  - Expenses paid
  = Expected closing balance

Custodian Cash Balance (actual)
  = Statement balance

Break = Expected - Actual
```

### 3. Trade Reconciliation

Match trades across counterparties:

| Field | Tolerance |
|-------|-----------|
| Trade date | Exact match |
| Settlement date | Exact match |
| Security identifier | ISIN/CUSIP/SEDOL match |
| Quantity | Exact match |
| Price | ±0.01% |
| Gross amount | ±$1 (rounding) |
| Net amount | ±$1 (rounding) |

### 4. Transaction Reconciliation

Match fund flows:
- Subscription/redemption orders vs. transfer agent records
- Wire transfers vs. bank statements
- Fee invoices vs. general ledger entries

## Workflow

### Step 1: Data Ingestion

Load data from both sides of the reconciliation:
- Parse CSV/Excel/SWIFT files from each source
- Normalize identifiers (ISIN → CUSIP mapping if needed)
- Standardize date formats and currencies
- Apply FX rates for cross-currency matching

### Step 2: Automated Matching

Apply matching rules in priority order:

| Priority | Rule | Description |
|----------|------|-------------|
| 1 | Exact match | All fields match within tolerance |
| 2 | Partial match | Key fields match, minor variances |
| 3 | Net match | Multiple records on one side = single record on other |
| 4 | Fuzzy match | Security name similarity + amount match |
| 5 | Unmatched | No counterpart found |

### Step 3: Break Analysis

For each unmatched item, classify the break:

| Category | Examples | Typical Resolution |
|----------|---------|-------------------|
| Timing | Trade not yet booked on one side | Wait for next day |
| Data entry | Wrong quantity, price, or date | Correct in source system |
| Missing | Trade exists in one system only | Investigate and book |
| Corporate action | Stock split, dividend not reflected | Apply corporate action |
| FX rate | Different FX rates applied | Agree on rate source |
| Settlement | Failed settlement | Coordinate with broker |

### Step 4: Resolution Workflow

```
Break Identified
  → Auto-resolve (timing, rounding)
  → Manual review (data entry, missing)
  → Escalate (>$10K, >3 days aged)
  → Write-off (approved, documented)
```

### Step 5: Reporting

```
## Reconciliation Report
Date: [YYYY-MM-DD]
Reconciliation Type: [Position/Cash/Trade]

### Summary
| Metric | Value |
|--------|-------|
| Total records (Side A) | X,XXX |
| Total records (Side B) | X,XXX |
| Auto-matched | X,XXX (XX%) |
| Manually matched | XXX (X%) |
| Open breaks | XX (X%) |
| Break value | $XXX,XXX |

### Aged Breaks
| Age | Count | Value |
|-----|-------|-------|
| 0-1 days | XX | $XX,XXX |
| 2-5 days | XX | $XX,XXX |
| 5+ days | XX | $XX,XXX |

### Break Detail
[Top breaks by value with category and proposed resolution]

### Action Items
- [Specific items requiring attention]
```

## Control Framework

| Control | Frequency | Standard |
|---------|-----------|----------|
| Position reconciliation | Daily | 100% match before NAV |
| Cash reconciliation | Daily | $0 variance tolerance |
| Trade reconciliation | T+1 | All trades matched by T+1 |
| Break aging | Daily | No breaks > 5 days without escalation |
| Management reporting | Weekly | Break trends and resolution rates |

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `nav-calc` | Upstream: clean positions required for NAV |
| `anthropic-xlsx` | Generate reconciliation worksheets |
| `anthropic-docx` | Formal reconciliation reports |
| `parallel-web-search` | Corporate action verification, market data |
