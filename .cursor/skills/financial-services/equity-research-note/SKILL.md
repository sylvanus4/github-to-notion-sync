# Equity Research Note — Sell-Side Research Report

Produce institutional-quality equity research notes: investment thesis, financial model summary, valuation, catalysts, risks, and rating with price target.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `equity-research` vertical plugin.

## Triggers

Use when the user asks to "write research note", "equity research report", "initiation of coverage", "earnings review note", "stock rating", "price target analysis", "sell-side research", "리서치 노트 작성", "주식 리서치 보고서", "커버리지 개시", "실적 리뷰 노트", "투자의견", "목표주가 분석", or needs a structured equity research document.

Do NOT use for personal stock analysis without research-note format (use trading-us-stock-analysis). Do NOT use for earnings event processing (use earnings-reviewer agent). Do NOT use for quick price target checks without full analysis.

## Research Note Types

### 1. Initiation of Coverage
- Full deep-dive (20-40 pages equivalent)
- All sections below required
- Includes industry primer section

### 2. Company Update / Note
- Event-driven (5-10 pages equivalent)
- Focus on what changed and thesis impact
- Abbreviated financials

### 3. Earnings Review
- Post-results analysis (3-5 pages equivalent)
- Beat/miss analysis, guidance changes
- Model revision summary
- Typically same-day turnaround

### 4. Industry Note
- Sector-level thematic (10-20 pages equivalent)
- Cross-company comparison
- Theme-driven rather than company-specific

## Standard Research Note Structure

### Header Block
```
[Bank Name] Equity Research
[Company Name] ([Ticker])
Rating: [Buy/Hold/Sell] | Price Target: $XX
Current Price: $XX | Market Cap: $XXB
Date: [YYYY-MM-DD]
Analyst: [Name]
```

### Key Takeaways (3-5 bullets)
- Most important points for a time-constrained reader
- Each bullet is one sentence, data-backed

### Investment Thesis
- Core thesis statement (2-3 sentences)
- 3-4 supporting pillars with evidence
- Why now (catalyst or timing argument)

### Business Overview
- Company description
- Revenue breakdown by segment
- Key competitive advantages (moat analysis)
- TAM / market share

### Financial Analysis
- Revenue model (drivers by segment)
- Margin trajectory and drivers
- Cash flow analysis
- Balance sheet health (leverage ratios)
- Key metrics table:

| Metric | FY-2 | FY-1 | FY0E | FY1E | FY2E |
|--------|------|------|------|------|------|
| Revenue ($M) | | | | | |
| YoY Growth (%) | | | | | |
| Gross Margin (%) | | | | | |
| EBITDA ($M) | | | | | |
| EBITDA Margin (%) | | | | | |
| EPS ($) | | | | | |
| FCF ($M) | | | | | |

### Valuation
- Primary methodology (DCF, comps, or blended)
- Trading comps summary
- DCF summary (key assumptions, WACC, terminal)
- Price target derivation (show math)
- Valuation vs. history (current multiple vs. 3Y/5Y average)
- Football field chart specification

### Catalysts (with timeline)
| Catalyst | Expected Timeline | Thesis Impact |
|----------|------------------|---------------|
| Earnings beat | Next quarter | Positive |
| Product launch | H2 2026 | Positive |
| Regulatory decision | Q3 2026 | Binary |

### Risks
- **Bull case risks**: What could make the stock go higher than PT
- **Bear case risks**: What could cause underperformance
- Each risk quantified where possible (e.g., "10% revenue downside scenario")

### Rating Rationale
- Clear mapping from valuation to rating
- State thresholds: "We rate Buy when expected upside > 15%"
- Contrast with consensus and explain divergence

## Writing Standards

- Objective, evidence-based tone (sell-side standard)
- All projections clearly labeled as estimates
- Consensus comparison where available
- Sources cited for all third-party data
- "E" suffix for estimates (e.g., FY1E)
- Comply with research publication standards (no guarantees of returns)

## Workflow

1. Gather company filings, recent earnings, and market data
2. Run comps-analysis for peer valuation context
3. Run dcf-model for intrinsic value estimate
4. Perform web research for catalysts, recent news, industry trends
5. Build financial summary table with estimates
6. Draft each section
7. Derive price target with clear methodology
8. Cross-check all figures for consistency

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `comps-analysis` | Peer valuation multiples |
| `dcf-model` | Intrinsic value estimate |
| `three-statement-model` | Financial projections |
| `competitive-analysis` | Industry positioning |
| `parallel-web-search` | Catalysts, news, consensus data |
| `anthropic-docx` | Final report formatting |
