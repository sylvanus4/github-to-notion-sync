# Autoimprove: trading-options-theta

## Experiment 0 (baseline assessment)

- **Score:** 15/25 (60%)
- **Weakest evals:** Uniform structured wrapper across 12 prompts (EVAL1), enforced numeric echo from user params (EVAL2), actionable session decision (EVAL3), min risk/invalidation (EVAL4), no invented earnings/strikes (EVAL5). Cross-input: "AAPL covered call" could misfire scope.

## Experiment 1

- **Mutation:** Under `### Step 4: Report`, added `#### Global Wrapper (Apply to Every Prompt Output)` with five labeled subsections, provenance rule, redirect note for covered calls / long premium, and one-sentence closing.
- **Score:** 25/25 (100%)
- **Outcome:** Kept — stopped after one experiment.
