---
name: financial-report-analyzer
description: >-
  Financial statement analysis pipeline that parses PDF reports (10-K, 10-Q,
  annual reports, earnings), extracts key financial data, computes ratios and
  trends, detects anomalies, and generates an executive briefing as .docx with
  a visual financial dashboard. Uses OpenDataLoader for high-fidelity PDF
  extraction and evaluation-engine for multi-dimensional financial health
  scoring. Use when the user asks to "analyze financial report", "parse 10-K",
  "financial statement analysis", "financial-report-analyzer", "earnings
  analysis", "재무제표 분석", "재무 리포트 분석", "10-K 파싱", "손익계산서 분석", "재무 건전성 평가", "실적
  분석", or wants to extract, analyze, and summarize financial statements from
  PDF documents. Do NOT use for stock price technical analysis (use
  trading-technical-analyst). Do NOT use for market environment analysis (use
  trading-market-environment-analysis). Do NOT use for portfolio risk
  monitoring (use toss-risk-monitor). Do NOT use for accounting journal
  entries (use kwp-finance-journal-entry-prep).
---

# Financial Report Analyzer

Parse PDF financial statements, extract key data, compute ratios, detect anomalies, and deliver executive briefings.

## When to Use

- A PDF financial report (10-K, 10-Q, annual report, earnings release) needs structured analysis
- Investor relations or finance team needs automated ratio computation and trend detection
- Board meeting preparation requires an executive financial summary
- Due diligence requires comparative financial analysis across periods

## Output Artifacts

| Phase | Stage Name         | Output File                                                       |
| ----- | ------------------ | ----------------------------------------------------------------- |
| 1     | Extract            | `outputs/financial-report-analyzer/{date}/extracted-data.md`       |
| 2     | Structure          | `outputs/financial-report-analyzer/{date}/financial-tables.md`     |
| 3     | Analyze            | `outputs/financial-report-analyzer/{date}/analysis.md`             |
| 4     | Anomalies          | `outputs/financial-report-analyzer/{date}/anomalies.md`            |
| 5     | Report             | `outputs/financial-report-analyzer/{date}/exec-briefing.docx`      |
| 5     | Dashboard          | `outputs/financial-report-analyzer/{date}/dashboard.html`          |
| 6     | Manifest           | `outputs/financial-report-analyzer/{date}/manifest.json`           |

## Workflow

### Phase 1: Extract

Accept financial document input:
- **PDF file path**: Extract via `opendataloader` for high-fidelity table preservation
- **Multiple PDFs**: Process each sequentially for period comparison
- **URL to PDF**: Download first, then extract via `opendataloader`

Extract to clean markdown preserving:
- Financial statement tables (income statement, balance sheet, cash flow)
- Notes to financial statements
- Management discussion & analysis (MD&A) sections
- Key metrics highlighted by the company

Save to `extracted-data.md`.

### Phase 2: Structure

Parse extracted content into structured financial data tables:

**Income Statement:**

| Line Item | Current Period | Prior Period | YoY Change |
|-----------|---------------|-------------|------------|
| Revenue | | | |
| Cost of Revenue | | | |
| Gross Profit | | | |
| Operating Expenses | | | |
| Operating Income | | | |
| Net Income | | | |
| EPS (Basic) | | | |
| EPS (Diluted) | | | |

**Balance Sheet:**

| Line Item | Current | Prior | Change |
|-----------|---------|-------|--------|
| Total Assets | | | |
| Current Assets | | | |
| Total Liabilities | | | |
| Current Liabilities | | | |
| Shareholders' Equity | | | |
| Cash & Equivalents | | | |

**Cash Flow Statement:**

| Line Item | Current | Prior | Change |
|-----------|---------|-------|--------|
| Operating Cash Flow | | | |
| Capital Expenditure | | | |
| Free Cash Flow | | | |
| Financing Activities | | | |

Save structured tables to `financial-tables.md`.

### Phase 3: Analyze

Compute key financial ratios and metrics:

**Profitability Ratios:**

| Ratio | Formula | Benchmark |
|-------|---------|-----------|
| Gross Margin | Gross Profit / Revenue | Industry-dependent |
| Operating Margin | Operating Income / Revenue | Industry-dependent |
| Net Margin | Net Income / Revenue | Industry-dependent |
| ROE | Net Income / Shareholders' Equity | > 15% good |
| ROA | Net Income / Total Assets | > 5% good |

**Liquidity Ratios:**

| Ratio | Formula | Benchmark |
|-------|---------|-----------|
| Current Ratio | Current Assets / Current Liabilities | > 1.5 healthy |
| Quick Ratio | (Current Assets - Inventory) / Current Liabilities | > 1.0 healthy |
| Cash Ratio | Cash / Current Liabilities | Context-dependent |

**Efficiency Ratios:**

| Ratio | Formula | Benchmark |
|-------|---------|-----------|
| Asset Turnover | Revenue / Total Assets | Industry-dependent |
| Revenue per Employee | Revenue / Headcount (if available) | Industry-dependent |

**Growth Metrics:**

| Metric | Calculation |
|--------|-------------|
| Revenue Growth (YoY) | (Current - Prior) / Prior |
| Net Income Growth | (Current - Prior) / Prior |
| EPS Growth | (Current - Prior) / Prior |
| FCF Growth | (Current - Prior) / Prior |

Score overall financial health using `evaluation-engine`:

| Dimension | Weight | Scale |
|-----------|--------|-------|
| Profitability | 0.25 | 1-10 |
| Liquidity | 0.20 | 1-10 |
| Growth | 0.25 | 1-10 |
| Efficiency | 0.15 | 1-10 |
| Cash generation | 0.15 | 1-10 |

Assign composite grade: A (8+), B (6-7.9), C (4-5.9), D (<4).

Save to `analysis.md`.

### Phase 4: Anomaly Detection

Scan for financial red flags:

| Anomaly Type | Detection Rule |
|-------------|----------------|
| Revenue-earnings divergence | Revenue growing but net income declining for 2+ periods |
| Cash flow mismatch | Net income positive but operating cash flow negative |
| Working capital deterioration | Current ratio declining quarter-over-quarter |
| Unusual expense spikes | Any expense category increasing >30% without revenue growth |
| Debt accumulation | Total debt / equity ratio increasing >20% YoY |
| Margin compression | Gross or operating margin declining 200+ bps YoY |
| Inventory buildup | Inventory growing faster than revenue |
| Receivables aging | A/R growing faster than revenue (potential collection issues) |

Classify each anomaly: Critical / Warning / Informational.

Save to `anomalies.md` with context and potential explanations.

### Phase 5: Generate Deliverables

**Executive Briefing** via `anthropic-docx`:

| Section | Content |
|---------|---------|
| 1-page executive summary | Key headline metrics + overall grade via `long-form-compressor` |
| Financial highlights | Top 5 positive metrics with context |
| Concerns | Anomalies ranked by severity |
| Ratio dashboard | All computed ratios in organized tables |
| Period comparison | Side-by-side current vs prior period |
| Outlook indicators | Growth trajectory, cash position, margin trends |

Polish Korean text via `sentence-polisher`.

**Visual Dashboard** via `visual-explainer`:
- Revenue and income trend chart (if multi-period data available)
- Ratio comparison table with color-coded benchmarks
- Anomaly severity heat map
- Financial health scorecard radar chart

Save to `exec-briefing.docx` and `dashboard.html`.

### Phase 6: Deliver

1. Write `manifest.json` with:
   - Source document metadata (filename, pages, period covered)
   - Key metrics summary (revenue, net income, EPS, FCF)
   - Health grade and score breakdown
   - Anomaly count by severity
   - File paths and timestamps

2. Push summary to Notion via `md-to-notion`

3. Post summary to Slack (if available):
   - Headline: "{Company} {Period} Financial Analysis: Grade {X}"
   - Key metrics thread
   - Anomalies thread (if Critical or Warning found)

## Multi-Period Comparison

When multiple PDF reports are provided (e.g., 3 years of 10-K filings):

1. Process each through Phases 1-3 independently
2. Build a consolidated trend table spanning all periods
3. Compute CAGR for key metrics
4. Detect multi-year trend shifts (acceleration/deceleration)
5. Include multi-year charts in the dashboard

## Examples

### Example 1: Annual report (10-K) analysis

User says: "Analyze this 10-K filing for NVDA"

Actions:
1. Parse PDF via opendataloader, extract financial statements
2. Calculate key ratios (profitability, liquidity, leverage, efficiency)
3. Detect anomalies and significant YoY changes
4. Generate executive briefing with trend charts

Result: Executive .docx with ratio analysis, anomaly flags, and 5-year trend dashboard

### Example 2: Multi-quarter comparison

User says: "Compare Q1-Q4 earnings for these 3 companies"

Actions:
1. Parse 12 quarterly reports (4 quarters x 3 companies)
2. Normalize metrics across companies
3. Generate cross-company comparison matrix with peer benchmarks

Result: Comparative analysis .docx, HTML dashboard, Slack summary

## Error Handling

If PDF extraction partially fails (corrupted tables), the analysis proceeds with available data. Missing line items are marked as "N/A" with a note in `anomalies.md` about data gaps. Ratio calculations that require missing data return "N/A" rather than incorrect values.

## Gotchas

- PDF table extraction quality depends on document formatting; `opendataloader` handles most layouts but hand-check critical numbers
- Currency must be consistent; some international filings mix currencies in footnotes
- Non-GAAP metrics (adjusted EBITDA, etc.) should be flagged as such and separated from GAAP figures
- Fiscal year-end dates vary by company; ensure period labels match actual dates, not calendar quarters
- Some 10-K filings embed tables as images rather than text; `opendataloader` OCR handles this but accuracy may be lower
- Share counts for EPS calculation should use diluted shares outstanding, not basic
