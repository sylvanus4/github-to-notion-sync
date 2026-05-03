---
name: marketing-revenue-intelligence
description: >-
  Revenue intelligence combining Gong call insights, multi-touch
  content-to-revenue attribution, and automated client report generation with
  GA4, HubSpot, and Ahrefs integration.
disable-model-invocation: true
---

# Marketing Revenue Intelligence

Revenue intelligence system integrating Gong call analysis, multi-touch attribution modeling, and automated client report generation across GA4, HubSpot, Ahrefs, and Gong.

## Triggers

Use when the user asks to:

- "revenue attribution", "Gong insights", "content ROI", "client report"
- "marketing attribution", "revenue pipeline analysis"
- "매출 귀속", "Gong 인사이트", "콘텐츠 ROI", "클라이언트 리포트"

## Do NOT Use

- For marketing performance dashboards → use `kwp-marketing-performance-analytics`
- For general data visualization → use `kwp-data-data-visualization`
- For sales call preparation → use `kwp-sales-call-prep`

## Prerequisites

- Python 3.10+
- `pip install requests python-dotenv`
- Environment: `GONG_ACCESS_KEY`, `GONG_ACCESS_KEY_SECRET`, `HUBSPOT_API_KEY`
- Optional: `GA4_PROPERTY_ID`, `GA4_CREDENTIALS_JSON`, `AHREFS_TOKEN`

## Execution Steps

### Step 1: Gong Insight Pipeline

Run `scripts/gong_insight_pipeline.py` with flags: `--file` (local transcript), `--gong` (API fetch), `--content-topics`, `--follow-ups`.

### Step 2: Revenue Attribution

Run `scripts/revenue_attribution.py --report` for multi-touch attribution. Additional flags: `--gaps` (coverage gaps), `--cpa` (cost per acquisition).

### Step 3: Client Report Generation

Run `scripts/client_report_generator.py --client <name> --format markdown` with `--anomalies` and `--compare` for period comparison.

## Examples

### Example 1: Analyze a sales call

User: "Extract insights from yesterday's discovery call"

1. Run `scripts/gong_insight_pipeline.py --file call_transcript.txt --content-topics --follow-ups`

Result: Topic-mapped insights, objection patterns, follow-up actions, and content opportunity signals.

### Example 2: Generate client attribution report

User: "Show me content-to-revenue attribution for Acme Corp"

1. Run `scripts/revenue_attribution.py --report --client "Acme Corp" --period Q1-2026`

Result: Multi-touch attribution model showing which content influenced pipeline and revenue.

## Error Handling

| Error | Action |
|-------|--------|
| GONG_ACCESS_KEY not set | Required for API mode; use `--file` for local transcripts |
| HUBSPOT_API_KEY not set | Required for attribution; fall back to manual data input |
| No attribution data for client | Check client name spelling; verify HubSpot deal association |
| GA4 credentials missing | Attribution works without GA4 but website touchpoints are excluded |

## Output

- Gong insight summaries with content-topic mapping
- Multi-touch attribution report
- Client-ready performance reports
- Follow-up action items from call analysis
