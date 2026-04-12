---
name: kb-collect-marketing
description: >-
  Daily collector for Marketing KB topics (brand-guidelines, marketing-playbook,
  content-library). Monitors competitor content (blogs, landing pages, social),
  tracks SEO trends, collects industry benchmark reports, and updates brand
  reference materials. Uses Apple-inspired brand model as baseline.
  Use when the user asks to "collect marketing data", "update marketing KB",
  "마케팅 KB 수집", "콘텐츠 수집", "kb-collect-marketing",
  or when invoked by kb-daily-build-orchestrator.
  Do NOT use for sales competitive intel (use kb-collect-sales).
  Do NOT use for PM data (use kb-collect-pm).
  Korean triggers: "마케팅 KB 수집", "콘텐츠 수집", "브랜드 데이터 수집".
metadata:
  author: "thaki"
  version: "1.1.0"
  category: "execution"
  tags: ["knowledge-base", "marketing", "content", "brand", "daily-collector", "3-day-window"]
---

# KB Collect Marketing — Daily Marketing Intelligence Collector

Automated daily collector that gathers marketing content, SEO data, competitor content strategies, and brand reference materials into the marketing KB topics.

## Prerequisites

- `knowledge-bases/competitive-intel/competitor-registry.yaml` — competitor blog/landing URLs
- `knowledge-bases/_config/social-feeds.yaml` — marketing Twitter accounts and RSS feeds
- WebSearch tool available
- defuddle API available

## Collection Window

> **NEWS_WINDOW_DAYS=3** — All external content searches (competitor blogs, SEO trends, benchmarks, brand updates, social signals) use a 3-day rolling window. This balances freshness with coverage for items published on weekends or off-hours.

## Deduplication (collector-side)

Before writing any raw file, check existing files in the target `raw/` directory from the last 3 days:

1. **Scan** all `*.md` files in `knowledge-bases/{topic}/raw/` with dates within the last 3 days (based on filename `{date}-` prefix).
2. **Parse YAML frontmatter** of each file to extract `source` (URL) and `title`.
3. **Skip** writing a new file if either condition matches:
   - Same `source` URL already exists in any file from the last 3 days.
   - Same `title` (case-insensitive, trimmed) already exists in any file from the last 3 days.
4. **Track** the count of skipped items and report as `dedup_skipped` in the collector summary returned to the orchestrator.

## Workflow

### Phase 1: Competitor Content Monitoring

For each competitor in `competitor-registry.yaml` that has blog/RSS URLs:

1. Check RSS feeds (if available) for new posts in the last 3 days.
2. Use defuddle to extract new blog posts.
3. Analyze content type (product launch, thought leadership, case study, tutorial).
4. Save to `knowledge-bases/content-library/raw/{date}-{competitor}-{slug}.md` with frontmatter:
   ```yaml
   ---
   title: "{Competitor} Blog: {title}"
   source: "{url}"
   date_collected: "YYYY-MM-DD"
   content_type: "competitor-content"
   competitor: "{name}"
   content_format: "blog|case-study|tutorial|announcement"
   ---
   ```

### Phase 2: SEO Trend Tracking

1. WebSearch for trending keywords in cloud/AI space:
   - "AI platform trends 2026"
   - "cloud GPU market growth"
   - "AI agent enterprise adoption"
2. Compile keyword trends and search volume insights.
3. Save to `knowledge-bases/marketing-playbook/raw/{date}-seo-trends.md`.

### Phase 3: Industry Benchmark Updates

1. WebSearch for new marketing benchmark reports:
   - "B2B SaaS marketing benchmarks 2026"
   - "cloud marketing ROI report"
2. Extract and summarize findings.
3. Save to `knowledge-bases/marketing-playbook/raw/{date}-benchmarks.md` (only if new data found).

### Phase 4: Brand Reference Collection

1. Monitor Apple marketing updates (apple.com/newsroom) and other brand exemplars.
2. Collect new brand/design trend articles.
3. Save to `knowledge-bases/brand-guidelines/raw/{date}-brand-trends.md` (only if new data found).

### Phase 5: Social Content Collection

1. Read `social-feeds.yaml` → `marketing.twitter_accounts` and `marketing.hashtags`.
2. WebSearch for recent marketing-relevant social signals.
3. Monitor `marketing.rss_feeds` (HubSpot, CMI) for new articles.
4. Compile into `knowledge-bases/content-library/raw/{date}-social-digest.md`.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/content-library/raw/{date}-{competitor}-*.md` | Competitor content |
| 2 | `knowledge-bases/marketing-playbook/raw/{date}-seo-trends.md` | SEO trends |
| 3 | `knowledge-bases/marketing-playbook/raw/{date}-benchmarks.md` | Benchmarks |
| 4 | `knowledge-bases/brand-guidelines/raw/{date}-brand-trends.md` | Brand reference |
| 5 | `knowledge-bases/content-library/raw/{date}-social-digest.md` | Social digest |

## Gotchas

- RSS feeds may require User-Agent header; use defuddle or WebFetch as fallback.
- SEO keyword data from free sources is directional, not exact volumes.
- Only collect genuinely new content; skip if no updates since last run.
