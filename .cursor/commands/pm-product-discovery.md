## PM Product Discovery

Product discovery workflows: ideation, assumption testing, OST, customer interviews, feature prioritization, and experiment design. Based on Teresa Torres and Marty Cagan frameworks.

### Usage

```
<sub-skill> [context]
```

### Sub-Skills

| Sub-Skill | Shorthand | What it does |
|-----------|-----------|--------------|
| analyze-feature-requests | `triage` | Analyze and prioritize customer feature requests |
| brainstorm-ideas-existing | `ideas-existing` | Ideation for existing products (PM/Designer/Engineer views) |
| brainstorm-ideas-new | `ideas-new` | Ideation for new products in early discovery |
| brainstorm-experiments-existing | `experiments-existing` | Design experiments for existing product assumptions |
| brainstorm-experiments-new | `experiments-new` | Design pretotypes/experiments for new products |
| identify-assumptions-existing | `assumptions-existing` | Identify risky assumptions (Value/Usability/Viability/Feasibility) |
| identify-assumptions-new | `assumptions-new` | Map assumptions across 8 risk areas for new products |
| prioritize-assumptions | `prioritize` | Impact x Risk matrix for assumption triage |
| prioritize-features | `rank` | Rank feature backlog by impact, effort, risk |
| interview-script | `interview` | Create JTBD + Mom Test interview scripts |
| summarize-interview | `summarize` | Summarize interview transcripts into JTBD insights |
| opportunity-solution-tree | `ost` | Build Opportunity Solution Trees (Teresa Torres) |
| metrics-dashboard | `metrics` | Design product metrics dashboards |

### Execution

Read and follow the `pm-product-discovery` skill (`.cursor/skills/pm-product-discovery/SKILL.md`) for the full workflow, sub-skill selection, and error handling.

### Examples

```bash
# Full discovery flow
/pm-product-discovery ost -- build an OST for our checkout conversion problem

# Brainstorm ideas for existing product
/pm-product-discovery ideas-existing -- feature ideas for our SaaS dashboard

# Identify and prioritize assumptions
/pm-product-discovery assumptions-new -- map risks for our new marketplace MVP

# Create interview script
/pm-product-discovery interview -- JTBD interview for B2B onboarding

# Triage feature requests
/pm-product-discovery triage -- prioritize these 20 customer requests
```
