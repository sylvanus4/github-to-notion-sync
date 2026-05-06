# Comps Analysis — Comparable Company Valuation

Identify peer companies, pull trading metrics, calculate valuation multiples, and produce a formatted comp table with median/mean statistics.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `financial-analysis` vertical plugin.

## Triggers

Use when the user asks for "comps analysis", "comparable companies", "trading comps", "peer valuation", "relative valuation", "comp table", "동종 기업 분석", "비교 기업 분석", "밸류에이션 멀티플", "Comps", or needs a peer-based valuation framework.

Do NOT use for DCF valuation (use dcf-model). Do NOT use for precedent transactions (different methodology). Do NOT use for LBO analysis (use lbo-model).

## Workflow

### Step 1: Identify Comparable Companies

Select 4-8 peers based on:
- **Business model similarity**: revenue model, customer type, go-to-market
- **Industry/sector**: same GICS sub-industry preferred
- **Size**: within 0.3x-3.0x of target market cap (flexible for unique businesses)
- **Geography**: same primary market exposure
- **Growth profile**: similar revenue growth trajectory

Document inclusion/exclusion rationale for each candidate.

### Step 2: Gather Financial Data

For each comp, collect:

| Metric | Source Period |
|--------|-------------|
| Market Cap | Current |
| Enterprise Value | Current (Market Cap + Net Debt + Minority Interest + Preferred - Cash) |
| Revenue | LTM, CY, CY+1, CY+2 |
| EBITDA | LTM, CY, CY+1, CY+2 |
| EBIT | LTM, CY, CY+1, CY+2 |
| Net Income / EPS | LTM, CY, CY+1, CY+2 |
| Revenue Growth | YoY for each period |
| EBITDA Margin | For each period |
| Net Debt | Current |
| FCF Yield | LTM |

Sources: financial data providers, SEC filings, consensus estimates.

### Step 3: Calculate Valuation Multiples

Core multiples:
- **EV/Revenue**: CY, CY+1, CY+2
- **EV/EBITDA**: LTM, CY, CY+1, CY+2
- **EV/EBIT**: CY, CY+1
- **P/E**: LTM, CY, CY+1
- **PEG Ratio**: P/E ÷ Earnings Growth
- **EV/FCF**: LTM

Growth-adjusted:
- **EV/Revenue/Growth** (for high-growth SaaS/tech)
- **Rule of 40** score (Revenue Growth + EBITDA Margin)

### Step 4: Statistical Analysis

For each multiple, calculate:
- Mean (exclude outliers > 2σ)
- Median (primary reference point)
- 25th / 75th percentile (valuation range)
- High / Low

Flag any comps trading at extreme premiums/discounts and note potential reasons (M&A speculation, restructuring, one-time events).

### Step 5: Apply to Target

```
Implied EV = Target Metric × Comp Median Multiple
Implied Equity = Implied EV - Net Debt + Cash
Implied Price = Implied Equity ÷ Diluted Shares
```

Generate a range using 25th-75th percentile of comp multiples.

### Step 6: Football Field Summary

Present all valuation approaches in a horizontal bar chart format:

```
EV/Revenue CY+1:    |----[====]------|  $XX - $XX
EV/EBITDA CY+1:     |------[===]----|  $XX - $XX
P/E CY+1:           |---[=====]-----|  $XX - $XX
Current Price:       |--------X------|  $XX
```

## Output Format

1. Peer selection rationale (table with inclusion criteria)
2. Detailed comp table (all metrics, multiples)
3. Statistical summary (mean, median, quartiles)
4. Implied valuation range per multiple
5. Football field visualization (text-based)
6. Key observations and caveats

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `dcf-model` | Cross-reference intrinsic value vs relative value |
| `competitive-analysis` | Deeper qualitative comparison of business models |
| `anthropic-xlsx` | Export comp table to Excel workbook |
