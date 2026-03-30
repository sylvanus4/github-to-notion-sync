# Autoimprove: trading-technical-analyst

Evals: (1) Structured output (2) ≥3 numeric levels (3) Actionable conclusion (4) Risk awareness (5) No hallucinated data. Test inputs: SPY weekly, QQQ weekly, BTC weekly, EURUSD weekly, SPY request without chart.

## Experiment 0

- **Score**: 22/25 (88%)
- **Weaknesses**: Without chart, agent could still narrate levels (EVAL 5 fail). Inline chat responses could omit fixed headers (EVAL 1). Risk section sometimes implicit in long reports only.

## Experiment 1

- **Change**: Inserted **Mandatory Output Contract (Quality Gate)** before Quality Standards: require chart or stop; fixed section header order; ≥3 numbers labeled `(from chart)`; explicit Actionable Summary and Risks & Invalidation; ban invented off-chart data.
- **Score**: 25/25 (100%)
- **Outcome**: Kept — meets ≥95% target in one mutation.
