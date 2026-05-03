---
name: goose-competitive-pricing-intel
description: >-
  Monitor competitor pricing pages via live web scrape and Web Archive
  snapshots. Track plan changes, tier restructuring, new pricing models, and
  feature gating shifts. Produces a pricing comparison matrix and flags when a
  competitor changes packaging.
---

# Goose Competitive Pricing Intel

Monitor competitor pricing pages via live web scrape and Web Archive snapshots. Track plan changes, tier restructuring, new pricing models, and feature gating shifts. Produces a pricing comparison matrix and flags when a competitor changes packaging.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/competitive-pricing-intel.

## When to Use

- "Track competitor pricing changes"
- "Build a pricing comparison matrix"
- "경쟁사 가격 모니터링", "가격 비교 매트릭스"
- "Has [competitor] changed their pricing?"

## Do NOT Use

- For general competitive analysis (use kwp-product-management-competitive-analysis)
- For pricing strategy design (use pm-product-strategy)
- For value-based pricing frameworks (use marketing-sales-playbook)

## Methodology

### Phase 1: Current Price Capture
- Fetch each competitor's /pricing page via web search or browser
- Extract: plan names, prices, billing intervals, feature lists per tier, limits/quotas
- Capture enterprise/custom pricing signals (contact sales indicators)

### Phase 2: Historical Price Tracking
- Check Web Archive (web.archive.org) for previous versions of pricing pages
- Detect changes: price increases/decreases, tier additions/removals, feature gating shifts
- Track pricing model evolution (per-seat → usage-based, etc.)

### Phase 3: Comparison Matrix Assembly

## Output Format

```markdown
# Pricing Comparison: [Your Product] vs Competitors

| Dimension | [You] | [Comp 1] | [Comp 2] | [Comp 3] |
|-----------|-------|----------|----------|----------|
| Free tier | | | | |
| Starter price | | | | |
| Pro price | | | | |
| Enterprise | | | | |
| Billing model | | | | |
| Key limits | | | | |

## Recent Changes Detected
| Competitor | Change | Approximate Date | Impact |
|-----------|--------|-------------------|--------|

## Pricing Strategy Insights
[Analysis of positioning, anchoring, bundling, and gating patterns]

## Recommendations
[How to position your pricing relative to detected competitor moves]
```
