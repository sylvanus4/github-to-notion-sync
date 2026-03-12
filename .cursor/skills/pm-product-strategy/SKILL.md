---
name: pm-product-strategy
description: >-
  Orchestrate product strategy workflows: vision, strategy canvas, value
  propositions, Lean Canvas, Business Model Canvas, SWOT, PESTLE, Ansoff Matrix,
  Porter's Five Forces, and monetization/pricing strategy. Based on
  phuryn/pm-skills frameworks. Use when the user asks for "product strategy",
  "product vision", "business model", "lean canvas", "SWOT analysis", "PESTLE",
  "Porter's Five Forces", "pricing strategy", "monetization", "value
  proposition", "Ansoff matrix", or "startup canvas". Do NOT use for product
  discovery/ideation (use pm-product-discovery), competitive analysis only (use
  kwp-product-management-competitive-analysis), or execution/PRD (use
  pm-execution). Korean triggers: "워크플로우", "스킬", "모델".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Product Strategy

Orchestrate product strategy workflows using phuryn/pm-skills frameworks — vision, strategy canvas, value propositions, Lean/Business Model/Startup Canvas, SWOT, PESTLE, Ansoff, Porter's Five Forces, monetization, and pricing.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|--------------|-----------|
| ansoff-matrix | Growth options, market expansion, strategic growth paths | [references/ansoff-matrix.md](references/ansoff-matrix.md) |
| business-model | Business model canvas, BMC, how value is created/captured | [references/business-model.md](references/business-model.md) |
| lean-canvas | Lean startup canvas, hypothesis testing, new venture | [references/lean-canvas.md](references/lean-canvas.md) |
| monetization-strategy | Revenue models, how to monetize, pricing exploration | [references/monetization-strategy.md](references/monetization-strategy.md) |
| pestle-analysis | Macro environment, external factors, market entry | [references/pestle-analysis.md](references/pestle-analysis.md) |
| porters-five-forces | Industry dynamics, competitive forces, market attractiveness | [references/porters-five-forces.md](references/porters-five-forces.md) |
| pricing-strategy | Setting prices, pricing models, WTP, price elasticity | [references/pricing-strategy.md](references/pricing-strategy.md) |
| product-strategy | Product strategy canvas, strategic plan, product direction | [references/product-strategy.md](references/product-strategy.md) |
| product-vision | Vision statement, inspiring direction, team alignment | [references/product-vision.md](references/product-vision.md) |
| startup-canvas | New product launch, startup concept, strategy + business model | [references/startup-canvas.md](references/startup-canvas.md) |
| swot-analysis | Strategic assessment, strengths/weaknesses/opportunities/threats | [references/swot-analysis.md](references/swot-analysis.md) |
| value-proposition | Value prop design, JTBD, why customers choose you | [references/value-proposition.md](references/value-proposition.md) |

## Workflow

1. **Identify sub-skill**: From the user’s request and trigger words, pick the matching sub-skill from the index.
2. **Read reference**: Load the corresponding `references/<name>.md` file and review its Instructions, Input Requirements, and Output Process.
3. **Follow instructions**: Replace `$ARGUMENTS` in the reference with the user’s context; follow the framework and output process; produce structured output (markdown, tables, or templates as specified).

## Examples

### Example 1: Product Vision
- **Trigger**: "Help me define a product vision for our B2B analytics platform."
- **Action**: Use product-vision reference; brainstorm 3–5 vision options; recommend one with rationale.
- **Result**: Inspiring, achievable, emotion-driven vision statement plus alignment notes.

### Example 2: Startup Canvas
- **Trigger**: "We're launching a new SaaS for SMBs. Need a startup canvas."
- **Action**: Use startup-canvas reference; complete Part 1 (Product Strategy) and Part 2 (Business Model); validate coherence.
- **Result**: 11-section Startup Canvas with hypothesis list and suggested experiments.

### Example 3: Pricing Strategy
- **Trigger**: "How should we price our API product? Compare freemium vs usage-based."
- **Action**: Use pricing-strategy reference; evaluate models; analyze competitive pricing; design tiers and experiments.
- **Result**: Pricing recommendation (model, tiers, value metric), assumptions, risks, and test plan.

## Error Handling

| Situation | Action |
|-----------|--------|
| Ambiguous request (e.g. "strategy") | Ask: vision, strategy, canvas, or analysis? Suggest product-strategy or product-vision. |
| Multiple sub-skills implied | Start with the highest-impact (e.g. product-strategy before value-proposition). |
| Missing context (product, market) | Request: product description, target segment, competitive context. |
| Request out of scope (competitive analysis only, PRD) | Redirect: kwp-product-management-competitive-analysis or pm-execution. |
