---
description: "Generate a response, score it against a quality rubric, and auto-revise weak dimensions"
argument-hint: "<question or task to answer and self-evaluate>"
---

# Self-Evaluation Scorecard

Generate a response, then score it against an explicit quality rubric. If any dimension scores below 7, auto-revise that section and re-score.

## Usage

```
/eval-self Write a technical design doc for migrating to event-driven architecture
/eval-self Explain the trade-offs of different caching strategies
/eval-self Create a runbook for handling database failover
/eval-self GPU 클라우드 플랫폼 가격 책정 전략 분석
/eval-self Design an onboarding flow for our developer platform
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Generate response** — Produce a complete answer to `$ARGUMENTS`
2. **Define rubric** — Score across 5 dimensions:
   - **Accuracy** (1-10): Are all facts, numbers, and claims correct?
   - **Completeness** (1-10): Does it cover all relevant aspects?
   - **Clarity** (1-10): Is it easy to follow and well-structured?
   - **Actionability** (1-10): Can the reader act on this immediately?
   - **Evidence Quality** (1-10): Are claims backed by data, examples, or citations?
3. **Score each dimension** — 1-10 with a one-line justification
4. **Calculate composite** — Average of all 5 dimensions
5. **Auto-revise** — If any dimension scores < 7, revise that section specifically
6. **Re-score** — Score the revised version

### Output Format

```
## Response
[Complete answer]

## Self-Evaluation Scorecard

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Accuracy | X/10 | [...] |
| Completeness | X/10 | [...] |
| Clarity | X/10 | [...] |
| Actionability | X/10 | [...] |
| Evidence Quality | X/10 | [...] |
| **Composite** | **X.X/10** | |

## Revisions (if any dimension < 7)
[Targeted improvements with before/after]

## Post-Revision Scores
[Updated scorecard]
```

### Constraints

- Scoring must be honest — inflated scores defeat the purpose
- Justifications must be specific: "Clarity: 6/10 — the caching strategy section jumps between L1/L2/distributed without transitions"
- If the composite stays below 7 after revision, acknowledge the limitation explicitly
- Do not revise dimensions scoring 8+ — avoid unnecessary changes

### Execution

Reference `ce-advanced-evaluation` (`.cursor/skills/ce/ce-advanced-evaluation/SKILL.md`) for rubric-based evaluation methodology. Reference `workflow-eval-opt` (`.cursor/skills/workflow/workflow-eval-opt/SKILL.md`) for the evaluator-optimizer loop pattern.
