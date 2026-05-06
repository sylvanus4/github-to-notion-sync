# LBO Model — Leveraged Buyout Analysis

Build a complete leveraged buyout model: sources & uses, debt schedule, operating projections, returns analysis, and sensitivity tables.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks to "build an LBO model", "leveraged buyout", "LBO analysis", "sponsor returns", "PE returns model", "LBO 모델", "차입매수 분석", "사모펀드 수익률", "LBO 분석", or needs to evaluate a PE acquisition.

Do NOT use for DCF valuation without leverage (use dcf-model). Do NOT use for comp tables only (use comps-analysis). Do NOT use for M&A merger analysis.

## Modeling Principles

1. **Left-to-right, top-to-bottom**: Inputs at top, calculations flow downward
2. **Blue for inputs, black for formulas**: Color convention for auditability
3. **No hardcoded numbers in formulas**: All assumptions in clearly labeled input cells
4. **Annual periods**: Use annual for standard LBO (quarterly only if covenant-heavy)
5. **Circular reference avoidance**: Use iterative cash sweep or copy-paste macro approach

## Workflow

### Step 1: Transaction Assumptions

| Parameter | Typical Range |
|-----------|--------------|
| Entry multiple (EV/EBITDA) | 6x-12x (sector dependent) |
| Equity contribution | 30-50% of TEV |
| Management rollover | 0-15% of equity |
| Transaction fees | 2-3% of TEV |
| Financing fees | 1-3% of debt raised |
| Holding period | 3-7 years |

### Step 2: Sources & Uses

**Uses:**
- Purchase equity value
- Refinance existing debt
- Transaction expenses (advisory, legal, accounting)
- Financing fees (capitalized and amortized)

**Sources:**
- Senior secured debt (Term Loan A, Term Loan B)
- Subordinated / mezzanine debt
- High yield bonds
- Seller financing (if applicable)
- Sponsor equity
- Management rollover equity

Verify: Total Sources = Total Uses (hard check).

### Step 3: Operating Model (5-7 Year Projection)

Build from the three-statement-model framework:
- Revenue growth by segment
- EBITDA margin trajectory (with PE value-add assumptions)
- CapEx as % of revenue
- Working capital assumptions
- Management add-backs and synergies (if bolt-on)

Key PE value creation levers to model separately:
1. Revenue growth (organic + acquisitions)
2. Margin expansion (cost optimization, pricing)
3. Multiple expansion (entry vs exit multiple delta)
4. Debt paydown (cash flow to deleverage)

### Step 4: Debt Schedule

For each tranche, model:
- Opening balance
- Mandatory amortization
- Optional prepayment / cash sweep
- Closing balance
- Interest expense (fixed vs floating + spread)

Cash sweep priority: Senior → Sub → Mezzanine → Cash build

Track leverage ratios at each year-end:
- Total Debt / EBITDA
- Senior Debt / EBITDA
- Interest Coverage (EBITDA / Interest)
- Fixed Charge Coverage

### Step 5: Returns Analysis

At each potential exit year (Year 3, 4, 5, 6, 7):

```
Exit EV = Exit EBITDA × Exit Multiple
- Net Debt at Exit
- Transaction costs at exit (1-2%)
= Equity Proceeds to Sponsor

Sponsor Equity Invested → Equity Proceeds
→ Money Multiple (MOIC) = Proceeds / Invested
→ IRR = internal rate of return over holding period
```

### Step 6: Sensitivity Tables

**Primary sensitivity**: Entry Multiple vs Exit Multiple

| | Exit 7x | Exit 8x | Exit 9x | Exit 10x |
|---|---|---|---|---|
| **Entry 8x** | IRR / MOIC | ... | ... | ... |
| **Entry 9x** | ... | ... | ... | ... |
| **Entry 10x** | ... | ... | ... | ... |

**Secondary sensitivity**: EBITDA Growth vs Leverage

**PE hurdle check**: Highlight cells meeting 20%+ IRR / 2.0x+ MOIC targets.

### Step 7: Credit Analysis

Verify the deal is financeable:
- Max leverage: typically 4-6x total debt/EBITDA
- Interest coverage > 2.0x at close
- DSCR > 1.0x in all projection years
- No covenant breach in base or downside cases

## Output Format

1. Transaction summary (1-page overview)
2. Sources & Uses table
3. Operating projections (P&L summary)
4. Debt schedule with covenant tracking
5. Returns matrix (IRR/MOIC by exit year)
6. Sensitivity tables (entry/exit multiple, growth/leverage)
7. Credit statistics over hold period

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Determine entry/exit multiple ranges from public comps |
| `three-statement-model` | Detailed financial projections feeding the LBO |
| `dcf-model` | Cross-check intrinsic value vs LBO-implied price |
| `anthropic-xlsx` | Generate Excel workbook with tabs |
