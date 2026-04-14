---
name: marketing-harness
version: 1.0.0
description: >
  Marketing domain harness orchestrator — Composite pattern combining a sequential
  brand foundation pipeline with parallel channel execution across 31 marketing
  skills. Covers brand voice, content creation, SEO, campaigns, growth experiments,
  performance analytics, conversion optimization, podcast ops, outbound, sales
  pipeline, revenue intelligence, and team operations. Use when the user asks to
  "run marketing pipeline", "marketing harness", "campaign pipeline", "마케팅 하네스",
  "마케팅 파이프라인", "marketing-harness", or wants end-to-end marketing operations.
  Do NOT use for individual marketing operations (invoke marketing-* or
  kwp-marketing-* directly). Do NOT use for sales prospecting (use sales-harness).
tags: [harness, marketing, orchestrator, composite, campaign, brand, growth]
triggers:
  - "marketing harness"
  - "marketing pipeline"
  - "campaign pipeline"
  - "run marketing harness"
  - "marketing operations"
  - "marketing-harness"
  - "마케팅 하네스"
  - "마케팅 파이프라인"
  - "캠페인 파이프라인"
  - "마케팅 종합"
  - "마케팅 운영"
do_not_use:
  - "For individual marketing skill operations (invoke marketing-* directly)"
  - "For sales prospecting and outreach (use sales-harness)"
  - "For PM product discovery (use pm-harness)"
  - "For engineering code review (use engineering-harness)"
composes:
  - kwp-brand-voice-discover-brand
  - kwp-brand-voice-guideline-generation
  - kwp-brand-voice-brand-voice-enforcement
  - kwp-marketing-content-creation
  - kwp-marketing-campaign-planning
  - kwp-marketing-competitive-analysis
  - kwp-marketing-brand-voice
  - kwp-marketing-performance-analytics
  - marketing-seo-ops
  - marketing-growth-engine
  - marketing-conversion-ops
  - marketing-podcast-ops
  - marketing-outbound-engine
  - marketing-sales-pipeline
  - marketing-revenue-intelligence
  - marketing-finance-ops
  - marketing-team-ops
  - marketing-content-ops
  - content-repurposing-engine
  - content-repurposing-engine-pro
  - hook-generator
  - video-script-generator
  - content-auto-gate
  - hypothesis-marketing
---

# Marketing Harness Orchestrator

Composite pattern: sequential Brand Foundation pipeline, then parallel Channel Execution across content, SEO, campaigns, growth, and outbound, followed by sequential Performance Analysis.

## When to Use

- Full marketing lifecycle from brand foundation through campaign execution and performance analysis
- Multi-channel content creation with brand voice enforcement
- Growth experiment design, execution, and measurement
- Campaign planning with budget allocation and KPI tracking
- Any "run the marketing pipeline" or "마케팅 파이프라인" request

## Architecture

```
User Request (mode selection)
       │
       ▼
┌──────────────────────────────────────────┐
│          BRAND FOUNDATION                 │
│  Phase 1: Discover → Phase 2: Guidelines  │  ← Sequential
│  Phase 3: Enforcement baseline            │
└──────────────────┬───────────────────────┘
                   │
     ┌─────────────┼─────────────┬───────────────┐
     ▼             ▼             ▼               ▼
┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐  ← Fan-out (parallel)
│ CONTENT │ │   SEO   │ │ CAMPAIGN │ │ OUTBOUND │
│ Phase 4 │ │ Phase 5 │ │ Phase 6  │ │ Phase 7  │
│ blog,   │ │ keyword │ │ planning │ │ cold seq │
│ email,  │ │ gap,    │ │ budget,  │ │ optimize │
│ social  │ │ attack  │ │ KPIs     │ │          │
└────┬────┘ └────┬────┘ └────┬─────┘ └────┬─────┘
     └───────────┼───────────┼─────────────┘
                 ▼
       ┌──────────────────┐
       │   GROWTH ENGINE  │  ← Phase 8: Experiments + scoring
       │   Phase 8        │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │ PERFORMANCE      │  ← Phase 9: Analytics + CRO
       │ Phase 9          │
       └────────┬─────────┘
                ▼
       ┌──────────────────┐
       │ REPURPOSE        │  ← Phase 10: Multi-platform distribution
       │ Phase 10         │
       └──────────────────┘
```

## Modes

| Mode | Phases | Use Case |
|------|--------|----------|
| `brand` | 1→2→3 | Brand discovery, guideline generation, and voice setup |
| `content` | 4 only | Multi-channel content creation with brand voice |
| `seo` | 5 only | SEO operations (attack briefs, keyword analysis) |
| `campaign` | 6 only | Campaign planning with targets and KPIs |
| `outbound` | 7 only | Cold outbound sequence optimization |
| `growth` | 8 only | Growth experiment lifecycle |
| `analytics` | 9 only | Performance analytics + conversion rate optimization |
| `repurpose` | 10 only | Transform content into 10+ platform formats |
| `podcast` | `marketing-podcast-ops` | Podcast-to-everything pipeline |
| `full` | 1→2→3 → Fan-out(4∥5∥6∥7) → 8→9→10 | Complete marketing pipeline |

Default mode: `full`

## Pipeline

### Phase 1: Brand Discovery

Discover existing brand materials across enterprise platforms.

**Skill**: `kwp-brand-voice-discover-brand`
**Input**: Company/product name, platform access
**Output**: `outputs/marketing-harness/{date}/phase1-brand-discovery.md`

Searches: Notion, Confluence, Google Drive, Figma, Slack, Gong.

### Phase 2: Guideline Generation

Generate or update brand voice guidelines from discovered materials.

**Skill**: `kwp-brand-voice-guideline-generation`
**Input**: Phase 1 brand materials
**Output**: `outputs/marketing-harness/{date}/phase2-brand-guidelines.md`

### Phase 3: Voice Enforcement Baseline

Establish brand voice enforcement rules for all downstream content.

**Skills**: `kwp-brand-voice-brand-voice-enforcement`, `kwp-marketing-brand-voice`
**Input**: Phase 2 guidelines
**Output**: `outputs/marketing-harness/{date}/phase3-voice-enforcement.md`

### Phase 3.5: Performance Diagnosis (Optional)

When campaign metrics underperform, A/B tests yield ambiguous results, or channel performance degrades unexpectedly, invoke `hypothesis-marketing` for structured experiment design and performance diagnosis before doubling down or pivoting. Triggered automatically when:

- Campaign conversion rates drop >20% from baseline without obvious cause
- A/B test results are statistically insignificant after sufficient sample size
- Multiple channels underperform simultaneously, suggesting a systemic issue
- User requests marketing diagnosis or asks "why isn't this campaign working"

**Skill**: `hypothesis-marketing`
**Input**: Phase 1-3 outputs + campaign performance data
**Output**: `outputs/marketing-harness/{date}/phase3.5-performance-diagnosis.md`
**Skip Flag**: `skip-hypothesis`

### Phase 4: Content Creation (Fan-out Branch A)

Create marketing content across channels with brand voice enforcement.

**Skills**: `kwp-marketing-content-creation`, `marketing-content-ops`, `hook-generator`, `video-script-generator`
**Input**: Campaign brief + Phase 3 voice rules
**Output**: `outputs/marketing-harness/{date}/phase4-content/`

Covers: blog posts, social media, email newsletters, landing pages, press releases, case studies, video scripts.

### Phase 5: SEO Operations (Fan-out Branch B)

Search engine optimization: content attack briefs, keyword gap analysis, trend scouting.

**Skill**: `marketing-seo-ops`
**Input**: Target keywords + competitive landscape
**Output**: `outputs/marketing-harness/{date}/phase5-seo.md`

### Phase 6: Campaign Planning (Fan-out Branch C)

Plan marketing campaigns with objectives, audience segmentation, channel strategy, and budget.

**Skills**: `kwp-marketing-campaign-planning`, `kwp-marketing-competitive-analysis`
**Input**: Phase 3 brand voice + market context
**Output**: `outputs/marketing-harness/{date}/phase6-campaign.md`

### Phase 7: Outbound Engine (Fan-out Branch D)

Cold outbound sequence optimization with ICP targeting and capacity planning.

**Skill**: `marketing-outbound-engine`
**Input**: ICP definition + infrastructure audit
**Output**: `outputs/marketing-harness/{date}/phase7-outbound.md`

### Phase 8: Growth Engine

Autonomous marketing experiment lifecycle: create, run, measure, optimize.

**Skill**: `marketing-growth-engine`
**Input**: Phases 4-7 outputs (channel performance data)
**Output**: `outputs/marketing-harness/{date}/phase8-growth.md`

Covers: experiment design, statistical scoring, pacing alerts, weekly scorecards.

### Phase 9: Performance Analysis

Analyze performance and optimize conversion rates.

**Skills**: `kwp-marketing-performance-analytics`, `marketing-conversion-ops`, `marketing-revenue-intelligence`
**Input**: Phase 8 experiment results + channel metrics
**Output**: `outputs/marketing-harness/{date}/phase9-performance.md`

Covers: channel ROI, CRO audit, attribution, content-to-revenue mapping.

### Phase 10: Content Repurposing

Transform long-form content into platform-specific formats for distribution.

**Skills**: `content-repurposing-engine`, `content-repurposing-engine-pro`
**Input**: Phase 4 content + Phase 9 performance insights
**Output**: `outputs/marketing-harness/{date}/phase10-repurposed/`

Covers: Twitter threads, LinkedIn posts, newsletter sections, blog summaries, video scripts, infographic briefs, email snippets (10+ formats).

## Skill Routing Table

| User Intent | Routed Skill | Phase |
|-------------|-------------|-------|
| "Discover brand materials" | `kwp-brand-voice-discover-brand` | 1 |
| "Create brand guidelines" | `kwp-brand-voice-guideline-generation` | 2 |
| "Write blog post" | `kwp-marketing-content-creation` | 4 |
| "SEO attack brief" | `marketing-seo-ops` | 5 |
| "Plan a campaign" | `kwp-marketing-campaign-planning` | 6 |
| "Cold outbound setup" | `marketing-outbound-engine` | 7 |
| "Run growth experiment" | `marketing-growth-engine` | 8 |
| "Analyze channel ROI" | `kwp-marketing-performance-analytics` | 9 |
| "CRO audit" | `marketing-conversion-ops` | 9 |
| "Repurpose content" | `content-repurposing-engine-pro` | 10 |
| "Podcast pipeline" | `marketing-podcast-ops` | — |
| "Team performance" | `marketing-team-ops` | — |
| "Marketing finance" | `marketing-finance-ops` | — |
| "Competitive analysis" | `kwp-marketing-competitive-analysis` | 6 |
| "Generate hooks" | `hook-generator` | 4 |
| "Video script" | `video-script-generator` | 4 |

## Error Handling

| Error | Recovery |
|-------|----------|
| Fan-out branch fails | Other branches continue. Failed branch output marked as INCOMPLETE. |
| Brand discovery finds no materials | Phase 2 generates guidelines from scratch using user input. |
| Growth experiment below threshold | Auto-pause experiment; report in Phase 9 analytics. |
| Phase N fails | Prior phase outputs remain valid. Fix and re-run from Phase N. |
| Content quality gate fails | Loop back to Phase 4 with feedback (max 2 iterations via `marketing-content-ops`). |

## Output Artifacts

| Phase | Stage Name | Output File | Skip Flag |
|-------|-----------|-------------|-----------|
| 1 | Brand Discovery | `outputs/marketing-harness/{date}/phase1-brand-discovery.md` | `skip-discover` |
| 2 | Guidelines | `outputs/marketing-harness/{date}/phase2-brand-guidelines.md` | `skip-guidelines` |
| 3 | Voice Enforcement | `outputs/marketing-harness/{date}/phase3-voice-enforcement.md` | `skip-voice` |
| 4 | Content | `outputs/marketing-harness/{date}/phase4-content/` | `skip-content` |
| 5 | SEO | `outputs/marketing-harness/{date}/phase5-seo.md` | `skip-seo` |
| 6 | Campaign | `outputs/marketing-harness/{date}/phase6-campaign.md` | `skip-campaign` |
| 7 | Outbound | `outputs/marketing-harness/{date}/phase7-outbound.md` | `skip-outbound` |
| 8 | Growth | `outputs/marketing-harness/{date}/phase8-growth.md` | `skip-growth` |
| 9 | Performance | `outputs/marketing-harness/{date}/phase9-performance.md` | `skip-perf` |
| 10 | Repurpose | `outputs/marketing-harness/{date}/phase10-repurposed/` | `skip-repurpose` |

## Workspace Convention

- Intermediate files: `_workspace/marketing-harness/`
- Final deliverables: `outputs/marketing-harness/{date}/`
- Brand guidelines cache: `_workspace/marketing-harness/brand-guidelines.md`

## Constraints

- All content must pass brand voice enforcement (Phase 3 rules) before publishing
- Fan-out channel branches must not share mutable state
- Growth experiments require statistical significance before declaring winners
- Content quality gate (via `marketing-content-ops`) must score ≥90 points before Phase 10
- Podcast mode (`marketing-podcast-ops`) is standalone and does not chain into the main pipeline
- Team ops (`marketing-team-ops`) is a cross-cutting utility for Elon Algorithm audits and meeting intelligence
