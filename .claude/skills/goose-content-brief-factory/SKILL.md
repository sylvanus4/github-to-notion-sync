---
name: goose-content-brief-factory
description: >-
  Generate detailed content briefs for blog posts, guides, and landing pages.
  Covers target keyword, search intent, SERP analysis, outline with H2/H3
  structure, key points per section, internal linking targets, and CTA
  strategy. Designed to make any writer produce consistent, SEO-optimized
  content wit
---

# Goose Content Brief Factory

Generate detailed content briefs for blog posts, guides, and landing pages. Covers target keyword, search intent, SERP analysis, outline with H2/H3 structure, key points per section, internal linking targets, and CTA strategy. Designed to make any writer produce consistent, SEO-optimized content without being an SEO expert.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/content-brief-factory.

## When to Use

- "Create a content brief for [topic]"
- "Generate a blog post brief targeting [keyword]"
- "콘텐츠 브리프 생성", "블로그 포스트 기획"
- "SEO content brief for our next article"

## Do NOT Use

- For full topical authority mapping (use goose-topical-authority-mapper)
- For programmatic SEO templates (use goose-programmatic-seo-planner)
- For writing the actual content (use kwp-marketing-content-creation)

## Methodology

### Phase 1: Keyword & Intent Analysis
- Primary keyword and search volume estimate
- Search intent: informational, commercial, navigational, transactional
- Related keywords and LSI terms
- SERP feature opportunities (featured snippet, FAQ, how-to)

### Phase 2: SERP Analysis
Analyze top 5-10 ranking pages:
- Content type (listicle, guide, comparison, tutorial)
- Average word count
- Common H2/H3 headings
- Unique angles or gaps in existing content
- Backlink profiles (what makes top content linkable?)

### Phase 3: Content Structure
- **Title options** (3 variants: keyword-first, benefit-first, curiosity-driven)
- **Meta description** template
- **H2/H3 outline** with key points per section
- **Introduction hook** — what stops the scroll?
- **Conclusion + CTA** — what should the reader do next?

### Phase 4: Differentiation
- What angle makes this better than current top results?
- Original data, framework, or perspective to include
- Internal linking targets (existing pages to link to/from)
- External authority sources to cite

## Output Format

```markdown
# Content Brief: [Title]
Target Keyword: [keyword] | Intent: [type] | Est. Volume: [range]
Content Type: [blog/guide/comparison] | Target Length: [words]
Difficulty: [low/medium/high]

## Outline
### H2: [Section 1]
- Key point A
- Key point B
### H2: [Section 2]
...

## Differentiation Angle
[What makes this better than existing content]

## Internal Links
- Link TO: [existing pages]
- Link FROM: [pages that should link here]

## CTA Strategy
[Primary CTA with placement recommendation]
```
