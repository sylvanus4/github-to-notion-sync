---
name: cloud-requirements-analyst
description: >-
  클라우드 기술팀에 직접 문의하지 않고도 요구사항을 상세 수집하고, 기술적
  타당성을 분석하며, 기획안의 현실성·누락·리스크를 평가하는 스킬이다.
  구조화된 질문 프레임워크로 요구사항을 정제하고, 웹 리서치와 클라우드 서비스
  공식 문서를 기반으로 기술 타당성을 독자적으로 분석한다.
  Use when the user asks to "요구사항 수집", "기술 타당성 평가", "기획안 평가",
  "클라우드 요구사항 분석", "cloud requirements analysis",
  "기술적 현실성 검토", "리스크 평가", "누락 검토", "기술 검증",
  "요구사항 정리해줘", "기획안 기술 검토", "feasibility assessment",
  or needs to evaluate planning proposals from a cloud/technical perspective
  without directly consulting the tech team.
  Do NOT use for explaining tech docs to non-technical audiences (use tech-doc-translator).
  Do NOT use for writing technical documentation (use technical-writer).
  Do NOT use for market/competitor research (use parallel-deep-research).
  Do NOT use for PRD creation (use pm-execution or prd-research-factory).
metadata:
  author: thaki
  version: "1.0.1"
  category: execution
---

# Cloud Requirements Analyst

Pipeline + inversion skill: collect and refine requirements without a direct cloud-tech team handoff, and independently assess technical feasibility of proposals. AI performs first-pass analysis and explicitly tags items that still need engineering confirmation.

**Core principle**: This skill does not replace the tech team. It raises readiness before those conversations and surfaces the key questions to ask engineering.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

What the user provides:

1. **Proposal** — Notion URL, markdown file, or pasted text
2. **Cloud context** (optional) — Current platform (AWS/GCP/Azure), existing architecture notes
3. **Focus** (optional) — `feasibility` / `risk` / `gap` / `full` (default: full)
4. **Existing stack** (optional) — Technologies already in use

## Workflow

### Phase 1: Requirements interview (inversion)

**HARD-GATE: Do not enter Phase 2 until all required items below are obtained or explicitly attempted.**

Use structured questions from [references/requirements-interview.md](references/requirements-interview.md).

#### Required items (HARD-GATE)

| # | Item | If missing |
|---|------|------------|
| 1 | Core feature list (min 3) | Extract from proposal → else ask user |
| 2 | Expected user scale | Extract → else ask |
| 3 | Performance (latency, throughput) | Extract → else state industry assumption + label it |
| 4 | Data requirements (types, volume, retention) | Extract → else ask |
| 5 | Schedule constraint (target launch) | Extract → else ask |

#### Optional items

- Security/compliance requirements
- Integration with existing systems
- Budget constraints
- Global/multi-region needs
- Availability / SLA expectations

Extract as much as possible from the proposal first; ask only for missing required items. Ask at most 3 questions per round.

### Phase 2: Technical research and analysis

Analyze feasibility from the gathered requirements.

#### 2-1. Cloud service mapping

Map each functional requirement to suitable cloud services.

Sources:
- Official cloud docs (WebSearch)
- Service limits (quotas)
- Pricing (calculator references)
- Comparable case studies at similar scale

#### 2-2. Draft architecture options

Produce high-level architecture options.

For each option:
- Components (service list)
- Estimated monthly cost band
- Implementation complexity (1–5)
- Scalability assessment
- Pros and cons

#### 2-3. Technical constraints

Identify gaps between requirements and technical reality.

| Constraint type | Description |
|-----------------|-------------|
| **Service limits** | Default quotas/limits of managed services |
| **Performance** | Required vs achievable performance |
| **Cost** | Estimated cost vs budget |
| **Time** | Complexity vs schedule |
| **Regulation** | Data handling and retention rules |

### Phase 3: Proposal evaluation report

Produce a consolidated report. Criteria: [references/cloud-evaluation-criteria.md](references/cloud-evaluation-criteria.md). Risk taxonomy: [references/risk-categories.md](references/risk-categories.md).

#### 3-1. Feasibility score

Per feature, rate technical feasibility 1–5:

| Score | Meaning |
|-------|---------|
| 5 | Standard pattern, straightforward to implement |
| 4 | Some customization, still feasible |
| 3 | Possible with care/optimization |
| 2 | Hard or expensive |
| 1 | Impractical or not viable with stated constraints |

#### 3-2. Risk matrix

Map risks by probability × impact:

| | Low impact | Medium | High |
|---|------------|--------|------|
| **High probability** | Medium | High | Critical |
| **Medium** | Low | Medium | High |
| **Low** | Info | Low | Medium |

Add mitigation per risk.

#### 3-3. Gaps

From a technical lens, list what the proposal omits:
- Undefined states/scenarios
- Ignored technical constraints
- Missing non-functional requirements
- Integrations mentioned nowhere but required

#### 3-4. Alternatives

For low feasibility (scores 1–2), suggest viable alternatives:
- Alternate services/tech
- Reduced-scope version
- Phased delivery

#### 3-5. Engineering confirmation checklist

**CRITICAL**: State AI limitations explicitly and list items that **must** be validated with the tech team.

Reasons confirmation is needed:
- Internal system specifics (unknown externally)
- Accurate infra constraints
- Security/compliance internal standards
- Team skill/capacity judgment

## Examples

### Example 1: Feasibility for a new feature

User: "Review technical feasibility of the real-time dashboard proposal"

Actions:
1. Extract: 1s refresh, 100+ widgets, 1000 concurrent users
2. Phase 1 HARD-GATE: ask data sources and retention if missing
3. Map services: WebSocket + Redis Pub/Sub + observability stack options
4. Scores: 1s refresh (4/5), 100 widgets (3/5 — render optimization), 1000 users (5/5)
5. Risks: realtime cost (High), render performance (Medium)
6. Engineering checks: pipeline latency, infra budget

Result: Feasibility report (avg 4.0/5, 2 risks, 3 gaps, 4 engineering checks, 1 alternative)

### Example 2: Full proposal review

User: "Full technical review of the marketplace proposal"

Actions:
1. Parse: seller onboarding, search, payments, reviews, recommendations
2. Phase 1: ask traffic, payment methods, geo constraints if missing
3. Per-feature scores: search (5/5), payments (4/5 — PG complexity), recommendations (3/5 — ML infra)
4. Risk matrix: payment security (Critical), search perf (Medium), ML cost (High)
5. Gaps: DR scenarios, backup policy, seller verification flow
6. Alternative: rules-based recommendations first, ML in phase 2

Result: Full report (5 features, avg 3.8/5, 1 Critical, 6 gaps, phased plan)

## Error Handling

| Error | Action |
|-------|--------|
| Proposal too abstract (no feature list) | Request feature list in Phase 1 |
| Cloud platform unspecified | Run generic analysis across AWS/GCP/Azure patterns |
| Pricing not found via research | Label as estimate + link official calculators |
| Notion inaccessible | Ask user to paste text |
| Too many features (20+) | Propose scoping to top 10 by priority |
| Missing internal system detail | Tag for engineering confirmation (use Korean label in deliverables) and continue with generic analysis |

## Evolution

### Eval criteria (binary)

| ID | Eval | Pass condition |
|----|------|----------------|
| E1 | HARD-GATE | Block Phase 2 or extract/ask until required items addressed |
| E2 | Feasibility score | Per-feature 1–5 with rationale + aggregate |
| E3 | Risk matrix | Probability×impact + severity + mitigations |
| E4 | Engineering confirmation | Dedicated section + reasons |
| E5 | Alternatives | Actionable alternatives for 1–2 score items |

### Autoimprove hook

- **Test inputs**: realtime dashboard, marketplace, chat, API Gateway, serverless backend (5 types)
- **Baseline target**: E1–E5 pass rate ≥ 80%
- **Mutation focus**: HARD-GATE question precision, cost estimation, mitigation specificity
