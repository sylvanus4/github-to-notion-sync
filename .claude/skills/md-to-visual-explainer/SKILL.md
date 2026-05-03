---
name: md-to-visual-explainer
description: >-
  Transform complex markdown documents (architecture reviews, technical specs,
  analysis reports, PRDs) into self-contained visual HTML explainer pages with
  Mermaid diagrams, before/after comparisons, evidence sections, severity
  badges, and ELI5 (elementary school version) explanations for each item. Use
  when the user asks to "make this document visual", "explain visually",
  "시각적으로 설명", "이해하기 쉽게 HTML로", "초등학생 버전", "visual explainer", "쉽게 풀어서", "그림으로
  설명", "다이어그램으로 설명", "문서 시각화", "리뷰 시각화", "md-to-visual-explainer", or wants a
  markdown document transformed into an interactive visual page for
  comprehension and review. Do NOT use for generating diagrams from scratch
  without a source document (use visual-explainer). Do NOT use for simple
  markdown-to-HTML conversion without visual enhancement. Do NOT use for slide
  deck generation (use nlm-slides or anthropic-pptx). Korean triggers: "시각적
  설명", "문서 시각화", "쉽게 이해", "초등학생 버전", "그림으로".
---

# Markdown to Visual Explainer

Transform a markdown document into a self-contained HTML page that makes every item **visually comprehensible** through diagrams, comparisons, evidence, and ELI5 explanations.

## When to Use

| Input | Output |
|---|---|
| Architecture review markdown | Visual HTML with flow diagrams, gap checklist |
| Technical spec / RFC | HTML with component diagrams, dependency flows |
| Analysis report | HTML with comparison panels, evidence cards |
| PRD / planning doc | HTML with state diagrams, coverage matrix |

## vs. visual-explainer

`visual-explainer` generates diagrams from a **topic or concept**. This skill transforms an **existing markdown document** into a comprehension-optimized HTML page, preserving all items and adding visual layers.

## Workflow

### 1. Analyze Source Document

Read the input markdown and extract:

- **Document type**: review, spec, analysis, plan, etc.
- **Items list**: numbered issues, sections, or key points
- **Severity/priority**: if present (critical/high/moderate/low)
- **Relationships**: dependencies, flows, before/after states
- **Technical concepts**: that benefit from diagrams

### 2. Plan Visual Elements

For each item, decide what visual treatment it needs:

| Item characteristic | Visual treatment |
|---|---|
| Architecture conflict | Mermaid flowchart: current vs proposed |
| Missing component | Mermaid graph showing the gap |
| Process/flow issue | Mermaid sequence or flowchart diagram |
| Comparison (before/after) | Side-by-side comparison panels |
| Data/metrics | Stat cards or summary badges |
| Policy/principle conflict | Comparison panel with conflict highlight |
| Complex concept | ELI5 box with analogy |

**Every item gets**: problem card + diagram + evidence box + ELI5 box.

**Winston Visual-First Rules** (apply ONLY when the user explicitly states the output will be presented live — do NOT apply to analysis documents, review reports, or reference material):
- **Minimal text per card**: problem cards ≤ 40 words visible; move detail into collapsible evidence sections
- **Storytelling structure**: order items as observation → hypothesis → test → learning where applicable, not just severity ranking
- **Near Miss panels**: when explaining a concept, add an "A but not B" comparison panel to sharpen understanding

**For analysis documents** (the default use case): maximize information density. Problem cards should contain full explanations, evidence should be inline (not collapsed), and all technical detail should be visible without extra clicks.

### 3. Generate HTML

Produce a single self-contained HTML file with this structure:

```
Hero Section (title, subtitle, source document)
├── Verdict Banner (overall assessment + score)
├── Stats Row (issue counts by severity)
├── Table of Contents (linked, color-coded)
├── Item Sections (one per item)
│   ├── Section Header (severity badge + title)
│   ├── Problem Card (what's the issue)
│   ├── Comparison Panel (before/after or current/proposed)
│   ├── Diagram (Mermaid flowchart/sequence/graph)
│   ├── Evidence Box (code refs, doc quotes, data)
│   └── ELI5 Box (elementary school version analogy)
├── Positive Items Section (if present)
└── Final Checklist (action items summary)
```

### 4. Styling Specification

Use this CSS design system for consistency:

**Color tokens** (dark theme primary):

```
--bg: #0f1117          (page background)
--surface: #1a1d27     (card background)
--surface2: #242836    (diagram/code background)
--border: #2e3345      (borders)
--text: #e1e4ed        (primary text)
--muted: #8b90a0       (secondary text)
--accent: #6c8cff      (links, highlights)
--critical: #ff6b6b    (critical severity)
--high: #ffa94d        (high severity)
--moderate: #ffd43b    (moderate severity)
--positive: #51cf66    (positive/good items)
--info: #74c0fc        (informational)
```

**Font stack**: `'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` for body; `'JetBrains Mono', 'Fira Code', monospace` for code.

**Key components**:

- `.hero` — gradient background, centered title/subtitle
- `.verdict-banner` — accent-tinted border, large score display
- `.stats-row` — 4-column grid of severity count cards
- `.toc` — 2-column grid of linked items with color dots
- `.card` — rounded surface card for each item's content
- `.comparison` — 2-column grid: `.side.before` + `.side.after`
- `.diagram-wrapper` — surface2 background, full-width Mermaid, cursor: zoom-in, "🔍 클릭하여 확대" hint
- `.evidence` — accent-tinted box with label badge, code styling
- `.eli5` — green-tinted box with "초등학생 버전" label
- `.gap-item` — icon + content flex row for checklist items

### 5. Mermaid Diagrams

Include both Mermaid and svg-pan-zoom CDN scripts:

```html
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
```

Initialize Mermaid with **red arrows** for high visibility on dark backgrounds:

```javascript
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#2a3050',
    primaryTextColor: '#e1e4ed',
    primaryBorderColor: '#4a5580',
    lineColor: '#ff4757',       // RED arrows for visibility
    secondaryColor: '#1a2040',
    tertiaryColor: '#242836',
    fontSize: '16px'            // larger text for readability
  },
  flowchart: { curve: 'basis', padding: 20 },
  securityLevel: 'loose'
});
```

For each item, generate the appropriate Mermaid diagram type:
- `flowchart TD` for architecture and component flows
- `sequenceDiagram` for request/response flows
- `graph TD` for dependency graphs
- `flowchart LR` only for simple 3-4 node linear flows

#### Diagram Sizing

Diagrams MUST render large and readable by default:

- `.diagram-wrapper` uses `width: 100%` with NO max-width constraint
- `.mermaid svg` set to `width: 100%; min-height: 400px`
- DO NOT center-shrink diagrams — let them fill the container width
- Mermaid fontSize is `16px` (not 14px) for readability

#### Click-to-Zoom Fullscreen Lightbox

Every diagram gets click-to-expand capability:

1. Add a `cursor: zoom-in` and a "🔍 클릭하여 확대" hint label on each `.diagram-wrapper`
2. On click, clone the SVG into a fullscreen overlay (`position: fixed; inset: 0; z-index: 9999`)
3. Inside the overlay, initialize `svgPanZoom()` on the cloned SVG for mouse-wheel zoom + drag pan
4. Close with: ESC key, click on backdrop, or X button in top-right corner
5. Overlay background: `rgba(0,0,0,0.92)` for contrast

Implementation template:

```javascript
document.querySelectorAll('.diagram-wrapper').forEach(wrapper => {
  wrapper.style.cursor = 'zoom-in';
  wrapper.addEventListener('click', () => {
    const svg = wrapper.querySelector('svg');
    if (!svg) return;
    const overlay = document.createElement('div');
    overlay.className = 'diagram-overlay';
    const clone = svg.cloneNode(true);
    clone.style.width = '90vw';
    clone.style.height = '85vh';
    clone.style.maxWidth = 'none';
    overlay.innerHTML = '<button class="overlay-close">&times;</button>';
    overlay.appendChild(clone);
    document.body.appendChild(overlay);
    const pz = svgPanZoom(clone, {
      zoomEnabled: true, controlIconsEnabled: true,
      fit: true, center: true, minZoom: 0.5, maxZoom: 10
    });
    overlay.querySelector('.overlay-close').onclick = () => { overlay.remove(); };
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
    document.addEventListener('keydown', function handler(e) {
      if (e.key === 'Escape') { overlay.remove(); document.removeEventListener('keydown', handler); }
    });
  });
});
```

Required CSS for the overlay:

```css
.diagram-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,0.92);
  display: flex; align-items: center; justify-content: center;
}
.overlay-close {
  position: absolute; top: 20px; right: 20px;
  background: none; border: none; color: white;
  font-size: 2rem; cursor: pointer; z-index: 10000;
}
.diagram-hint {
  font-size: 0.75rem; color: var(--muted); text-align: right;
  margin-top: 8px; opacity: 0.7;
}

### 6. ELI5 Explanations

Every technical item gets an ELI5 ("Explain Like I'm 5" / 초등학생 버전) box. Rules:

- Use a real-world analogy (school, sports team, restaurant, etc.)
- Max 3 sentences
- No technical jargon
- End with the key takeaway in one line
- Style in a green-tinted card with "초등학생 버전" label

### 7. Output & Delivery

**Filename**: Place the HTML file next to the source markdown with `-visual` suffix:
- Input: `docs/review.md` → Output: `docs/review-visual.html`
- Input: `docs/architecture.md` → Output: `docs/architecture-visual.html`

If the source path is unclear, write to `~/.agent/diagrams/<descriptive-name>-visual.html`.

After writing, open in browser:
- macOS: `open <path>`
- Linux: `xdg-open <path>`

Report the file path to the user.

## Quality Checklist

Before delivering, verify:

- [ ] Every item from the source document is represented
- [ ] Each item has: problem card + diagram + evidence + ELI5
- [ ] Mermaid diagrams render without syntax errors
- [ ] Severity badges match the source document's classification
- [ ] Table of contents links to all sections
- [ ] Stats row counts match actual items
- [ ] ELI5 boxes use real-world analogies, no jargon
- [ ] File opens cleanly in browser with no console errors
- [ ] HTML is self-contained (no external assets except CDN)
- [ ] **Content completeness**: Source document tables MUST be reproduced in evidence boxes (not summarized away)
- [ ] **Skill coverage**: Skill names, descriptions, and usage prompts from the source MUST appear in the HTML
- [ ] **Usage guides**: If the source contains "usage guide", "how to use", or trigger examples, render as a dedicated card
- [ ] **No content omission**: Do NOT omit content to save space — use collapsible `<details>` sections if needed
- [ ] **Diagrams clickable**: Every Mermaid diagram has a zoom-in cursor and "🔍 클릭하여 확대" hint
- [ ] **Winston text density** (presentation mode only — skip for analysis docs): Problem cards ≤ 40 words of visible text; additional detail in collapsible evidence sections
- [ ] **Winston Near Miss** (presentation mode only — skip for analysis docs): Concept explanations include "A but not B" comparison where applicable

## Example

**User**: "이 리뷰 문서 시각적으로 설명해줘" (pointing to `10-v071-architecture-review.md`)

**Actions**:
1. Read the markdown — 13 review items (5 critical, 4 high, 4 moderate) + 4 positive evaluations
2. Generate HTML with hero, verdict (75/100), stats (5C 4H 4M 4P), TOC, 17 sections
3. Each section: problem definition, Mermaid architecture diagram, evidence box, ELI5
4. Final gap checklist with severity-coded action items
5. Write to `10-v071-architecture-review-visual.html`, open in browser

## Limitations

- Mermaid CDN required (not fully offline)
- Very large documents (50+ items) may produce slow-rendering HTML
- Diagrams are auto-generated approximations — complex custom layouts may need manual adjustment

## Composability

- **visual-explainer** — Generates diagrams from topics/concepts; this skill transforms existing markdown into visual HTML
- **winston-speaking-coach** — Run a full Winston coaching session before presenting the visual explainer live; applies Empowerment Promise, Circle & Star, and delivery technique

## Winston Framework Integration (Presentation Mode Only)

These rules apply ONLY when the user explicitly states the visual explainer will be used for live presentation or walkthroughs. **Do NOT apply to analysis documents, review reports, technical specs, or reference material** — those should maximize information density with full text, inline evidence, and complete technical detail.

| Winston Principle | Application (presentation only) |
|-------------------|-------------|
| **≤40 words per card** | Problem cards cap visible text; details move to collapsible evidence sections |
| **Near Miss panels** | Concept explanations include "A but not B" comparison panels |
| **Storytelling** | Items can be ordered as observation → hypothesis → test → learning, not just severity |
| **Image-centric** | Diagrams are the dominant visual element; text supports the diagram, not the other way around |

**Analysis document default**: Full explanations inline, evidence visible without collapsing, all technical detail preserved. Information density > visual minimalism.

For a full Winston coaching session on the visual explainer content, run `winston-speaking-coach` before presenting.
