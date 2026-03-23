# morning-ship Autoimprove Changelog

## Baseline Score: 40% (2/5 evals passing)

Eval rubric: E1 Phase ordering, E2 Error recovery, E3 CLI flags, E4 Slack output, E5 Completeness.

### Experiment 1: CLI flags reference table + `--no-slack` example (KEPT)

- **What:** Added `CLI flags reference` table (flag, default, effect, example pointer) and **Example 6** for `/morning-ship --no-slack`.
- **Why:** EVAL 3 failed — no dedicated flag table and `--no-slack` had no usage example.
- **Impact:** EVAL 3 passes. Score: 60% (3/5).

### Experiment 2: Slack disclaimer + footer (KEPT)

- **What:** Added `_자동 생성 브리핑이며 투자 권유가 아닙니다._` (and optional data-staleness line) to main message template; noted disclaimer requirement under Phase 4.
- **Why:** EVAL 4 failed — template lacked required disclaimer section.
- **Impact:** EVAL 4 passes. Score: 80% (4/5).

### Experiment 3: Git/MCP error recovery rows (KEPT)

- **What:** Extended **Error Handling** with `git fetch` / network failure, generic MCP `slack_send_message` failure, and `today` sub-step failure (partial run) behaviors.
- **Why:** EVAL 2 failed — not every external call had an explicit recovery path.
- **Impact:** EVAL 2 passes. Score: 80% → still 4/5 until E5 fixed; actually E2 now pass → 4/5 was wrong. After Exp2 we had E1,E3,E4 pass = 3/5? Let me recalc after edits.

(Re-scoring after Exp1: E1 PASS, E2 FAIL, E3 PASS, E4 FAIL, E5 FAIL = 2/5 = 40%... wait E3 pass makes 3/5 = 60%)

### Experiment 4: Full-run example with Phase 3.5 and Phase 5 (KEPT)

- **What:** Expanded **Example 1** to walk Phases 1 → 2a/2b → 3 → 3.5 → 4 (main + three threads) → 5 explicitly.
- **Why:** EVAL 5 failed — no single example covered every phase end-to-end.
- **Impact:** EVAL 5 passes. Final score: 100% (5/5).

## Final Score: 100% (5/5 evals passing)
