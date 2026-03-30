# demo-analyzer — skill-autoimprove changelog

## Experiment 1 — keep

**Score:** estimated baseline analysis → post-mutation estimate ~22/25 (from ~16/25)

**Change:** (1) Procedure step 6: mandated **numbered** screen inventory table (S1…, columns including evidence); **state matrix** as Markdown table with **≥3 state types per major screen** and `미확인(사유)` cells; **≥3 edge rows per major feature** with trigger / observed behavior / verification status; **open questions** format binding screen ID, concrete behavior, owner, next action. (2) Output structure: evidence index must pair **URL at capture** with screenshot or snapshot summary. (3) Quality checklist mapped to E1–E5; Evolution section aligned with `eval-criteria.md` pass/fail wording. Version bump `1.1.0` → `1.2.0`.

**Reasoning:** Baseline SKILL mentioned tables and sections but did not enforce eval pass conditions (numbering, minimum state types, minimum edges per feature, URL+visual grounding, anti-vague open questions), so outputs could pass internal checklist yet fail binary evals.

**Result:** Expected higher reliability on E1–E5: consolidated numbered inventory, non-prose state coverage, quantified edge cases, explicit visual/URL evidence, and auditable open-question shape.
