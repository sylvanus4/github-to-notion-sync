---
name: pm-marketing-growth
description: >-
  Orchestrate product marketing and growth workflows: marketing ideas,
  positioning, value proposition statements, North Star metrics, and product
  naming. Based on phuryn/pm-skills. Use when the user asks for "marketing
  ideas", "positioning", "value proposition statements", "North Star metric",
  "product name ideas", or "growth metrics". Do NOT use for marketing campaign
  planning (use kwp-marketing-campaign-planning), brand voice (use
  kwp-marketing-brand-voice), or GTM strategy (use pm-go-to-market). Korean triggers: "마케팅 아이디어", "포지셔닝", "가치 제안 문구",
  "North Star 메트릭", "제품 이름", "노스스타", "마케팅 캠페인", "브랜딩", "네이밍".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Marketing and Growth

Orchestrate product marketing and growth workflows using phuryn/pm-skills — marketing ideas, positioning, value proposition statements, North Star metrics, and product naming.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|--------------|-----------|
| marketing-ideas | Marketing campaigns, product promotion, creative tactics | [references/marketing-ideas.md](references/marketing-ideas.md) |
| north-star-metric | North Star Metric, metrics framework, OMTM, key metric | [references/north-star-metric.md](references/north-star-metric.md) |
| positioning-ideas | Product positioning, differentiation, brand positioning | [references/positioning-ideas.md](references/positioning-ideas.md) |
| product-name | Product naming, rebranding, name ideas | [references/product-name.md](references/product-name.md) |
| value-prop-statements | Marketing copy, sales messaging, onboarding copy | [references/value-prop-statements.md](references/value-prop-statements.md) |

## Workflow

1. **Identify sub-skill**: From the user's request and trigger words, pick the matching sub-skill from the index.
2. **Read reference**: Load the corresponding `references/<name>.md` file and review its Instructions, Prompt, and Tips.
3. **Follow instructions**: Replace `$ARGUMENTS` in the reference with the user's context; follow the framework; produce structured output (tables, lists, or statements as specified).

## Examples

### Example 1: Marketing Ideas
- **Trigger**: "Give me 5 creative marketing ideas for our B2B SaaS product."
- **Action**: Use marketing-ideas reference; generate 5 ideas with channel, message, rationale, cost efficiency.
- **Result**: Table or list of 5 ideas with channel, core message, why it works, and cost-efficiency notes.

### Example 2: North Star Metric
- **Trigger**: "Help us define our North Star Metric for our marketplace."
- **Action**: Use north-star-metric reference; classify business game; validate NSM against 7 criteria; define 3–5 input metrics.
- **Result**: Business game classification, North Star Metric, input metrics constellation, and brief rationale.

### Example 3: Product Name
- **Trigger**: "We need product name ideas for our AI writing assistant."
- **Action**: Use product-name reference; suggest 5 names with rationale, brand fit, memorability, domain/trademark notes.
- **Result**: 5 name candidates with rationale and fit assessment.

## Error Handling

| Situation | Action |
|-----------|--------|
| Ambiguous request (e.g. "marketing") | Ask: ideas, positioning, metrics, naming, or value props? Suggest marketing-ideas or positioning-ideas. |
| Multiple sub-skills implied | Start with the highest-impact (e.g. positioning before marketing-ideas). |
| Missing context (product, audience) | Request: product description, target segment, existing value props or positioning. |
| Request out of scope (full campaign plan, brand guidelines) | Redirect: kwp-marketing-campaign-planning or kwp-marketing-brand-voice. |
