# skill-autoimprove — ai-quality-evaluator

Evals: (1) Sub-skill delegation order (2) Error recovery (3) Output aggregation (4) Config/override. Test inputs ×4 = 20 binary cells.

## Experiment 0 — baseline

**Score:** 10/20 (50.0%)

**Change:** none (measured `SKILL.md.baseline`)

**Reasoning:** Core workflow strong for primary intent; adjacent prompts lacked explicit ordered handoffs, per-intent merge rules, and override keys.

**Result:** Failures clustered on E1/E3/E4 for non-primary prompts.

## Experiment 1 — keep

**Score:** 19/20 (95.0%)

**Change:** Added `## Meta-Orchestration` with five-row prompt router, error recovery table, aggregated output contract, and user overrides (`DATE`, paths, `SKIP_DB`).

**Reasoning:** Satisfies meta-orchestration evals across all five representative user phrases while preserving existing quality-dimension content.

**Result:** E1–E4 pass for mapped rows; one residual ambiguity if user mixes multiple intents in one message (document assumes single primary intent).
