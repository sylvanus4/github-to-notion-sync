---
name: deep-review
description: >-
  Run 4+1 parallel domain-expert reviews (Frontend, Backend/DB, Security, Test Coverage,
  and optional Architecture Deepening) to review code from multiple engineering perspectives
  and auto-fix findings. Supports diff/today/full scoping with adversarial tier scaling
  and 8/10 confidence gate.
disable-model-invocation: true
arguments: [scope]
---

# Deep Review — Multi-Domain Full-Stack Review

Review code from 4+1 engineering perspectives simultaneously. Complements `/simplify` (code craftsmanship) with domain expertise.

## Usage

```
/deep-review              # diff mode (default)
/deep-review today        # files changed today
/deep-review full         # entire project
/deep-review --arch       # include Architecture Deepening agent
```

## Scoping Modes

| Mode | Trigger | Scope |
|------|---------|-------|
| `diff` (default) | `/deep-review` | Git diff (unstaged + staged + HEAD) |
| `today` | `/deep-review today` | All files changed today |
| `full` | `/deep-review full` | All source files in the project |

## Adversarial Review Tiers

Review intensity scales with diff size:

| Diff Size | Tier | Behavior |
|-----------|------|----------|
| 1-50 lines | Standard | Normal 4-agent review |
| 51-200 lines | Elevated | Cross-file consistency checks added |
| 201-500 lines | Adversarial | "Find at least 3 issues. If zero, explain why provably correct." |
| 500+ lines | Critical | Adversarial + mandatory refine loop + blast radius warning |

## Confidence Gate (8/10)

Every finding must include a confidence score (1-10):
- **8-10**: Report and eligible for auto-fix
- **5-7**: Log internally, do not surface unless `--show-low-confidence`
- **1-4**: Discard silently

## Fix-First Pattern

| Category | Criteria | Action |
|----------|----------|--------|
| Auto-fixable | Single-file, mechanical (unused import, missing null check) | Fix silently, note in report |
| Requires judgment | Multi-file impact, architectural choice | Report with options |
| Informational | Best practice suggestion | Report as Low, never auto-fix |

## Workflow

### Step 1: Identify and Classify Files

Resolve target files based on scoping mode. Classify each by domain:
- **Frontend**: `*.tsx`, `*.jsx`, `*.vue`, `*.css`, files in `components/`, `pages/`
- **Backend**: `*.go`, `*.py`, `*.rs`, files in `services/`, `api/`, `handlers/`
- **Infra**: `*.yaml`, `*.yml`, `Dockerfile`, `*.tf`, `*.hcl`, Helm charts
- **Test**: `*_test.*`, `*.test.*`, `*.spec.*`

### Step 2: Fan Out 4+1 Review Agents

Launch parallel review agents, each analyzing the same files from their perspective:

**Agent 1: Frontend Review**
- Component architecture, prop typing, state management
- Performance (re-renders, bundle impact, lazy loading)
- Accessibility (ARIA, keyboard nav, contrast)

**Agent 2: Backend/DB Review**
- API design, error handling, input validation
- Database queries (N+1, missing indexes, migration safety)
- Concurrency, connection pooling, timeout handling

**Agent 3: Security Review**
- OWASP Top 10 quick checks
- Secret detection, injection vectors
- Auth/authz gaps, tenant isolation

**Agent 4: Test Coverage Review**
- Missing test cases for changed code
- Test quality (assertions, edge cases, mocking)
- Integration test gaps

**Agent 5 (optional, `--arch` or `full` scope): Architecture Deepening**
- Shallow module detection (many methods, no deep functionality)
- Architectural friction (circular deps, god objects, leaky abstractions)
- Seam analysis for testability and extensibility

### Step 3: Aggregate Findings

Merge all agent outputs, deduplicate overlapping findings, sort by severity:
1. Critical (security, data loss, crash)
2. High (correctness, performance regression)
3. Medium (code quality, maintainability)
4. Low (style, best practices)

### Step 4: Apply Auto-Fixes

For auto-fixable findings (confidence >= 8, single-file scope):
1. Apply fix
2. Run lint/typecheck on modified file
3. If lint fails, revert and report as manual fix needed

### Step 5: Generate Report

```markdown
## Deep Review Report

### Summary
- Files reviewed: N
- Findings: X Critical, Y High, Z Medium, W Low
- Auto-fixed: N issues
- Requires human judgment: M issues

### Findings by Domain
[grouped by agent, sorted by severity]

### Auto-Fixed Items
[list with before/after]

### Recommended Actions
[prioritized list]
```

## Test Invocation

```
/deep-review
/deep-review full --arch
/deep-review today focus on security
```
