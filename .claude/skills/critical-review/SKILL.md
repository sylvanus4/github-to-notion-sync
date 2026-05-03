---
name: critical-review
description: >-
  End-to-end CTO/CEO critical review and remediation pipeline: parallel
  technical and strategic critiques (4 review sections x 4 issues each), PM
  documentation (PRD, OKRs, Lean Canvas, SWOT), 3-sprint remediation
  execution, and executive summary .docx generation. Use when the user asks to
  "critical review", "CTO CEO review", "platform review", "run critical
  review", "critical-review", "CTO 리뷰", "CEO 리뷰", "신랄한 비판", "플랫폼 리뷰", "전체 리뷰 후
  개선", or wants a comprehensive dual-perspective project audit with
  remediation. Do NOT use for single-domain code review (use deep-review or
  simplify), release preparation (use release-commander), daily stock analysis
  (use today), or role-dispatch without remediation (use role-dispatcher).
---

# Critical Review — CTO/CEO Dual-Perspective Audit and Remediation Pipeline

One command to produce brutally honest CTO and CEO critiques of the entire project, generate PM strategy documents from the findings, execute a prioritized 3-sprint remediation, and deliver a professional executive summary. Orchestrates 12+ specialized skills across 4 sequential phases.

## Usage

```
/critical-review                      # full pipeline (all 4 phases)
/critical-review review-only          # Phase 1 only — CTO + CEO reviews
/critical-review with-implementation  # Phases 1-3 — reviews + PM docs + sprints
/critical-review docs-only            # Phase 4 only — generate docs from existing reviews
```

## Pipeline Overview

```
Phase 1 (parallel): Critical Reviews
  ├─ role-cto    → Architecture, Code Quality, Tests, Performance (4 issues each)
  └─ role-ceo    → Product-Market Fit, Business Model, UX Quality, Differentiation

    ↓ Output: cto-review-{YYYY-MM}.md + ceo-review-{YYYY-MM}.md

Phase 2 (sequential): PM Document Generation
  ├─ pm-execution       → PRD + OKRs + Sprint Plan
  └─ pm-product-strategy → Lean Canvas + SWOT + Value Proposition

    ↓ Output: PRD, OKRs, strategy docs in docs/reviews/

Phase 3 (sequential): Sprint Execution
  ├─ Sprint 1: Foundation Fixes    (backend-expert, frontend-expert)
  ├─ Sprint 2: Test Quality Uplift (qa-test-expert, db-expert)
  └─ Sprint 3: UX & Performance   (frontend-expert, db-expert, security-expert)

    ↓ Output: Code changes, migrations, new components

Phase 4 (sequential): Documentation
  ├─ remediation-summary-{YYYY-MM}.md
  └─ executive-summary-{YYYY-MM}.docx (via anthropic-docx)
```

## Workflow

### Step 0: Pre-flight

1. Determine the execution mode from user input (`review-only`, `with-implementation`, `docs-only`, or full).
2. Create the output directory: `docs/reviews/`.
3. Resolve the date suffix: `{YYYY-MM}` from today's date.
4. If mode is `docs-only`, verify that `docs/reviews/cto-review-*.md` and `docs/reviews/ceo-review-*.md` already exist. If not, inform the user and suggest running the full pipeline.

### Step 1: Phase 1 — Critical Reviews (parallel)

Launch 2 sub-agents simultaneously via the Task tool (max 4 slots, using 2):

**Agent 1: CTO Review**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/role/role-cto/SKILL.md`. Analyze the entire project from the CTO perspective. The topic is "Full Platform Critical Review". Produce a structured Korean analysis document with relevance score. Cover 4 review sections, each surfacing up to 4 top issues:
  1. Architecture Review — service layer consistency, state management, configuration, module boundaries
  2. Code Quality Review — DRY violations, API consistency, error handling, code hygiene
  3. Test Review — coverage thresholds, environment parity, E2E config, critical path coverage
  4. Performance Review — query optimization, caching strategy, bundle size, background tasks
- Write the output to `docs/reviews/cto-review-{YYYY-MM}.md`.
- See [references/pipeline-steps.md](references/pipeline-steps.md) for the full prompt template.

**Agent 2: CEO Review**
- `subagent_type: generalPurpose`
- Prompt: Read and follow `.cursor/skills/role/role-ceo/SKILL.md`. Analyze the entire project from the CEO perspective. The topic is "Full Platform Critical Review". Produce a structured Korean analysis document with relevance score. Cover 4 strategic issues:
  1. Product-Market Fit — feature sprawl vs focused value
  2. Business Model — monetization path, pricing, retention
  3. User-Facing Quality — loading states, error recovery, onboarding
  4. Competitive Differentiation — unique value vs commodity features
- Include a SWOT analysis and market positioning recommendation.
- Write the output to `docs/reviews/ceo-review-{YYYY-MM}.md`.
- See [references/pipeline-steps.md](references/pipeline-steps.md) for the full prompt template.

**Gate**: Both reviews must complete. If either fails, retry once. If still failing, proceed with partial results and note the gap.

If mode is `review-only`, stop here and present a summary of findings.

### Step 2: Phase 2 — PM Document Generation (sequential)

Read both review documents from Phase 1 as input context.

**Step 2a: pm-execution**
- Read and follow `.cursor/skills/pm/pm-execution/SKILL.md`.
- Sub-skill: `create-prd` — Generate a PRD titled "Platform Quality Uplift v1" addressing the top 8 issues from CTO/CEO reviews. Use the template in `.cursor/skills/pm/pm-execution/references/create-prd.md`.
- Sub-skill: `brainstorm-okrs` — Generate quarterly OKRs aligned to review findings. Use the template in `.cursor/skills/pm/pm-execution/references/brainstorm-okrs.md`.
- Sub-skill: `sprint-plan` — Plan 3 two-week sprints prioritized by impact/effort.
- Output: `docs/reviews/PRD-platform-quality-uplift-v1.md`, `docs/reviews/OKRs-platform-{QUARTER}-{YEAR}.md`

**Step 2b: pm-product-strategy**
- Read and follow `.cursor/skills/pm/pm-product-strategy/SKILL.md`.
- Sub-skill: `lean-canvas` — Generate a Lean Canvas for the platform.
- Sub-skill: `swot-analysis` — Produce a SWOT analysis.
- Sub-skill: `value-proposition` — Define the competitive value proposition.
- Output: `docs/reviews/strategy-lean-canvas-swot.md`

### Step 3: Phase 3 — Sprint Execution (sequential)

Execute the 3 sprints defined in the PRD. Each sprint follows this pattern:

1. Read the sprint plan from the PRD
2. For each task in the sprint, delegate to the appropriate sub-skill
3. Apply changes, verify with `ReadLints`, fix issues
4. Report progress

**Sprint 1: Foundation Fixes**

| Task | Sub-skill | Target Files |
|------|-----------|-------------|
| Fix error response contract | `frontend-expert` | `frontend/src/lib/api.ts` |
| Extract shared query builders | `backend-expert` | `backend/app/api/v1/events.py` |
| Standardize port configuration | Direct edit | e2e config, docs, IDE config |
| Move in-memory state to Redis | `backend-expert` | `backend/app/api/v1/stock_prices.py` |

**Sprint 2: Test Quality Uplift**

| Task | Sub-skill | Target Files |
|------|-----------|-------------|
| Raise coverage thresholds | Direct edit | `backend/pyproject.toml`, `frontend/vitest.config.ts` |
| Add database indexes | `db-expert` | New Alembic migration |
| Clean up inline imports/magic numbers | `backend-expert` | Backend API files |

**Sprint 3: UX and Performance**

| Task | Sub-skill | Target Files |
|------|-----------|-------------|
| Create skeleton/error/empty components | `frontend-expert` | `frontend/src/components/ui/` |
| Apply Redis caching to endpoints | `backend-expert` | API endpoint files |
| Optimize frontend bundle chunks | `frontend-expert` | `frontend/vite.config.ts` |

If mode is `with-implementation`, stop here and present a summary of changes.

### Step 4: Phase 4 — Documentation (sequential)

**Step 4a: Remediation Summary**
- Compile all changes from Phase 3 into `docs/reviews/remediation-summary-{YYYY-MM}.md`.
- Structure: Executive Summary, Sprint 1/2/3 details (file, change, impact), Metrics table (before/after/target), Remaining Recommendations.
- See [references/output-templates.md](references/output-templates.md) for the template.

**Step 4b: Executive Summary DOCX**
- Read and follow `.cursor/skills/anthropic/anthropic-docx/SKILL.md`.
- Generate `docs/reviews/executive-summary-{YYYY-MM}.docx` using the docx-js library.
- Content: Background, Key Findings (CTO + CEO highlights), Actions Taken (3 sprints), Metrics Table, Strategic Deliverables, Next Steps.
- See [references/output-templates.md](references/output-templates.md) for the DOCX structure.
- Delete the generation script after producing the .docx.

### Step 5: Final Report

Present a structured summary:

```
Critical Review Pipeline Report
================================
Phase 1: Critical Reviews
  CTO Review:  [N] issues across 4 sections → docs/reviews/cto-review-{YYYY-MM}.md
  CEO Review:  [N] strategic gaps identified → docs/reviews/ceo-review-{YYYY-MM}.md

Phase 2: PM Documents
  PRD:         Platform Quality Uplift v1 → docs/reviews/PRD-*.md
  OKRs:        [N] objectives, [N] key results → docs/reviews/OKRs-*.md
  Strategy:    Lean Canvas + SWOT + Value Prop → docs/reviews/strategy-*.md

Phase 3: Sprint Execution
  Sprint 1:    [N] foundation fixes applied
  Sprint 2:    [N] test/DB improvements
  Sprint 3:    [N] UX/performance changes

Phase 4: Documentation
  Summary:     docs/reviews/remediation-summary-{YYYY-MM}.md
  DOCX:        docs/reviews/executive-summary-{YYYY-MM}.docx

Overall: [COMPLETE | PARTIAL — reason]
```

## Output Directory Convention

All outputs go to `docs/reviews/` with date-stamped filenames:

| File | Phase | Description |
|------|-------|-------------|
| `cto-review-{YYYY-MM}.md` | 1 | CTO technical critique |
| `ceo-review-{YYYY-MM}.md` | 1 | CEO strategic critique |
| `PRD-platform-quality-uplift-v1.md` | 2 | Product Requirements Document |
| `OKRs-platform-{QUARTER}-{YEAR}.md` | 2 | Quarterly Objectives and Key Results |
| `strategy-lean-canvas-swot.md` | 2 | Lean Canvas, SWOT, Value Proposition |
| `remediation-summary-{YYYY-MM}.md` | 4 | Sprint execution results |
| `executive-summary-{YYYY-MM}.docx` | 4 | Executive summary Word document |

## Examples

### Example 1: Full pipeline

User: `/critical-review`

All 4 phases execute sequentially. CTO and CEO reviews run in parallel, PM documents are generated, 3 sprints of fixes are applied, and the executive summary .docx is produced. Total: ~12 skills orchestrated, 7 output documents.

### Example 2: Review only

User: `/critical-review review-only`

Phase 1 only. CTO and CEO reviews run in parallel. Two review documents are generated. No code changes. Use this to assess the project state before committing to remediation.

### Example 3: Generate docs from existing reviews

User: `/critical-review docs-only`

Phase 4 only. Reads existing review and remediation files from `docs/reviews/`. Generates the remediation summary .md and executive summary .docx. Use after manually addressing review findings.

## Error Handling

| Scenario | Action |
|----------|--------|
| CTO/CEO review agent fails | Retry once; proceed with partial results |
| PM skill missing template | Fall back to freeform generation with review context |
| Sprint task fails to apply | Log the failure, continue with remaining tasks |
| DOCX generation fails | Generate markdown-only summary as fallback |
| Output directory missing | Create `docs/reviews/` automatically |
| Existing review files found | Overwrite with new date-stamped versions |
| Sub-agent timeout | Re-launch once with reduced scope |

## Troubleshooting

- **"No review documents found" in docs-only mode**: Run the full pipeline first, or at least `review-only` mode to generate the CTO and CEO review files.
- **PM skill produces incomplete output**: Ensure the CTO and CEO review files contain structured findings. The PM skills parse these as input context.
- **DOCX generation script error**: Verify `docx` is installed globally (`npm install -g docx`). Use `NODE_PATH=$(npm root -g)` when running the script.
- **Sprint changes conflict with existing code**: The pipeline applies fixes incrementally. If a conflict occurs, it will skip the conflicting change and report it in the remediation summary.


## Subagent Contract

When spawning Task tool subagents:

- Always pass **absolute file paths** — subagent working directories are unpredictable
- Share only **load-bearing code snippets** — omit boilerplate the subagent can discover itself
- Require subagents to return: `{ status, file, summary }` — not full analysis text
- Include a **purpose statement** in every subagent prompt: "You are a subagent whose job is to [specific goal]"
- Never say "do everything" — list the 3-5 specific outputs expected
