# Changelog — agentic-competency-framework autoimprove

## Baseline (v1.1.0)

- Starting version: 1.1.0 (post English translation + optimization)
- Baseline established: 2026-03-27
- **Score: 22/25 (88%)**
- Failures:
  - T2 EVAL 4: Mode 2 (single competency) produces no artifact file
  - T4 EVAL 4: Mode 2 (overview) produces no artifact file
  - T4 EVAL 5: Overview requests have no explicit next steps section
   - Weakness targets for mutation:
     1. Add artifact creation to Mode 2 workflow
     2. Add explicit "Next Steps" output section to Mode 2
     3. Add vague-input routing logic (default to Mode 1)

---

## Experiment 1 — Add Step 4 to Mode 2 (KEEP)

- **Hypothesis**: Mode 2 lacks artifact creation and explicit next steps, causing EVAL 4 and EVAL 5 failures on T2 and T4
- **Mutation**: Added "Step 4 — Save mapping report and suggest next steps" to Mode 2 workflow, producing `output/competency/skill-map-{date}.md` and requiring 2+ concrete next steps
- **Result**: 25/25 (100%) — +3 from baseline
- **Decision**: KEEP — all 3 identified weaknesses addressed in a single targeted mutation
- **Version**: 1.1.0 → 1.2.0

---

