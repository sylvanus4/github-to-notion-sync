# morning skill — skill-autoimprove changelog

## Experiment 0 (baseline)

- **Change**: None (copied to `SKILL.md.baseline`).
- **Scores**: EVAL1 Pass, EVAL2 Fail, EVAL3 Fail, EVAL4 Fail, EVAL5 Fail → **20%**
- **Rationale**: Phase order OK; Phase 3 had no MCP failure path; several flags lacked examples; Slack template was single-message without required thread + disclaimer; no numbered end-to-end walkthrough.

## Experiment 1 — CLI propagation and `--dry-run` semantics

- **Change**: Added “CLI propagation and defaults” under Options; clarified `--dry-run` table row (Today forward + Google Daily manual Slack skip; Phase 3 skipped).
- **Scores**: EVAL1 Pass, EVAL2 Fail, EVAL3 Fail, EVAL4 Fail, EVAL5 Fail → **20%** (only EVAL1 was already pass; this removes ambiguity for executors).
- **Verdict**: **Keep** — improves EVAL1 evidence and removes contradiction between “all phases” and Phase 3 skip.

## Experiment 2 — Phase 3 Slack: parent + thread + disclaimer + MCP recovery

- **Change**: Replaced single `slack_send_message` with Step A (parent: header + signal summary), Step B (`thread_ts` + detail + Korean disclaimer); added “Phase 3 — Error recovery (Slack MCP)” (retry once, log, stop Phase 3 without invalidating Phases 1–2).
- **Scores**: EVAL1 Pass, EVAL2 Pass, EVAL3 Fail, EVAL4 Pass, EVAL5 Fail → **60%**
- **Verdict**: **Keep**

## Experiment 3 — Per-flag examples and briefing/dry-run examples

- **Change**: Added “Skip consolidated briefing only”, “Per-flag reference” table mapping each CLI flag to a concrete `/morning …` example line; aligned test inputs 1–5 to documented commands.
- **Scores**: EVAL1 Pass, EVAL2 Pass, EVAL3 Pass, EVAL4 Pass, EVAL5 Fail → **80%**
- **Verdict**: **Keep**

## Experiment 4 — End-to-end walkthrough (all phases)

- **Change**: Added “End-to-end walkthrough (all phases, default flags)” with numbered steps 1–4 covering Google Daily, gate, Today full pipeline, Phase 3 (with skip conditions).
- **Scores**: All Pass → **100%**
- **Verdict**: **Keep**

## Final status

- **Stopped**: Target **≥95%** reached after experiment 4 (100%).
- **dashboard.html**: Skipped per user instruction.
