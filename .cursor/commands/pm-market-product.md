---
description: Creative marketing toolkit — campaign ideas, positioning, value prop statements, product naming. Modular: run all or select modules.
argument-hint: "<product description> | [ideas|positioning|valueprop|name|all]"
---

# PM Market Product

Creative marketing toolkit: campaign ideas, positioning, value proposition statements, and product naming. References pm-marketing-growth skill with marketing-ideas, positioning-ideas, value-prop-statements, product-name sub-skills. Modular — run all or select specific modules.

## Usage

```
/pm-market-product 5 marketing ideas for our B2B analytics SaaS
/pm-market-product 우리 AI 쓰기 도구 — 포지셔닝, 밸류프롭, 제품 이름 아이디어
```

## Workflow

### Step 1: Load skill and references

Read the `pm-marketing-growth` skill (`.cursor/skills/pm-marketing-growth/SKILL.md`) and references:

- `references/marketing-ideas.md`
- `references/positioning-ideas.md`
- `references/value-prop-statements.md`
- `references/product-name.md`

### Step 2: Parse scope

Determine which modules to run from user input:

- `ideas` — Marketing campaign ideas
- `positioning` — Positioning ideas
- `valueprop` — Value proposition statements
- `name` — Product name ideas
- `all` or unspecified — Run all modules

### Step 3: Execute selected modules

For each selected module:

- **marketing-ideas**: 5 ideas with channel, core message, rationale, cost-efficiency
- **positioning-ideas**: 3–5 positioning angles vs competitors
- **value-prop-statements**: 3–5 statements for marketing, sales, onboarding
- **product-name**: 5 name candidates with rationale, brand fit, memorability

### Step 4: Output

Deliver structured markdown per module with tables or bullet lists. If `all`, organize as sections: Ideas, Positioning, Value Props, Naming.

### Step 5: Optional iteration

Offer to iterate on any module (e.g., "more ideas," "different tone").

## Notes

- Request product description and target audience if missing.
- Value props should be benefit-led, not feature-led.
- For naming, check domain/trademark availability separately.
