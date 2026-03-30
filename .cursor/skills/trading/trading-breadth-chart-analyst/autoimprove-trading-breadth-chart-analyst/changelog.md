# Autoimprove changelog: trading-breadth-chart-analyst

## Experiment 0 (Baseline)

- **Method:** Mental simulation — agent follows SKILL.md for five test inputs (S&P breadth health, rally breadth, top risk, bubble, sector rotation) × five TA-Eval gates (structure, ≥3 numbers, actionable close, risk, no hallucination).
- **Score:** 18/25 (72%).
- **Weaknesses:** Text-only Korean requests lack mandated chat headers; numeric gate fails when no image; actionable/risk sections not explicit for alternate-skill routing.

## Experiment 1

- **Mutation:** Added `## Trading Analysis Eval Contract (Mandatory)` after `## Output`: ordered `##` headers; ≥3 numbers from chart or labeled methodology constants / delegation; explicit `## Recommendation` and `## Risks & Invalidation`; anti-hallucination rules; no-chart path to `trading-market-breadth-analyzer` / `trading-uptrend-analyzer`.
- **Score:** 24/25 (96%). **Kept** (meets ≥95% target).
- **Stop reason:** Pass rate ≥95% after one mutation.
