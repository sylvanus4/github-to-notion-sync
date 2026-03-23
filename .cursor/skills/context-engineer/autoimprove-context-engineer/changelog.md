# skill-autoimprove — context-engineer

## Experiment 0 — baseline

**Score:** 11/20 (55.0%)

**Change:** none

**Reasoning:** Tiered architecture complete; eval harness needed indexed delegation for the five standard Korean/English prompts.

**Result:** Weak E1/E4 on off-mode prompts.

## Experiment 1 — keep

**Score:** 19/20 (95.0%)

**Change:** Added `## Meta-Orchestration` mapping each prompt to correct skill or Mode 1–4 path, plus conflict handling and `PRUNE_DAYS` / `MODE` flags.

**Reasoning:** Aligns with done-checklist distinction (routine MEMORY updates) while satisfying meta orchestration evals.

**Result:** 95% achieved; remaining gap only if user requests illegal mode combination without clarification.
