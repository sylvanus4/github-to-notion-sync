---
description: "Reconcile Toss Securities holdings against pipeline analysis signals — detect drift, mismatches, and missed opportunities"
---

# Tossinvest Portfolio Reconciliation

## Skill Reference

Read and follow the skill at `.cursor/skills/toss-portfolio-recon/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Run portfolio reconciliation between Toss Securities holdings and the analysis pipeline outputs:

1. **Auth check:** Verify session via `tossctl auth status --output json`.

2. **Fetch actual holdings:** `tossctl portfolio positions --output json`.

3. **Load pipeline signals:** Read the latest `outputs/screener-*.json` and `outputs/analysis-*.json`.

4. **Reconciliation analysis:** Compare and categorize into:
   - **Signal mismatches**: Held stocks with SELL signals (urgent)
   - **Unknown positions**: In Toss but not tracked by pipeline
   - **Missed opportunities**: Pipeline BUY signals not held
   - **Allocation drift**: Position weights deviating from target

5. **Save report:** Write to `outputs/toss/recon-{date}.json`.

6. **Present in Korean:** Structured report with severity-ranked findings.

7. **Decision routing:** If signal mismatches exist, route to `#효정-의사결정` via decision-router.

If $ARGUMENTS contains a specific date, use that date's pipeline outputs instead of today's.

## Constraints

- Read-only — no trading mutations
- Requires both tossctl auth and pipeline outputs
- Signal mismatches are highest priority findings
- Present all output in Korean
