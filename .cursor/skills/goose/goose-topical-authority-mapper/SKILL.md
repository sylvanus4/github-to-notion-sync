# Goose Topical Authority Mapper

Build a topical authority map for SEO — a hierarchy of pillar pages, cluster articles, and supporting content organized around your core topics. Maps keyword intent, content gaps, and internal linking opportunities. Designed to make you the definitive resource for your topic cluster.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/topical-authority-mapper.

## When to Use

- "Build a topical authority map for [topic]"
- "Create a content cluster strategy"
- "토피컬 오소리티 맵", "콘텐츠 클러스터 전략"
- "What content do we need for topical authority?"

## Do NOT Use

- For individual content briefs (use goose-content-brief-factory)
- For SEO technical audit (use goose-seo-content-audit)
- For programmatic SEO template pages (use goose-programmatic-seo-planner)

## Methodology

### Phase 1: Core Topic Identification
- What 3-5 topics does your product own?
- What does your ICP search for at each buying stage?
- Map topics to business value (which topics drive revenue?)

### Phase 2: Keyword Research & Clustering
For each core topic:
- **Head terms** — high volume, competitive (pillar page targets)
- **Body terms** — moderate volume (cluster article targets)
- **Long-tail terms** — low volume, high intent (supporting content)
- Intent classification: informational, navigational, commercial, transactional

### Phase 3: Content Hierarchy Design
```
Pillar Page: [Core Topic]
├── Cluster Article: [Subtopic 1]
│   ├── Supporting: [Long-tail 1a]
│   └── Supporting: [Long-tail 1b]
├── Cluster Article: [Subtopic 2]
│   ├── Supporting: [Long-tail 2a]
│   └── Supporting: [Long-tail 2b]
└── Cluster Article: [Subtopic 3]
```

### Phase 4: Gap Analysis
- Existing content mapped to the hierarchy
- Missing content (gaps in the map)
- Weak content (exists but underperforming)
- Cannibalization (multiple pages targeting same keyword)

### Phase 5: Internal Linking Blueprint
- Link from every supporting → cluster → pillar
- Cross-link between related clusters
- Ensure every page has both inbound and outbound internal links

## Output: Topical Authority Map with hierarchy, keyword assignments, gap analysis, and internal linking blueprint
