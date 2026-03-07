---
description: "Create Draw.io XML diagrams to visualize financial logic chains and transmission flows"
---

# AlphaEar Logic Visualizer

## Skill Reference

Read and follow the skill at `.cursor/skills/alphaear-logic-visualizer/SKILL.md`.

## Your Task

User input: $ARGUMENTS

### Step 1: Parse Request

- If `$ARGUMENTS` contains a logic flow description, use it as input nodes
- If `$ARGUMENTS` contains a signal or thesis reference, extract the transmission chain
- If `$ARGUMENTS` mentions "html" or "canvas", consider using `visual-explainer` as alternative
- If `$ARGUMENTS` is empty, ask user for the logic flow to visualize

### Step 2: Execute

Follow the workflow in the skill:

1. Parse the logic description into nodes and edges
2. Generate Draw.io XML using the prompt from `references/PROMPTS.md`
3. Render to HTML via `VisualizerTools.render_drawio_to_html`

### Step 3: Report

Present results with:
- Path to generated HTML file
- Description of the diagram structure (nodes and connections)
- Instructions to open in browser
