# Autoimprove changelog: trading-market-breadth-analyzer

## Experiment 0 (Baseline)

- **Score:** 20/25 (80%).
- **Weaknesses:** Phase 2 “Present Results” did not require markdown structure or minimum numeric citations from generated artifacts; failure path unclear for eval gates.

## Experiment 1

- **Mutation:** Inserted `### Phase 2b: Trading Analysis Eval Contract (Mandatory)` with table mapping five gates to pass conditions; text-only path must still run script or show CLI + headers.
- **Score:** 24/25 (96%).
- **Stop reason:** ≥95% target met.
