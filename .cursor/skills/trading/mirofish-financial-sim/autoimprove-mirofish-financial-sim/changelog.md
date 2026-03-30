# skill-autoimprove — mirofish-financial-sim

## Experiment 0 (baseline)

- Eval failures: EVAL 4 (`simulation/create` body did not match production API); EVAL 1–3 mostly absent for structured seeds and reports.

## Experiment 1

- Replaced incorrect `create` example with full Phase-1/2 HTTP sequence aligned to `mirofish`.
- Added **Quality Contract** covering seed markdown rules, parameter defaults (rounds, agents, project_name), report deliverable bullets, and explicit endpoint list.
- Wired Fed / NVDA prompt hints into EVAL 1 section.
- **Files changed:** `SKILL.md`
