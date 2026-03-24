# Doc Quality Gate — Autoimprove Changelog

Autonomous skill prompt optimization log.

**Target:** `.cursor/skills/doc-quality-gate/SKILL.md`
**Eval criteria:** 5 binary checks x 5 runs = max score 25
**Started:** 2026-03-24

## Eval Definitions

```
EVAL 1: Dimension Scoring — Does the output score all 6 dimensions (completeness, clarity, consistency, actionability, traceability, compliance)?
EVAL 2: Actionable Feedback — For each failing dimension, does the output provide specific location + concrete fix?
EVAL 3: Verdict — Does the output include a clear APPROVED/NEEDS REVISION verdict with the score?
EVAL 4: Type Detection — Does the skill correctly identify or use the specified document type to apply type-specific criteria?
EVAL 5: Red Flag Detection — Does the output flag vague terms ("적절한", "필요 시", "등") when present in requirements?
```

---

## Experiment 0 — baseline

**Score:** TBD
**Change:** None — original skill as-is
**Reasoning:** Establish measurement baseline before any mutations
**Result:** Pending first autoimprove run
**Failing outputs:** Pending
