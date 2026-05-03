---
name: data-analyst-orchestrator
description: >-
  Unified data analysis entry point that routes user questions to the
  appropriate kwp-data-* skill, supports an interactive evaluator-optimizer
  analysis loop, integrates experiment design (A/B testing, cohort analysis),
  and produces self-contained HTML dashboards as default output.
---

# Data Analyst Orchestrator

Unified entry point for data analysis workflows. Routes questions to the right specialist skill, iterates on visualizations interactively, and outputs self-contained HTML dashboards.

## When to Use

- User provides a dataset (CSV, JSON, TSV, or database connection) and asks open-ended questions
- Exploratory data analysis where the right chart type or statistical method isn't known upfront
- Building a dashboard from raw data in a single workflow
- Experiment design and results analysis (A/B tests, cohort analysis)
- Any "here's data, make sense of it" request

## Architecture

```
User Question + Data
       │
       ▼
┌─────────────┐
│  INTAKE      │ ← Accept data, detect format, profile
└──────┬──────┘
       ▼
┌─────────────┐
│  ROUTE       │ ← Classify intent, select skill(s)
└──────┬──────┘
       ▼
┌─────────────┐
│  ANALYZE     │ ← Execute via routed skill
└──────┬──────┘
       ▼
┌─────────────┐
│  PRESENT     │ ← Visualize results, build dashboard
└──────┬──────┘
       ▼
┌─────────────┐
│  ITERATE     │ ← User refines, loop back to ROUTE
└─────────────┘
```

## Pipeline

### Phase 1: Intake

Accept data and establish the working dataset.

**Supported input formats**:

| Format | Detection | Handling |
|---|---|---|
| CSV/TSV | File extension or delimiter detection | Parse with pandas, infer types |
| JSON/JSONL | File extension or `{`/`[` start | Flatten nested structures |
| Excel (.xlsx) | File extension | Read with openpyxl, list sheets |
| SQL query result | User provides query + connection | Execute via `kwp-data-sql-queries` |
| Pasted table | Markdown or tab-delimited in message | Parse inline |

**Profiling** (auto-run via `kwp-data-data-exploration`):
- Row count, column count, data types
- Null percentages per column
- Unique value counts for categorical columns
- Min/max/mean/median for numeric columns
- Sample rows (first 5)

**Output**: `outputs/analysis/{date}/profile.json` + summary presented to user.

### Phase 2: Route

Classify user intent and select the appropriate skill(s).

| Intent Pattern | Routed To | Example |
|---|---|---|
| "Show me the distribution of X" | `kwp-data-data-visualization` | Histogram, box plot |
| "What's the correlation between X and Y" | `kwp-data-statistical-analysis` | Correlation matrix, scatter |
| "Write a query to get X" | `kwp-data-sql-queries` | SQL generation |
| "Is this data clean?" | `kwp-data-data-validation` | Null audit, outlier detection |
| "What patterns do you see?" | `kwp-data-data-exploration` | Full EDA |
| "Build a dashboard" | `kwp-data-interactive-dashboard-builder` | HTML dashboard |
| "Design an A/B test" | Experiment Design module (below) | Sample size, test plan |
| "Analyze this experiment" | `pm-data-analytics` + `kwp-data-statistical-analysis` | Significance, lift |

**Ambiguous intent**: If the question is vague ("analyze this"), run `kwp-data-data-exploration` first, then present top 3 suggested follow-up analyses.

### Phase 3: Analyze

Execute the routed skill and capture results.

**Execution rules**:
- Pass the profiled dataset path (not raw data) to the routed skill
- Capture all generated artifacts (charts, tables, statistical outputs)
- Save intermediate results to `outputs/analysis/{date}/`

**Multi-skill chains**: Some questions require chaining:
1. "Compare revenue across regions, flag anomalies" → `kwp-data-data-visualization` (bar chart) + `kwp-data-statistical-analysis` (outlier detection)
2. "Build a retention dashboard" → `pm-data-analytics` (cohort curves) + `kwp-data-interactive-dashboard-builder` (HTML assembly)

### Phase 4: Present

Visualize results and optionally assemble into a dashboard.

**Default output**: Self-contained HTML dashboard via `kwp-data-interactive-dashboard-builder`:
- Chart.js visualizations with dropdown filters
- Data tables with sorting
- Key metrics cards
- No server required

**Alternative outputs**:
- `--markdown`: Markdown report with inline chart references
- `--notebook`: Jupyter notebook with code cells
- `--charts-only`: Individual chart images (PNG/SVG)

Save all outputs to `outputs/analysis/{date}/`.

### Phase 5: Iterate (Interactive Loop)

After presenting results, enter an evaluator-optimizer loop.

**Loop mechanics**:
1. Present results to user
2. User provides feedback: "zoom in on Q3", "add a trend line", "what about segment X"
3. Route the refinement back to Phase 2 (ROUTE)
4. Re-analyze with the refined scope
5. Update the dashboard/output
6. Repeat until user is satisfied or says "done"

**Max iterations**: 10 (warn at 7, suggest finalizing)

**Context preservation**: Maintain a running analysis context:
```json
{
  "dataset_path": "...",
  "profile": { ... },
  "questions_asked": ["Q1", "Q2"],
  "analyses_run": ["exploration", "correlation"],
  "charts_generated": ["bar_revenue.html", "scatter_xy.html"],
  "refinements": ["added trend line", "filtered to Q3"]
}
```

## Experiment Design Module

Integrated experiment design and analysis, combining `pm-data-analytics` with statistical methods.

### A/B Test Design

When user asks to "design an A/B test" or "calculate sample size":

1. **Define hypothesis**: Null (H0) and alternative (H1) with effect size
2. **Calculate sample size**: Using power analysis (α=0.05, β=0.20 default)
3. **Estimate duration**: Based on current traffic/conversion rates
4. **Generate test plan**:

```markdown
## A/B Test Plan

**Hypothesis**: {H1 statement}
**Primary metric**: {metric name}
**Current baseline**: {value}
**Minimum detectable effect**: {MDE}%
**Required sample size**: {N per group}
**Estimated duration**: {days} at {daily traffic} daily visitors
**Significance level**: α = 0.05
**Power**: 1 - β = 0.80

### Guardrail Metrics
- {metric}: must not degrade by more than {threshold}
```

### A/B Test Analysis

When user provides experiment results:

1. **Statistical significance**: Chi-squared or Z-test with p-value
2. **Confidence interval**: 95% CI for the difference
3. **Practical significance**: Is the effect size meaningful?
4. **Segment analysis**: Break down by key dimensions
5. **Recommendation**: Ship / iterate / kill with reasoning

### Cohort Analysis

When user asks to "analyze cohorts" or "retention curves":

1. **Cohort definition**: Group users by signup week/month
2. **Retention curves**: Day-1, Day-7, Day-30 retention by cohort
3. **Trend visualization**: Heatmap or line chart via `kwp-data-data-visualization`
4. **Insight extraction**: Which cohorts perform best? What changed?

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--data` | required | Path to data file or "clipboard" for pasted data |
| `--output` | dashboard | Output format: dashboard, markdown, notebook, charts-only |
| `--output-dir` | auto | Directory for outputs (default: `outputs/analysis/{date}/`) |
| `--max-iterations` | 10 | Maximum interactive loop iterations |
| `--experiment` | false | Enable experiment design mode |
| `--sql-dialect` | postgresql | SQL dialect for query generation |

## Constraints

- Never modify the user's source data file — work on a copy
- All generated charts must include axis labels and a title
- Statistical claims must include confidence intervals and p-values
- Dashboard HTML must be self-contained (no CDN dependencies that could break offline)
- For datasets >100K rows, warn about processing time and suggest sampling
- PII columns (detected by name pattern: email, phone, ssn, name) are auto-excluded from visualizations unless explicitly requested
