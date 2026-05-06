# Pitch Agent — Investment Banking Deal Orchestrator

End-to-end investment banking agent that orchestrates the full pitch process: company analysis, valuation work, deal positioning, deck population, and QC — composing multiple financial analysis skills into a unified deal workflow.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `pitch-agent` agent plugin.

## Triggers

Use when the user asks to "run pitch agent", "IB deal workflow", "full pitch process", "end-to-end deal analysis", "sell-side pitch workflow", "buy-side pitch workflow", "management presentation workflow", "피치 에이전트", "IB 딜 워크플로우", "전체 피치 프로세스", "딜 분석 워크플로우", or needs to orchestrate the complete investment banking pitch process from analysis through deck delivery.

Do NOT use for single DCF valuation only (use dcf-model). Do NOT use for deck formatting only (use pitch-deck). Do NOT use for comps table only (use comps-analysis). Do NOT use for deck quality check only (use deck-qc).

## Agent Artifacts

The Pitch Agent produces these deliverables sequentially:

| Artifact | Description | Depends On |
|----------|-------------|------------|
| Company profile | Business overview, financial summary, market position | — |
| Trading comps | Peer universe with valuation multiples | Company profile |
| Transaction comps | Relevant precedent transactions | Company profile |
| DCF valuation | Intrinsic value with scenario analysis | Trading comps |
| Football field | Consolidated valuation summary chart | All valuations |
| Pitch deck | Populated presentation sections | All above |
| QC report | Quality verification of final deliverable | Pitch deck |

## Workflow

### Phase 1: Company Analysis [sequential]

**Skill: `competitive-analysis` + `parallel-web-search`**

1. Gather comprehensive company profile:
   - Business description, segments, key products/services
   - Revenue model and growth drivers
   - Management team and ownership structure
   - Recent strategic events (M&A, restructuring, new launches)

2. Market and competitive positioning:
   - Industry overview and market sizing
   - Competitive landscape and market share
   - Key differentiators and competitive advantages
   - Industry trends and tailwinds/headwinds

### Phase 2: Valuation Work [parallel where possible]

**Skills: `comps-analysis`, `dcf-model`, `three-statement-model`**

Run in parallel:
1. **Trading comps** (`comps-analysis`):
   - Select 4-6 comparable public companies
   - Pull EV/Revenue, EV/EBITDA, P/E multiples (NTM and LTM)
   - Calculate mean/median with and without outliers

2. **Transaction comps** (`parallel-web-search` + structured analysis):
   - Identify 5-10 relevant precedent transactions
   - Pull transaction multiples (EV/Revenue, EV/EBITDA)
   - Note premium paid, deal type, strategic vs. financial buyer

3. **DCF valuation** (`dcf-model`):
   - Build 5-year projection using `three-statement-model`
   - Apply WACC range from comps beta analysis
   - Terminal value via both perpetuity growth and exit multiple
   - Sensitivity tables (WACC × growth, WACC × exit multiple)

### Phase 3: Valuation Synthesis

**Football field construction:**

```
Methodology          Low        Mid        High
──────────────────────────────────────────────
Trading Comps       $XX.XX    $XX.XX     $XX.XX
Transaction Comps   $XX.XX    $XX.XX     $XX.XX
DCF (base)          $XX.XX    $XX.XX     $XX.XX
52-Week Range       $XX.XX    $XX.XX     $XX.XX
Analyst Targets     $XX.XX    $XX.XX     $XX.XX
──────────────────────────────────────────────
```

Reconcile ranges and identify the implied valuation range.

### Phase 4: Deal Positioning

Based on the deal context (sell-side, buy-side, or strategic alternatives):

1. **Sell-side**: Frame valuation to maximize seller's outcome
   - Emphasize premium methodologies
   - Highlight strategic value and synergy potential
   - Position floor price with support from multiple methodologies

2. **Buy-side**: Frame valuation for disciplined acquisition
   - Focus on downside protection methodologies
   - Emphasize standalone value vs. synergy-adjusted
   - Identify negotiation leverage points

3. **Strategic alternatives**: Present full range objectively
   - Status quo DCF vs. sale vs. merger vs. IPO vs. recapitalization
   - Risk-adjusted NPV for each alternative
   - Timeline and execution risk comparison

### Phase 5: Deck Population

**Skill: `pitch-deck`**

Populate the pitch deck sections:
1. Situation overview
2. Company overview and financial summary
3. Market and competitive analysis
4. Valuation analysis (comps, DCF, football field)
5. Transaction considerations
6. Appendix (detailed model outputs, methodology notes)

### Phase 6: Quality Control

**Skill: `deck-qc`**

Run comprehensive QC:
- Data consistency across all slides
- Source verification for all figures
- Formatting standards compliance
- Numerical formatting consistency
- Chart and table integrity
- Disclaimer and compliance check

## Composed Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `competitive-analysis` | 1 | Market positioning and industry analysis |
| `comps-analysis` | 2 | Trading comparable companies |
| `three-statement-model` | 2 | Financial projections for DCF |
| `dcf-model` | 2 | Discounted cash flow valuation |
| `pitch-deck` | 5 | Deck content population |
| `deck-qc` | 6 | Final quality verification |
| `parallel-web-search` | 1, 2 | Market data and transaction research |
| `anthropic-docx` | 5 | Formatted output generation |
| `anthropic-pptx` | 5 | Slide deck output (if applicable) |

## Quality Standards

- Every number in the deck must trace to a source (filing, data provider, calculation)
- Valuation ranges must be internally consistent (football field matches detail pages)
- All methodologies must use the same financial period basis (NTM, LTM, or CY)
- Management projections vs. street estimates clearly distinguished
- Sensitivity tables must bracket the base case symmetrically
- No placeholder text in final output — all sections substantively populated
