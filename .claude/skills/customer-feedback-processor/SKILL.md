---
name: customer-feedback-processor
description: >-
  Multi-channel feedback pipeline: ingests from app stores, surveys, support
  tickets, social media, NPS, and Slack; classifies by topic and sentiment;
  scores with RICE framework; synthesizes themes; generates executive .docx
  report with visual dashboard. Extends feedback-miner with automated RICE
  prioritization and executive deliverables. Use when the user asks to
  "process customer feedback", "feedback report", "multi-channel feedback
  analysis", "customer-feedback-processor", "RICE feedback prioritization",
  "고객 피드백 처리", "다채널 피드백 분석", "피드백 리포트 생성", "피드백 프로세서", or wants
  feedback-to-executive-report pipeline. Do NOT use for basic feedback mining
  (use feedback-miner). Do NOT use for financial sentiment (use
  alphaear-sentiment). Do NOT use for survey design (use
  kwp-design-user-research). Do NOT use for support ticket response (use
  kwp-customer-support-response-drafting).
---

# Customer Feedback Processor

Ingest multi-channel customer feedback, classify and score with RICE, and produce an executive-ready report with visual dashboard.

## When to Use

- Feedback from 2+ channels needs unified analysis (app reviews + surveys + tickets)
- Product team needs RICE-scored, executive-ready feedback prioritization
- Quarterly or monthly feedback review cycle requires a structured deliverable
- Management needs anonymized customer quotes with sentiment and trend data

## Output Artifacts

| Phase | Stage Name         | Output File                                                       |
| ----- | ------------------ | ----------------------------------------------------------------- |
| 1     | Ingest             | `outputs/customer-feedback-processor/{date}/raw-feedback.jsonl`   |
| 2     | Classify           | `outputs/customer-feedback-processor/{date}/classified.jsonl`     |
| 3     | Score              | `outputs/customer-feedback-processor/{date}/rice-scores.tsv`      |
| 4     | Synthesize         | `outputs/customer-feedback-processor/{date}/themes.md`            |
| 5     | Report             | `outputs/customer-feedback-processor/{date}/feedback-report.docx` |
| 5     | Dashboard          | `outputs/customer-feedback-processor/{date}/dashboard.html`       |
| 6     | Manifest           | `outputs/customer-feedback-processor/{date}/manifest.json`        |

## Workflow

### Phase 1: Ingest

Collect feedback from multiple channels via `feedback-miner` ingestion patterns:

| Channel | Method |
|---------|--------|
| App store reviews | `defuddle` on Apple App Store / Google Play review URLs |
| Survey responses | Read CSV/Excel file with columns: response, rating, date, segment |
| Support tickets | Read CSV/JSON export from helpdesk (Zendesk, Intercom, Freshdesk) |
| Social media | `defuddle` on Twitter/Reddit/forum URLs |
| NPS comments | Read CSV/text dump with score + comment columns |
| Slack feedback | `slack_search` MCP for messages in feedback-related channels |

Normalize each item to a unified schema:

```json
{
  "id": "unique-id",
  "source": "app-store|survey|ticket|social|nps|slack",
  "text": "feedback content",
  "rating": null,
  "date": "ISO-8601",
  "customer_tier": "free|pro|enterprise|unknown",
  "metadata": {}
}
```

Save as JSONL to `raw-feedback.jsonl`. Use `batch-agent-runner` for large datasets (100+ items).

### Phase 2: Classify

For each feedback item, extract:

| Field | Values |
|-------|--------|
| Topic cluster | Feature request / Bug report / UX complaint / Praise / Churn risk / Pricing |
| Sentiment | Positive / Negative / Neutral / Mixed |
| Urgency | Critical / High / Medium / Low |
| Feature area | Map to product areas (e.g., auth, dashboard, API, billing) |
| Customer tier | Free / Pro / Enterprise / Unknown |

Use `batch-agent-runner` for bulk classification (process in batches of 20-50). Save to `classified.jsonl`.

### Phase 3: Score & Prioritize

Apply RICE scoring via `evaluation-engine` rubric for each topic cluster:

| Dimension | Scale | What It Measures |
|-----------|-------|------------------|
| Reach | 1-10 | How many users mention this topic |
| Impact | 1-10 | Severity: minor annoyance (1) → blocking (10) |
| Confidence | 1-10 | Data volume and consistency supporting this topic |
| Effort | 1-10 | Estimated implementation complexity (inverted: 10 = trivial) |

RICE Score = (Reach * Impact * Confidence) / Effort

Rank all topic clusters by RICE score. Save to `rice-scores.tsv` with columns: rank, topic, reach, impact, confidence, effort, rice_score, sample_count.

### Phase 4: Synthesize

Group classified feedback by theme. For each of the top 5 themes:

| Element | Description |
|---------|-------------|
| Theme title | Clear 1-line label |
| Item count | Number of feedback items in this cluster |
| Sentiment distribution | % positive / negative / neutral / mixed |
| Representative quotes | 3-5 anonymized quotes that best illustrate the theme |
| Trend indicator | New / Growing / Stable / Declining (based on date distribution) |
| RICE score | From Phase 3 |

Detect emerging trends: themes appearing in the most recent 30% of feedback that were absent in earlier data.

Save to `themes.md`.

### Phase 5: Generate Report

Create executive feedback report via `anthropic-docx`:

| Section | Content |
|---------|---------|
| Executive summary | 1-page overview via `long-form-compressor` |
| Methodology | Channels analyzed, volume, date range, classification approach |
| Theme breakdown | Top 5 themes with sentiment charts (described in tables) |
| RICE-prioritized actions | Ranked action items with scores and rationale |
| Customer quotes | Anonymized, organized by theme |
| Trend analysis | Emerging themes, growing/declining patterns |
| Recommendations | Top 3 product actions based on RICE ranking |

Polish Korean text via `sentence-polisher`.

Generate visual dashboard via `visual-explainer`:
- Sentiment distribution pie chart
- Theme frequency bar chart
- RICE score ranking table
- Trend timeline

Save report to `feedback-report.docx`, dashboard to `dashboard.html`.

### Phase 6: Deliver

1. Write `manifest.json` with:
   - Total feedback items processed
   - Channel breakdown (count per source)
   - Top 5 themes with RICE scores
   - File paths and timestamps
   - Phase completion status

2. Push `themes.md` summary to Notion via `md-to-notion`

3. Post summary thread to Slack (if Slack MCP available):
   - Main message: top 3 themes + RICE scores
   - Thread reply: full theme breakdown + action items

## Examples

### Example 1: Multi-channel feedback analysis

User says: "Process all customer feedback from last month"

Actions:
1. Ingest feedback from App Store reviews, Zendesk tickets, NPS survey, and Slack #feedback
2. Classify each item by topic and sentiment
3. Score with RICE framework and cluster into themes
4. Generate executive .docx report with visual dashboard

Result: RICE-prioritized report, theme clusters, visual HTML dashboard, Slack summary

### Example 2: Korean app store feedback

User says: "고객 피드백 처리해줘 — App Store 리뷰 중심으로"

Actions:
1. Extract Korean app store reviews via structured-extractor
2. Run sentiment analysis with Korean NLP
3. Generate Korean executive report with action recommendations

Result: Korean .docx report with sentiment breakdown and prioritized improvements

## Error Handling

If classification fails for a batch, the remaining batches continue. Failed items are logged in `manifest.json` with `status: "classification_failed"`. Re-run Phase 2 for failed items only. Phase 3+ reads from `classified.jsonl` and processes only successfully classified items.

## Gotchas

- App store review URLs vary by region; Apple uses `apps.apple.com/{region}/`, Google uses `play.google.com/store/apps/details?id=`
- CSV column naming is inconsistent across helpdesk exports; detect columns by content pattern, not header name
- NPS scores without comments are excluded from text analysis but included in volume counts
- Anonymization must strip names, emails, and account IDs from quotes before including in reports
- Large datasets (1000+ items) should use `batch-agent-runner` with batches of 50 to avoid context limits
