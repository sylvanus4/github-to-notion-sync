---
name: architecture-diagram
description: >-
  Create professional dark-themed architecture diagrams as standalone HTML files
  with inline SVG (Cocoon-AI-style self-contained HTML + semantic palette, merged
  with this repo's 12 layouts and Thaki stack context). Supports z-order arrow
  masking, 12 visual styles, and 12 layout patterns. ALWAYS invoke when the user
  wants a browser-openable architecture diagram as HTML/SVG (not Mermaid-only,
  not Python-generated raster). Use when the user asks to "create architecture
  diagram", "draw system architecture", "visualize layers", "architecture
  overview", "system design diagram", "SVG architecture", "dark-theme diagram",
  "microservice architecture", "HTML diagram", "inline SVG architecture",
  "아키텍처 다이어그램", "시스템 아키텍처", "다크 테마 다이어그램", "레이어
  다이어그램", or needs a visual map of components and relationships. Do NOT use
  for simple flowcharts (use flowchart skill). Do NOT use for data visualization
  charts (use infographic skill). Do NOT use for cloud provider deployment
  topology with vendor-specific icons (use deployment-diagram skill). Do NOT use
  for UML class or sequence diagrams (use class-diagram or the appropriate UML
  skill). Do NOT use for Python diagrams-as-code PNG/SVG generation (use
  diagrams-generator skill). Do NOT use for Mermaid-based visual explainers or
  diff reviews (use visual-explainer skill).
metadata:
  author: thaki
  version: 1.2.0
  category: diagrams
---

# Architecture Diagram Generator

## Role

You are a technical diagram specialist. Deliver one self-contained `.html` file
with inline SVG that matches this skill's dark theme, semantic colors, and
z-order rules. Prefer the simplest layout that fits the user's description.

**Workflow:** Identify components and relationships -> Choose layout from
`references/patterns.md` -> Copy `assets/template.html` -> Customize SVG ->
Save as standalone `.html` -> Run **Verification**.

Merge **Cocoon-AI-style** traits (standalone HTML, dark canvas, readable SVG)
with **this repository's** pattern catalog and optional **Thaki / ai-platform-strategy**
context (`--project-context` or **Project Context** section).

## Honest Reporting

When the prompt is ambiguous or missing deployment detail, state uncertainty
explicitly. Do not invent components, trust zones, data flows, or vendor choices
the user did not supply.

## Rationalization Detection

Before placing every box or arrow, ask whether it is grounded in the user text.
If you infer structure, label it in the diagram (for example `inferred` in the
sublabel) or ask the user to confirm before claiming **VERDICT: PASS**.

## Domain Memory

- Layout and style catalog: `references/patterns.md` (12 layouts, 12 styles).
- Stack defaults for this product: **Project Context** below; honor
  `--project-context` when the user passes it.

## Failure Modes Checklist

Scan before save: overlapping boxes without 40px vertical gap; arrows drawn
after component rects; legend inside a boundary group; missing opaque `#0f172a`
mask rect; semantic color mismatch for layer type; viewBox too small for content.

## Design System

### Color Palette

| Component Type | Fill (rgba) | Stroke |
|---|---|---|
| Frontend | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
| Backend | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| Database | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| Cloud / Infra | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| Security / Auth | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| Messaging / Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
| External / Generic | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

### Typography

JetBrains Mono via Google Fonts. Sizes: 12px component names, 9px sublabels, 8px annotations, 7px tiny labels.

### Background

Dark slate `#020617` with subtle SVG grid pattern (`#1e293b`, 40px spacing, 0.5px stroke).

### Component Box

Two-layer rect for arrow masking: opaque background (`#0f172a`) then semi-transparent styled rect on top. Rounded corners `rx="6"`, 1.5px stroke.

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#0f172a"/>
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1.5"/>
<text x="CX" y="Y+20" fill="white" font-size="11" font-weight="600" text-anchor="middle">LABEL</text>
<text x="CX" y="Y+36" fill="#94a3b8" font-size="9" text-anchor="middle">sublabel</text>
```

### Arrows and Connections

Define an SVG marker for arrowheads. Draw arrows **early** in the SVG (after background grid) so they render behind component boxes (SVG paints in document order).

```svg
<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
</marker>
```

Auth/security flows: dashed lines in rose (`#fb7185`). Message buses: orange rect connectors (`rx="4"`, height 20px).

### Boundary Groups

- **Security groups:** Dashed stroke (`stroke-dasharray="4,4"`), transparent fill, rose color.
- **Region/cluster boundaries:** Larger dashed stroke (`stroke-dasharray="8,4"`), amber color, `rx="12"`.

## Constraints

**Freedom level: Medium** -- structured output format (HTML+SVG), but flexible component arrangement and labeling.

1. **Self-contained output** -- single `.html` file with embedded CSS and inline SVG. No external stylesheets except Google Fonts. No JavaScript.
2. **Arrow z-order masking** -- draw connection arrows before component boxes in SVG. Use opaque background rect (`#0f172a`) under each component to fully mask arrows behind semi-transparent fills.
3. **Spacing discipline** -- standard component height 60px, minimum vertical gap 40px. Place inline connectors (message buses) centered in gaps, never overlapping adjacent components.
4. **Legend outside boundaries** -- legends must be placed at least 20px below the lowest boundary box. Expand SVG viewBox height as needed.
5. **Incremental creation** -- build step by step: SVG frame and defs -> boundary groups -> arrows -> component boxes -> labels -> legend.
6. **No empty lines in HTML** -- keep the entire HTML block continuous to prevent Markdown parsing errors.

## Output Discipline

- Do not add components, layers, or connections the user did not request
- Do not add decorative SVG elements (gradients, shadows, animations) beyond the design system
- Match diagram complexity to the described architecture -- a 3-component system does not need 20 boxes
- Try the simplest layout first; escalate to complex patterns only when the architecture demands it

## Gotcha Catalog

| Bug | Cause | Fix |
|---|---|---|
| Arrows visible through components | Missing opaque background rect | Add `fill="#0f172a"` rect before styled rect |
| Component overlap | Vertical gap < 40px | Recalculate Y positions with minimum spacing |
| Legend inside cluster boundary | Legend Y < boundary bottom | Move legend below all boundaries, expand viewBox |
| Bus connector overlaps component | Bus placed at boundary instead of gap center | Center bus in the gap between components |
| Font not rendering | Missing Google Fonts link | Add JetBrains Mono `<link>` in `<head>` |

## Project Context

When diagramming this project's architecture, use these domain terms:

- **Frontend:** React 19, Vite, TDS (@thakicloud/shared)
- **Backend:** Go/Fiber microservices, NATS messaging
- **Auth:** Keycloak SSO, RBAC
- **Data:** PostgreSQL, Redis
- **Infra:** K8s (multi-cluster: control-plane + worker), ArgoCD, Kueue (GPU scheduling), Helm
- **AI/ML:** vLLM inference, fine-tuning pipelines

## Layout Patterns & Visual Styles

Read `references/patterns.md` for the full catalog: 12 visual styles (Steel Blue through Slate Dark), 12 layout patterns (three-column, pipeline, dashboard, nested containers, etc.), CSS class reference, and SVG-specific layout examples.

## Template

Copy and customize the base template at `assets/template.html`. Key customization points:

1. Update `<title>` and header text
2. Modify SVG viewBox dimensions (default: `1100 x 700`)
3. Add/remove/reposition component boxes using the color palette
4. Draw connection arrows between components (before component rects)
5. Update the three summary cards
6. Update footer metadata

## Output

Save the generated `.html` file. The file must:
- Render correctly when opened directly in any modern browser
- Contain no external dependencies except Google Fonts CDN
- Use the dark theme design system defined above
- Include a header, SVG diagram, summary cards, and footer

## Verification

Before declaring the diagram complete, check each item and report the result:

1. Confirm all arrows are drawn before component rects in SVG order
2. Verify minimum 40px vertical gap between all adjacent components
3. Check legend position is outside all boundary groups
4. Validate all component colors match the semantic palette
5. Open the file in a browser to visually verify rendering (or state if browser
   access is unavailable and rely on 1-4 plus checklist)
6. For org-wide, security-boundary, or customer-facing diagrams: confirm with the
   user that inferred zones and trust boundaries are acceptable before **PASS**
7. If any element is not directly supported by the user prompt, it is labeled
   `inferred` or removed

**VERDICT: PASS** if checks 1-5 and 7 pass, and check 6 is satisfied when it
applies. **VERDICT: FAIL — [item numbers]** otherwise.
