---
name: alphaear-logic-visualizer
description: >-
  Creates Draw.io XML diagrams to visualize financial logic chains and
  transmission flows. Use when explaining investment theses, signal transmission
  chains, or complex finance logic flows as diagrams. Do NOT use for general
  architecture diagrams or system design visuals (use visual-explainer). Do NOT
  use for slide decks or data tables (use visual-explainer). Do NOT use for
  written financial reports (use alphaear-reporter). Korean triggers:
  "논리 흐름", "전달 체인", "Draw.io", "투자 다이어그램".
metadata:
  version: "1.1.0"
  last_updated: "2026-03-27"
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

## AlphaEar Quality Standards (auto-improved)

### Intent → sub-skill routing

| User query pattern | This skill vs other |
|--------------------|---------------------|
| Draw.io / diagrams.net XML for finance logic or transmission chain | **This skill** |
| General architecture / slide charts | `visual-explainer` |
| Full narrative report | `alphaear-reporter` |

### Data source attribution (required)

In the diagram legend or companion note, state node data origins when applicable: `(노드 근거: InvestmentSignal.transmission_chain)`, `(근거: 사용자 서술)`, `(근거: alphaear-search 요약)` — so viewers know provenance.

### Korean output

Node labels may be Korean or bilingual; accompanying user message in natural Korean explaining the 다이어그램.

### Fallback protocol

Invalid XML / viewer fail → `Draw.io XML 검증 실패 — 재생성` or `visual-explainer HTML 대안 사용` 명시. Unwritable path → 임시 디렉터리 사용 및 경로 안내.
