# Autoimprove: trading-trade-hypothesis-ideator

## Experiment 0 (baseline assessment)

- **Score:** 14/25 (56%)
- **Weakest evals:** All five evals weak for direct user prompts — SKILL pointed to scripts without mandating structured hypothesis cards, numeric grounding, or risk in natural-language responses.

## Experiment 1

- **Mutation:** Added `## Mandatory Hypothesis-Card Output Shape (User-Facing)` with full section template (input summary, ranked H1/H2…, scores, pursue/park/kill, risks, provenance) and instruction to normalize free text to `example_input.json` or request fields.
- **Score:** 25/25 (100%)
- **Outcome:** Kept — threshold exceeded; stopped after one experiment.
