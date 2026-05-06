# DCF Model — Discounted Cash Flow Valuation

Build institutional-quality DCF valuation models with scenario analysis and sensitivity tables.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks to "build a DCF", "DCF valuation", "discounted cash flow", "value this company", "intrinsic value", "DCF 모델", "기업가치 평가", "할인현금흐름", "DCF 분석", or needs a fundamental valuation of a public or private company.

Do NOT use for comparable company analysis only (use comps-analysis). Do NOT use for LBO modeling (use lbo-model). Do NOT use for quick market multiples without cash flow projection.

## Workflow

### Step 1: Gather Historical Data

Collect 3-5 years of historical financials:
- Revenue, COGS, Gross Profit
- SG&A, R&D, EBITDA, EBIT
- Capital expenditures, D&A
- Net working capital changes
- Tax rate (effective vs statutory)
- Share count, net debt

Sources: SEC filings (10-K, 10-Q), earnings releases, financial data providers (if MCP connectors available: Daloopa, FactSet, S&P Capital IQ).

### Step 2: Build Revenue Projections

Create 3-scenario framework (Bear / Base / Bull):

| Assumption | Bear | Base | Bull |
|-----------|------|------|------|
| Revenue growth | Conservative | Consensus-aligned | Upside |
| Margin trajectory | Compression | Stable/slight improvement | Expansion |
| Terminal growth | 1.5-2.0% | 2.0-2.5% | 2.5-3.0% |

Project 5-10 years of revenue with clear driver-based assumptions:
- Volume x Price decomposition where applicable
- Segment-level build-up for multi-business companies
- TAM penetration for high-growth companies

### Step 3: Model Operating Expenses and Free Cash Flow

For each projection year:
1. COGS → Gross Profit (margin trend)
2. SG&A, R&D → EBIT (operating leverage)
3. D&A and CapEx (separately, not netted)
4. Changes in Net Working Capital
5. Tax (use marginal rate for projections)

**Free Cash Flow = EBIT × (1 - Tax Rate) + D&A - CapEx - ΔNWC**

### Step 4: Calculate WACC

Using CAPM for cost of equity:
- Risk-free rate: 10Y Treasury yield
- Equity risk premium: 5-6% (Damodaran or similar)
- Beta: regression vs S&P 500 (levered → unlevered → re-levered)
- Cost of debt: weighted average interest rate on outstanding debt
- Tax shield: marginal corporate tax rate
- Weights: market cap / (market cap + net debt)

**WACC = (E/V) × Ke + (D/V) × Kd × (1 - T)**

### Step 5: Discount Cash Flows and Terminal Value

Two terminal value approaches:
1. **Gordon Growth**: TV = FCF_terminal × (1 + g) / (WACC - g)
2. **Exit Multiple**: TV = EBITDA_terminal × Exit_Multiple

Use comps-analysis output to inform exit multiple range (median peer EV/EBITDA).

Discount all cash flows to present value using mid-year convention.

### Step 6: Bridge to Equity Value

```
Enterprise Value (sum of discounted FCFs + discounted TV)
+ Cash and equivalents
- Total debt
- Minority interest
- Preferred stock
+ Equity method investments (pro-rata)
= Equity Value
÷ Diluted shares outstanding (treasury method)
= Implied share price
```

### Step 7: Sensitivity Analysis

Build a 2-way sensitivity table:

| | WACC -0.5% | WACC Base | WACC +0.5% |
|---|---|---|---|
| **Growth -0.5%** | $XX | $XX | $XX |
| **Growth Base** | $XX | $XX | $XX |
| **Growth +0.5%** | $XX | $XX | $XX |

Also show: implied P/E, implied EV/EBITDA vs comps median.

## Output Format

Structured markdown report with:
1. Executive summary (1-paragraph verdict with price range)
2. Key assumptions table
3. Projected financials (5-10 year)
4. WACC build-up
5. DCF output with scenario ranges
6. Sensitivity tables
7. Comps cross-check (if comps-analysis was run)

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Inform terminal exit multiple and cross-check implied valuation |
| `three-statement-model` | Full financial statement projection (if deeper modeling needed) |
| `anthropic-xlsx` | Generate Excel workbook output |

## Key Assumptions to Document

- Revenue growth drivers and rationale
- Margin expansion/compression thesis
- CapEx intensity assumptions
- Working capital cycle assumptions
- Terminal growth rate justification
- Beta source and adjustment methodology
- Equity risk premium source
