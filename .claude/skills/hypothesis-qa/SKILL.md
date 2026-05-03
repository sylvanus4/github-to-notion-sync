---
name: hypothesis-qa
description: >-
  Scientific-method investigation loop adapted for QA test failures: Observe
  test failure patterns in CI or test suites → Hypothesize root causes of
  flakiness or regression → Experiment with minimal targeted checks → Conclude
  with evidence-backed fix or test improvement. Persists reasoning to
  INVESTIGATION.md. Use when tests fail intermittently in CI (flaky), when a
  passing test suddenly regresses after a deploy, when test failures don't
  correlate with code changes, when CI is red but local is green, or when the
  user asks to "triage test failure", "hypothesis QA", "investigate flaky
  test", "why does this test fail in CI", "QA 가설 검증", "테스트 실패 진단", "플레이키 테스트
  조사", "회귀 테스트 원인", "CI 실패 가설 조사", "QA test triage". Do NOT use for debugging
  application code bugs without test context (use hypothesis-investigation).
  Do NOT use for writing new tests from scratch (use qa-test-expert). Do NOT
  use for test strategy design without a specific failure (use
  qa-test-expert). Do NOT use for E2E test creation (use e2e-testing). Do NOT
  use for general code review without test failure context (use deep-review).
disable-model-invocation: true
---

# Hypothesis-Driven QA Investigation

Adapted from the core `hypothesis-investigation` methodology for test failure triage.

## Iron Laws (QA Context)

1. **No test modifications before hypotheses are listed** — write ≥3 competing explanations for the failure
2. **Each experiment ≤ 5 lines of change** — isolate one variable (timing, data, env, assertion)
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if timing isn't the flake cause twice, move on
5. **Explicit predictions with pass/fail criteria** — "If H1 is correct, running with [X] should make it pass/fail consistently"

## Phase 1: Observe (Failure Signals)

1. **Identify the trigger** — which test(s) failed? Since when? In which environment?
2. **Collect failure data** — error messages, stack traces, CI logs, timing data
3. **Classify the failure**:
   - Flaky (intermittent) vs Deterministic (always fails)
   - Local vs CI-only vs Environment-specific
   - Regression (was passing) vs New (never passed)
4. **Map the working boundary** — which similar tests DO pass? What changed recently?
5. **Create investigation file** — initialize from `hypothesis-investigation/references/investigation-template.md`

Compose with: `qa-test-expert` (test analysis), `diagnose` (parallel RCA), `ci-quality-gate` (CI execution)

## Phase 2: Hypothesize (Competing Explanations)

Generate **minimum 3** competing explanations:
- **Flaky tests**: "Fails because of [race condition / timing / shared state / external dependency / resource contention]"
- **Regressions**: "Broke because of [code change / dependency update / config change / data migration]"
- **CI vs Local**: "Differs because of [env variable / Docker image / parallel execution / file system / timezone]"

Compose with: `sp-debugging` (systematic approach), `e2e-testing` (Playwright specifics)

## Phase 3: Experiment (Minimal Targeted Check)

Test one hypothesis at a time:
1. **For flaky tests** — add one log, one timing check, one isolation (run solo vs parallel)
2. **For regressions** — bisect to one commit, one dependency change, one config diff
3. **For CI/local mismatch** — compare one env variable, one Docker layer, one file path
4. Record prediction and actual result for each

Compose with: `e2e-testing` (Playwright), `ci-quality-gate` (CI execution), `omc-ultraqa` (autonomous QA cycling)

### Experiment Guardrails

- Maximum 10 experiments before stepping back to re-observe
- If all hypotheses are rejected, return to Phase 1 with new observations (add more logging, broader env diff)
- Always revert experimental changes before the next experiment
- Always log pivot decisions in INVESTIGATION.md Pivot Log section

## Phase 4: Conclude (Fix or Improve)

1. **State the validated finding** — one sentence: "Test X flakes because [root cause]"
2. **Apply the fix**:
   - Test-level fix? → Fix assertion, add retry, improve isolation
   - Code-level bug? → Fix the code, keep the test as regression guard
   - Environment issue? → Fix CI config, document requirements
3. **Verify stability** — run the test 10+ times to confirm it's no longer flaky
4. **Update INVESTIGATION.md** — complete all sections

Compose with: `qa-test-expert` (test improvement), `omc-ultraqa` (autonomous fix-verify cycling)

## Quality Gates

### Observation Quality Gate
Before proceeding to Phase 2, verify:
- [ ] Failure classified (flaky / deterministic / regression / environment-specific)
- [ ] CI logs and error messages collected
- [ ] Working boundary identified (which similar tests DO pass)
- [ ] Recent changes enumerated (commits, dependency updates, config changes)
- [ ] Investigation file created at `outputs/investigation/{date}/`

### Hypothesis Quality Gate
Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis targets one variable (timing, data, env, assertion)
- [ ] Each experiment designed ≤ 5 lines of change
- [ ] Pass/fail predictions written for each experiment

### Conclusion Quality Gate
Before declaring done:
- [ ] Root cause documented in one sentence
- [ ] Fix applied (test-level, code-level, or environment-level)
- [ ] Stability verified (10+ consecutive passes)
- [ ] Experimental changes reverted before fix applied
- [ ] INVESTIGATION.md fully completed

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| "Let me just skip this flaky test" | Masks real bugs that surface in production | Investigate root cause with hypotheses |
| Rewriting the entire test | Can't tell if the test was wrong or the code | Max 5 lines per experiment |
| Running only locally after CI failure | Misses env-specific causes | Test hypothesis in the failing environment |
| Blaming "infrastructure" without evidence | Stops investigation prematurely | Require proof: specific env diff, timing data |
| Adding `retry(3)` without understanding | Hides intermittent bugs | Find and fix the race/timing/state issue |

## Harness Integration

Integrates into `engineering-harness` alongside the existing test review agents. Also composes with `omc-ultraqa` as the hypothesis-driven investigation mode when autonomous QA cycling detects persistent failures.
