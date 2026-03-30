# Autoimprove: trading-position-sizer

Evals: structure, numerics, actionable conclusion, risk, no fabricated quotes. Tests: fixed fractional, ATR stop, Kelly, constraints, incomplete user inputs.

## Experiment 0

- **Score**: 21/25 (84%)
- **Weaknesses**: Chat-style replies could skip binding-constraint clarity (EVAL 1). Missing prices risk silent fabrication (EVAL 5).

## Experiment 1

- **Change**: Added **Mandatory Output Contract** with Parameters → Method → Numeric table → Binding constraint → One-line recommendation → Risks; **ASSUMED:** tagging when prices inferred; minimum three numbers.
- **Score**: 25/25 (100%)
- **Outcome**: Kept.
