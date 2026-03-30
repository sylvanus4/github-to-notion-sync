# today skill — autoimprove changelog

## Experiment #0 — Baseline

- **Score:** 12/25 (48%) — see `results.json` matrix
- **Gaps:** No natural-language routing for Korean sync-only / morning; no per-step error recovery table; CLI table lacked `Default` column and `skip-slack` row; no combined-flag example; Example 1 omitted phases 2.5, 3.5, 5b½, 5d, 5½, 6 ordering detail; Slack thread template had no standalone disclaimer line; strict E2 failed (not every script/MCP step had stated recovery).

## Experiments #1–#5 — Targeted mutations (batched in one edit pass)

1. **Natural language triggers** — Mapped all five test utterances to phase scope and flags (including `morning-ship` delegation and sync-only flag chain).
2. **Error recovery by step** — Added table covering Phase 0–6, Python scripts, Node report, evaluator, Slack MCP, Twitter.
3. **CLI Arguments** — Added **Default** column, documented `skip-slack`, **Combined flags** + `dry-run skip-twitter`, **Sync-only preset** cross-reference.
4. **Slack thread template** — Appended Korean mrkdwn disclaimer line for investment-not-advice.
5. **Examples** — Replaced Example 1 with full ordered checklist (Phases 0,1,2,2.5,3,3.5,4,4.5,5a–d,5½,5b½,6); added Example 1b for `dry-run skip-twitter`.

## Experiment #6 — Verification

- **Score:** 25/25 (100%) — all eval × input cells pass; **status: complete** (≥ 95% target).
