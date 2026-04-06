---
name: evaluation-engine
description: >-
  Generalized multi-block evaluation framework that scores any entity (stock,
  company, paper, tool, opportunity) against configurable dimension rubrics.
  Produces structured A-F graded reports with weighted composite scores.
user_invocable: true
---

# Evaluation Engine

Score any entity against a configurable set of evaluation dimensions using
structured rubric blocks. Produces graded reports (A-F) with weighted composite
scores and actionable recommendations.

## When to Use

- Evaluating stocks, companies, tools, papers, or opportunities across multiple dimensions
- Comparing N candidates on the same rubric
- User says "evaluate", "score", "grade", "rate", "평가", "점수", "등급"
- Building decision matrices with structured scoring

## Do NOT Use

- Simple binary pass/fail checks (use quality gates directly)
- LLM prompt evaluation (use evals-skills)
- Code review (use deep-review or simplify)

## Architecture

```
Evaluation Engine
├── Load rubric config (config/ops/eval-rubrics/{domain}.yaml)
├── For each dimension block:
│   ├── Gather evidence (web search, file read, API call)
│   ├── Score 1-10 with justification
│   └── Assign letter grade (A-F)
├── Calculate weighted composite score
├── Generate structured report
└── Archive to data/ops/evaluations/
```

## Rubric Configuration

Rubrics are defined in `config/ops/eval-rubrics/{domain}.yaml`:

```yaml
domain: stock-evaluation
version: 1
description: Multi-factor stock evaluation rubric

dimensions:
  - id: fundamentals
    name: Fundamental Analysis
    weight: 0.25
    criteria:
      - P/E ratio vs sector median
      - Revenue growth trajectory (3Y)
      - Free cash flow yield
      - Debt/equity ratio
      - ROE consistency

  - id: technicals
    name: Technical Analysis
    weight: 0.20
    criteria:
      - Trend alignment (20/55/200 SMA)
      - RSI position (oversold/neutral/overbought)
      - Volume pattern (accumulation/distribution)
      - Support/resistance proximity

  - id: sentiment
    name: Market Sentiment
    weight: 0.15
    criteria:
      - Analyst consensus (buy/hold/sell ratio)
      - Social media sentiment trend
      - Institutional ownership changes
      - Short interest ratio

  - id: catalyst
    name: Catalyst Assessment
    weight: 0.20
    criteria:
      - Upcoming earnings/events
      - Industry tailwinds/headwinds
      - Regulatory environment
      - Competitive position shifts

  - id: risk
    name: Risk Profile
    weight: 0.20
    criteria:
      - Downside volatility (beta, max drawdown)
      - Concentration risk
      - Liquidity risk
      - Black swan exposure

grading_scale:
  A: { min: 8.5, label: "Strong Buy / Excellent" }
  B: { min: 7.0, label: "Buy / Good" }
  C: { min: 5.5, label: "Hold / Average" }
  D: { min: 4.0, label: "Weak / Below Average" }
  F: { min: 0.0, label: "Avoid / Poor" }
```

## Execution Flow

### Step 1: Select Rubric

Based on entity type or user specification:
- `stock-evaluation` for tickers
- `paper-evaluation` for academic papers
- `tool-evaluation` for software/tools
- `opportunity-evaluation` for business opportunities
- Custom YAML for domain-specific evaluations

### Step 2: Gather Evidence per Block

For each dimension:
1. Identify data sources (APIs, web search, local data, user input)
2. Collect evidence using available tools
3. Summarize evidence as bullet points

### Step 3: Score Each Dimension

For each dimension, produce:
```markdown
### [Dimension Name] — Score: X/10 (Grade)

**Evidence:**
- [bullet 1]
- [bullet 2]

**Assessment:**
[1-2 sentence justification for the score]

**Weight:** 0.XX → Weighted contribution: X.XX
```

### Step 4: Compute Composite

```
Composite = Σ (dimension_score × dimension_weight)
Final Grade = lookup(composite, grading_scale)
```

### Step 5: Generate Report

Output format:
```markdown
# Evaluation Report: [Entity Name]

**Date:** YYYY-MM-DD
**Rubric:** [domain] v[version]
**Composite Score:** X.XX / 10
**Final Grade:** [A-F] — [label]

## Summary
[2-3 sentence executive summary]

## Dimension Scores

| Dimension | Score | Grade | Weight | Weighted |
|-----------|-------|-------|--------|----------|
| [name]    | X/10  | [A-F] | 0.XX   | X.XX     |
| ...       | ...   | ...   | ...    | ...      |
| **Composite** | | **[Grade]** | | **X.XX** |

## Detailed Analysis
[Per-dimension blocks as in Step 3]

## Recommendations
1. [Top action item based on weakest dimensions]
2. [Second action]
3. [Third action]

## Comparables
[If comparing multiple entities, include comparison matrix]
```

### Step 6: Archive

Save report to `data/ops/evaluations/{domain}-{entity}-{date}.md`

## Comparison Mode

When evaluating multiple entities against the same rubric:

1. Run evaluation for each entity
2. Build comparison matrix:
   ```
   | Dimension    | Entity A | Entity B | Entity C |
   |--------------|----------|----------|----------|
   | Fundamentals | 8.0 (A)  | 6.5 (B)  | 5.0 (C)  |
   | ...          | ...      | ...      | ...      |
   | **Composite**| **7.8**  | **6.2**  | **5.5**  |
   ```
3. Rank entities by composite score
4. Identify differentiating dimensions

## Built-in Rubric Domains

| Domain | Use For |
|--------|---------|
| `stock-evaluation` | Ticker analysis (fundamentals + technicals + sentiment) |
| `paper-evaluation` | Academic paper quality (novelty + rigor + applicability) |
| `tool-evaluation` | Software tool assessment (capability + DX + cost + maturity) |
| `opportunity-evaluation` | Business opportunity (market + feasibility + ROI + risk) |

Create custom rubrics by adding YAML files to `config/ops/eval-rubrics/`.

## Integration Points

- **batch-agent-runner**: Evaluate N entities in parallel via batch processing
- **pipeline-inbox**: Queue items for later evaluation
- **report-archiver**: Manage evaluation report lifecycle
- **daily-stock-check**: Stock evaluation feeds into daily signals
- **paper-review**: Paper evaluation enhances review pipeline

## Constraints

- Each dimension score must include evidence citations
- Weighted scores must sum to the composite (arithmetic check)
- Never change rubric weights mid-evaluation
- Archive all reports — never overwrite previous evaluations
