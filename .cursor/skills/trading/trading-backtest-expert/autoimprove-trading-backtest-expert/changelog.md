# Autoimprove: trading-backtest-expert

Evals: structure, numerics from user metrics, actionable verdict, risk/failure modes, no invented stats. Tests: full metrics packet, parameter sensitivity question, walk-forward interpretation, sub-30 trades, evaluate_backtest.py usage.

## Experiment 0

- **Score**: 20/25 (80%)
- **Weaknesses**: Free-form answers could bury verdict (EVAL 3). Agent might paraphrase without quoting user’s numeric inputs (EVAL 2/5).

## Experiment 1

- **Change**: Added **Standard Response Format (Every Engagement)** with seven labeled sections including **Verdict** and **Next experiments**; required ≥3 numeric inputs from user; explicit failure-mode / bias coverage.
- **Score**: 24/25 (96%)
- **Outcome**: Kept — ≥95% target met.
