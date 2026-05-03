---
name: marketing-sales-playbook
description: >-
  Value-based pricing framework — pre-call briefings with competitive
  intelligence, tier-based pricing package design, sales call scoring, and
  pattern library for pricing strategy evolution.
disable-model-invocation: true
---

# Marketing Sales Playbook

Value-based pricing framework for scaling from $10K/mo to $40-100K/mo engagements. Includes pre-call briefings, tier package design, call analysis scoring, and a self-learning pattern library.

## Triggers

Use when the user asks to:
- "value pricing", "sales playbook", "pricing framework", "call analyzer"
- "pricing briefing", "tier packaging", "value-based selling"
- "가치 기반 가격", "세일즈 플레이북", "가격 프레임워크"

## Do NOT Use

- For sales call preparation and context → use `kwp-sales-call-prep`
- For competitive battlecards → use `kwp-sales-competitive-intelligence`
- For account research → use `kwp-sales-account-research`
- For compensation benchmarking → use `kwp-human-resources-compensation-benchmarking`

## Prerequisites

- Python 3.10+
- `pip install requests anthropic`
- Optional: `AHREFS_API_KEY`, `SEMRUSH_API_KEY`, `ANTHROPIC_API_KEY`

## Execution Steps

### Step 1: Value Pricing Briefing
Run `scripts/value_pricing_briefing.py --domain <client_domain> --competitors <comp1,comp2>` to generate pre-call competitive intelligence and value opportunity analysis.

### Step 2: Tier Package Design
Run `scripts/value_pricing_packager.py --target-monthly <amount> --services <svc1,svc2>` to design value-based pricing tiers.

### Step 3: Call Analysis
Run `scripts/call_analyzer.py --transcript <file>` to score sales calls on value articulation, objection handling, and close techniques.

### Step 4: Pattern Library
Run `scripts/pricing_pattern_library.py --list` to browse winning patterns. Use `--add` to register new patterns from successful deals.

## Examples

### Example 1: Prepare for a sales call

User: "Create a pre-call briefing for meeting with acme.com"

1. Run `scripts/value_pricing_briefing.py --domain acme.com --competitors competitor1.com,competitor2.com`

Result: Competitive intelligence brief with value positioning opportunities and price anchoring strategy.

### Example 2: Design pricing tiers

User: "Design a 3-tier pricing package targeting $50K/mo"

1. Run `scripts/value_pricing_packager.py --target-monthly 50000 --services "seo,content,paid"`

Result: Value-based tier structure with ROI justification for each level.

## Error Handling

| Error | Action |
|-------|--------|
| Domain data unavailable | Falls back to manual competitive research prompts |
| No Ahrefs/SEMrush API key | Competitive data is limited; use web search as alternative |
| Transcript parse error | Verify file encoding (UTF-8 expected) |
| Pattern library empty | Start with `--add` to seed initial patterns from historical deals |

## Output

- Pre-call briefing document
- Tiered pricing proposal
- Call score card with improvement suggestions
- Pattern library with win/loss correlation
