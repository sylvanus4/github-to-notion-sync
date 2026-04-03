---
description: "Generate formatted outputs from a KB — slides, charts, reports, diagrams"
---

# KB Output

## Skill Reference

Read and follow the skill at `.cursor/skills/knowledge-base/kb-output/SKILL.md`.

## Your Task

User input: $ARGUMENTS

Generate a formatted output from a Knowledge Base. `$ARGUMENTS` should contain:

1. **Topic name** — the KB topic
2. **Output type** — slides, chart, report, diagram, explainer
3. **Subject** (optional) — specific focus within the KB

Examples:
- `transformer-architectures slides` — overview slide deck
- `ml-foundations report attention mechanisms` — focused research report
- `robotics chart timeline of key developments` — matplotlib timeline
- `diffusion-models diagram architecture comparison` — Mermaid diagram

If arguments are ambiguous, suggest the most appropriate output format.
