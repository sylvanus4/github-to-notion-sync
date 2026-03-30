# Spec-State Validator — Autoimprove Changelog

Autonomous skill prompt optimization log.

**Target:** `.cursor/skills/spec-state-validator/SKILL.md`
**Eval criteria:** 5 binary checks x 5 runs = max score 25
**Started:** 2026-03-24

## Eval Definitions

```
EVAL 1: Spec Parsing — Does the output extract testable artifacts (states, transitions, edge cases) from the spec?
EVAL 2: Code Scanning — Does the output search code files and report file:line locations for found artifacts?
EVAL 3: Gap Classification — Does the output classify gaps as covered/partial/missing/contradicting?
EVAL 4: Coverage Metric — Does the output include a coverage percentage with the formula (covered / total)?
EVAL 5: Remediation Plan — Does the output provide an ordered list of items to fix, grouped by severity?
```

---

## Experiment 0 — baseline

**Score:** TBD
**Change:** None — original skill as-is
**Reasoning:** Establish measurement baseline before any mutations
**Result:** Pending first autoimprove run
**Failing outputs:** Pending
