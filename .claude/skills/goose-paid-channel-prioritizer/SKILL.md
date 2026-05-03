---
name: goose-paid-channel-prioritizer
description: >-
  For founders who don't know where to start with paid ads. Analyzes ICP,
  competitor ad presence, budget constraints, and product type to recommend
  which 1-2 paid channels to start with and provides a 90-day ramp plan.
  Prevents the common mistake of spreading a small budget across too many
  platforms.
---

# Goose Paid Channel Prioritizer

For founders who don't know where to start with paid ads. Analyzes ICP, competitor ad presence, budget constraints, and product type to recommend which 1-2 paid channels to start with and provides a 90-day ramp plan. Prevents the common mistake of spreading a small budget across too many platforms. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/paid-channel-prioritizer.

## When to Use

- "Which paid channels should we start with?"
- "Where should I spend my ad budget?"
- "유료 광고 채널 추천", "광고 예산 배분"
- "90-day paid ads ramp plan"

## Do NOT Use

- For creating actual ad campaigns (use kwp-marketing-campaign-planning)
- For SEO strategy (use goose-seo-opportunity-finder)
- For content-only marketing plans (use kwp-marketing-content-creation)

## Methodology

### Input Analysis
1. **ICP profile** — role, company size, buying behavior, where they spend time online
2. **Budget** — monthly ad spend available
3. **Product type** — B2B SaaS, dev tools, marketplace, consumer
4. **Competitor ad presence** — where are competitors advertising?

### Channel Scoring Matrix
Score each channel (1-10) across 5 dimensions:

| Channel | ICP Match | Intent Signal | Cost Efficiency | Learning Speed | Scalability |
|---------|-----------|--------------|-----------------|---------------|-------------|
| Google Search | | | | | |
| LinkedIn Ads | | | | | |
| Meta (FB/IG) | | | | | |
| Reddit Ads | | | | | |
| Twitter/X Ads | | | | | |
| YouTube Ads | | | | | |
| Bing Ads | | | | | |
| Programmatic | | | | | |

### Budget Threshold Rules
- Under $2K/mo: 1 channel only
- $2K-5K/mo: 1 primary + 1 test
- $5K-15K/mo: 2 primary channels
- $15K+/mo: 2-3 channels with retargeting layer

### 90-Day Ramp Plan
- **Month 1:** Foundation (pixel/tracking setup, audience build, 3-5 creative tests)
- **Month 2:** Optimization (scale winners, kill losers, test new angles)
- **Month 3:** Scale (increase budget on proven performers, add retargeting, test new channel)

## Output: Channel recommendation with scoring rationale + 90-day ramp plan
