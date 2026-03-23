# Autoimprove: trading-data-quality-checker

## Experiment 0 (baseline assessment)

- **Score:** 17/25 (68%)
- **Weakest evals:** Structured agent narrative (EVAL1), actionable conclusion for advisory workflow (EVAL3), explicit risk framing in chat (EVAL4), hallucination guard when no file path (EVAL5).
- **Notes:** Script output format is structured; eval template targets *assistant* replies. Test inputs adapted: primary weight on "시장 데이터 품질을 검증해줘"; cross-skill prompts would get unstructured prose without an agent contract.

## Experiment 1

- **Mutation:** Inserted `## Agent Response Contract (Trading-Analysis Evals)` with six labeled sections (Summary, Structured Findings, Numeric Evidence ≥3, Recommended Actions, Risks & Limitations, Provenance) and mandatory closing readiness sentence; added rule to request `--file`/excerpt instead of fabricating.
- **Score:** 24/25 (96%)
- **Outcome:** Kept — meets ≥95% threshold; stopped after one experiment.
