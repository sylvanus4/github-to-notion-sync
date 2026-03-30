# Phase Templates

Default skill assignments for each of the 5 standard phases. The planner selects applicable skills based on goal domain and scope.

## Table of Contents

- [Phase 1: Survey and Gap Analysis](#phase-1-survey-and-gap-analysis)
- [Phase 2: Multi-Role Requirement Analysis](#phase-2-multi-role-requirement-analysis)
- [Phase 3: Research, Analysis, and Planning](#phase-3-research-analysis-and-planning)
- [Phase 4: Implementation](#phase-4-implementation)
- [Phase 5: Testing and Validation](#phase-5-testing-and-validation)
- [Phase Selection Quick Reference](#phase-selection-quick-reference)

## Phase 1: Survey and Gap Analysis

**Objective**: Map existing state against requirements. Identify gaps, ownership, and change risk.

**Default Skills**:

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Git history analysis | codebase-archaeologist | Ownership maps, churn hotspots, bus factor | A |
| Context restoration | recall | Cross-session context from MEMORY.md | A |
| Change risk assessment | refactor-simulator | Blast radius for areas needing changes | A |

**Input Sources**: README.md, MEMORY.md, tasks/todo.md, KNOWN_ISSUES.md, docs/prd/, docs/roadmap.md, docs/okrs.md

**Output**: `docs/project-survey-gap-analysis.md` with feature inventory, requirement traceability, tech debt inventory, known blockers.

---

## Phase 2: Multi-Role Requirement Analysis

**Objective**: Analyze the goal from 10 organizational perspectives. Synthesize into prioritized requirements.

**Default Skills**:

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Batch 1 | role-ceo | Strategic impact, market positioning | A |
| Batch 1 | role-cto | Architecture gaps, tech debt, security | A |
| Batch 1 | role-pm | PRD gaps, sprint priorities, OKR alignment | A |
| Batch 1 | role-developer | Implementation complexity, testing gaps | A |
| Batch 2 | role-cso | Market sizing, competitive positioning | B |
| Batch 2 | role-ux-designer | UX gaps, accessibility, design system | B |
| Batch 2 | role-security-engineer | STRIDE threats, OWASP gaps, compliance | B |
| Batch 2 | role-finance | ROI analysis, budget requirements | B |
| Batch 3 | role-sales | Sales enablement, demo needs | C |
| Batch 3 | role-hr | Team capacity, hiring needs | C |
| Orchestrator | role-dispatcher | Dispatches to all roles, collects results | - |
| Synthesis | executive-briefing | Cross-role consensus, conflict resolution | D |

**Input Sources**: Phase 1 output, project documentation

**Output**: `docs/multi-role-requirements-analysis.md` with 10 role sections (10 requirements each), consensus matrix, priority ranking.

---

## Phase 3: Research, Analysis, and Planning

**Objective**: Conduct research and produce a detailed implementation plan document.

**Default Skills**:

### 3A. Research (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Market research | pm-market-research | Personas, competitor analysis, market sizing | A |
| Product discovery | pm-product-discovery | Assumption testing, OST, feature prioritization | A |
| Strategy analysis | pm-product-strategy | Vision alignment, Lean Canvas, SWOT | A |
| Domain research | alphaear-search | Finance-domain web/local search | A |

### 3B. Planning (sequential)

| Sub-step | Skill | Purpose | Order |
|----------|-------|---------|-------|
| PRD writing | pm-execution | PRDs, OKRs, sprint breakdown, user stories | 1 |
| GTM strategy | pm-go-to-market | GTM for user-facing features, ICP validation | 2 |
| Metrics design | pm-data-analytics | Success metrics, cohort analysis, A/B plans | 3 |
| Growth planning | pm-marketing-growth | Positioning, value proposition refinement | 4 |

### 3C. Document Generation (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Technical docs | technical-writer | ADRs, API documentation updates | E |
| Architecture diagrams | visual-explainer | Data flow visualizations | E |
| Word document | anthropic-docx | Professional .docx output | E |
| Presentation | presentation-strategist | Presentation blueprint | E |

**Input Sources**: Phase 2 output, project documentation

**Output**: `docs/implementation-plan.md` + `outputs/implementation-plan.docx` with prioritized backlog, updated PRDs, sprint breakdown, architecture diagrams, success metrics, risk assessment.

---

## Phase 4: Implementation

**Objective**: Execute the plan using engineering skills.

**Default Skills**:

### 4A. Architecture and Design (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| System design | system-thinker | Data flows, feedback loops | A |
| Backend design | backend-expert | FastAPI services, Pydantic models | A |
| Frontend design | frontend-expert | React component architecture | A |
| DB design | db-expert | Schema changes, migrations, queries | A |
| UI/UX audit | design-architect | Design quality audit | B |

### 4B. Code Implementation (sequential by priority)

| Sub-step | Skill | Purpose | Order |
|----------|-------|---------|-------|
| Standards | ecc-coding-standards | TypeScript/Python coding standards | 1 |
| Existing solutions | ecc-search-first | Search before writing new code | 2 |
| Security review | security-expert | Threat modeling on new endpoints | 3 |
| Translation sync | i18n-sync | Translation keys for new UI strings | 4 |
| Dependency audit | dependency-auditor | CVE check on new dependencies | 5 |

### 4C. Code Review (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Multi-domain review | deep-review | 4-agent parallel review | C |
| Code quality | simplify | DRY, tech debt cleanup | C |
| Adversarial review | code-review-all | Crash checklist, security hacking | C |
| Quality loop | workflow-eval-opt | Iterative quality refinement | D |

### 4D. Ship (sequential)

| Sub-step | Skill | Purpose | Order |
|----------|-------|---------|-------|
| Documentation | technical-writer | ADRs, API docs, guides | 1 |
| Commits | domain-commit | Domain-split git commits | 2 |
| Push + PR | release-ship | Push and create PR | 3 |

**Input Sources**: Phase 3 output, implementation plan

**Output**: Committed code changes, open PR, updated documentation.

---

## Phase 5: Testing and Validation

**Objective**: Validate all implementations comprehensively.

**Default Skills**:

### 5A. Test Strategy (sequential)

| Sub-step | Skill | Purpose | Order |
|----------|-------|---------|-------|
| Strategy design | qa-test-expert | Unit, integration, E2E strategy | 1 |
| Test lifecycle | test-suite | Coverage review → generation → execution | 2 |

### 5B. Execution (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| CI pipeline | ci-quality-gate | Full local CI (lint, test, build) | A |
| E2E tests | e2e-testing | Playwright tests for new UI | A |
| Browser tests | playwright-runner | Ad-hoc browser automation | A |
| Web app tests | anthropic-webapp-testing | Playwright-based web testing | B |

### 5C. Security (parallel)

| Sub-step | Skill | Purpose | Parallel Group |
|----------|-------|---------|----------------|
| Threat model | security-expert | STRIDE, vulnerability assessment | C |
| Dependency scan | dependency-auditor | CVE scan on all deps | C |
| Compliance | compliance-governance | Data classification, access control | C |

### 5D. Final Validation (sequential)

| Sub-step | Skill | Purpose | Order |
|----------|-------|---------|-------|
| AI quality | ai-quality-evaluator | Score AI outputs for accuracy | 1 |
| Diagnosis | diagnose | 3-agent root cause for remaining issues | 2 |
| Release check | release-commander | Full release lifecycle validation | 3 |
| Ship | ship | Final pre-merge pipeline | 4 |

**Input Sources**: Phase 4 code changes, test configurations

**Output**: `docs/test-results-report.md` with coverage metrics, security scan results, performance benchmarks, AI quality scores, pass/fail summary.

---

## Phase Selection Quick Reference

| Goal Type | Phases | Typical Skill Count |
|-----------|--------|---------------------|
| Full feature development | 1, 2, 3, 4, 5 | 40-50 |
| Code-only task (no research) | 1, 4, 5 | 15-25 |
| Audit / review only | 1, 2, 5 | 20-30 |
| Research / planning only | 1, 2, 3 | 20-30 |
| Quick implementation | 4, 5 | 10-15 |
| Security audit | 1, 5 | 8-12 |
