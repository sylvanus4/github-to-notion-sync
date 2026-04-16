---
description: "Run the Planner-Generator-Evaluator (PGE) development loop — expand a prompt into a product spec, implement features incrementally, and evaluate with rubric-based scoring"
---

# PGE Loop

## Skill Reference

Read and follow the skill at `.cursor/skills/workflow/pge-loop/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

Determine the **mode** from user input:

- **--skip-planner**: Skip Phase 1 (Planner). Requires an existing spec at the path provided via `--spec-path`.
- **--spec-path [path]**: Path to an existing spec document. Used with `--skip-planner`.
- **--deliberate**: Include `omc-ralplan` 3-agent consensus loop in the Planner phase.
- **No flags**: Run the full PGE loop (Planner → Generator → Evaluator).

The remaining text (excluding flags) is the `prompt` — the product idea or feature request to expand.

### Step 2: Execute PGE Loop

Follow the `pge-loop` skill phases in order:

1. **Phase 1 (Planner)**: Expand the prompt into `spec.md` using `sp-brainstorming` + `spec-driven-development`. If `--deliberate`, add `omc-ralplan`. Skip if `--skip-planner`.
2. **Phase 2 (Generator)**: Implement features from the spec using `fe-pipeline` / `incremental-implementation`. One feature per sprint, self-evaluate with `tsc`/lint.
3. **Phase 3 (Evaluator)**: Run tool-based gates (`omc-ultraqa`), AI evaluation (`qa-dogfood`, `design-review`), and rubric scoring (`workflow-eval-opt` + `pge-rubric.yaml`).
4. **Phase 4 (Feedback Loop)**: If score < 7.5, feed specific feedback to Generator and repeat (max 2 iterations).

### Step 3: Summary

Report the final result:
- Spec path and scope summary
- Features implemented per sprint
- Final evaluation score (per dimension + composite)
- Pass/Fail status
- Remaining issues (if max iterations reached without passing)

## Constraints

- Planner must focus on product scope and UX, not technical implementation details
- Generator implements one feature at a time with periodic context resets
- Evaluator runs as `readonly` with `model: fast` to minimize cost
- Tool-based gates (tsc/lint/test) run before AI evaluation — hard fail skips AI eval
- Rubric defined in `.cursor/skills/workflow/pge-rubric.yaml`
- All artifacts persist to `outputs/pge/{date}/{slug}/`

## Examples

```bash
# Full PGE loop with a new feature idea
/pge 사용자 프로필 페이지 — 아바타, 활동 이력, 설정 관리

# Skip planner, use existing spec
/pge --skip-planner --spec-path outputs/pge/2026-04-15/profile/spec.md

# Include consensus planning for high-risk features
/pge --deliberate 멀티테넌시 프로젝트 전환 UI
```
