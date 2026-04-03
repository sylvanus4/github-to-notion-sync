---
name: marketing-finance-ops
version: 1.0.0
description: Marketing-specific financial operations — CFO briefing generation from QuickBooks data, marketing spend scenario modeling, development cost estimation, and ROI analysis.
---

# Marketing Finance Ops

Marketing-focused financial operations. Generates CFO-grade briefings from QuickBooks exports, models marketing spend scenarios, estimates development costs, and analyzes AI tool ROI.

## Triggers

Use when the user asks to:

- "marketing ROI", "CFO briefing", "marketing budget scenario", "cost estimation"
- "marketing spend analysis", "runway analysis", "burn rate"
- "마케팅 ROI", "CFO 브리핑", "마케팅 예산 시나리오"

## Do NOT Use

- For corporate accounting and reconciliation → use `kwp-finance-*` skills
- For financial statements generation → use `kwp-finance-financial-statements`
- For general variance analysis → use `kwp-finance-variance-analysis`
- For audit support → use `kwp-finance-audit-support`

## Prerequisites

- Python 3.10+
- QuickBooks CSV/XLSX export files
- `pip install pandas openpyxl`

## Execution Steps

### Step 1: CFO Analysis

Run `scripts/cfo-analyzer.py --input <quickbooks_export>` to generate anomaly detection, burn rate analysis, and runway projection.

### Step 2: Scenario Modeling

Run `scripts/scenario-modeler.py` with growth/contraction scenarios to model marketing spend impact on revenue.

### Step 3: Cost Estimation

Analyze codebase or project scope using rates from `references/rates.md` and overhead from `references/org-overhead.md`.

### Step 4: Report Generation

Format output using `references/output-template.md` with metrics from `references/metrics-guide.md`.

## Reference Files

- `references/metrics-guide.md` — KPI definitions and benchmarks
- `references/rates.md` — Market rate data for cost estimation
- `references/org-overhead.md` — Organizational overhead multipliers
- `references/team-cost.md` — Team composition cost models
- `references/claude-roi.md` — AI tool ROI calculation framework
- `references/quickbooks-formats.md` — QB export format guide
- `references/output-template.md` — Report template

## Examples

### Example 1: Generate a CFO briefing

User: "Create a CFO briefing from our latest QuickBooks export"

1. Run `scripts/cfo-analyzer.py --input exports/q1-2026.csv`

Result: Anomaly detection report, burn rate analysis, and 12-month runway projection.

### Example 2: Model growth scenarios

User: "What happens if we double marketing spend next quarter?"

1. Run `scripts/scenario-modeler.py --base-spend 50000 --scenarios "2x,1.5x,0.5x"`

Result: Three scenario projections with revenue impact, break-even timeline, and risk assessment.

## Error Handling

| Error | Action |
|-------|--------|
| QuickBooks CSV format mismatch | Consult `references/quickbooks-formats.md` for expected columns |
| Missing pandas/openpyxl | Install: `pip install pandas openpyxl` |
| Insufficient data for projection | Minimum 3 months of financial data recommended |
| Currency mismatch | Specify currency in input or use `--currency USD` flag |

## Output

- CFO briefing document (markdown)
- Scenario comparison matrix
- Cost estimation breakdown
- ROI analysis with confidence intervals
