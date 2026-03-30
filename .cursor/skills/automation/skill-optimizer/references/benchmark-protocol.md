# Benchmark Protocol

Quantitative performance measurement for skills. Runs the eval workflow multiple times and computes statistical metrics to measure reliability, efficiency, and regression.

## Table of Contents

- [When to Use](#when-to-use)
- [Configuration](#configuration)
- [Metrics](#metrics)
- [Execution Protocol](#execution-protocol)
- [Interpreting Results](#interpreting-results)
- [Error Handling](#error-handling)

## When to Use

- **New skill validation**: Establish a quality baseline before deployment
- **Post-edit verification**: Confirm changes didn't degrade performance
- **Model update compatibility**: Check if a model upgrade breaks existing skills
- **Skill comparison**: Quantify which of two approaches performs better over time

## Configuration

```yaml
benchmark:
  skill: skill-name
  test_cases: path/to/test-cases.yaml  # or auto-generate from eval framework
  iterations: 3                         # number of full eval runs (default: 3)
  baseline_path: .cursor/skills/skill-name/benchmarks/  # where to store results
```

### Choosing iteration count

| Scenario | Recommended iterations | Why |
|----------|----------------------|-----|
| Quick check | 2 | Minimum for variance calculation |
| Standard benchmark | 3 | Good balance of signal vs cost |
| High-confidence measurement | 5 | Needed for statistical significance claims |
| Regression suite | 3 | Run on every skill edit or model update |

## Metrics

### Primary metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Pass rate** | (passing test cases across all iterations) / (total test case runs) | Overall reliability — target >= 80% |
| **Mean quality score** | mean(all Grader scores) | Average output quality — scale 1-10 |
| **Consistency index** | 1 - (std_dev / mean_score) | How stable results are — target >= 0.7 |
| **Token efficiency** | mean(output_tokens) / mean(quality_score) | Cost per unit of quality — lower is better |

### Derived metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Skill impact** | mean(with_skill_score) - mean(without_skill_score) | Net quality contribution of the skill |
| **Regression flag** | current_pass_rate < (previous_pass_rate - 0.10) | True if pass rate dropped > 10% from last benchmark |
| **Redundancy signal** | without_skill_pass_rate >= with_skill_pass_rate | True if base model matches skill-assisted quality |

## Execution Protocol

### Phase 1: Setup

1. Load target skill and test cases (from eval framework or user-provided)
2. Check for previous benchmark results in `baseline_path`
3. If previous results exist, load them for regression comparison

### Phase 2: Iterative Execution

For each iteration `i` in `1..N`:

1. Run the full eval workflow (see [eval-framework.md](eval-framework.md))
2. For each test case, record:
   - `pass`: boolean (did it pass all criteria?)
   - `score`: float (weighted average quality score, 1-10)
   - `tokens`: int (output token count, from subagent metadata if available)
   - `elapsed_ms`: int (execution time, from subagent metadata if available)
   - `with_skill_score`: float (score for the with-skill execution)
   - `without_skill_score`: float (score for the without-skill execution)

### Phase 3: Statistical Analysis

Compute per-test-case statistics:

```
Test: [test-name]
  Pass rate:       [N]% across [iterations] runs
  Mean score:      [X.X] (std dev: [X.X])
  Score range:     [min] - [max]
  Consistency:     [X.X]
  Token mean:      [N] tokens
  Skill impact:    +[X.X] / -[X.X]
```

Compute aggregate statistics:

```
Overall:
  Pass rate:       [N]%
  Mean score:      [X.X]
  Consistency:     [X.X]
  Token efficiency: [X.X] tokens/quality-point
  Skill impact:    [X.X]
  Regression:      [YES/NO] (vs previous: [date])
```

### Phase 4: Regression Detection

If a previous benchmark exists:

1. Compare current pass rate vs previous pass rate
2. Compare current mean score vs previous mean score
3. Flag regression if:
   - Pass rate dropped by more than 10 percentage points
   - Mean score dropped by more than 1.0 points
   - Any previously-passing test case now consistently fails

Present regression details:

```
Regression Alert
================
Previous benchmark: [date]
Pass rate:    [prev]% → [current]% (Δ [change])
Mean score:   [prev] → [current] (Δ [change])

Newly failing tests:
  - [test-name]: was PASS, now FAIL — [reason from Grader]
```

### Phase 5: Store Results

Save benchmark results to `baseline_path` for future regression comparison:

```
.cursor/skills/[skill-name]/benchmarks/
└── benchmark-[YYYY-MM-DD].md
```

Format:

```markdown
# Benchmark: [skill-name]
Date: [YYYY-MM-DD]
Iterations: [N]
Model: [model identifier if known]

## Results
| Test Case | Pass Rate | Mean Score | Std Dev | Tokens | Skill Impact |
|-----------|-----------|------------|---------|--------|--------------|
| [name]    | [N]%      | [X.X]      | [X.X]   | [N]    | +[X.X]       |

## Aggregate
- Pass rate: [N]%
- Mean score: [X.X]
- Consistency: [X.X]
- Token efficiency: [X.X]
- Regression: [YES/NO]
```

## Interpreting Results

### Quality thresholds

| Pass Rate | Quality Score | Assessment |
|-----------|--------------|------------|
| >= 90% | >= 8.0 | Excellent — skill is production-ready |
| 70-89% | 6.0-7.9 | Good — consider targeted improvements |
| 50-69% | 4.0-5.9 | Fair — skill needs significant work |
| < 50% | < 4.0 | Poor — consider rewriting or retiring |

### Consistency thresholds

| Consistency Index | Assessment |
|-------------------|------------|
| >= 0.85 | Highly stable — reliable across runs |
| 0.70-0.84 | Stable — minor variance, acceptable |
| 0.50-0.69 | Unstable — investigate variance sources |
| < 0.50 | Unreliable — skill produces inconsistent results |

### Decision matrix

| Pass Rate | Skill Impact | Consistency | Recommendation |
|-----------|-------------|-------------|----------------|
| High | Positive | High | Ship confidently |
| High | Negligible | High | Skill may be redundant — test without it |
| High | Positive | Low | Investigate variance — may need tighter specification |
| Low | Positive | Any | Skill helps when it works — fix failing cases |
| Low | Negative | Any | Retire or rewrite the skill |

## Error Handling

| Error | Action |
|-------|--------|
| Iteration produces all-SKIP results | Exclude that iteration from statistics, note in report |
| Fewer than 2 valid iterations | Cannot compute variance — report raw scores only |
| Previous benchmark uses different test cases | Skip regression comparison, note incompatibility |
| Baseline path not writable | Print results to stdout, warn about persistence |
