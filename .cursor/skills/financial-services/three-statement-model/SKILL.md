# Three-Statement Model — Integrated Financial Projections

Build a fully integrated income statement, balance sheet, and cash flow statement model with linked circular references resolved.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks to "build a three-statement model", "integrated financial model", "financial projections", "3-statement model", "P&L BS CF model", "재무 3표 모델", "통합 재무 모델", "재무 추정", "손익 대차 현금흐름", or needs detailed multi-year financial forecasting.

Do NOT use for DCF valuation only (use dcf-model). Do NOT use for LBO-specific modeling (use lbo-model, which calls this skill internally). Do NOT use for simple comp tables (use comps-analysis).

## Modeling Standards

- **Periods**: 3 years historical + 5 years projected (adjustable)
- **Frequency**: Annual (quarterly only when user specifies)
- **Color code**: Blue = input/assumption, Black = formula
- **No circular references**: Use iterative method or copy-paste macro for interest ↔ cash balance circularity
- **Units**: Consistent (millions unless stated otherwise)

## Workflow

### Step 1: Gather Historical Data

Collect 3 years of:
- Income statements (revenue through net income)
- Balance sheets (all major line items)
- Cash flow statements (operating, investing, financing)
- Key per-share data and share count

Sources: SEC filings (10-K), CapIQ, Bloomberg, company IR page.

### Step 2: Revenue Build

Choose the appropriate approach:
| Approach | When to Use |
|----------|-------------|
| Top-down | Market size × share × pricing |
| Bottom-up | Units × ASP by product/segment |
| Growth rate | Mature business, stable growth |
| Segment build | Diversified company with distinct segments |

For each segment:
- Historical growth rates (CAGR, YoY)
- Management guidance
- Analyst consensus
- Industry growth benchmarks

### Step 3: Cost Structure

**COGS / Cost of Revenue:**
- Gross margin trend analysis
- Fixed vs variable cost decomposition
- Input cost assumptions (raw materials, labor)

**Operating Expenses:**
- SGA as % of revenue (with scale leverage assumptions)
- R&D as % of revenue (sector benchmarks)
- D&A from asset schedule (link to CapEx)

**Below the line:**
- Interest income/expense (links to debt schedule)
- Other income/expense
- Tax rate (effective vs statutory, DTA/DTL)

### Step 4: Balance Sheet Build

**Assets:**
- Cash & equivalents (plug from CF statement)
- Accounts receivable (DSO × revenue / 365)
- Inventory (DIO × COGS / 365)
- PP&E schedule (opening + CapEx - D&A - disposals)
- Intangibles amortization schedule
- Other assets (grow with revenue or flat)

**Liabilities:**
- Accounts payable (DPO × COGS / 365)
- Accrued liabilities
- Debt schedule (current + long-term, link to financing)
- Deferred revenue (if applicable)

**Equity:**
- Retained earnings (opening + net income - dividends)
- Share repurchases (treasury stock method)
- AOCI, NCI if applicable

**Balance check**: Total Assets = Total Liabilities + Equity (every period).

### Step 5: Cash Flow Statement

**Operating:**
- Net income
- Add back: D&A, SBC, deferred taxes
- Working capital changes (AR, Inv, AP, Accrued)

**Investing:**
- CapEx (maintenance + growth, separately if possible)
- Acquisitions (if modeled)
- Asset disposals

**Financing:**
- Debt issuance / repayment
- Dividends
- Share repurchases
- Equity issuance

**Ending cash** = Beginning cash + Operating CF + Investing CF + Financing CF

### Step 6: Circularity Resolution

Interest expense depends on average debt balance.
Cash balance depends on interest expense.
This creates a circular reference.

Resolution approach:
1. Calculate interest on beginning-of-period balances (no circularity, slight inaccuracy)
2. OR use average balance with iterative calculation enabled
3. Flag which method is used

### Step 7: Sanity Checks

Build an automated check sheet:
- [ ] BS balances every period
- [ ] Cash flow reconciles to BS cash change
- [ ] Net income flows correctly to retained earnings
- [ ] D&A ≤ PP&E beginning balance
- [ ] Interest expense directionally consistent with debt levels
- [ ] Tax rate within reasonable range (15-30% for US corps)
- [ ] Working capital days within industry norms

## Output Format

1. Assumptions page (all blue inputs in one place)
2. Income statement (historical + projected)
3. Balance sheet (historical + projected)
4. Cash flow statement (historical + projected)
5. Supporting schedules (debt, PP&E, working capital, shares)
6. Check sheet with all validations

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Benchmark margins and growth vs peers |
| `dcf-model` | Use projections as DCF input |
| `lbo-model` | Provide operating model for LBO returns |
| `anthropic-xlsx` | Generate formatted Excel workbook |
