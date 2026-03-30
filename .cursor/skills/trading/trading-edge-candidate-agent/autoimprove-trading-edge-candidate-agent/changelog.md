# Autoimprove: trading-edge-candidate-agent

## Experiment 0 (baseline assessment)

- **Score:** 16/25 (64%)
- **Weakest evals:** Structured output for chat-first use (EVAL1), numeric specificity without OHLCV (EVAL2), actionable pipeline handoff (EVAL3), falsification / schema risk (EVAL4), hallucinated tickers (EVAL5) when user only pastes text.

## Experiment 1

- **Mutation:** Added `## Agent Narrative Output (Research / Edge Requests)` with seven mandatory sections including ranked list with numeric anomaly fields, exportability labels, provenance rules, and explicit **go / no-go** closing.
- **Score:** 24/25 (96%)
- **Outcome:** Kept — ≥95%; stopped after one experiment.
