# Autoimprove: trading-options-strategy-advisor

## Experiment 0 (baseline assessment)

- **Score:** 20/25 (80%)
- **Weakest evals:** Strict section headers (EVAL1), guaranteed ≥3 numeric scenario rows (EVAL2), single trade decision close (EVAL3), stop/invalidation (EVAL4), FMP vs user vs model labeling (EVAL5).

## Experiment 1

- **Mutation:** Expanded `## Output Format` with `### Required Section Headers (Eval-Aligned)` (Setup through Data Provenance), scenario table requirement, **Hallucination guard** for failed FMP / missing inputs, and single-sentence **Closing** trade decision.
- **Score:** 25/25 (100%)
- **Outcome:** Kept — stopped after one experiment.
