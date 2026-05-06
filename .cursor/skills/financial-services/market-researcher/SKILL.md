# Market Researcher — Sector & Thematic Research Agent

Produce comprehensive sector or thematic market research: industry deep-dive, competitive landscape, market sizing, trend analysis, investment implications, and formatted research report — orchestrating multiple skills.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `market-researcher` agent plugin.

## Triggers

Use when the user asks to "market research", "sector research", "industry analysis report", "thematic research", "market deep-dive", "sector overview", "industry report", "시장 조사", "섹터 리서치", "산업 분석 보고서", "테마 리서치", "시장 심층 분석", "업종 분석", or needs a comprehensive research report on an industry, sector, or investment theme.

Do NOT use for single-company equity research (use equity-research-note). Do NOT use for daily market environment analysis (use trading-market-environment-analysis). Do NOT use for competitive intelligence without research report output (use competitive-analysis).

## Agent Artifacts

| Artifact | Description |
|----------|-------------|
| Industry overview | Market definition, structure, value chain, regulatory environment |
| Market sizing | TAM/SAM/SOM with growth projections and methodology |
| Competitive landscape | Key players, market share, positioning matrix |
| Trend analysis | Secular trends, disruption vectors, technology shifts |
| Investment framework | Sector picks, risk factors, catalyst calendar |
| Formatted report | Professional research report as .docx |

## Workflow

### Phase 1: Scope Definition

Clarify the research scope with the user:
- **Sector or theme**: Which industry vertical or cross-cutting theme?
- **Geography**: Global, regional, or country-specific?
- **Depth**: Overview (10-page) or deep-dive (30+ page)?
- **Investment angle**: Buy-side (stock picks) or sell-side (coverage initiation)?
- **Time horizon**: Near-term catalysts or secular multi-year thesis?

### Phase 2: Data Collection [parallel]

**Skills: `parallel-web-search`, `parallel-deep-research`, `comps-analysis`**

Run 4 parallel research streams:

1. **Industry structure**
   - Value chain mapping
   - Key participants by segment
   - Regulatory framework and recent policy changes
   - Industry associations and data sources

2. **Market data**
   - Market size estimates from multiple sources (cross-verify)
   - Growth rates (historical 5Y, projected 5Y)
   - Segmentation by product, geography, end-market
   - Pricing trends and unit economics

3. **Competitive dynamics**
   - Market share data and trends
   - Recent M&A and strategic moves
   - New entrants and disruptors
   - Barriers to entry analysis

4. **Trend analysis**
   - Technology disruption vectors
   - Consumer/enterprise behavior shifts
   - Regulatory tailwinds/headwinds
   - ESG and sustainability factors

### Phase 3: Analysis Framework [sequential]

**Skill: `competitive-analysis`**

1. **Porter's Five Forces** for the sector
2. **PESTLE analysis** (Political, Economic, Social, Tech, Legal, Environmental)
3. **Industry lifecycle positioning** (growth, maturity, decline)
4. **Key success factors** for participants
5. **Risk factor taxonomy** (cyclical, regulatory, technology, competitive)

### Phase 4: Investment Implications [sequential]

**Skills: `comps-analysis`, `dcf-model`**

1. **Sector valuation context**
   - Historical sector P/E, EV/EBITDA ranges
   - Current valuation vs. historical average
   - Premium/discount drivers

2. **Sub-sector screening**
   - Identify attractively valued sub-segments
   - Map growth-value quadrant for sub-sectors

3. **Company selection** (if buy-side angle)
   - Screen for best-positioned companies
   - Preliminary comps table for top 5-8 names
   - Catalyst identification for each

4. **Risk assessment**
   - Key risks with probability and impact
   - Scenario analysis (bull/base/bear for the sector)
   - Hedging considerations

### Phase 5: Report Generation

**Skills: `anthropic-docx`, `deck-qc`**

Produce the formatted research report:

```
1. Executive Summary (1-2 pages)
2. Industry Overview
   2.1 Market Definition & Scope
   2.2 Value Chain
   2.3 Regulatory Environment
3. Market Sizing & Growth
   3.1 TAM/SAM/SOM
   3.2 Historical Growth Analysis
   3.3 Growth Projections
   3.4 Key Growth Drivers
4. Competitive Landscape
   4.1 Market Share Analysis
   4.2 Competitive Positioning Matrix
   4.3 Recent Strategic Moves
   4.4 Barriers to Entry
5. Trend Analysis
   5.1 Technology Trends
   5.2 Consumer/Enterprise Shifts
   5.3 Regulatory Outlook
6. Investment Framework
   6.1 Sector Valuation Context
   6.2 Sub-Sector Attractiveness
   6.3 Company Selection Criteria
   6.4 Top Picks (if applicable)
7. Risk Assessment
   7.1 Key Risks
   7.2 Scenario Analysis
   7.3 Catalyst Calendar
8. Appendix
   8.1 Methodology Notes
   8.2 Data Sources
   8.3 Detailed Comps Tables
```

### Phase 6: Quality Control & Distribution

**Skill: `deck-qc`**

- Verify all market size figures are sourced
- Cross-check growth rate calculations
- Ensure competitive data is current (within 6 months)
- Validate that investment implications follow from the analysis
- Check formatting and professional standards

## Composed Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `parallel-web-search` | 2 | Multi-source data gathering |
| `parallel-deep-research` | 2 | Deep research on complex topics |
| `competitive-analysis` | 3 | Structured analytical frameworks |
| `comps-analysis` | 4 | Sector valuation context |
| `dcf-model` | 4 | Company-level valuation (if needed) |
| `anthropic-docx` | 5 | Formatted report generation |
| `deck-qc` | 6 | Quality verification |
| `anthropic-xlsx` | 5 | Data tables and models |

## Quality Standards

- Market size estimates must cite at least 2 independent sources
- Growth projections must state methodology (top-down vs. bottom-up)
- Competitive data must be dated (when was market share last measured?)
- Every assertion about trends must cite evidence
- Investment implications must be actionable (not just descriptive)
- Distinguish clearly between facts, estimates, and opinions
