---
name: marketing-seo-ops
version: 1.0.0
description: SEO operations stack — content attack briefs, Google Search Console optimization, keyword gap analysis, and trend scouting for organic growth.
---

# Marketing SEO Ops

SEO operations stack combining content attack briefs, GSC data analysis, keyword gap identification, and trend scouting for systematic organic growth.

## Triggers

Use when the user asks to:

- "SEO analysis", "content attack brief", "GSC optimization", "keyword gap"
- "trend scout", "SEO audit", "striking distance keywords"
- "SEO 분석", "콘텐츠 어택 브리프", "키워드 갭 분석"

## Do NOT Use

- For 4-pillar strategic SEO audit (AEO, Core Web Vitals, technical audit, content gap) → use `ai-seo-growth-engine`
- For general marketing performance analytics → use `kwp-marketing-performance-analytics`
- For content creation without SEO analysis → use `kwp-marketing-content-creation`
- For website cloning → use `clone-website`

## Prerequisites

- Python 3.10+
- `pip install google-auth google-auth-oauthlib google-api-python-client requests`
- Environment: `GSC_SITE_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- Optional: `AHREFS_TOKEN`, `BRAVE_API_KEY`

## Execution Steps

### Step 1: GSC Authentication

Run `scripts/gsc_auth.py` once to authenticate with Google Search Console.

### Step 2: Content Attack Brief

Run `scripts/content_attack_brief.py` to generate a comprehensive SEO brief with keyword clusters, competitor analysis, and content recommendations.

### Step 3: GSC Analysis

Run `scripts/gsc_client.py` with flags: `--striking` (near-first-page keywords), `--queries` (top queries), `--trend` (traffic trends).

### Step 4: Trend Scouting

Run `scripts/trend_scout.py` to discover emerging topics and search trends before competitors.

## Cadence

- Weekly: content attack brief
- Daily: striking distance keyword monitoring
- Bi-weekly: trend scouting

## Examples

### Example 1: Generate a content attack brief

User: "Create an SEO brief for our AI platform blog"

1. Run `scripts/content_attack_brief.py --domain example.com --topic "AI platform"`

Result: Comprehensive brief with keyword clusters, competitor content gaps, and content recommendations.

### Example 2: Find striking distance keywords

User: "Which keywords are we close to ranking on page 1?"

1. Run `scripts/gsc_client.py --striking --min-position 5 --max-position 20`

Result: Keywords where small improvements could push to page 1, ranked by opportunity.

## Error Handling

| Error | Action |
|-------|--------|
| GSC authentication failed | Run `scripts/gsc_auth.py` to re-authenticate |
| GSC_SITE_URL not set | Set env var to your Search Console property URL |
| No GSC data for domain | Verify domain is registered in Search Console |
| Rate limit on trend API | Implement backoff; default 1 request per second |

## Output

- Content attack brief (markdown)
- Keyword opportunity matrix
- Striking distance keyword list
- Trend alerts
