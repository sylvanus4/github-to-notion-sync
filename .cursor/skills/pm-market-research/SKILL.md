---
name: pm-market-research
description: >-
  Orchestrate market research workflows: user personas, market segmentation,
  customer journey mapping, competitive analysis, sentiment analysis, and
  market sizing (TAM/SAM/SOM). Based on phuryn/pm-skills. Use when the user
  asks for "user persona", "market segmentation", "customer journey map",
  "competitor analysis", "sentiment analysis", "market sizing", "TAM SAM SOM",
  or "user segmentation". Do NOT use for product discovery ideation (use
  pm-product-discovery), marketing campaigns (use kwp-marketing-campaign-planning),
  or sales competitive intelligence (use kwp-sales-competitive-intelligence).
metadata:
  author: thaki
  version: 1.0.0
  upstream: https://github.com/phuryn/pm-skills
---

# PM Market Research

Orchestrates product-market research workflows using seven sub-skills. Routes user requests to the appropriate reference, applies structured analysis steps, and delivers research-backed outputs for personas, segments, journeys, competitors, sentiment, and market sizing.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| user-personas | Build personas from survey/interview data; 3 personas with JTBD, pains, gains | `references/user-personas.md` |
| user-segmentation | Segment user base from feedback; 3+ behavioral/needs-based segments | `references/user-segmentation.md` |
| market-segments | Identify 3–5 customer segments with demographics, JTBD, product fit | `references/market-segments.md` |
| customer-journey-map | Map awareness→advocacy; touchpoints, emotions, pain points, opportunities | `references/customer-journey-map.md` |
| competitor-analysis | 5 direct competitors; strengths, weaknesses, differentiation opportunities | `references/competitor-analysis.md` |
| sentiment-analysis | Analyze feedback at scale; segments, sentiment scores, satisfaction insights | `references/sentiment-analysis.md` |
| market-sizing | TAM/SAM/SOM; top-down and bottom-up; growth projections | `references/market-sizing.md` |

## Workflow

1. **Route** — Match the user’s question to one (or more) sub-skills using the index above.
2. **Read** — Load the relevant reference(s) and follow the analysis steps (Input → Steps → Output).
3. **Execute** — Run the analysis (web search, file read, synthesis) and produce the structured output. Replace `{product}` with the user’s product/market/context.

## Examples

| Trigger | Sub-Skill | Outcome |
|---------|-----------|---------|
| "Create personas from these survey responses" | user-personas | 3 personas with JTBD, pains, gains, unexpected insight |
| "Map the customer journey for our SaaS onboarding" | customer-journey-map | Journey table by stage with touchpoints, emotions, pain points, opportunities |
| "Size the market for our AI writing tool in the US" | market-sizing | TAM/SAM/SOM with top-down, bottom-up, and assumption mapping |

## Error Handling

| Condition | Action |
|-----------|--------|
| Ambiguous target (no product/market named) | Ask user for product name or market segment before analysis |
| No user-provided data but skill expects it (personas, sentiment) | Use web search for public sources; state data source limitations |
| Conflicting sub-skill matches | Prefer the most specific (e.g., sentiment-analysis over user-segmentation for feedback sentiment) |
| Missing or empty reference file | Fall back to inline sub-skill instructions from this SKILL; log missing reference |
