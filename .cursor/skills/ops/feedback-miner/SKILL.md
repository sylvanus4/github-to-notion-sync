---
name: feedback-miner
version: 1.0.0
description: >
  Mine bulk customer feedback from multiple sources (app store reviews, survey CSVs,
  support ticket exports, NPS comments, G2/Capterra reviews), cluster by topic,
  score with RICE framework, and produce a prioritized product signal report.
tags: [feedback, product, prioritization, RICE, sentiment, clustering]
triggers:
  - "mine feedback"
  - "analyze customer feedback"
  - "feedback mining"
  - "prioritize feature requests"
  - "customer voice analysis"
  - "NPS analysis"
  - "app store reviews"
  - "feedback report"
  - "product signals"
  - "pain point analysis"
  - "피드백 마이닝"
  - "고객 피드백 분석"
  - "피드백 우선순위"
  - "기능 요청 분석"
  - "고객 목소리"
  - "NPS 분석"
  - "앱스토어 리뷰"
  - "페인포인트 분석"
do_not_use:
  - "For general sentiment scoring of financial text (use alphaear-sentiment)"
  - "For survey design or user research planning (use kwp-design-user-research)"
  - "For competitive analysis without customer feedback (use kwp-product-management-competitive-analysis)"
  - "For support ticket response drafting (use kwp-customer-support-response-drafting)"
  - "For meeting feedback synthesis (use meeting-digest)"
composes:
  - defuddle
  - opendataloader
  - batch-agent-runner
  - evaluation-engine
  - visual-explainer
  - decision-router
  - md-to-notion
  - anthropic-docx
---

# Feedback Miner

Mine bulk customer feedback, cluster topics, score with RICE, and produce prioritized product signals.

## When to Use

- Bulk customer feedback needs analysis (100+ items)
- Product team needs data-backed feature prioritization
- App store reviews require systematic triage
- NPS/CSAT survey open-text responses need clustering
- Support ticket themes need quantification

## Pipeline

```
Ingest → Classify → Score → Visualize → Output
```

### Phase 1: Ingest

Accept feedback from multiple source types. Route each to the appropriate extractor.

| Source Type | Extractor | Input Format |
|---|---|---|
| CSV/TSV export | Direct parse | Zendesk, Intercom, survey tools |
| JSON export | Direct parse | API exports, structured dumps |
| Web reviews | `defuddle` | App Store, G2, Capterra URLs |
| PDF survey reports | `opendataloader` | Research reports, NPS summaries |
| Slack channel | Slack MCP `slack_search` | Customer feedback channels |

**Normalization**: Every feedback item is normalized to a canonical record:

```json
{
  "id": "string",
  "source": "appstore|g2|capterra|zendesk|survey|slack|manual",
  "text": "string",
  "author": "string (anonymized if PII)",
  "date": "ISO-8601",
  "rating": "number|null (1-5 scale)",
  "metadata": {}
}
```

For large datasets (500+ items), use `batch-agent-runner` TSV pattern:
1. Write normalized records to `outputs/feedback/{date}/intake.tsv`
2. Process in batches of 50 with parallel subagents
3. Track progress with TSV state column

### Phase 2: Classify

LLM-based topic clustering with a configurable taxonomy.

**Default taxonomy** (override with `--taxonomy custom.json`):

| Category | Description |
|---|---|
| `bug` | Broken functionality, errors, crashes |
| `feature_request` | New capability requests |
| `ux_friction` | Usability issues, confusing flows |
| `performance` | Speed, latency, resource usage |
| `praise` | Positive feedback, satisfaction |
| `pricing` | Cost concerns, plan limitations |
| `onboarding` | First-run experience issues |
| `integration` | Third-party connectivity needs |
| `documentation` | Help content gaps |

**Classification prompt pattern**:
- Present 10-20 feedback items per LLM call for efficiency
- Each item gets: `category`, `subcategory` (freeform), `sentiment` (-1 to 1), `urgency` (low/medium/high)
- Cross-validate: if a single batch has >80% one category, re-run with shuffled items to prevent anchoring bias

**Cluster aggregation**:
- Group by `category` + `subcategory`
- Merge subcategories with <3 items into nearest semantic neighbor
- Compute per-cluster: count, avg_sentiment, avg_rating, date_range, representative_quotes (top 3 by extremity)

### Phase 3: Score

Apply RICE framework via `evaluation-engine` dimension rubric.

Configure `evaluation-engine` with these 4 dimensions:

| Dimension | Weight | Scoring Guide |
|---|---|---|
| **Reach** | 25% | How many users mention this? <5 items=D, 5-20=C, 20-50=B, 50+=A |
| **Impact** | 30% | Sentiment severity × user segment value. Critical bugs=A, nice-to-haves=D |
| **Confidence** | 20% | Data quality. Single source=D, multi-source corroboration=A, includes quotes=+1 tier |
| **Effort** | 25% | Estimated implementation complexity (inferred from request specificity). Vague="high effort"=D, specific+small=A |

Output: Each cluster gets a composite RICE score (0-100) and letter grade (A-F).

### Phase 4: Visualize

Generate a priority matrix HTML artifact via `visual-explainer`.

**Required visualizations**:
1. **Priority Matrix** (2x2): Impact (Y) vs Effort (X), bubble size = Reach, color = Confidence
2. **Category Distribution**: Horizontal bar chart of feedback count per category
3. **Sentiment Trend**: If date range > 30 days, line chart of rolling avg sentiment
4. **Top Clusters Table**: Ranked by RICE score, showing category, count, sentiment, score, representative quote

Save to `outputs/feedback/{date}/priority-matrix.html`.

### Phase 5: Output

Produce the final feedback report.

**File outputs** (all under `outputs/feedback/{date}/`):
- `feedback-report.md` -- Full report with executive summary, methodology, findings, recommendations
- `priority-matrix.html` -- Interactive visualization (from Phase 4)
- `clusters.json` -- Machine-readable cluster data with scores
- `intake.tsv` -- Normalized intake data (from Phase 1)

**Optional distribution**:
- `--notion`: Publish report to Notion via `md-to-notion`
- `--docx`: Generate Word document via `anthropic-docx`
- `--slack`: Post executive summary to Slack (1 main message + threaded top-5 clusters)

**Decision routing**: Any cluster scoring A or B on RICE with sentiment < -0.3 is auto-routed to `decision-router` for escalation.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `--sources` | required | Comma-separated list of file paths or URLs |
| `--taxonomy` | built-in | Path to custom taxonomy JSON |
| `--min-cluster` | 3 | Minimum items to form a cluster |
| `--rice-threshold` | 70 | RICE score threshold for decision routing |
| `--sentiment-threshold` | -0.3 | Sentiment threshold for escalation |
| `--notion` | false | Publish to Notion |
| `--docx` | false | Generate Word document |
| `--slack` | false | Post summary to Slack |
| `--date` | today | Date stamp for output directory |

## Report Structure

```markdown
# Feedback Mining Report — {date}

## Executive Summary
- Total items analyzed: N
- Sources: [list]
- Date range: start — end
- Top finding: [highest RICE cluster summary]

## Methodology
- Ingestion: [sources and counts]
- Classification: [taxonomy used, any customizations]
- Scoring: RICE framework with [weights]

## Priority Clusters (ranked by RICE)

### 1. [Cluster Name] — RICE: 85/100 (A)
- **Category**: feature_request
- **Count**: 47 items across 3 sources
- **Sentiment**: -0.4 (frustrated)
- **Representative quotes**: [3 quotes]
- **Recommendation**: [actionable next step]

### 2. ...

## Category Distribution
[bar chart reference]

## Sentiment Analysis
[trend chart reference, if applicable]

## Raw Data
- Intake: outputs/feedback/{date}/intake.tsv
- Clusters: outputs/feedback/{date}/clusters.json

## Appendix: Decision Routing
[items auto-routed to decision-router, if any]
```

## Constraints

- Never output raw PII (emails, full names) — anonymize in the normalization step
- Limit web scraping to publicly accessible review pages
- For datasets >2000 items, enforce batch processing via `batch-agent-runner`
- Validate source file encoding (UTF-8 required, auto-convert if possible)
- Report all confidence intervals when extrapolating from samples
