---
name: prd-lifecycle-orchestrator
description: >-
  End-to-end PRD lifecycle pipeline: research-backed PRD generation with
  quality gate loop, cascade sync to dependent documents, and stakeholder
  review orchestration. Chains prd-research-factory → doc-quality-gate
  (evaluator-optimizer loop, max 2 iterations) → prd-cascade-sync →
  doc-review-orchestrator. Use when the user asks for "PRD lifecycle",
  "full PRD pipeline", "PRD end-to-end", "PRD 라이프사이클", "PRD 전체
  파이프라인", "기획서 전체 프로세스", or wants automated PRD creation through
  stakeholder review. Do NOT use for PRD creation only (use prd-research-
  factory). Do NOT use for doc quality check only (use doc-quality-gate).
  Do NOT use for simple PRD without research (use pm-execution create-prd).
metadata:
  version: "1.0.0"
  tags: ["orchestrator", "planning", "prd", "harness", "pipeline-quality-gate"]
  pattern: "pipeline with quality gates (evaluator-optimizer)"
  composes:
    - prd-research-factory
    - doc-quality-gate
    - prd-cascade-sync
    - doc-review-orchestrator
---

# Planning PRD Lifecycle Orchestrator

Pipeline with quality gates: research → quality gate (loop) → cascade → review.

## Usage

```
/prd-lifecycle "meeting URL or transcript"    # Full PRD lifecycle from meeting
/prd-lifecycle "topic description"            # Full lifecycle from topic
/prd-lifecycle --skip cascade,review          # Skip specific phases
/prd-lifecycle --max-iterations 1             # Single quality gate pass
/prd-lifecycle --dry-run                      # Show plan without executing
```

## Skip Flags

| Flag | Skips | Default |
|------|-------|---------|
| `research` | `prd-research-factory` (Phase 1) | included |
| `quality` | `doc-quality-gate` (Phase 2) | included |
| `cascade` | `prd-cascade-sync` (Phase 3) | included |
| `review` | `doc-review-orchestrator` (Phase 4) | included |

## Agent Team

| Phase | Agent | Skill | Execution | Output |
|-------|-------|-------|-----------|--------|
| 1 | Research Factory | `prd-research-factory` | Task (opaque) | `_workspace/prd-lifecycle/01_prd.md` |
| 2 | Quality Gate | `doc-quality-gate` | Task (loop) | `_workspace/prd-lifecycle/02_quality.md` |
| 3 | Cascade Sync | `prd-cascade-sync` | Task | `_workspace/prd-lifecycle/03_cascade.md` |
| 4 | Review Orchestrator | `doc-review-orchestrator` | Task | `_workspace/prd-lifecycle/04_review.md` |

## Workflow

### Pre-flight

1. Parse `$ARGUMENTS` for input (meeting URL, transcript text, or topic), `--skip`, `--max-iterations` (default: 2), `--dry-run`.
2. `Shell: mkdir -p _workspace/prd-lifecycle`
3. If `--dry-run`, print the execution plan and stop.

### Phase 1: Research-Backed PRD Generation

Launch 1 Task for `prd-research-factory` (treated as opaque — its 7 internal phases stay internal):

```
You are a PRD researcher and writer.

## Skill Reference
Read and follow `.cursor/skills/planning/prd-research-factory/SKILL.md`.

## Task
Generate a comprehensive PRD from the following input:
{meeting URL, transcript, or topic description}

Run the full 7-phase pipeline: meeting analysis → market research →
fact verification → PRD writing → competitive analysis → market sizing →
confidence scoring.

## Output
Write the complete PRD to `_workspace/prd-lifecycle/01_prd.md`.

## Completion
Return PRD title and section count.
```

### Phase 2: Quality Gate (Evaluator-Optimizer Loop)

Unless `--skip quality`:

Launch `doc-quality-gate` in an evaluator-optimizer loop:

**Iteration 1:**
```
You are a document quality evaluator.

## Skill Reference
Read and follow `.cursor/skills/planning/doc-quality-gate/SKILL.md`.

## Task
Evaluate the PRD at `_workspace/prd-lifecycle/01_prd.md` against quality criteria:
- Completeness (all required PRD sections present)
- Specificity (measurable requirements, not vague)
- Consistency (no contradictions between sections)
- Source attribution (data claims cite sources)
- Actionability (clear enough for engineering to implement)

## Output
Write quality report to `_workspace/prd-lifecycle/02_quality.md`.
Include an overall score (1-10) and per-dimension scores.

## Completion
Return the overall score and PASS/FAIL verdict.
```

**Gate logic:**
- **Score >= 8.0** → PASS — proceed to Phase 3
- **Score 6.0–7.9** → REFINE — feed quality feedback back to Phase 1 (regenerate weak sections only), then re-evaluate (max `--max-iterations` total, default 2)
- **Score < 6.0** → FAIL — halt pipeline, report score breakdown to user

**Refinement (if needed):**
```
You are a PRD editor.

## Context
Read the original PRD at `_workspace/prd-lifecycle/01_prd.md`.
Read the quality feedback at `_workspace/prd-lifecycle/02_quality.md`.

## Task
Address ONLY the specific quality issues identified in the feedback.
Do not rewrite sections that scored well.

## Output
Write the refined PRD to `_workspace/prd-lifecycle/01_prd.md` (overwrite).

## Completion
Return list of sections refined.
```

**Stopping criteria:**
- Score reaches >= 8.0
- Max iterations reached (proceed with best version, note quality score)
- No improvement between iterations (score delta < 0.5)

### Phase 3: Cascade Sync

Unless `--skip cascade`:

Launch 1 Task for `prd-cascade-sync`:

```
You are a document dependency manager.

## Skill Reference
Read and follow `.cursor/skills/planning/prd-cascade-sync/SKILL.md`.

## Context
Read the finalized PRD at `_workspace/prd-lifecycle/01_prd.md`.

## Task
Propagate PRD changes to dependent documents:
- Technical specifications
- API contracts
- Test plans
- Timeline documents

Identify which dependent docs need updates and generate change summaries.

## Output
Write cascade report to `_workspace/prd-lifecycle/03_cascade.md`.

## Completion
Return count of dependent docs identified and updated.
```

### Phase 4: Stakeholder Review

Unless `--skip review`:

Launch 1 Task for `doc-review-orchestrator`:

```
You are a review coordinator.

## Skill Reference
Read and follow `.cursor/skills/planning/doc-review-orchestrator/SKILL.md`.

## Context
Read the finalized PRD at `_workspace/prd-lifecycle/01_prd.md`.
Read the quality report at `_workspace/prd-lifecycle/02_quality.md`.

## Task
Orchestrate stakeholder review:
1. Identify required reviewers (PM, Engineering, Design, QA)
2. Generate review request with PRD summary and key decision points
3. Create Notion page for the PRD
4. Post review request to Slack

## Output
Write review coordination report to `_workspace/prd-lifecycle/04_review.md`.
Include Notion page URL and Slack message timestamp.

## Completion
Return review status and reviewer list.
```

### Final Output

Produce summary at `outputs/prd-lifecycle/prd-{date}-{slug}.md`:

```markdown
# PRD Lifecycle Summary — {date}

## PRD: {title}

## Quality Score: {score}/10 ({iterations} iteration(s))

## Cascade Impact
{count} dependent documents identified

## Review Status
{reviewer list and status}

## Artifacts
- PRD: _workspace/prd-lifecycle/01_prd.md
- Quality Report: _workspace/prd-lifecycle/02_quality.md
- Cascade Report: _workspace/prd-lifecycle/03_cascade.md
- Review Report: _workspace/prd-lifecycle/04_review.md
```

## Error Handling

| Failure | Action |
|---------|--------|
| Research factory fails | Abort — PRD is the foundation. |
| Quality gate fails to evaluate | Skip gate, proceed with warning. |
| Quality score < 6.0 after max iterations | Halt and report to user with breakdown. |
| Cascade sync fails | Log warning. Proceed to review with note. |
| Review orchestrator fails | Log warning. PRD is still available. |

## Data Flow

```
Input (meeting URL | transcript | topic)
    │
    ▼
Phase 1: Research Factory (opaque, 7 phases)
    │   → 01_prd.md
    │
    ▼
Phase 2: Quality Gate (evaluator-optimizer loop)
    │   doc-quality-gate → score
    │   ├─ >= 8.0 → PASS
    │   ├─ 6.0-7.9 → REFINE → re-evaluate (max 2 iterations)
    │   └─ < 6.0 → FAIL (halt)
    │   → 02_quality.md
    │
    ▼
Phase 3: Cascade Sync
    │   prd-cascade-sync → propagate changes
    │   → 03_cascade.md
    │
    ▼
Phase 4: Stakeholder Review
    │   doc-review-orchestrator → coordinate reviews
    │   → 04_review.md + Notion + Slack
    │
    ▼
Output: outputs/prd-lifecycle/prd-{date}-{slug}.md
```
