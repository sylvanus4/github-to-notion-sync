---
name: kb-collect-sales
description: >-
  Daily collector for Sales KB topics (competitive-intel, sales-playbook).
  Scrapes competitor product/pricing pages, fetches G2/Capterra reviews,
  monitors industry news and press releases, collects social signals from
  tracked Twitter accounts, and ingests results into KB raw/ directories.
  Use when the user asks to "collect sales data", "update competitive intel",
  "sales KB collect", "영업 KB 수집", "경쟁사 데이터 수집", "kb-collect-sales",
  or when invoked by kb-daily-build-orchestrator.
  Do NOT use for marketing content collection (use kb-collect-marketing).
  Do NOT use for PM meeting sync (use kb-collect-pm).
  Do NOT use for manual KB ingestion (use kb-ingest).
  Korean triggers: "영업 KB 수집", "경쟁사 수집", "세일즈 데이터 수집".
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  tags: ["knowledge-base", "sales", "competitive-intel", "daily-collector"]
---

# KB Collect Sales — Daily Sales Intelligence Collector

Automated daily collector that gathers competitive intelligence and sales enablement data, then ingests into the `competitive-intel` and `sales-playbook` Knowledge Bases.

## Prerequisites

- `knowledge-bases/competitive-intel/competitor-registry.yaml` — competitor definitions
- `knowledge-bases/_config/social-feeds.yaml` — Twitter accounts and hashtags for sales
- WebSearch tool available
- defuddle API available
- kb-ingest skill available

## Input

No user input required for daily runs. Reads configuration from:
1. `competitor-registry.yaml` — competitor URLs per product line
2. `social-feeds.yaml` — Twitter accounts under `sales:` section

Optional: `--product-line <iaas|ai_platform|agent_studio|autonomous_agent>` to scope to one product line.

## Workflow

### Phase 1: Competitor Page Collection (parallel per product line)

For each competitor in `competitor-registry.yaml`:

1. **Product/Pricing Pages** — Use defuddle to extract clean markdown from competitor URLs (product pages, pricing pages, blog posts).
2. **Press Releases** — WebSearch for `"{competitor_name}" press release site:{competitor_domain} after:YYYY-MM-DD` (last 24 hours).
3. **G2/Capterra Reviews** — WebSearch for `site:g2.com/products/{g2_slug}/reviews` and `site:capterra.com/software/{capterra_slug}/reviews` to find recent reviews.
4. Save each result as a markdown file in `knowledge-bases/competitive-intel/raw/` with frontmatter:
   ```yaml
   ---
   title: "{Competitor} - {content_type}"
   source: "{url}"
   date_collected: "YYYY-MM-DD"
   content_type: "competitor-{product_page|pricing|press_release|review}"
   product_line: "{iaas|ai_platform|agent_studio|autonomous_agent}"
   competitor: "{competitor_name}"
   ---
   ```

### Phase 2: Industry News & Analyst Reports

1. WebSearch for recent cloud/AI industry news (last 24 hours):
   - "cloud infrastructure market news today"
   - "AI platform industry report"
   - "agent platform enterprise adoption"
2. Use defuddle to extract content from top results.
3. Save to `knowledge-bases/competitive-intel/raw/` with `content_type: "industry-news"`.

### Phase 3: Social Signal Collection

1. Read `social-feeds.yaml` → `sales.twitter_accounts` and `sales.hashtags`.
2. For each account/hashtag, WebSearch for recent tweets (last 24 hours):
   - `site:x.com "{account}" after:YYYY-MM-DD`
3. Compile social signals into a daily digest: `knowledge-bases/competitive-intel/raw/{date}-social-signals.md`.

### Phase 4: Sales Playbook Updates

1. WebSearch for new sales methodology content, win/loss analysis frameworks, and objection handling techniques.
2. If substantial new content is found, save to `knowledge-bases/sales-playbook/raw/`.

### Phase 5: Manifest Update

Update `manifest.json` for both `competitive-intel` and `sales-playbook` with new source entries and updated `raw_count`.

## Output Artifacts

| Phase | Output File | Description |
|-------|-------------|-------------|
| 1 | `knowledge-bases/competitive-intel/raw/{date}-{competitor}-{type}.md` | Competitor page extracts |
| 2 | `knowledge-bases/competitive-intel/raw/{date}-industry-news.md` | Industry news digest |
| 3 | `knowledge-bases/competitive-intel/raw/{date}-social-signals.md` | Social media signals |
| 4 | `knowledge-bases/sales-playbook/raw/{date}-{topic}.md` | Sales playbook updates |
| 5 | `knowledge-bases/*/manifest.json` | Updated manifests |

## Error Recovery

- If defuddle fails for a URL, fall back to WebFetch.
- If WebSearch returns no results for a competitor, skip and log.
- If social feed collection fails, continue with other phases.

## Gotchas

- G2/Capterra may block scraping; WebSearch excerpts are often sufficient.
- Rate-limit defuddle calls (max 2 per second).
- Competitor pricing pages change format frequently; extract text, not structure.
- Twitter/X search via WebSearch is unreliable for real-time data; accept daily-level granularity.
