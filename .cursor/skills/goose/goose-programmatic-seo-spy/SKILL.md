# Goose Programmatic SEO Spy

Reverse-engineer how competitors do programmatic SEO. Detects URL pattern clusters (vs/, integrations/, for-{industry}/), estimates page count per pattern, analyzes template quality, infers which patterns actually drive traffic, and identifies gaps you can exploit. Outputs a competitive pSEO landscape report.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/programmatic-seo-spy.

## When to Use

- "How does [competitor] do programmatic SEO?"
- "Reverse-engineer competitor pSEO strategy"
- "경쟁사 프로그래매틱 SEO 분석", "pSEO 스파이"
- "Detect URL patterns on [competitor site]"

## Do NOT Use

- For designing your own pSEO (use goose-programmatic-seo-planner)
- For general competitor analysis without SEO focus (use kwp-marketing-competitive-analysis)
- For full SEO audit (use goose-seo-content-audit)

## Methodology

### Phase 1: Sitemap/URL Discovery
Crawl sitemap.xml or robots.txt, infer URL patterns from structure.

### Phase 2: Pattern Detection
Cluster URLs by template type using path segments:
- Count pages per pattern cluster
- Identify variable segments vs static segments
- Map pattern hierarchy (parent/child relationships)

### Phase 3: Template Quality Analysis
Sample 3-5 pages per pattern:
- Content depth and uniqueness per page
- Dynamic vs static content ratio
- Internal linking structure within the pattern
- Schema markup and meta optimization

### Phase 4: Traffic Inference
Estimate which patterns drive organic traffic using:
- Search volume for pattern keywords
- Domain authority of the pages
- SERP presence for sampled keywords
- Backlink distribution across patterns

### Phase 5: Gap Analysis
- Patterns they have that you don't
- Patterns where their template quality is weak (opportunity to outperform)
- Underserved variable permutations

## Output: Competitive pSEO Landscape Report with pattern inventory, quality scores, traffic estimates, and exploitation opportunities
