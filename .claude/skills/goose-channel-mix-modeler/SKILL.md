---
name: goose-channel-mix-modeler
description: >-
  Model the optimal marketing channel mix based on budget, ICP, product stage,
  and growth goals. Allocates spend across organic, paid, outbound, community,
  and partnership channels using a framework that accounts for CAC payback,
  time-to-impact, and scalability. Pure reasoning skill.
---

# Goose Channel Mix Modeler

Model the optimal marketing channel mix based on budget, ICP, product stage, and growth goals. Allocates spend across organic, paid, outbound, community, and partnership channels using a framework that accounts for CAC payback, time-to-impact, and scalability. Pure reasoning skill.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/channel-mix-modeler.

## When to Use

- "How should we allocate our marketing budget?"
- "Model our channel mix for next quarter"
- "채널 믹스 모델링", "마케팅 예산 배분"
- "Which channels should we invest in?"

## Do NOT Use

- For paid channel selection only (use goose-paid-channel-prioritizer)
- For campaign planning on specific channels (use kwp-marketing-campaign-planning)
- For general marketing strategy (use pm-marketing-growth)

## Methodology

### Phase 1: Growth Context
Assess current situation:
- **Product stage**: Pre-PMF, Post-PMF, Scale
- **MRR/ARR**: Current and target
- **Budget**: Monthly marketing spend available
- **ICP**: Who and where are they?
- **Current channels**: What's working, what's not?

### Phase 2: Channel Evaluation Matrix
Score each channel on 5 dimensions:
| Channel | CAC | Payback | Scalability | Time-to-Impact | ICP Fit |
|---------|-----|---------|-------------|----------------|---------|
| Organic SEO | Low | 6-12mo | High | Slow | Varies |
| LinkedIn organic | Zero | 1-3mo | Medium | Medium | B2B high |
| Cold outbound | Medium | 1-2mo | Medium | Fast | High |
| Google ads | High | Immediate | High | Fast | Intent-based |
| LinkedIn ads | High | 1-2mo | Medium | Fast | B2B high |
| Community | Low | 3-6mo | Low-Med | Medium | Dev/niche |
| Referral | Low | 2-4mo | Low-Med | Medium | Product-led |
| Partnerships | Medium | 3-6mo | High | Slow | Strategic |

### Phase 3: Budget Allocation Model
Recommend allocation based on stage:
- **Pre-PMF** ($0-5K/mo): 70% founder-led (organic+outbound), 20% content, 10% experiment
- **Post-PMF** ($5-20K/mo): 40% proven channel, 30% content/SEO, 20% paid test, 10% experiment
- **Scale** ($20K+/mo): 50% scaled winners, 25% new channels, 15% brand, 10% experiment

### Phase 4: Scenario Modeling
Generate 3 budget scenarios (conservative, moderate, aggressive) with:
- Expected pipeline per channel
- CAC per channel
- Payback period
- Break-even timeline

## Output: Channel Mix Model with allocation recommendations, scenario projections, and quarterly milestone targets
