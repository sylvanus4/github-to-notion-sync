---
name: goose-campaign-brief-generator
description: >-
  Generate a complete marketing campaign brief from a launch goal, ICP, and
  product context. Pure reasoning skill. Outputs channel plan, messaging
  angles, content types, timeline, and success metrics. Designed for
  seed/Series A founders and small GTM teams who need to run focused campaigns
  without bei
---

# Goose Campaign Brief Generator

Generate a complete marketing campaign brief from a launch goal, ICP, and product context. Pure reasoning skill. Outputs channel plan, messaging angles, content types, timeline, and success metrics. Designed for seed/Series A founders and small GTM teams who need to run focused campaigns without being professional marketers.

Adapted from [gooseworks-ai/goose-skills](https://github.com/gooseworks-ai/goose-skills) composites/campaign-brief-generator.

## When to Use

- "Generate a campaign brief for our product launch"
- "Create a marketing campaign plan"
- "Campaign brief from ICP and product context"
- "캠페인 브리프 생성", "마케팅 캠페인 기획"

## Do NOT Use

- For brand voice enforcement (use kwp-brand-voice-brand-voice-enforcement)
- For full GTM strategy with battlecards (use pm-go-to-market)
- For content repurposing across platforms (use content-repurposing-engine)

## Methodology

### Phase 1: Campaign Foundation
1. **Campaign goal** — primary metric (signups, MQLs, demos, revenue)
2. **ICP distillation** — role, company size, pain, buying trigger
3. **Product-market angle** — what changed that makes this campaign timely?

### Phase 2: Channel Plan
Recommend 2-3 channels based on ICP + budget:
| Channel | Best For | Budget Threshold |
|---------|----------|-----------------|
| LinkedIn organic | B2B, founder-led | $0 |
| Cold email | Direct outreach, proven ICP | $50-200/mo tools |
| SEO/content | Long-term, compound | $0 (time cost) |
| LinkedIn ads | Precise B2B targeting | $3K+/mo |
| Google ads | High-intent search | $2K+/mo |
| Community/Reddit | Dev tools, niche B2B | $0 |

### Phase 3: Messaging Angles
Generate 3-5 messaging angles per channel, each with:
- Hook (first line / subject line)
- Core claim (what you're promising)
- Proof point (evidence or social proof)
- CTA (specific next step)

### Phase 4: Content Types & Calendar
Map content to campaign phases:
- **Week 1-2:** Awareness (educational, problem-focused)
- **Week 3-4:** Consideration (comparison, proof, case study)
- **Week 5-6:** Decision (offer, demo, trial)

### Phase 5: Success Metrics
Define leading and lagging indicators with targets:
- Leading: impressions, clicks, email opens, demo requests
- Lagging: MQLs, SQLs, pipeline, closed revenue

## Output Format

```markdown
# Campaign Brief: [Campaign Name]
Goal: [Primary metric + target]
ICP: [One-line summary]
Timeline: [Duration]
Budget: [Range]

## Channel Plan
[2-3 channels with rationale]

## Messaging Angles
[3-5 angles per channel]

## Content Calendar
[Week-by-week plan]

## Success Metrics
[Leading + lagging indicators with targets]

## Risks & Mitigations
[Top 3 risks and how to address them]
```
