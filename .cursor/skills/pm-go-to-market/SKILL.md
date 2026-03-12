---
name: pm-go-to-market
description: >-
  Orchestrate go-to-market workflows: GTM strategy and launch plans, ideal
  customer profiles, beachhead segments, growth loops, GTM motions assessment,
  and competitive battlecards. Based on phuryn/pm-skills. Use when the user asks
  for "GTM strategy", "go-to-market plan", "ideal customer profile", "ICP",
  "beachhead segment", "growth loops", "GTM motions", "battlecard", or "launch
  plan". Do NOT use for product discovery (use pm-product-discovery), marketing
  content creation (use kwp-marketing-content-creation), or sales outreach (use
  kwp-sales-draft-outreach). Korean triggers: "시장", "계획", "워크플로우", "스킬".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Go-to-Market

Orchestrate go-to-market workflows using phuryn/pm-skills frameworks — GTM strategy, ICP, beachhead segments, growth loops, GTM motions, and competitive battlecards.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|--------------|-----------|
| beachhead-segment | First market, initial customer segment, market entry | [references/beachhead-segment.md](references/beachhead-segment.md) |
| competitive-battlecard | Sales prep vs competitor, battlecard, "why not X?" | [references/competitive-battlecard.md](references/competitive-battlecard.md) |
| growth-loops | Growth loops, flywheels, PLG traction, viral loops | [references/growth-loops.md](references/growth-loops.md) |
| gtm-motions | Inbound/outbound, PLG vs sales, marketing channels | [references/gtm-motions.md](references/gtm-motions.md) |
| gtm-strategy | GTM plan, launch strategy, launch roadmap | [references/gtm-strategy.md](references/gtm-strategy.md) |
| ideal-customer-profile | ICP, target customer, PMF survey synthesis | [references/ideal-customer-profile.md](references/ideal-customer-profile.md) |

## Workflow

1. **Identify sub-skill**: From the user's request and trigger words, pick the matching sub-skill from the index.
2. **Read reference**: Load the corresponding `references/<name>.md` file and review its Instructions, Input Format, and Output.
3. **Follow instructions**: Substitute user-provided context for any placeholders; follow the framework; produce structured output (markdown, tables, templates as specified).

## Examples

### Example 1: GTM Strategy
- **Trigger**: "Create a go-to-market plan for our new B2B analytics product launching Q3."
- **Action**: Use gtm-strategy reference; gather research; define channels, messaging, metrics; build launch timeline.
- **Result**: GTM strategy document with channels, messaging, KPIs, and 90-day roadmap.

### Example 2: Ideal Customer Profile
- **Trigger**: "Define our ICP from this PMF survey data."
- **Action**: Use ideal-customer-profile reference; segment by value; profile demographics, behaviors, JTBD; document pain points.
- **Result**: Comprehensive ICP with firmographics, JTBD, disqualification criteria.

### Example 3: Competitive Battlecard
- **Trigger**: "We're up against Competitor X. Create a battlecard for sales."
- **Action**: Use competitive-battlecard reference; research competitor; create battlecard with comparison, objections, win/loss patterns.
- **Result**: Sales-ready battlecard with tables, objection handling, landmines to plant.

## Error Handling

| Situation | Action |
|-----------|--------|
| Ambiguous request (e.g. "GTM") | Ask: strategy, motions, launch plan, or ICP? Suggest gtm-strategy or gtm-motions. |
| Multiple sub-skills implied | Start with highest-impact (e.g. gtm-strategy before gtm-motions). |
| Missing context (product, market, competitor) | Request: product description, target segment, competitor name, or research data. |
| Request out of scope (content creation, outreach drafting) | Redirect: kwp-marketing-content-creation or kwp-sales-draft-outreach. |
