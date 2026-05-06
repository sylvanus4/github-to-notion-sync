# Financial Services Orchestrator — Unified FSI Skill Router

Intelligent router that classifies financial services tasks by domain and workflow type, then dispatches to the appropriate financial-services skill. Handles ambiguous requests by asking clarifying questions. Acts as the single entry point for all financial services work.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) — Anthropic FSI vertical + agent plugins.

## Triggers

Use when the user asks for general financial analysis, mentions financial services work without specifying a domain, says "financial services", "FSI analysis", "금융 분석", "금융 서비스", "financial-services-orchestrator", or any broad financial request where the specific sub-domain is not yet clear. Also use when orchestrating multi-step financial workflows that span multiple sub-skills.

Do NOT use when the user already specifies a specific financial task (route to the specific skill directly). Do NOT use for daily stock screening pipeline (use today). Do NOT use for personal portfolio trading (use trading-* skills).

## Skill Registry

### Core Financial Analysis (financial-analysis vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `dcf-model` | DCF, discounted cash flow, intrinsic value, 기업가치 평가 | Build DCF valuation models |
| `comps-analysis` | comps, comparable companies, trading multiples, 동종 기업 분석 | Peer-based relative valuation |
| `lbo-model` | LBO, leveraged buyout, sponsor returns, 차입매수 | PE acquisition analysis |
| `three-statement-model` | 3-statement, financial projections, P&L BS CF, 재무 3표 | Integrated financial model |
| `competitive-analysis` | competitive landscape, industry analysis, 경쟁사 분석 | Porter's, positioning, SWOT |
| `deck-qc` | QC deck, review presentation, 덱 QC | Presentation quality check |

### Investment Banking (investment-banking vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `pitch-deck` | pitch deck, pitch book, IB presentation, 피치 덱 | IB presentation builder |

### Private Equity (private-equity vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `ic-memo` | IC memo, investment committee, deal memo, IC 메모 | PE investment memo |

### Equity Research (equity-research vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `equity-research-note` | research note, initiation, coverage, 리서치 노트 | Sell-side research report |

### Wealth Management (wealth-management vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `portfolio-rebalance` | rebalance, allocation, drift, 리밸런싱 | Portfolio optimization |

### Fund Administration (fund-administration vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `nav-calc` | NAV, net asset value, fund valuation, NAV 계산 | Daily fund NAV calculation |

### Financial Operations (financial-operations vertical)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `reconciliation` | reconcile, trade matching, break resolution, 대사 | Position/trade/cash recon |

### Agent Workflows (agent plugins — multi-skill orchestrators)

| Skill | Trigger Keywords | Purpose |
|-------|-----------------|---------|
| `earnings-reviewer` | earnings review, earnings call, quarterly results, 실적 리뷰 | End-to-end earnings processing |
| `pitch-agent` | pitch agent, full pitch process, IB deal workflow, 피치 에이전트 | Full IB pitch orchestration |
| `market-researcher` | market research, sector research, industry report, 시장 조사 | Comprehensive sector/thematic research |

## Routing Logic

```
1. Parse user request for domain keywords
   → Match found in Skill Registry? Route to that skill. STOP.

2. No clear match? Classify by workflow type:
   - "Valuation" → Ask: DCF vs. Comps vs. LBO?
   - "Model" → Ask: 3-statement vs. DCF vs. LBO?
   - "Report" → Ask: Research note vs. IC memo vs. Market research?
   - "Review/QC" → Ask: Earnings vs. Deck QC?
   - "Portfolio" → Route to portfolio-rebalance
   - "Reconciliation" → Route to reconciliation

3. Multi-step workflow detected?
   → Decompose into sequential skill chain.
   Example: "Full deal analysis" →
     competitive-analysis → comps-analysis → dcf-model → pitch-deck → deck-qc

4. Still ambiguous?
   → Ask ONE clarifying question with options.
```

## Multi-Step Workflow Templates

### Deal Analysis Pipeline
1. `competitive-analysis` — Industry context
2. `comps-analysis` — Peer valuation benchmarks
3. `dcf-model` — Intrinsic valuation
4. `three-statement-model` — Financial projections (if needed)
5. `pitch-deck` — Client presentation
6. `deck-qc` — Quality gate

### Earnings Event Pipeline
1. `earnings-reviewer` — Orchestrates pre-earnings prep through post-earnings distribution

### Investment Evaluation Pipeline
1. `competitive-analysis` — Market positioning
2. `three-statement-model` — Financial projections
3. `lbo-model` — Returns analysis
4. `ic-memo` — Committee memorandum

### Sector Research Pipeline
1. `market-researcher` — Orchestrates full sector deep-dive with formatted report

## MCP Connectors (from source repo)

The source repository references these MCP connectors for enriched financial data. When available, skills should leverage:

| Connector | Data | Skills That Use It |
|-----------|------|-------------------|
| Daloopa | Standardized financials, KPIs | dcf-model, three-statement-model, comps-analysis |
| Morningstar | Equity data, fund analytics | comps-analysis, nav-calc, portfolio-rebalance |
| S&P Global | Market intelligence, credit ratings | competitive-analysis, market-researcher |
| FactSet | Multi-asset analytics | comps-analysis, equity-research-note |
| Moody's | Credit risk, economic forecasts | lbo-model, ic-memo |
| CapIQ | Company financials, transactions | comps-analysis, pitch-deck |
| Calcbench | SEC filings, XBRL data | three-statement-model, earnings-reviewer |

When MCP connectors are not configured, skills fall back to web search and publicly available data sources.

## Quality Gate

Before routing, verify:
- User intent is clear enough to select a skill
- Required inputs are specified (company name, ticker, etc.)
- Scope is defined (single company vs. sector vs. portfolio)

After execution, verify:
- Output format matches the skill's documented output
- Data sources are cited
- Numerical consistency across interconnected outputs
