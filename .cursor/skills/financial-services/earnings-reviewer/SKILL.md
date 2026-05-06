# Earnings Reviewer — Earnings Event Analysis Agent

End-to-end earnings event processing: pre-earnings prep, real-time transcript analysis, post-earnings note generation, model update, and client alert — orchestrating multiple financial analysis skills.

Adapted from [anthropics/financial-services](https://github.com/anthropics/financial-services) `earnings-reviewer` agent plugin.

## Triggers

Use when the user asks to "review earnings", "earnings analysis", "earnings call review", "quarterly results", "earnings transcript analysis", "post-earnings update", "실적 리뷰", "어닝스 분석", "분기 실적 분석", "어닝스 콜 분석", "실적 발표 후 분석", or needs to process a company's earnings event from preparation through distribution.

Do NOT use for single DCF valuation without earnings context (use dcf-model). Do NOT use for general equity research without an earnings event (use equity-research-note). Do NOT use for daily stock signal analysis (use daily-stock-check).

## Agent Artifacts

The Earnings Reviewer produces these deliverables:

| Artifact | Description |
|----------|-------------|
| Pre-earnings brief | Consensus expectations, key questions, historical beat/miss pattern |
| Transcript analysis | Beat/miss on each metric, management tone, guidance changes |
| Model update | Revised revenue/EPS estimates post-results |
| Flash note | 1-page summary for immediate distribution |
| Detailed note | Full equity-research-note with updated thesis |
| Client alert | Structured Slack/email summary with rating implication |

## Workflow

### Phase 1: Pre-Earnings Preparation

**Skill: `comps-analysis` + `parallel-web-search`**

1. **Consensus gathering**
   - Revenue, EPS, EBITDA consensus estimates (street median)
   - Whisper numbers if available from buy-side surveys
   - Key metric expectations (subscriber count, GMV, bookings, etc.)

2. **Historical pattern**
   - Last 8 quarters beat/miss history on revenue and EPS
   - Stock price reaction pattern (1-day, 5-day post-earnings)
   - Management guidance accuracy track record

3. **Key questions list**
   - 5-8 questions that will determine the stock reaction
   - Grouped by: growth trajectory, margins, capital allocation, guidance

### Phase 2: Earnings Release Processing

**Skill: `three-statement-model` + web research**

When actual results are available:

1. **Beat/miss scorecard**
   | Metric | Consensus | Actual | Beat/Miss | Magnitude |
   |--------|-----------|--------|-----------|-----------|
   | Revenue | $X.XB | $X.XB | Beat | +X.X% |
   | EPS | $X.XX | $X.XX | Miss | -X.X% |
   | [KPI] | X.XM | X.XM | Beat | +X.X% |

2. **Guidance assessment**
   - Compare new guidance range to prior consensus
   - Identify any guide-down or guide-up on key metrics
   - Assess quality of guidance (narrow vs. wide range, confidence language)

3. **Segment analysis**
   - Revenue by segment vs. expectations
   - Margin by segment vs. expectations
   - Any segment-level surprises or trend changes

### Phase 3: Transcript Analysis

**Skill: `equity-research-note`**

Parse the earnings call transcript for:

1. **Management tone analysis**
   - Confidence level (language patterns)
   - Cautious vs. optimistic framing
   - New strategic language or priorities

2. **Key Q&A extraction**
   - Analyst questions and management responses
   - Evasive or non-answers flagged
   - New disclosure or data points from Q&A

3. **Forward indicators**
   - Pipeline commentary
   - Hiring/investment plans
   - Competitive landscape observations
   - Macro commentary and assumptions

### Phase 4: Model Update

**Skill: `dcf-model` + `three-statement-model`**

1. Update revenue model with actuals and new guidance
2. Adjust margin assumptions based on trends
3. Revise EPS trajectory
4. Recalculate DCF fair value
5. Update comps-implied valuation range

### Phase 5: Note Generation

**Skill: `equity-research-note`**

Produce two documents:

**Flash Note** (within 1 hour):
```
## [Company] Q[X] Earnings Flash
Rating: [Maintain/Upgrade/Downgrade] | PT: $XX → $XX

### Key Takeaways
- [3-5 bullet points]

### Beat/Miss Summary
[Scorecard table]

### Guidance Change
[One paragraph]

### Initial Reaction
[Stock movement and reasoning]
```

**Detailed Note** (within 24 hours):
- Full equity-research-note format
- Updated model with new estimates
- Revised price target derivation
- Catalyst calendar update

### Phase 6: Distribution

Post structured summary to relevant channels:
- Flash note → Slack #효정-주식 for personal portfolio relevance
- Key takeaways → appropriate research channel
- Model update summary → research archive

## Composed Skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `comps-analysis` | 1 | Consensus and peer context |
| `three-statement-model` | 2, 4 | Financial model updates |
| `dcf-model` | 4 | Valuation update |
| `equity-research-note` | 5 | Note generation |
| `parallel-web-search` | 1, 2 | Market data, consensus, reactions |
| `deck-qc` | 5 | Quality check on output |
| `anthropic-docx` | 5 | Formatted report output |

## Quality Standards

- All numbers must be sourced (10-Q, press release, transcript)
- Beat/miss calculations must use the SAME consensus source consistently
- Price targets must show the math (DCF output, not assertion)
- Tone analysis must cite specific management quotes
- Model changes must be explicitly flagged (old → new)
