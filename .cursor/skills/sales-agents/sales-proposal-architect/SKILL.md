---
name: sales-proposal-architect
version: 1.0.0
description: >
  Generate segment-aware proposal drafts for ThakiCloud customers. Identifies
  customer segment (AI Agent Startup, SaaS/Platform Team, Enterprise/Public/Financial),
  selects appropriate value messages and architecture options (on-prem/hybrid/cloud),
  and produces a proposal outline with section drafts, competitive positioning,
  and next-action list. Chains from sales-rfp-interpreter (#1) and
  sales-security-qa (#2) outputs.
  Use when the user asks to "draft proposal", "generate proposal",
  "proposal architect", "create proposal draft", "제안서 초안",
  "솔루션 설계 초안", "제안서 생성", "sales-proposal-architect",
  "세그먼트별 제안서", or needs a ThakiCloud proposal draft based on
  structured requirements.
  Do NOT use for generic meeting-to-proposal without ThakiCloud context
  (use proposal-sow-generator). Do NOT use for RFP parsing
  (use sales-rfp-interpreter). Do NOT use for security Q&A
  (use sales-security-qa). Do NOT use for competitive intelligence only
  (use kwp-sales-competitive-intelligence).
tags: [sales, proposal, architecture, segment, thakicloud, value-proposition]
triggers:
  - "draft proposal"
  - "generate proposal"
  - "proposal architect"
  - "create proposal draft"
  - "solution design draft"
  - "sales-proposal-architect"
  - "제안서 초안"
  - "솔루션 설계 초안"
  - "제안서 생성"
  - "세그먼트별 제안서"
  - "제안서 작성"
  - "아키텍처 제안"
do_not_use:
  - "Generic meeting-to-proposal without ThakiCloud segment context (use proposal-sow-generator)"
  - "RFP document parsing (use sales-rfp-interpreter)"
  - "Security question answering (use sales-security-qa)"
  - "Competitive intelligence gathering only (use kwp-sales-competitive-intelligence)"
  - "General DOCX document creation (use anthropic-docx)"
composes:
  - proposal-sow-generator
  - anthropic-docx
  - kwp-sales-competitive-intelligence
  - kb-query
metadata:
  author: "thaki"
  category: "sales-agents/proposal"
  autonomy: "L2"
---

# Sales Proposal / Solution Design Architect

Generate ThakiCloud-specific proposal drafts with segment-appropriate messaging, architecture options, competitive positioning, and actionable next steps.

## When to Use

- Structured requirements from `sales-rfp-interpreter` are ready for proposal drafting
- Sales needs a first-draft proposal for a specific customer segment
- Architecture option comparison (on-prem vs hybrid vs cloud) is needed for a customer
- Proposal needs competitive positioning against specific competitors

## Segment Templates

### Segment A: AI Agent Startup

| Aspect | Message |
|--------|---------|
| **Hero Message** | "Deploy your AI Agent to production today — not next quarter" |
| **Key Values** | Speed to production, pay-per-use GPU, managed inference, simple API |
| **Architecture** | Cloud-first, shared infrastructure, API-driven |
| **References** | Startup case studies, time-to-deploy metrics |
| **Anti-pattern** | Don't lead with enterprise compliance features |

### Segment B: SaaS / Platform Team

| Aspect | Message |
|--------|---------|
| **Hero Message** | "Accelerate from experiment to production-scale AI" |
| **Key Values** | Multi-model serving, A/B testing, cost optimization, observability |
| **Architecture** | Cloud or hybrid, dedicated namespace, CI/CD integration |
| **References** | Platform team case studies, cost-per-inference benchmarks |
| **Anti-pattern** | Don't lead with on-prem deployment or air-gap |

### Segment C: Enterprise / Public / Financial

| Aspect | Message |
|--------|---------|
| **Hero Message** | "Data sovereignty and enterprise-grade AI — on your terms" |
| **Key Values** | On-prem deployment, data residency, audit logging, compliance (CSAP/ISO/SOC2) |
| **Architecture** | On-premise or hybrid, dedicated hardware, air-gap capable |
| **References** | Enterprise/public sector case studies, compliance certifications |
| **Anti-pattern** | Don't lead with speed or simplicity — lead with control and compliance |

## Pipeline

```
Inputs (requirements table + security Q&A + segment)
       │
       ▼
┌─────────────────────────────┐
│  Phase 1: Segment            │
│  Identification              │
│  Auto-detect or user-        │
│  specified segment           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 2: Value Message      │
│  Selection                   │
│  Template-driven messaging   │
│  pillars for the segment     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 3: Architecture       │
│  Options                     │
│  Trade-off matrix for        │
│  deployment models           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 4: Competitive        │
│  Positioning                 │
│  kwp-sales-competitive-      │
│  intelligence for context    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Phase 5: Proposal Assembly  │
│  TOC + section drafts +      │
│  next actions via            │
│  proposal-sow-generator      │
│  + anthropic-docx            │
└─────────────────────────────┘
```

## Architecture Options Matrix

Generated for every Enterprise/Public/Financial proposal:

| Dimension | On-Premise | Hybrid | Cloud |
|-----------|-----------|--------|-------|
| **Data Residency** | Full control, data never leaves premises | Control plane cloud, data plane on-prem | Provider region-based |
| **GPU Management** | Customer-managed hardware | ThakiCloud-managed remote + local | Fully managed |
| **Update Model** | Manual or air-gap delivery | Automated control, manual data plane | Fully automated |
| **Compliance** | Maximum control for auditors | Balanced — audit logs both sides | Provider certifications |
| **Cost Model** | CapEx + support license | Mixed CapEx/OpEx | Pure OpEx |
| **Time to Deploy** | Weeks to months | Days to weeks | Hours to days |

## Proposal Outline Template

```markdown
# [Customer Name] — ThakiCloud AI Platform Proposal

## 1. Executive Summary
   - Customer challenge (from requirements)
   - ThakiCloud value proposition (segment-specific hero message)
   - Recommended approach (architecture choice)

## 2. Understanding Your Requirements
   - Requirements summary (from sales-rfp-interpreter output)
   - Key priorities identified
   - Assumptions and clarifications needed

## 3. Proposed Solution
   - Architecture overview (with diagram reference)
   - Deployment model recommendation with trade-off rationale
   - Component mapping to requirements

## 4. Security & Compliance
   - Security posture summary (from sales-security-qa output)
   - Compliance coverage matrix
   - Data sovereignty approach

## 5. Why ThakiCloud
   - Competitive differentiation (from competitive intelligence)
   - Customer segment-specific value points
   - Reference cases

## 6. Implementation Approach
   - Phased rollout plan
   - Timeline estimates
   - Success criteria

## 7. Commercial Framework
   - Pricing model overview (NOT specific numbers — sales negotiates)
   - Support tier options
   - SLA summary

## 8. Next Steps
   - Technical deep-dive demo scope
   - POC/pilot definition
   - Decision timeline
```

## Execution Instructions

### Step 0 — Input Validation

1. Verify that at least one of the following inputs is available: `sales-rfp-interpreter` structured output, user-provided requirements list, or explicit customer segment + verbal brief. If none are available, abort with a clear error message — never generate a proposal from zero context.
2. If `sales-rfp-interpreter` output is provided, validate it contains at least 3 distinct requirements. Fewer than 3 suggests incomplete extraction — recommend re-running the interpreter before proceeding.
3. If `sales-security-qa` output is provided, verify it contains at least one answered question. If all answers have confidence < 0.7, flag the security section as "needs expert review before inclusion in proposal."

### Step 1 — Identify Customer Segment

1. If `sales-rfp-interpreter` output is available, infer segment from requirement patterns:
   - Heavy compliance/sovereignty requirements → Enterprise/Public/Financial
   - API-first, speed-focused requirements → AI Agent Startup
   - Multi-model, CI/CD, scaling requirements → SaaS/Platform Team
   - Mixed signals (e.g., startup speed + enterprise compliance) → flag as "hybrid" and ask the user
2. For conglomerates or large organizations with multiple business units, identify which specific unit is the buyer — a startup division within a large enterprise may need Segment A messaging, not Segment C.
3. If ambiguous after requirement analysis, ask the user to confirm the segment. Never guess — segment misidentification is the highest-impact failure mode for this skill.
4. Select the corresponding segment template.

### Step 2 — Select Value Messages

1. Load the segment template's hero message, key values, and anti-patterns.
2. Cross-reference with customer requirements to prioritize the most relevant value points.
3. Use `kb-query` against `product-strategy` KB for latest ThakiCloud positioning data.

### Step 3 — Generate Architecture Options

1. For Enterprise/Public/Financial: always include the full trade-off matrix.
2. For Startup/SaaS: default to cloud, mention hybrid only if requirements suggest it.
3. Recommend one option as primary with clear rationale.

### Step 4 — Competitive Positioning

1. If a specific competitor is known, use `kwp-sales-competitive-intelligence` for battlecard data.
2. If no specific competitor, generate generic differentiation based on ThakiCloud strengths.
3. Never disparage competitors — focus on ThakiCloud's unique value.

### Step 5 — Assemble Proposal

1. Use `proposal-sow-generator` for structural assembly. Pass section content as structured inputs — never pass raw unformatted text.
2. Fill each section using the segment template, requirement data, and competitive intelligence.
3. Verify that every section references at least one customer requirement — sections that don't map to requirements should be removed or marked optional.
4. Generate the final DOCX via `anthropic-docx`.
5. Verify total page count is 8-12 pages. If over 12, remove lowest-priority sections. If under 8, add more detail to the Proposed Solution and Implementation Approach sections.
6. Persist to `outputs/sales-proposals/{date}/{customer-slug}/`.

## Constraints

- Do not invent customer requirements — use only what `sales-rfp-interpreter` extracted or the user explicitly stated
- Commercial Framework section must NEVER include specific pricing numbers — only model descriptions (sales negotiates pricing directly)
- Architecture recommendation must include rationale tied to specific customer requirements, not generic preference
- Competitive positioning must focus on ThakiCloud strengths — never disparage competitors by name with unverifiable claims
- Proposal length should target 8-12 pages; longer proposals lose executive attention
- Proposal sections must not repeat the same value proposition in more than 2 sections — deduplicate during assembly
- Architecture diagrams must use only current ThakiCloud offering names verified against `product-strategy` KB — never reference deprecated or internal codenames
- For proposals with `sales-security-qa` input, every security claim must be traceable to a specific Q&A answer with its confidence score attached

## Gotchas

- Segment misidentification is the highest-impact failure — an enterprise proposal with startup messaging wastes deal credibility; always confirm segment when ambiguous
- The anti-pattern for each segment is as important as the messaging pillars: leading with compliance for a startup or speed for a public sector customer signals poor fit
- Architecture trade-off matrix values change as ThakiCloud's product evolves — cross-check against `product-strategy` KB before including specific timelines
- `proposal-sow-generator` expects structured section inputs; passing unstructured text results in poorly formatted DOCX output
- Competitive intelligence from `kwp-sales-competitive-intelligence` may be stale for fast-moving competitors — include a "last verified" date

## Verification

Before marking proposal draft as ready for human review:
1. Customer segment is explicitly identified and all messaging matches that segment
2. Every proposal section maps to at least one customer requirement
3. Architecture recommendation includes the trade-off matrix for Enterprise/Public/Financial segments
4. Commercial Framework contains zero specific pricing numbers
5. All competitive claims are verifiable from KB or web sources

## Autonomy Level: L2

- **Auto**: Segment detection, template selection, section drafting, competitive lookup
- **Human Review Required**: Full proposal before customer delivery, pricing/commercial sections, architecture recommendations
- **Never Auto**: Sending proposals to customers, committing to specific pricing, making delivery timeline commitments

## Integration Points

- **Upstream**: Consumes `sales-rfp-interpreter` (requirements table) and `sales-security-qa` (security answers)
- **Downstream**: Produced proposal feeds into `sales-deal-prep` for meeting context
- **Harness**: Invoked as Phase 3 of `sales-agent-harness` in `rfp-flow` mode
