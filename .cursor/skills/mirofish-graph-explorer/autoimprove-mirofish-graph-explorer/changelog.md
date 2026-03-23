# skill-autoimprove — mirofish-graph-explorer

## Experiment 0 (baseline)

- EVAL 4 passed (correct `/api/graph/*` and entity routes). EVAL 1–2 ambiguous for a read-only skill. EVAL 3 missing (no required structure for answers).

## Experiment 1

- Added **Quality Contract** explaining how each eval applies when the user only explores graphs vs when they need simulation.
- Documented mandatory summary shape for agent responses and a step-by-step semiconductor entity exploration using `by-type` filters + keyword matching.
- Clarified not to use non-existent `POST /graph` shorthands.
- **Files changed:** `SKILL.md`
