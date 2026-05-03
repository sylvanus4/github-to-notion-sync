---
name: goose-seo-content-audit
description: >-
  Audit existing website content for SEO performance — identify
  underperforming pages, cannibalization issues, thin content, missing
  internal links, and quick-win optimization opportunities. Prioritizes fixes
  by effort vs impact. Pure reasoning skill that works from a content
  inventory or sitemap.
---

# Goose SEO Content Audit

Audit existing website content for SEO performance — identify underperforming pages, cannibalization issues, thin content, missing internal links, and quick-win optimization opportunities. Prioritizes fixes by effort vs impact. Pure reasoning skill that works from a content inventory or sitemap.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/seo-content-audit.

## When to Use

- "Audit our blog content for SEO"
- "Find underperforming pages on our site"
- "SEO 콘텐츠 감사", "SEO 콘텐츠 최적화"
- "Which pages should we update or consolidate?"

## Do NOT Use

- For creating new content briefs (use goose-content-brief-factory)
- For topical authority planning (use goose-topical-authority-mapper)
- For technical SEO audit (use marketing-seo-ops)

## Methodology

### Phase 1: Content Inventory
Build or import a content inventory:
- URL, title, publish date, last updated
- Target keyword (if any), current ranking
- Traffic trend (up/down/flat)
- Word count, internal links in/out

### Phase 2: Classification
Classify each page:
- **Stars** — high traffic, good ranking, keep optimizing
- **Quick wins** — ranking page 2-3, small tweaks = big gains
- **Underperformers** — old content, declining traffic, needs update or consolidation
- **Thin content** — <500 words, no target keyword, low value
- **Cannibals** — multiple pages competing for same keyword

### Phase 3: Optimization Recommendations
For each category:
| Action | Pages | Effort | Impact |
|--------|-------|--------|--------|
| Update + republish | Quick wins | Low | High |
| Consolidate (301 redirect) | Cannibals | Medium | High |
| Expand + add media | Thin content | Medium | Medium |
| Delete or noindex | Zero-value | Low | Low |
| New internal links | Stars | Low | Medium |

### Phase 4: Priority Matrix
Plot all recommendations on:
- X-axis: Effort (low → high)
- Y-axis: Impact (low → high)
- Execute top-right quadrant first (low effort, high impact)

## Output: SEO Content Audit Report with classified inventory, optimization recommendations, and prioritized action plan
