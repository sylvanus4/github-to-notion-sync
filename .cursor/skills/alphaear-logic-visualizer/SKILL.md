---
name: alphaear-logic-visualizer
description: >-
  Creates Draw.io XML diagrams to visualize financial logic chains and
  transmission flows. Use when explaining investment theses, signal transmission
  chains, or complex finance logic flows as diagrams. Do NOT use for general
  architecture diagrams or system design visuals (use visual-explainer). Do NOT
  use for slide decks or data tables (use visual-explainer). Korean triggers:
  "생성", "설계", "슬라이드", "데이터".
metadata:
  version: "1.0.0"
  category: "visualization"
  author: "alphaear"
---
# AlphaEar Logic Visualizer

## Overview

Agentic workflow to generate Draw.io XML diagrams for financial logic flows. The agent: (1) uses the **Draw.io XML Generation** prompt from `references/PROMPTS.md` to produce valid mxGraphModel XML; (2) calls `scripts/visualizer.py` method `VisualizerTools.render_drawio_to_html(xml_content, filename)` to render an HTML file viewable in a browser. Can also use the project's `visual-explainer` skill for HTML canvas as an alternative.

## Prerequisites

- Python 3.10+
- Standard library only (no heavy deps)
- `scripts/visualizer.py` — `VisualizerTools.render_drawio_to_html`
- `references/PROMPTS.md` — Draw.io XML prompt and template

## Workflow

1. **Gather logic**: Obtain nodes/edges description (e.g., from `InvestmentSignal.transmission_chain` or user-provided flow).
2. **Generate XML**: Use **Draw.io XML Generation** prompt from `references/PROMPTS.md` — input `title` and `nodes_json`; output valid `<mxGraphModel>...</mxGraphModel>` XML.
3. **Render to HTML**: Call `VisualizerTools.render_drawio_to_html(xml_content, filename, title)` from `scripts/visualizer.py`. Creates an HTML file with embedded diagrams.net viewer.
4. **Return path**: Output path for user to open in browser.

## Examples

| Trigger | Action | Result |
|---------|--------|--------|
| "Visualize this signal chain" | Prompt → XML → `render_drawio_to_html` | `chain_visual.html` |
| "Draw the transmission flow" | Build nodes from logic → prompt → render | HTML file |
| "Diagram for investment thesis" | Parse thesis → XML prompt → render | Viewable HTML |

## Error Handling

| Error | Behavior | Recovery |
|-------|----------|----------|
| Invalid XML | Viewer may not load | Ensure output starts with `<mxGraphModel>` and ends with `</mxGraphModel>` |
| Missing script | ImportError | Confirm `scripts/visualizer.py` exists in skill folder |
| Dir not writable | File write fails | Use temp dir or user-specified path |
| Overlapping nodes | Diagram cluttered | Prompt asks for layer-based layout (x=0,200,400; y=0,100,200) |

## Troubleshooting

- **XML not rendering**: Validate XML structure; diagrams.net viewer requires plain (non-compressed) XML.
- **Alternative output**: Use project's `visual-explainer` skill for HTML canvas rendering instead of Draw.io.
- **Color coding**: Prompt specifies Positive=green (#d5e8d4), Negative=red (#f8cecc), Neutral=grey (#f5f5f5).
