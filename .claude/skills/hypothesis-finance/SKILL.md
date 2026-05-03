---
name: hypothesis-finance
description: >-
  Scientific-method investigation loop adapted for Finance: Observe variance
  signals → Hypothesize root causes of financial deviations → Experiment with
  minimal data checks → Conclude with evidence-backed explanations and
  corrective actions. Persists reasoning to INVESTIGATION.md. Use when
  budget-vs-actual variance exceeds thresholds, when reconciliation items are
  unexplained, when cash flow deviates from forecast, when financial close
  reveals anomalies, or when the user asks to "investigate variance",
  "hypothesis finance", "diagnose budget deviation", "why is revenue off",
  "variance root cause", "재무 가설 조사", "예산 차이 진단", "수익 이탈 원인", "재무 이상 조사". Do
  NOT use for routine month-end close without anomalies (use
  kwp-finance-close-management). Do NOT use for standard variance reporting
  without investigation intent (use kwp-finance-variance-analysis). Do NOT use
  for journal entry prep without a discrepancy (use
  kwp-finance-journal-entry-prep). Do NOT use for audit support without a
  specific finding (use kwp-finance-audit-support). Do NOT use for campaign
  performance diagnosis (use hypothesis-marketing).
---

# Hypothesis-Driven Financial Investigation

Adapted from the core `hypothesis-investigation` methodology for financial variance investigation.

## Iron Laws (Finance Context)

1. **No adjusting entries before hypotheses are listed** — write ≥3 competing explanations for the variance
2. **Each check examines 1 account or transaction set** — isolate the variable
3. **All evidence persists to file** — `outputs/investigation/{date}/INVESTIGATION.md` survives context compaction
4. **Two same-direction failures → forced pivot** — if revenue recognition isn't the cause twice, move on
5. **Explicit predictions with dollar thresholds** — "If H1 is correct, account X should show a $Y difference"

## Phase 1: Observe (Financial Signals)

1. **Identify the trigger** — which variance exceeded the threshold? Which reconciling item is unexplained?
2. **Collect financial data** — GL balances, sub-ledger details, bank statements, transaction logs
3. **Map the materiality** — how large is the variance? Which accounts are affected?
4. **Working boundary** — which accounts DO reconcile? Which periods ARE clean?
5. **Create investigation file** — initialize from `hypothesis-investigation/references/investigation-template.md`

Compose with: `kwp-finance-variance-analysis`, `kwp-finance-reconciliation`, `kwp-finance-financial-statements`

## Phase 2: Hypothesize (Competing Explanations)

Generate **minimum 3** competing explanations:
- "Revenue variance is caused by [timing / recognition policy / contract change / FX]"
- "Reconciling difference is from [posting error / cutoff issue / system mapping / unrecorded transaction]"
- "Cash flow deviation is due to [collections timing / prepayment / investment / one-time item]"

Compose with: `kwp-finance-variance-analysis` (decomposition), `kwp-finance-audit-support` (control testing)

## Phase 3: Experiment (Minimal Data Check)

Test one hypothesis at a time:
1. Query one specific account, period, or transaction set
2. Compare one sub-ledger to one GL account
3. Trace one transaction through the system

Compose with: `kwp-data-sql-queries` (data extraction), `kwp-finance-reconciliation` (comparison)

### Experiment Guardrails

- Maximum 7 data checks before stepping back to re-observe with broader account scope
- If all hypotheses are rejected, return to Phase 1 — the variance classification may be wrong
- Always log pivot decisions in INVESTIGATION.md Pivot Log section
- Preserve audit trail — never delete or overwrite intermediate findings

## Phase 4: Conclude (Corrective Action)

1. **State the validated finding** — one sentence with dollar impact
2. **Map to action** — adjusting entry, process fix, system correction, policy update
3. **Document for audit** — complete audit trail in INVESTIGATION.md
4. **Prevent recurrence** — recommend control improvement

Compose with: `kwp-finance-journal-entry-prep` (corrective entries), `kwp-finance-audit-support` (documentation)

## Quality Gates

### Observation Quality Gate
Before proceeding to Phase 2, verify:
- [ ] Variance trigger clearly documented (which account, dollar amount)
- [ ] Financial data collected (GL, sub-ledger, bank statements)
- [ ] Materiality assessed
- [ ] Working boundary identified (which accounts DO reconcile)
- [ ] Investigation file created at `outputs/investigation/{date}/`

### Hypothesis Quality Gate
Before proceeding to Phase 3, verify:
- [ ] ≥ 3 hypotheses written in INVESTIGATION.md
- [ ] Each hypothesis examines 1 account or transaction set
- [ ] Dollar-amount predictions written for each hypothesis
- [ ] Audit trail preserved for all intermediate findings

### Conclusion Quality Gate
Before declaring done:
- [ ] Validated finding documented with dollar impact
- [ ] Corrective action mapped (adjusting entry, process fix, system correction)
- [ ] Complete audit trail in INVESTIGATION.md
- [ ] Recurrence prevention documented
- [ ] INVESTIGATION.md fully completed and archived

## Anti-Patterns

| Anti-Pattern | Why It Fails | What To Do Instead |
|---|---|---|
| Booking an adjusting entry before finding root cause | Masks the real issue, fails audit | Investigate root cause with hypotheses first |
| Checking all accounts at once | Can't isolate which account drives the variance | Query one account or transaction set at a time |
| "It's a timing issue" without proof | Lazy explanation that hides real errors | Verify cutoff dates, posting dates, and clearing dates |
| Overwriting intermediate findings | Destroys audit trail | Append, never overwrite -- preserve full evidence chain |

## Harness Integration

Integrates into `finance-harness` as a diagnostic mode when variance analysis surfaces unexplained deviations.
