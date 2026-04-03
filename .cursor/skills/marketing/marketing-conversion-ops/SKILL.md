---
name: marketing-conversion-ops
version: 1.0.0
description: Conversion rate optimization — CRO audits with 8-dimension scoring for landing pages, and survey-to-lead-magnet engine that segments survey data into targeted content briefs.
---

# Marketing Conversion Ops

CRO audit system and survey-to-lead-magnet engine. Scores landing pages across 8 dimensions and converts survey CSV data into segmented lead magnet briefs.

## Triggers

Use when the user asks to:
- "CRO audit", "landing page score", "conversion optimization", "lead magnet"
- "survey to lead magnet", "landing page audit", "conversion rate"
- "전환율 최적화", "랜딩 페이지 감사", "리드 마그넷"

## Do NOT Use

- For UX heuristic evaluation → use `ux-expert`
- For A/B test statistical analysis → use `pm-data-analytics`
- For growth hacking ideation → use `agency-growth-hacker`
- For design system compliance audit → use `design-qa-checklist`

## Prerequisites

- Python 3.10+
- `pip install requests beautifulsoup4 pandas`
- No API keys required

## Execution Steps

### Step 1: CRO Audit
Run `scripts/cro_audit.py --url <landing_page_url>` for single page or `--urls <url1> <url2>` for batch. Add `--industry <type>` for benchmark comparison. Use `--json` for machine-readable output.

### Step 2: Survey Lead Magnet
Run `scripts/survey_lead_magnet.py --csv <survey_data.csv> --pain-columns <col1,col2>` to segment respondents and generate lead magnet briefs. Use `--top-segments <N>` to limit output.

## Examples

### Example 1: Audit a landing page

User: "Score our pricing page for conversion"

1. Run `scripts/cro_audit.py --url https://example.com/pricing --industry saas`

Result: 8-dimension score card (clarity, CTA, trust, speed, mobile, copy, design, social proof) with prioritized fixes.

### Example 2: Generate lead magnets from survey data

User: "Turn our customer survey into lead magnet ideas"

1. Run `scripts/survey_lead_magnet.py --csv survey_results.csv --pain-columns "biggest_challenge,desired_outcome" --top-segments 5`

Result: 5 segmented lead magnet briefs with audience profile, pain points, and content outlines.

## Error Handling

| Error | Action |
|-------|--------|
| URL unreachable | Verify URL is publicly accessible; check for authentication walls |
| CSV column not found | Verify `--pain-columns` match exact column headers in CSV |
| BeautifulSoup parse error | URL may use heavy JavaScript; try with rendered page source |
| No industry benchmarks available | Audit runs without benchmarks; generic thresholds apply |

## Output

- 8-dimension CRO score card per landing page
- Prioritized improvement recommendations
- Segmented lead magnet briefs with content outlines
- Industry benchmark comparison (when available)
