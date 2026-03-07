# Eval Report Templates

Standardized report formats for all skill-optimizer modes. Copy and fill the appropriate template when presenting results.

## Table of Contents

- [Eval Report](#eval-report)
- [Benchmark Report](#benchmark-report)
- [A/B Comparison Report](#ab-comparison-report)
- [Usage Notes](#usage-notes)

## Eval Report

```
Skill Eval Report
=================
Skill: [skill-name]
Date:  [YYYY-MM-DD]
Mode:  eval
Test cases: [N]

Classification: [capability-uplift / encoded-preference]

Overall Results
───────────────
Pass rate (with skill):    [N]% ([passed]/[total])
Pass rate (without skill): [N]% ([passed]/[total])
Mean quality score:        [X.X] / 10 (with) vs [X.X] / 10 (without)
Skill impact delta:        [+/-X.X]

Per-Test Results
────────────────
┌─────────────────┬────────┬───────────┬───────────────┬──────────────────────┐
│ Test Case       │ Result │ Score     │ Skill Impact  │ Notes                │
├─────────────────┼────────┼───────────┼───────────────┼──────────────────────┤
│ [test-name-1]   │ PASS   │ [X.X]/10  │ +[X.X]        │ [one-line reason]    │
│ [test-name-2]   │ FAIL   │ [X.X]/10  │ -[X.X]        │ [failure reason]     │
│ [test-name-3]   │ PASS   │ [X.X]/10  │ +[X.X]        │ [one-line reason]    │
│ [test-name-4]   │ SKIP   │ —         │ —             │ [skip reason]        │
└─────────────────┴────────┴───────────┴───────────────┴──────────────────────┘

Criterion Breakdown (aggregated across test cases)
───────────────────────────────────────────────────
┌──────────────────────────┬────────────────┬─────────────────┐
│ Criterion                │ Mean Score     │ Pass Rate       │
├──────────────────────────┼────────────────┼─────────────────┤
│ [criterion-1]            │ [X.X]/10       │ [N]%            │
│ [criterion-2]            │ [X.X]/10       │ [N]%            │
│ [criterion-3]            │ [X.X]/10       │ [N]%            │
└──────────────────────────┴────────────────┴─────────────────┘

Anti-Behavior Violations: [N] detected
  - [test-name]: [anti-behavior description]

Assessment
──────────
Skill impact: [POSITIVE / NEUTRAL / NEGATIVE]
Recommendation: [KEEP / IMPROVE / RETIRE]
Reasoning: [2-3 sentences explaining the recommendation]

Suggested improvements (if IMPROVE):
  1. [specific improvement]
  2. [specific improvement]
```

## Benchmark Report

```
Skill Benchmark Report
======================
Skill: [skill-name]
Date:  [YYYY-MM-DD]
Mode:  benchmark
Iterations: [N]
Test cases: [N]

Aggregate Metrics
─────────────────
Pass rate:         [N]%
Mean quality:      [X.X] / 10
Consistency index: [X.X] (target >= 0.70)
Token efficiency:  [N] tokens / quality point
Skill impact:      [+/-X.X]

Per-Test Statistics
───────────────────
┌─────────────────┬───────────┬────────────┬─────────┬──────────┬──────────────┐
│ Test Case       │ Pass Rate │ Mean Score │ Std Dev │ Tokens   │ Skill Impact │
├─────────────────┼───────────┼────────────┼─────────┼──────────┼──────────────┤
│ [test-name-1]   │ [N]%      │ [X.X]      │ [X.X]   │ [N]      │ +[X.X]       │
│ [test-name-2]   │ [N]%      │ [X.X]      │ [X.X]   │ [N]      │ -[X.X]       │
│ [test-name-3]   │ [N]%      │ [X.X]      │ [X.X]   │ [N]      │ +[X.X]       │
└─────────────────┴───────────┴────────────┴─────────┴──────────┴──────────────┘

Quality Assessment
──────────────────
  Pass rate:    [EXCELLENT / GOOD / FAIR / POOR] (threshold: 90/70/50)
  Consistency:  [STABLE / ACCEPTABLE / UNSTABLE / UNRELIABLE] (threshold: 0.85/0.70/0.50)
  Overall:      [production-ready / needs-improvement / needs-rewrite / retire]

Regression Check
────────────────
  Previous benchmark: [date or "none"]
  Pass rate change:   [prev]% → [current]% (Δ [change])
  Score change:       [prev] → [current] (Δ [change])
  Regression:         [YES / NO / N/A]
  Newly failing:      [list of test names or "none"]

Recommendation
──────────────
[2-3 sentences: what to do based on the benchmark results]
```

## A/B Comparison Report

```
A/B Comparison Report
=====================
Skill: [skill-name]
Date:  [YYYY-MM-DD]
Mode:  compare
Comparison: [Version-X label] vs [Version-Y label]
Test cases: [N]

Overall Winner: [Version-X / Version-Y / Tie]

Detailed Verdicts
─────────────────
┌─────────────────┬──────────────────┬────────┬──────────┬─────────────────────────┐
│ Test Case       │ Criterion        │ Winner │ Conf(1-5)│ Reasoning               │
├─────────────────┼──────────────────┼────────┼──────────┼─────────────────────────┤
│ [test-1]        │ [criterion-1]    │ [X/Y]  │ [N]      │ [one-line reason]       │
│ [test-1]        │ [criterion-2]    │ Tie    │ [N]      │ [one-line reason]       │
│ [test-2]        │ [criterion-1]    │ [X/Y]  │ [N]      │ [one-line reason]       │
│ ...             │ ...              │ ...    │ ...      │ ...                     │
└─────────────────┴──────────────────┴────────┴──────────┴─────────────────────────┘

Summary Scoreboard
──────────────────
  [Version-X]:  [N] wins ([%]), confidence-weighted: [score]
  [Version-Y]:  [N] wins ([%]), confidence-weighted: [score]
  Ties:         [N] ([%])

Per-Criterion Breakdown
───────────────────────
┌──────────────────────────┬───────────────┬───────────────┬──────────┐
│ Criterion                │ Version-X     │ Version-Y     │ Ties     │
├──────────────────────────┼───────────────┼───────────────┼──────────┤
│ [criterion-1]            │ [N] wins      │ [N] wins      │ [N]      │
│ [criterion-2]            │ [N] wins      │ [N] wins      │ [N]      │
└──────────────────────────┴───────────────┴───────────────┴──────────┘

Recommendation
──────────────
  Verdict: [Ship Version-X / Keep Version-Y / No significant difference]
  Confidence: [HIGH / MEDIUM / LOW]
  Reasoning: [2-3 sentences explaining the recommendation]
```

## Usage Notes

- Reports are designed for terminal display — use monospace font for table alignment
- All scores use a 1-10 scale unless otherwise noted
- Confidence-weighted scores normalize wins by the Comparator's stated confidence (1-5)
- SKIP results are excluded from aggregate calculations
- Present the appropriate report format based on the mode the user selected
