# Critical Review — Pipeline Step Details

Detailed agent prompts and expected outputs for each phase of the critical-review pipeline.

## Table of Contents

- [Phase 1: Critical Reviews](#phase-1-critical-reviews)
  - [CTO Review Agent Prompt](#cto-review-agent-prompt)
  - [CEO Review Agent Prompt](#ceo-review-agent-prompt)
- [Phase 2: PM Document Generation](#phase-2-pm-document-generation)
- [Phase 3: Sprint Execution Guidelines](#phase-3-sprint-execution-guidelines)
- [Phase 4: Documentation](#phase-4-documentation)

## Phase 1: Critical Reviews

### CTO Review Agent Prompt

```
You are a brutally honest CTO performing a critical technical review of this project.
Analyze the ENTIRE codebase — backend, frontend, infrastructure, tests.

Review the following 4 sections, surfacing up to 4 top issues per section.
For each issue:
  1. Describe the problem with file and line references
  2. Present 2-3 options (always include "do nothing" where reasonable)
  3. For each option: effort, risk, impact, maintenance burden
  4. Recommend one option with engineering-preference-based reasoning
  5. Classify severity: Critical / High / Medium / Low

## Section 1: Architecture Review
Evaluate:
- Service layer consistency (Repository/Service pattern adherence)
- State management (in-memory vs distributed)
- Configuration management (port conflicts, env var chaos)
- Module boundaries and coupling (feature module sprawl)
- Dependency graph and scaling characteristics

## Section 2: Code Quality Review
Evaluate:
- DRY violations — be aggressive
- API consistency (error format, response contract)
- Error handling patterns and missing edge cases
- Code hygiene (inline imports, unused dependencies, magic numbers)
- Technical debt hotspots

## Section 3: Test Review
Evaluate:
- Coverage thresholds (current vs target)
- Test environment parity (dev vs CI)
- E2E configuration (ports, base URLs)
- Critical path coverage gaps
- Test quality and assertion strength

## Section 4: Performance Review
Evaluate:
- Database query optimization (missing indexes, N+1 queries)
- Caching strategy (what should be cached, TTLs)
- Frontend bundle size and chunking strategy
- Background task management (state, timeouts, cleanup)
- Memory usage concerns

Output format: Structured markdown with ## headings per section,
### per issue, and a summary table at the end.
Write the full document in Korean with English technical terms preserved.
Save to docs/reviews/cto-review-{YYYY-MM}.md.
```

### CEO Review Agent Prompt

```
You are a demanding CEO evaluating whether this project is investable and
market-ready. You care about product-market fit, revenue potential, and
competitive positioning — not code quality.

Analyze the project from 4 strategic angles, identifying critical gaps:

## 1. Product-Market Fit
- Is there feature sprawl without focused value delivery?
- Who is the target user and what is the "10x better" proposition?
- What would need to change to achieve product-market fit?

## 2. Business Model & Monetization
- Is there a clear path to revenue?
- What pricing model fits this product?
- What retention/engagement mechanisms exist?

## 3. User-Facing Quality
- Does the product feel "premium" or "prototype"?
- Loading states, error recovery, onboarding experience
- First-time user experience assessment

## 4. Competitive Differentiation
- What can this product do that alternatives cannot?
- Where is it commodity (easily replicated)?
- What is the unfair advantage?

Include:
- SWOT Analysis (table format)
- Market Positioning Recommendation (2-3 paragraphs)
- Top 3 Strategic Actions with expected impact

Output format: Structured markdown in Korean.
Save to docs/reviews/ceo-review-{YYYY-MM}.md.
```

### Expected Phase 1 Outputs

| File | Content | Typical Size |
|------|---------|-------------|
| `cto-review-{YYYY-MM}.md` | 4 sections x 4 issues + summary table | 300-500 lines |
| `ceo-review-{YYYY-MM}.md` | 4 strategic sections + SWOT + positioning | 200-400 lines |

---

## Phase 2: PM Document Generation

### PRD Generation Prompt

```
Using the CTO review at docs/reviews/cto-review-{YYYY-MM}.md and the CEO
review at docs/reviews/ceo-review-{YYYY-MM}.md as input context, generate
a Product Requirements Document.

Follow the pm-execution create-prd template. Key sections:

1. Summary (problem statement from reviews)
2. Contacts (Owner, PM, Engineering Lead)
3. Background & Strategic Context (synthesize review findings)
4. Objectives
   - SMART OKRs for the upcoming quarter
   - Mapped to specific review findings
5. Market Segments (from CEO analysis)
6. Value Propositions (differentiation points)
7. Solution Detail
   - Sprint 1: Foundation Fixes (highest severity CTO findings)
   - Sprint 2: Test Quality Uplift (test + DB issues)
   - Sprint 3: UX & Performance (CEO quality + CTO perf findings)
8. Success Metrics (measurable targets per sprint)
9. Risks and Mitigations

Title: "Platform Quality Uplift v1"
Save to docs/reviews/PRD-platform-quality-uplift-v1.md
```

### OKR Generation Prompt

```
From the PRD at docs/reviews/PRD-platform-quality-uplift-v1.md, generate
quarterly OKRs using the pm-execution brainstorm-okrs template.

Requirements:
- 3 Objectives aligned to the 3 sprints
- 3-4 Key Results per Objective (measurable, time-bound)
- Rationale for each KR explaining the "why"
- Baseline → Target progression

Save to docs/reviews/OKRs-platform-{QUARTER}-{YEAR}.md
```

### Strategy Document Prompt

```
Using all review and PRD context, generate a strategy document with:

1. Lean Canvas (9 blocks with 2-3 bullets each)
2. SWOT Analysis (strengths, weaknesses, opportunities, threats)
3. Value Proposition Statement
4. Competitive Positioning Map (description)
5. Key Hypotheses to Validate

Follow pm-product-strategy templates for lean-canvas, swot-analysis,
and value-proposition sub-skills.

Save to docs/reviews/strategy-lean-canvas-swot.md
```

### Expected Phase 2 Outputs

| File | Content | Typical Size |
|------|---------|-------------|
| `PRD-platform-quality-uplift-v1.md` | Full PRD with 3 sprints | 200-400 lines |
| `OKRs-platform-{Q}-{YYYY}.md` | 3 objectives, 9-12 KRs | 100-200 lines |
| `strategy-lean-canvas-swot.md` | Lean Canvas + SWOT + VP | 150-300 lines |

---

## Phase 3: Sprint Execution Guidelines

### Sprint Execution Pattern

For each sprint:

1. **Read** the sprint plan from the PRD
2. **Identify** the sub-skill for each task
3. **Delegate** to the sub-skill with a focused prompt:
   - Specify exact files to modify
   - Define the expected change
   - Set "must NOT have" guardrails (files not to touch)
4. **Verify** each change with `ReadLints`
5. **Report** progress after each task

### Sprint 1: Foundation Fixes

Priority order (highest impact first):

1. **Error response contract** — Fix the frontend API interceptor to parse `error.response?.data?.error?.message` (matching backend's AppException format). Target: `frontend/src/lib/api.ts`.

2. **DRY query builders** — Extract shared query filter logic into helper functions. Target: backend API route files with duplicated filter logic (events, stock_prices, etc.).

3. **Port configuration** — Standardize all port references to match actual dev ports (frontend: 4501, backend: 4567). Scan: e2e configs, docs, cursor rules, docker-compose.

4. **Redis state migration** — Move in-memory state dictionaries to Redis with TTL and fallback. Target: any API file using module-level dicts for request state.

### Sprint 2: Test Quality & DB

1. **Coverage thresholds** — Raise backend `fail_under` and frontend vitest thresholds by 15 points.

2. **Database indexes** — Create an Alembic migration adding composite indexes for frequently queried columns (ticker_id+date, published_at, org+market_type).

3. **Code hygiene** — Move inline imports to module top, replace magic numbers with named constants.

### Sprint 3: UX & Performance

1. **UI components** — Create reusable `TableSkeleton`, `CardSkeleton`, `ErrorState`, `EmptyState` components in `frontend/src/components/ui/`.

2. **Redis caching** — Apply `caching_strategy.get_or_compute` to expensive endpoints (dashboard stats, price queries) with 120-300s TTL.

3. **Bundle optimization** — Add manual chunks in `vite.config.ts` for heavy dependencies (radix, i18n, forms, state management).

---

## Phase 4: Documentation

### Remediation Summary Guidelines

- Structure as Executive Summary → Sprint 1/2/3 details → Metrics → Recommendations
- For each sprint: list files changed, describe the change, state the impact
- Include a before/after metrics table (coverage, bundle size, query time)
- End with "Remaining Recommendations" for future work

### Executive Summary DOCX Guidelines

- Use the `docx` npm library to generate a professional Word document
- Include: Background, Key Findings, Actions Taken, Metrics, Next Steps
- Apply professional styling: blue heading theme, numbered lists, bordered tables
- Generate via a temporary .cjs script, then delete the script after producing the .docx
- Fallback: if DOCX generation fails, produce a markdown summary instead
