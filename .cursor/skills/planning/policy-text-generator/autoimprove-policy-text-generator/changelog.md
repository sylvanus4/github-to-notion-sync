# Policy Text Generator — Autoimprove Changelog

Autonomous skill prompt optimization log.

**Target:** `.cursor/skills/policy-text-generator/SKILL.md`
**Eval criteria:** 5 binary checks x 5 runs = max score 25
**Started:** 2026-03-24

## Eval Definitions

```
EVAL 1: Policy Rule Extraction — Does the output correctly identify and list mandatory/forbidden rules from the policy source?
EVAL 2: Compliance Scoring — Does the output include a scored compliance breakdown per dimension?
EVAL 3: Multiple Candidates — Does the output present 3 distinct text candidates with individual scores?
EVAL 4: Error Guidance — When given an invalid policy source, does the skill stop and ask for correction?
EVAL 5: Korean Output — Is the generated text in Korean with English technical terms retained?
```

---

## Experiment 0 — baseline

**Score:** TBD
**Change:** None — original skill as-is
**Reasoning:** Establish measurement baseline before any mutations
**Result:** Pending first autoimprove run
**Failing outputs:** Pending
