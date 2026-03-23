# Autoimprove changelog: trading-us-market-bubble-detector

## Experiment 0 (Baseline)

- **Score:** 17/25 (68%).
- **Weaknesses:** Internal inconsistency (+5 vs +3); output format section too thin for structured chat; eval gates for table of collected data and anti-hallucination not explicit.

## Experiment 1

- **Mutation:** (1) Implementation Checklist and Principle 3 aligned to **+3** qualitative cap. (2) Added `### Trading Analysis Eval Contract (Mandatory)` under Output Format with Phase 1 Data Table schema and six required `##` sections.
- **Score:** 24/25 (96%).
- **Stop reason:** ≥95% target met.
