---
name: portal-scanner
description: >-
  Multi-strategy web scanner that extracts structured data from portals, job boards,
  product pages, or listing sites. Uses a 3-level content extraction cascade
  (Playwright browser → REST API → WebSearch fallback) with deduplication and
  scan history tracking.
user_invocable: true
---

# Portal Scanner

Scan web portals and listing sites to extract structured data using a tiered
extraction strategy. Tracks scan history to avoid re-processing and supports
configurable extraction templates per portal type.

## When to Use

- Scanning job boards, product listing pages, news portals, or aggregator sites
- Extracting structured data from multiple pages of a web portal
- User says "scan", "scrape portal", "extract listings", "포탈 스캔", "사이트 스캔"
- Building datasets from web sources with deduplication

## Do NOT Use

- Single-page content extraction (use defuddle)
- Interactive browser testing (use agent-browser or cursor-ide-browser)
- General web search without page extraction (use WebSearch)
- API-first data sources with official client libraries

## Architecture

```
Portal Scanner
├── Load portal config (config/ops/portals/{portal}.yaml)
├── 3-Level Extraction Cascade:
│   ├── L1: Browser automation (Playwright via agent-browser)
│   ├── L2: REST/JSON API (if portal exposes one)
│   └── L3: WebSearch + defuddle fallback
├── Parse & normalize results
├── Dedup against scan history (data/ops/scan-history.tsv)
├── Output structured results
└── Update scan history
```

## Portal Configuration

Define portals in `config/ops/portals/{name}.yaml`:

```yaml
portal: hacker-news-jobs
version: 1
description: HN Who is Hiring monthly threads

source:
  type: web
  base_url: "https://news.ycombinator.com"
  entry_path: "/jobs"
  pagination:
    type: next-link
    max_pages: 3

extraction:
  strategy: L1  # L1=browser, L2=api, L3=search
  fallback: true  # cascade to next level on failure
  selectors:
    title: ".titleline > a"
    url: ".titleline > a@href"
    metadata: ".subtext"
  timeout_ms: 15000

output:
  format: jsonl
  path: "data/ops/scans/{portal}-{date}.jsonl"
  fields:
    - id
    - title
    - url
    - source
    - scanned_at
    - metadata

dedup:
  key: url
  history_file: "data/ops/scan-history.tsv"

schedule:
  frequency: daily
  last_scan: null
```

## 3-Level Extraction Cascade

### Level 1: Browser Automation

Best for JavaScript-heavy sites, paginated listings, and authenticated portals.

1. Launch headless browser via `agent-browser` CLI or `cursor-ide-browser` MCP
2. Navigate to entry URL
3. Extract items using CSS selectors from config
4. Handle pagination (next-link, infinite scroll, or page numbers)
5. Capture screenshots for verification if needed

### Level 2: REST/JSON API

Best for portals with public APIs (GitHub, HN Algolia, Product Hunt, etc.).

1. Call API endpoint with appropriate parameters
2. Parse JSON response
3. Map API fields to output schema
4. Handle pagination via API cursors/offsets

### Level 3: WebSearch + Defuddle Fallback

Best when L1/L2 fail or for ad-hoc one-time scans.

1. WebSearch for `site:{domain} {query}`
2. Extract top result URLs
3. Defuddle each URL for clean content
4. Parse structured data from markdown output

## Execution Flow

### Step 1: Select Portal

Load portal config or create ad-hoc scan config from user request.

### Step 2: Pre-scan Check

1. Read `data/ops/scan-history.tsv` for this portal
2. Check last scan timestamp
3. If scanned within frequency window, ask to re-scan or skip

### Step 3: Extract

Run extraction cascade (L1 → L2 → L3) based on config:
1. Try configured strategy level first
2. If `fallback: true` and current level fails, try next level
3. Collect raw items from all successful levels

### Step 4: Normalize

Transform raw extracted data into output schema:
- Assign sequential IDs
- Normalize URLs (remove tracking params)
- Parse dates to ISO format
- Extract metadata fields

### Step 5: Dedup

Compare extracted items against scan history:
1. Read `data/ops/scan-history.tsv`
2. Filter out items where `dedup.key` already exists
3. Mark new items as `new`, existing as `seen`

### Step 6: Output

1. Write new items to `data/ops/scans/{portal}-{date}.jsonl`
2. Append new items to `data/ops/scan-history.tsv`
3. Report: total extracted / new / duplicates

## Scan History Format

`data/ops/scan-history.tsv`:

```tsv
portal	dedup_key	first_seen	last_seen	scan_count
hacker-news-jobs	https://example.com/job/123	2026-04-01	2026-04-06	3
tech-blogs	https://blog.example.com/post	2026-04-05	2026-04-05	1
```

## Commands

| Input | Action |
|-------|--------|
| `scan <portal>` | Run configured portal scan |
| `scan <url> --adhoc` | Ad-hoc single-URL extraction |
| `scan status` | Show scan history summary per portal |
| `scan list` | List configured portals |
| `scan history <portal>` | Show scan history for a portal |
| `scan new <name> <url>` | Create new portal config interactively |

## Built-in Portal Templates

| Template | Description |
|----------|-------------|
| `hacker-news` | HN front page, jobs, Show HN |
| `github-trending` | Trending repos by language/period |
| `arxiv-new` | New papers by category |
| `product-hunt` | Daily top products |
| `custom` | User-defined extraction config |

## Integration Points

- **pipeline-inbox**: Scan results feed into inbox for deferred processing
- **batch-agent-runner**: Batch-process scan results through evaluation
- **evaluation-engine**: Score scanned items against rubrics
- **unified-intel-intake**: Route scanned articles to appropriate pipelines
- **x-to-slack**: Scanned items can be posted to Slack channels
- **kb-ingest**: Import scan results into knowledge bases

## Constraints

- Respect `robots.txt` and rate limits (min 2s between requests)
- Never store credentials in portal config (use .env)
- Scan history is append-only; use `scan history --prune` to archive
- Max 100 items per scan run (paginate if larger)
- Log extraction level used for each item (L1/L2/L3) for quality tracking
