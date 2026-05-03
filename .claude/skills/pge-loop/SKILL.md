---
name: pge-loop
description: >-
  Planner-Generator-Evaluator orchestration loop that chains existing skills
  into a 4-phase development cycle: expand prompts into product specs
  (Planner), implement one feature at a time (Generator), score against a
  4-dimension rubric (Evaluator), and iterate with targeted feedback (Feedback
  Loop). Use when the user asks to "run PGE loop", "PGE", "planner generator
  evaluator", "PGE 루프", "PGE 실행", "기획-구현-평가 루프", "스펙부터 평가까지", "전체 개발 루프", "PGE
  pipeline", or wants a structured plan→build→evaluate cycle for frontend
  screen implementation. Do NOT use for individual planning (use
  sp-brainstorming). Do NOT use for code review without the full PGE cycle
  (use deep-review). Do NOT use for test-only runs (use omc-ultraqa). Do NOT
  use for fe-pipeline without evaluation intent (use fe-pipeline directly).
---

# PGE Loop — Planner-Generator-Evaluator Orchestrator

Thin harness that chains existing skills into an iterative development loop. Each phase delegates to specialist skills; this orchestrator manages sequencing, data flow, and the feedback cycle.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--skip-planner` | false | Skip Phase 1; use an existing spec file as input |
| `--deliberate` | false | Add `omc-ralplan` consensus loop in Phase 1 |
| `--with-pge` | true | Enable Phase 3 rubric evaluation (pass-through flag for fe-pipeline) |
| `--spec-path` | — | Path to existing spec when using `--skip-planner` |

## Output Directory

All artifacts persist to `outputs/pge/{YYYY-MM-DD}/{slug}/`:

```
outputs/pge/2026-04-16/user-settings/
├── spec.md              # Phase 1 output
├── sprint-1.md          # Phase 2 self-assessment per sprint
├── sprint-2.md
├── eval-v1.md           # Phase 3 evaluation report
├── eval-v2.md           # Phase 4 re-evaluation (if iteration occurred)
└── pge-report.md        # Final summary
```

## Phase 1 — Planner (Sequential)

**Goal**: Expand a short user prompt into an ambitious product spec focused on scope and UX, not implementation details.

**Planner Guardrail**: Do NOT specify libraries, implementation patterns, or technical architecture. Define WHAT the product does and WHO it serves. Use "Always / Ask first / Never" boundaries only.

### Steps

1. **Intent exploration** — invoke `sp-brainstorming`
   - Subagent: `subagent_type: generalPurpose`
   - Prompt: Explore user intent, generate 3+ alternative approaches, pressure-test assumptions (YC-style), get user approval on direction
   - Return: approved direction summary

2. **Spec generation** — invoke `spec-driven-development`
   - Subagent: `subagent_type: generalPurpose`
   - Input: approved direction from Step 1
   - Generate 6 sections: Objective, Commands, Structure, Style, Testing, Boundaries
   - Guardrail enforcement: reject any spec section containing implementation-specific technology choices; keep scope at product/UX level
   - Return: spec document

3. **Consensus review** (only if `--deliberate`) — invoke `omc-ralplan`
   - Subagent: `subagent_type: generalPurpose`
   - Run Planner → Architect → Critic loop (max 5 iterations)
   - Return: consensus-approved spec

4. **Persist**: Write final spec to `outputs/pge/{date}/{slug}/spec.md`

## Phase 2 — Generator (Sequential per feature)

**Goal**: Implement one feature/sprint at a time with self-validation before QA.

### Steps

1. **Decompose** spec into sprint-sized features (1 feature = 1 sprint)

2. **Per sprint**, invoke the appropriate generator:
   - New screen → `fe-pipeline` (with `--with-pge` flag to enable CP2.5 evaluation hook)
   - Feature addition to existing screen → `incremental-implementation`
   - Subagent: `subagent_type: generalPurpose`
   - Input: spec section for this sprint + relevant existing code context
   - Constraint: implement ONLY this sprint's scope

3. **Self-check** after each sprint:
   - Run `tsc --noEmit` (TypeScript compilation)
   - Run linter
   - If either fails → fix before proceeding

4. **Persist**: Write self-assessment to `outputs/pge/{date}/{slug}/sprint-{n}.md`

5. **Context reset**: Each sprint starts with fresh context (spec + sprint scope only)

## Phase 3 — Evaluator (Parallel fan-out → Sequential gate)

**Goal**: Score the implementation against `.cursor/skills/workflow/pge-rubric.yaml` using a 3-step pipeline.

### Step 1 — Tool-based gates (parallel, hard-fail)

Fan out 3 subagents simultaneously:

| Subagent | Skill | Goal | Hard fail? |
|----------|-------|------|------------|
| A | `omc-ultraqa` | `--goal typecheck` | Yes — tsc errors |
| B | `omc-ultraqa` | `--goal lint` | No — warnings acceptable |
| C | `omc-ultraqa` | `--goal tests` | Yes — test failures |

- If ANY hard-fail triggers → skip Step 2/3, return hard-fail feedback directly to Generator
- Subagent contract: `{ status: "pass"|"fail", error_count: N, summary: string }`

### Step 2 — AI-based evaluation (parallel, rubric scoring)

Fan out 2 subagents simultaneously:

| Subagent | Skill | Purpose | Model |
|----------|-------|---------|-------|
| D | `qa-dogfood --tier standard` | Health Score (functionality + visual) | default |
| E | `design-review` | Spec/Figma visual fidelity | default |

- Subagent contract: `{ health_score: N, findings: [{severity, description}], summary: string }`

### Step 3 — Integrated scoring (workflow-eval-opt)

Invoke `workflow-eval-opt` with:

```yaml
Generator task: "Implementation from Phase 2 (all sprint outputs)"
Evaluation criteria: <contents of .cursor/skills/workflow/pge-rubric.yaml dimensions + scoring_guide>
Quality threshold: 7.5
Max iterations: 1  # eval-opt handles its own internal iteration; PGE controls outer loop
Evaluator type: readonly, model: fast
Scope: modified files only
Additional context:
  - Step 1 results (tool gate pass/fail)
  - Step 2 results (health score + design review findings)
```

The evaluator scores each of the 4 dimensions using the rubric's scoring guide (1/5/10 anchors) and computes the weighted average per `.cursor/skills/workflow/pge-rubric.yaml` formula.

**Output**: evaluation report saved to `outputs/pge/{date}/{slug}/eval-v{N}.md`

### Decision gate

| Condition | Action |
|-----------|--------|
| `weighted_avg >= 7.5` AND no hard fails | **PASS** → proceed to Ship |
| `weighted_avg < 7.5` AND `iteration < max_iterations` | **ITERATE** → Phase 4 |
| `weighted_avg < 7.5` AND `iteration >= max_iterations` | **BEST EFFORT** → ship with quality warning |
| Score delta < 0.5 between iterations | **PLATEAU** → early stop, ship best version |

## Phase 4 — Feedback Loop

**Goal**: Feed evaluator feedback to Generator for targeted fixes (max 2 outer iterations).

### Steps

1. Extract `actionable_feedback` from evaluation report
2. Scope reduction: identify only the files/sections that need changes
3. Re-invoke Generator (Phase 2) with:
   - Original spec
   - Evaluation feedback (dimension scores + specific improvement items)
   - Scoped file list (do NOT regenerate passing code)
4. Re-run Evaluator (Phase 3)
5. Compare scores: if regression (v{N+1} < v{N}), keep v{N}

### Stopping criteria

Loop terminates when ANY condition is met:
- Score >= 7.5 with no hard fails
- 2 outer iterations completed
- Score plateau (delta < 0.5)
- Regression detected (new score < previous)

## Final Report

After the loop completes, generate `outputs/pge/{date}/{slug}/pge-report.md`:

```
PGE Loop Report
===============
Task: [user prompt]
Spec: outputs/pge/{date}/{slug}/spec.md
Iterations: {N} / 2
Final Score: {X.X} / 10.0
Status: PASS | BEST EFFORT | HARD FAIL

Dimension Scores:
  product_depth:  {score} / 10 (weight: 3)
  functionality:  {score} / 10 (weight: 3)
  visual_design:  {score} / 10 (weight: 2)
  code_quality:   {score} / 10 (weight: 2)

Iteration History:
  v1: {score} — {summary}
  v2: {score} — {summary}  (if applicable)

Hard Fails: {list or "none"}
Remaining Issues: {list or "none"}
Files Modified: {count}
```

## Skill Chaining Reference

| Phase | Skills Used | Pattern |
|-------|------------|---------|
| 1 Planner | sp-brainstorming → spec-driven-development → omc-ralplan (opt) | Sequential |
| 2 Generator | fe-pipeline / incremental-implementation | Sequential per sprint |
| 3 Evaluator | omc-ultraqa ×3 (parallel) → qa-dogfood + design-review (parallel) → workflow-eval-opt | Fan-out → Sequential |
| 4 Feedback | Phase 2 (scoped) → Phase 3 | Evaluator-Optimizer |

## Subagent Best Practices

- Pass **absolute file paths** — subagent working directories are unpredictable
- Share **spec context** but not full codebase dumps
- Require structured return format: `{ status, score?, summary, files_modified? }`
- Use `model: fast` for Evaluator subagents (cost control)
- Use `readonly: true` for evaluation-only subagents
