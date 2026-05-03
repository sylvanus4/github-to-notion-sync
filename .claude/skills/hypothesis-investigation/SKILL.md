---
name: hypothesis-investigation
description: >-
  Scientific-method investigation loop (Observe → Hypothesize → Experiment →
  Conclude) for debugging non-trivial code bugs, performance regressions, and
  system-level issues where guessing wastes tokens. Forces evidence
  persistence to INVESTIGATION.md, minimum 3 hypotheses before experimenting,
  max 5-line code changes, and mandatory pivot after 2 same-direction
  failures. Use when encountering a code bug that resists a quick fix, when
  initial debugging attempts fail, when the 30-minute bugfix rule triggers,
  when "diagnose --hypothesis-mode" is invoked, or when the user asks to
  "hypothesis investigation", "scientific debug", "hypothesis-driven debug",
  "가설 기반 디버깅", "가설 조사", "investigate this code bug", "stop guessing and
  reason", "evidence-based debug". Do NOT use for trivial one-line fixes with
  obvious root cause. Do NOT use for test suite flakiness or CI failures (use
  hypothesis-qa). Do NOT use for code review without a specific bug (use
  deep-review or simplify). Do NOT use for test strategy design (use
  qa-test-expert). Do NOT use for PM assumption validation (use
  hypothesis-pm). Do NOT use for general code exploration without a failure to
  investigate (use SemanticSearch or Grep directly).
disable-model-invocation: true
---

# Hypothesis-Driven Investigation

## Iron Laws

1. **No code changes before hypotheses are listed** — write ≥3 hypotheses in INVESTIGATION.md first
2. **Each experiment ≤ 5 lines of change** — surgical precision, not shotgun debugging
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if H1 fails twice, you MUST switch to a different hypothesis
5. **Explicit predictions before experiments** — write "expected if confirmed" AND "expected if rejected" before running

## Phase 1: Observe

Gather raw facts without interpretation. Do NOT theorize yet.

1. **Reproduce the failure** — get a reliable repro or document intermittent pattern
2. **Record exact error** — full stack trace, log output, or behavioral description
3. **Map the working boundary** — what nearby functionality DOES work? This narrows the search space
4. **Note environment details** — versions, config, OS, recent changes
5. **Create the investigation file**:
   ```
   mkdir -p outputs/investigation/$(date +%Y-%m-%d)
   ```
   Initialize `INVESTIGATION.md` from the template at `references/investigation-template.md`

### Observation Quality Gate

Before proceeding to Phase 2, verify:
- [ ] Failure is reproducible (or intermittent pattern documented)
- [ ] Exact error message/behavior recorded
- [ ] Working boundary identified (what works vs what doesn't)
- [ ] Environment captured

## Phase 2: Hypothesize

Generate **minimum 3** competing explanations. More is better — the goal is to avoid anchoring on the first idea.

1. **List assumptions** — what are you assuming about the system? Challenge each one
2. **Generate hypotheses** — each must be:
   - Falsifiable (an experiment can reject it)
   - Specific (names a component, line, or interaction)
   - Independent (testing one doesn't invalidate another)
3. **Rank by evidence** — for each hypothesis, list supporting and conflicting evidence from Phase 1
4. **Design minimal experiments** — each test should be ≤ 5 lines of change with predicted outcomes
5. **Write everything to INVESTIGATION.md** — hypotheses, evidence, and planned experiments

### Hypothesis Quality Gate

Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis has supporting/conflicting evidence
- [ ] Each hypothesis has a designed experiment (≤ 5 lines)
- [ ] Predictions written for each experiment (confirmed vs rejected outcomes)

## Phase 3: Experiment

Test hypotheses one at a time. Each experiment is a controlled, reversible change.

1. **Pick the hypothesis with the strongest evidence** — start where the odds are best
2. **Make the minimal change** (≤ 5 lines) — do NOT fix the bug yet, just test the hypothesis
3. **Record the prediction** — "If H1 is correct, I expect [X]. If H1 is wrong, I expect [Y]"
4. **Run the experiment** — execute the repro steps
5. **Record the actual result** — compare to prediction
6. **Verdict**: CONFIRMED / REJECTED / INCONCLUSIVE
7. **Revert the experiment** — unless it's the confirmed fix
8. **Update INVESTIGATION.md** — log everything

### Pivot Rule (CRITICAL)

If the same hypothesis direction fails **twice in a row**:
- You MUST switch to a different hypothesis
- Log the pivot in the Pivot Log section
- The failed direction is deprioritized until new evidence emerges

### Experiment Guardrails

- Maximum 10 experiments before stepping back to re-observe
- If all hypotheses are rejected, return to Phase 1 with new observations
- Never modify more than 5 lines per experiment
- Always revert experimental changes before the next experiment

## Phase 4: Conclude

Once a hypothesis is confirmed, apply the fix with discipline.

1. **State the root cause** — one sentence in INVESTIGATION.md
2. **Apply the minimal fix** — follow karpathy-coding-guard principles:
   - Surface assumptions before coding
   - Keep the fix as simple as possible
   - Verify against the original repro
3. **Write a regression test** — the bug must never return
4. **Verify the fix** — run the repro steps and confirm resolution
5. **Update INVESTIGATION.md** — complete the Fix section with files changed, test location, and verification command
6. **Archive** — the investigation file persists at `outputs/investigation/{date}/` for future reference

### Conclusion Quality Gate

Before declaring done:
- [ ] Root cause documented in one sentence
- [ ] Fix applied with minimal changes
- [ ] Regression test written and passing
- [ ] Original repro confirmed fixed
- [ ] INVESTIGATION.md fully completed

## Composing with Other Skills

This skill composes with:
- **diagnose** — invoke with `--hypothesis-mode` to use this methodology within the 3-agent parallel analysis
- **karpathy-coding-guard** — Phase 4 fix follows its principles (assumptions, simplicity, surgical changes)
- **bugfix-loop.mdc** — this skill is the structured fallback when the 30-Minute Rule triggers
- **sp-debugging** — can be used for initial observation gathering in Phase 1
- **problem-definition** — the 5D framework can feed into Phase 2 hypothesis generation

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| "Let me just try this fix" | Skips hypothesis → wastes tokens on wrong direction | Write 3+ hypotheses first |
| Changing 50 lines "to be safe" | Can't tell what fixed what | Max 5 lines per experiment |
| Keeping evidence in context only | Context compaction destroys reasoning chain | Write to INVESTIGATION.md |
| Doubling down on failed hypothesis | Confirmation bias wastes iterations | Pivot after 2 same-direction failures |
| Testing multiple hypotheses at once | Can't attribute results | One hypothesis per experiment |
