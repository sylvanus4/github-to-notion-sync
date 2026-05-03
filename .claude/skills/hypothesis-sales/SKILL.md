---
name: hypothesis-sales
description: >-
  Scientific-method investigation loop adapted for Sales: Observe deal signals
  → Hypothesize why deals stall/fail → Experiment with minimal outreach
  adjustments → Conclude with evidence-backed sales strategy changes. Persists
  reasoning to INVESTIGATION.md. Use when deals stall without clear reason,
  when win rates drop unexpectedly, when a sales motion stops working, when
  pipeline velocity decreases, or when the user asks to "diagnose deal",
  "hypothesis sales", "investigate pipeline", "why did we lose", "sales deal
  diagnosis", "딜 진단", "영업 가설 검증", "파이프라인 조사", "왜 졌는지 분석". Do NOT use for lead
  prospecting without a diagnostic question (use kwp-apollo-prospect). Do NOT
  use for call prep without investigation intent (use kwp-sales-call-prep). Do
  NOT use for competitive intelligence without a deal-loss hypothesis (use
  kwp-sales-competitive-intelligence). Do NOT use for account research without
  a stall diagnosis (use kwp-sales-account-research). Do NOT use for product
  feature adoption diagnosis (use hypothesis-pm).
---

# Hypothesis-Driven Sales Investigation

Adapted from the core `hypothesis-investigation` methodology for sales deal diagnosis.

## Iron Laws (Sales Context)

1. **No strategy changes before hypotheses are listed** — write ≥3 competing explanations for the stall/loss
2. **Each test ≤ 1 outreach or data check** — test one variable at a time
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if the same objection-handling approach fails twice, switch
5. **Explicit predictions before each test** — "If this is the blocker, the prospect should respond with [X]"

## Phase 1: Observe (Deal Signals)

1. **Identify the trigger** — which deal stalled, which metric dropped, which motion stopped working?
2. **Collect deal data** — email response rates, meeting outcomes, objection patterns, competitor mentions
3. **Map the pipeline** — which stages have the longest dwell time? Where do deals drop off?
4. **Working boundary** — which deals ARE progressing? Which segments ARE converting?
5. **Create investigation file** — initialize from `hypothesis-investigation/references/investigation-template.md`

Compose with: `kwp-sales-account-research`, `kwp-common-room-account-research`, `kwp-sales-daily-briefing`

## Phase 2: Hypothesize (Competing Explanations)

Generate **minimum 3** competing explanations:
- "Deals stall at stage X because [pricing / champion / timing / competitor]"
- "Win rate dropped because [ICP drift / messaging / market shift]"
- "Pipeline velocity decreased because [lead quality / qualification / handoff]"

Compose with: `kwp-sales-competitive-intelligence`, `kwp-common-room-contact-research`

## Phase 3: Experiment (Minimal Validation)

Test one hypothesis at a time:
1. Check one specific data point (email analytics, call outcome, competitor feature)
2. Run one targeted outreach variation
3. Analyze one lost-deal debrief

Compose with: `kwp-sales-draft-outreach`, `kwp-common-room-compose-outreach`, `kwp-sales-call-prep`

### Experiment Guardrails

- Maximum 7 tests before stepping back to re-observe with fresh pipeline data
- If all hypotheses are rejected, return to Phase 1 — the diagnosis framing may be wrong
- Always log pivot decisions in INVESTIGATION.md Pivot Log section

## Phase 4: Conclude (Strategy Adjustment)

1. **State the validated finding** — one sentence
2. **Map to action** — battlecard update, messaging pivot, ICP refinement, process change
3. **Track impact** — measure next-period win rate against the change

Compose with: `kwp-sales-competitive-intelligence` (battlecard update), `kwp-sales-create-an-asset` (collateral refresh)

## Quality Gates

### Observation Quality Gate
Before proceeding to Phase 2, verify:
- [ ] Deal/pipeline trigger clearly identified
- [ ] Deal data collected (response rates, objection patterns, competitor mentions)
- [ ] Pipeline stage dwell times mapped
- [ ] Working boundary identified (which deals/segments ARE converting)
- [ ] Investigation file created at `outputs/investigation/{date}/`

### Hypothesis Quality Gate
Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis has supporting/conflicting deal data
- [ ] Each hypothesis has a designed test (1 outreach or data check)
- [ ] Predictions written for each test (expected prospect response)

### Conclusion Quality Gate
Before declaring done:
- [ ] Validated finding documented in one sentence
- [ ] Action mapped to specific sales asset (battlecard, messaging, ICP, process)
- [ ] Impact tracking metric defined for next period
- [ ] INVESTIGATION.md fully completed and archived

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| "We lost because of price" (no evidence) | Stops investigation at the easiest excuse | List 3+ hypotheses, verify with actual prospect feedback |
| Changing the entire pitch after one loss | Can't isolate what failed | Test one messaging variable at a time |
| Blaming the prospect without data | Avoids systemic issues in the sales motion | Look for patterns across multiple deals |
| Assuming the competitor won on features | Ignores timing, relationship, or process factors | Check champion strength, timeline, and process fit |

## Harness Integration

Integrates into `sales-harness` as a diagnostic mode when pipeline metrics deviate from targets.
