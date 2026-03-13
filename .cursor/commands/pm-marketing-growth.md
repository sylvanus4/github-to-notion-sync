---
description: PM marketing and growth workflows — marketing ideas, positioning, value proposition statements, North Star metrics, product naming
argument-hint: "<product or marketing challenge>"
---

## PM Marketing and Growth

Product marketing and growth workflows: marketing ideas, positioning, value proposition statements, North Star metrics, and product naming.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| marketing-ideas | `ideas` | Generate 5 marketing ideas with channels and rationale |
| positioning-ideas | `positioning` | Positioning ideas differentiated from competitors |
| value-prop-statements | `valueprop` | Value proposition statements for marketing, sales, onboarding |
| north-star-metric | `northstar` | Define North Star metric and 3-5 input metrics |
| product-name | `name` | Generate 5 product name options with rationale |

### Execution

Read and follow the `pm-marketing-growth` skill (`.cursor/skills/pm-marketing-growth/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Generate marketing ideas
/pm-marketing-growth ideas -- 5 creative marketing ideas for our B2B SaaS

# Define positioning
/pm-marketing-growth positioning -- differentiate our product from top 3 competitors

# North Star metric
/pm-marketing-growth northstar -- define NSM for our marketplace platform

# Product naming
/pm-marketing-growth name -- name ideas for our AI writing assistant

# Value prop statements
/pm-marketing-growth valueprop -- marketing and sales copy for our analytics tool
```
