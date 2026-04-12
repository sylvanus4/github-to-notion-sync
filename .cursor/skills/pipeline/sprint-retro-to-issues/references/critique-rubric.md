---
name: critique-rubric
description: Quality gate rubric for adversarial review of extracted action items (Phase 4).
---

# Critique Rubric

## Scoring Dimensions

Score each action item on a 1-5 scale per dimension. An item must average >= 3.0 to pass without rewriting.

### 1. Completeness (1-5)

| Score | Criteria |
|-------|---------|
| 5 | All fields populated: title, description (50+ chars), acceptance criteria (2+), size, priority, category, source_quote |
| 4 | All required fields present, one optional field missing (dependencies or sprint_target) |
| 3 | Title, description, and priority present; acceptance criteria vague or single-item |
| 2 | Title and priority only; missing description or acceptance criteria |
| 1 | Title only; insufficient to create an actionable issue |

### 2. Clarity (1-5)

| Score | Criteria |
|-------|---------|
| 5 | A developer unfamiliar with the project could start work immediately after reading |
| 4 | A team member familiar with the project would need no clarification |
| 3 | Generally clear but one aspect requires inference or assumption |
| 2 | Ambiguous — multiple interpretations possible |
| 1 | Vague, abstract, or incomprehensible without additional context |

### 3. Actionability (1-5)

| Score | Criteria |
|-------|---------|
| 5 | Single concrete task, completable within the estimated size, clear start and end |
| 4 | Concrete task but might need one sub-task decomposition |
| 3 | Actionable but scope is borderline — could be split |
| 2 | More of a goal than a task — needs decomposition into 3+ sub-tasks |
| 1 | Aspirational statement, not an executable work item |

### 4. Traceability (1-5)

| Score | Criteria |
|-------|---------|
| 5 | source_quote directly quotes the retro discussion; source field is specific |
| 4 | source_quote paraphrases a specific discussion point accurately |
| 3 | source field is set but source_quote is generic or loosely connected |
| 2 | source field only; no supporting quote or reference |
| 1 | No connection to the retro content — appears fabricated |

### 5. Feasibility (1-5)

| Score | Criteria |
|-------|---------|
| 5 | Size/estimate is realistic, dependencies identified, no blockers apparent |
| 4 | Size/estimate reasonable; minor uncertainty about one dependency |
| 3 | Size might be underestimated by 1 level; dependencies partially identified |
| 2 | Size is clearly wrong (e.g., XS for a multi-file refactor); missing critical dependencies |
| 1 | Infeasible as described — requires resources, access, or skills not available |

## Pass/Fail Thresholds

| Average Score | Action |
|--------------|--------|
| >= 4.0 | PASS — create issue as-is |
| 3.0 - 3.9 | PASS with WARNINGS — note areas for improvement |
| 2.0 - 2.9 | REWRITE — improve description, acceptance criteria, and sizing before creation |
| < 2.0 | REJECT — flag for manual review, do not create issue |

## Adversarial Checks (Binary Pass/Fail)

These checks override the score-based pass:

| Check | Condition | Result |
|-------|-----------|--------|
| Empty acceptance criteria | `acceptance_criteria` is empty or all items < 10 chars | FAIL → rewrite |
| Stub description | `description` < 20 characters | FAIL → rewrite |
| Duplicate detection | Title or description >80% similar to another item | MERGE candidate → flag |
| Priority-size mismatch | P0 + XL → scope too large for "critical" | FLAG → suggest splitting |
| Orphan priority | P0/P1 with no acceptance criteria | FAIL → rewrite |

## Gap Detection Rules

After reviewing all individual items, check for coverage gaps:

1. **Topic coverage**: List all major topics from Phase 1 summary. Each should have >= 1 action item.
2. **Retro table coverage**: Each row in the retro table's "개선 아이디어" column should map to an item.
3. **Commitment coverage**: Scan transcript for commitment language and verify each is captured.
4. **Tech debt coverage**: Any mentioned tech debt should appear as a `tech-debt` category item.

Report gaps as warnings in `phase-4-critique.json → gap_warnings[]`.

## Rewrite Guidelines

When rewriting items that scored below 3.0:

1. Keep the original `source_quote` unchanged.
2. Expand `description` to include WHY, WHAT, and HOW.
3. Add 2-3 specific `acceptance_criteria` that are testable.
4. Adjust `size` and `estimate` if the original was unrealistic.
5. Preserve the original `id` — do not reassign.
