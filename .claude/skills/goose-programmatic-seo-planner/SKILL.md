---
name: goose-programmatic-seo-planner
description: >-
  Identify programmatic SEO page patterns worth building — vs/ pages,
  integrations/, for-{industry}/, alternatives-to/, use-cases/ — and design
  the template structure, data model, and priority order. Outputs a complete
  pSEO blueprint with URL patterns, title templates, content frameworks, and
  data sou
---

# Goose Programmatic SEO Planner

Identify programmatic SEO page patterns worth building — vs/ pages, integrations/, for-{industry}/, alternatives-to/, use-cases/ — and design the template structure, data model, and priority order. Outputs a complete pSEO blueprint with URL patterns, title templates, content frameworks, and data sources per variable.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/programmatic-seo-planner.

## When to Use

- "Design a programmatic SEO strategy"
- "What pSEO page types should we build?"
- "프로그래매틱 SEO 계획", "pSEO 블루프린트"
- "Plan template pages for SEO at scale"

## Do NOT Use

- For reverse-engineering competitor pSEO (use goose-programmatic-seo-spy)
- For individual content briefs (use goose-content-brief-factory)
- For general SEO audit (use goose-seo-content-audit)

## Methodology

### Phase 1: Pattern Discovery
Analyze product, ICP, and competitor landscape to identify viable pSEO patterns:
- **vs/ pages** — comparison with competitors or alternatives
- **integrations/** — partner/integration landing pages
- **for-{industry}/** — industry-specific landing pages
- **alternatives-to/** — capturing competitor brand search
- **use-cases/** — solution-oriented pages
- **glossary/** — educational keyword capture
- **templates/** — template library pages

### Phase 2: Template Design
For each pattern, define:
- URL structure: `/{pattern}/{variable}/`
- Title template: `[Variable] + [Value Prop]`
- H1, meta description templates
- Content framework (sections with variable and static content)
- Data model: what variables are needed and where they come from

### Phase 3: Prioritization
Score each pattern on:
- Search volume potential (aggregate across all variable permutations)
- Commercial intent alignment with ICP
- Data availability (can you populate the template?)
- Competition level per pattern
- Implementation effort

## Output: pSEO Blueprint Markdown with URL patterns, template designs, data models, and priority scores
