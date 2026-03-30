# skill-autoimprove — ai-workflow-integrator

## Experiment 0 — baseline

**Score:** 15/20 (75.0%)

**Change:** none

**Reasoning:** Strong stage composition and error policies; five fixed user phrases lacked a single lookup table tying delegation, merge, and flags.

**Result:** Partial passes on E1/E4 for prompts 1 and 3–5.

## Experiment 1 — keep

**Score:** 20/20 (100.0%)

**Change:** Added `## Meta-Orchestration` with prompt router, parallel-branch failure handling, and explicit post-run aggregation requirements plus `SKIP_DISCOVERY`, `PARALLEL_NEWS`, etc.

**Reasoning:** Aligns integrator behavior with evaluator expectations without duplicating Template A–D bodies.

**Result:** All four evals pass across the five test inputs.
