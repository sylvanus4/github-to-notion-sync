# IC Memo — Investment Committee Memorandum

Draft a comprehensive investment committee memo for PE deal evaluation: executive summary, investment thesis, company overview, market analysis, financial analysis, deal structure, value creation plan, risk assessment, and returns analysis.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `private-equity` vertical plugin.

## Triggers

Use when the user asks to "write IC memo", "investment committee memo", "IC memorandum", "PE deal memo", "investment recommendation", "deal memo", "IC 메모 작성", "투자위원회 보고서", "투자 메모", "PE 딜 메모", "투자 추천서", or needs a formal document for PE investment committee review.

Do NOT use for general investment research notes (use equity-research-note). Do NOT use for quick deal screening without IC-level depth (use lbo-model for initial returns). Do NOT use for post-investment portfolio reviews.

## Required Inputs

| Input | Source |
|-------|--------|
| Company overview & history | Due diligence materials, company website |
| Historical financials (3-5 years) | CIM, audited statements |
| Management projections | Management presentation |
| Market/industry data | Industry reports, web research |
| Transaction terms | LOI, term sheet |
| Comparable transactions | Precedent transaction search |

## IC Memo Structure

### 1. Executive Summary (1 page max)
- **Deal overview**: Target, sector, transaction type, proposed price
- **Investment thesis**: 3-5 bullet points summarizing why this is attractive
- **Key financials**: Revenue, EBITDA, growth rate, proposed entry multiple
- **Returns summary**: Base case IRR, MoM, equity check
- **Recommendation**: Proceed / Pass / Conditional (with conditions)

### 2. Investment Thesis
- **Thesis pillar 1**: Market position and competitive moat
- **Thesis pillar 2**: Growth opportunity (organic + M&A)
- **Thesis pillar 3**: Operational improvement potential
- **Thesis pillar 4**: Favorable industry dynamics
- Each pillar must include supporting evidence

### 3. Company Overview
- Business description and history
- Product/service portfolio
- Customer base (concentration, retention, contract type)
- Revenue model (recurring vs. non-recurring breakdown)
- Geographic presence
- Management team assessment
- Employee overview

### 4. Market Analysis
- TAM/SAM/SOM sizing
- Growth drivers and secular trends
- Competitive landscape map
- Regulatory environment
- Customer buying behavior

### 5. Financial Analysis
- Historical P&L walkthrough with margin bridge
- Revenue build (bottom-up by segment/product)
- Working capital analysis and cash conversion cycle
- Capex requirements (maintenance vs. growth)
- Quality of earnings adjustments
- Management case vs. sponsor case comparison

### 6. Deal Structure
- Transaction overview (asset vs. stock, consideration mix)
- Sources & uses table
- Pro forma capitalization
- Key terms and conditions
- Representations & warranties highlights
- Post-close adjustments (if any)

### 7. Value Creation Plan (100-Day + 3-5 Year)
| Lever | Action | EBITDA Impact | Timeline |
|-------|--------|---------------|----------|
| Revenue growth | Expansion, pricing, new products | $XM | Year 1-3 |
| Margin improvement | Procurement, efficiency, automation | $XM | Year 1-2 |
| M&A add-ons | Identified targets, synergies | $XM | Year 2-4 |
| Multiple expansion | Growth profile improvement | Entry X.Xx → Exit Y.Yx | Exit |

### 8. Risk Assessment
For each risk:
- **Risk description**: What could go wrong
- **Probability**: High / Medium / Low
- **Impact**: Severe / Moderate / Minor
- **Mitigation**: How the risk is managed or hedged
- **Residual risk**: After mitigation

Key risk categories:
- Market/macro risks
- Customer concentration
- Key person dependency
- Integration risks (for add-ons)
- Regulatory/compliance
- Technology disruption
- Financial/leverage risks

### 9. Returns Analysis
- Base case: Entry multiple, exit multiple, hold period, IRR, MoM, equity value
- Upside case: Higher growth / margin / exit multiple
- Downside case: Revenue miss / margin compression / lower exit
- Sensitivity table: Entry multiple vs. exit multiple vs. EBITDA growth
- Minimum returns threshold: Typically IRR > 20%, MoM > 2.0x

### 10. Appendices
- Detailed financial model (link to lbo-model output)
- Comparable transactions table
- Management bios
- Customer list (redacted if confidential)
- Due diligence tracker status

## Writing Standards

- Professional, analytical tone throughout
- All claims must cite sources or be flagged as assumptions
- Financial figures must be internally consistent
- Use `[DILIGENCE NEEDED]` for items requiring further verification
- Base case must be achievable without heroic assumptions
- Bull case should not be presented as base case

## Workflow

1. Collect all available data (CIM, financials, market research)
2. Run parallel-web-search for industry context
3. Run lbo-model for returns analysis
4. Run comps-analysis for comparable valuations
5. Draft each section with supporting data
6. Cross-check internal consistency of all financial figures
7. Generate final IC memo in markdown

## Composed Skills

| Skill | Purpose |
|-------|---------|
| `lbo-model` | Returns analysis and sensitivity tables |
| `comps-analysis` | Comparable company valuation |
| `competitive-analysis` | Market positioning section |
| `three-statement-model` | Financial projections |
| `parallel-web-search` | Industry and market data |
| `anthropic-docx` | Final DOCX formatting if needed |
