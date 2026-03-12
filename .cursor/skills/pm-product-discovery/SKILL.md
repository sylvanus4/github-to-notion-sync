---
name: pm-product-discovery
description: >-
  Orchestrate product discovery workflows: ideation, assumption testing,
  Opportunity Solution Trees, customer interview synthesis, feature
  prioritization, and experiment design. Based on Teresa Torres and Marty Cagan
  frameworks (phuryn/pm-skills). Use when the user asks for "brainstorm ideas",
  "identify assumptions", "opportunity solution tree", "interview script",
  "prioritize features", "analyze feature requests", "brainstorm experiments",
  or "summarize interview". Do NOT use for general user research synthesis (use
  kwp-product-management-user-research-synthesis), marketing campaign planning
  (use kwp-marketing-campaign-planning), or product strategy/vision (use
  pm-product-strategy). Korean triggers: "테스트", "분석", "설계", "검색".
metadata:
  author: "thaki"
  version: "1.0.0"
  upstream: "https://github.com/phuryn/pm-skills"
  category: "product"
---
# PM Product Discovery

Orchestrate product discovery workflows from ideation through validation using Teresa Torres and Marty Cagan frameworks.

## Sub-Skill Index

| Sub-Skill | When to Use | Reference |
|-----------|-------------|-----------|
| analyze-feature-requests | Triage backlog, prioritize customer requests | [references/analyze-feature-requests.md](references/analyze-feature-requests.md) |
| brainstorm-experiments-existing | Validate assumptions for an existing product | [references/brainstorm-experiments-existing.md](references/brainstorm-experiments-existing.md) |
| brainstorm-experiments-new | Pretotypes, landing pages, new product validation | [references/brainstorm-experiments-new.md](references/brainstorm-experiments-new.md) |
| brainstorm-ideas-existing | Feature ideation for live product (Product Trio) | [references/brainstorm-ideas-existing.md](references/brainstorm-ideas-existing.md) |
| brainstorm-ideas-new | Initial discovery, startup feature ideas | [references/brainstorm-ideas-new.md](references/brainstorm-ideas-new.md) |
| identify-assumptions-existing | Stress-test feature, 4 risks (Value/Usability/Viability/Feasibility) | [references/identify-assumptions-existing.md](references/identify-assumptions-existing.md) |
| identify-assumptions-new | New product risk mapping, 8 risk categories | [references/identify-assumptions-new.md](references/identify-assumptions-new.md) |
| interview-script | Create JTBD + Mom Test interview guide | [references/interview-script.md](references/interview-script.md) |
| metrics-dashboard | Design metrics dashboard, KPIs, North Star | [references/metrics-dashboard.md](references/metrics-dashboard.md) |
| opportunity-solution-tree | OST: outcome → opportunities → solutions → experiments | [references/opportunity-solution-tree.md](references/opportunity-solution-tree.md) |
| prioritize-assumptions | Impact × Risk matrix, triage assumptions | [references/prioritize-assumptions.md](references/prioritize-assumptions.md) |
| prioritize-features | Rank backlog, top 5 features | [references/prioritize-features.md](references/prioritize-features.md) |
| summarize-interview | JTBD summary from transcript | [references/summarize-interview.md](references/summarize-interview.md) |

## Workflow

1. **Identify sub-skill from user intent** — Match the request to the Sub-Skill Index. New vs existing product matters: use `*-new` for startups/MVPs, `*-existing` for live products.
2. **Read the reference file** — Load the linked `.md` in `references/` and follow its Context, Domain Context, and Instructions.
3. **Execute and chain** — Follow the reference instructions. Chain sub-skills when needed (e.g., identify-assumptions → prioritize-assumptions → brainstorm-experiments).

## Examples

| Trigger | Action | Result |
|--------|--------|--------|
| "Brainstorm solutions for our checkout drop-off problem" | Use brainstorm-ideas-existing | 15 ideas from PM/Designer/Engineer, top 5 with assumptions |
| "We have 20 feature requests from customers, help us prioritize" | Use analyze-feature-requests | Themed groups, strategic alignment, top 3 with test plans |
| "Create an interview script for our SaaS onboarding" | Use interview-script | JTBD script + Mom Test rules + note-taking template |

## Error Handling

| Error | Action |
|-------|--------|
| User intent ambiguous (new vs existing product) | Ask: "Is this for a new product/MVP or an existing live product?" |
| Missing research data for OST | Ask for interviews, surveys, or analytics before building the tree |
| Assumptions list empty | Run identify-assumptions-* first, then prioritize-assumptions |
| Feature requests in unstructured format | Parse or ask user to provide CSV/spreadsheet; summarize into table first |
