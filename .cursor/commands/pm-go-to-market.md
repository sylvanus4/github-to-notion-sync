---
description: PM go-to-market workflows — GTM strategy, ICP, beachhead segments, growth loops, battlecards
argument-hint: "<product or market to target>"
---

## PM Go-to-Market

Go-to-market workflows: GTM strategy, ideal customer profiles, beachhead segments, growth loops, GTM motions, and competitive battlecards.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| gtm-strategy | `gtm` | Full GTM strategy: channels, messaging, KPIs, launch plan |
| ideal-customer-profile | `icp` | Define ICP from demographics, behavior, JTBD |
| beachhead-segment | `beachhead` | Define first market segment for market entry |
| growth-loops | `loops` | Design growth loops and flywheels |
| gtm-motions | `motions` | Assess GTM motions (PLG, sales-led, inbound, outbound, etc.) |
| competitive-battlecard | `battlecard` | Sales-ready battlecard with objection handling |

### Execution

Read and follow the `pm-go-to-market` skill (`.cursor/skills/pm-go-to-market/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Build GTM strategy
/pm-go-to-market gtm -- launch plan for our B2B analytics product in Q3

# Define ICP
/pm-go-to-market icp -- ideal customer profile from our PMF survey data

# Create battlecard
/pm-go-to-market battlecard -- competitive battlecard vs Competitor X for sales team

# Design growth loops
/pm-go-to-market loops -- growth flywheels for our marketplace

# Evaluate GTM motions
/pm-go-to-market motions -- should we go PLG or sales-led?
```
