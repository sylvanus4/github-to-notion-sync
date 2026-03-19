---
name: visual-explainer
description: >-
  Generate beautiful, self-contained HTML pages that visually explain systems,
  code changes, plans, and data. Use when the user asks for a diagram,
  architecture overview, diff review, plan review, project recap, comparison
  table, or any visual explanation. Also use proactively when about to render a
  complex ASCII table (4+ rows or 3+ columns). Do NOT use for simple text-only
  responses, static markdown formatting, or non-visual documentation. Korean
  triggers: "리뷰", "생성", "계획", "문서".
metadata:
  author: "nicobailon (ported by thaki)"
  version: "0.4.3"
  category: "execution"
---
# Visual Explainer

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## HARD-GATE (Diagram & Slide Generation)

When generating a new diagram, visual plan, or slide deck (not diff-review, project-recap, or fact-check), do NOT start generating until these are confirmed:

1. **Subject matter** — What system, concept, or data is being visualized?
2. **Target audience** — Developers? PMs? Executives? (determines information density)

If the user's request is vague (e.g., "make a diagram"), ASK what to visualize and for whom before proceeding. Do not guess the subject matter.

This gate does NOT apply to: diff-review, plan-review, project-recap, fact-check, or proactive table rendering (these have sufficient context from git/files).

## Input

The user provides one of the following:
1. **Topic or subject** — for `/generate-web-diagram`, `/generate-visual-plan`, `/generate-slides`
2. **Git ref or PR number** — for `/diff-review` (branch, commit hash, `HEAD`, `#42`, range)
3. **Plan file path** — for `/plan-review` (path to markdown plan/spec/RFC)
4. **Time window** — for `/project-recap` (`2w`, `30d`, `3m`, etc.)
5. **File path** — for `/fact-check` (path to document to verify, or defaults to latest HTML)

## Workflow

### 1. Think (5 seconds, not 5 minutes)

Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Visual is always default.** Even essays, blog posts, and articles get visual treatment — extract structure into cards, diagrams, grids, tables.

Prose patterns (lead paragraphs, pull quotes, callout boxes) are **accent elements** within visual pages, not a separate mode. Use them to highlight key points or provide breathing room, but the page structure remains visual.

For prose accents, see "Prose Page Elements" in `./references/css-patterns.md`. For everything else, use the standard freeform approach with aesthetic directions below.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of content?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, data table, timeline, dashboard, or prose-first page. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**What aesthetic?** Pick one and commit. The constrained aesthetics (Blueprint, Editorial, Paper/ink) are safer — they have specific requirements that prevent generic output. The flexible ones (IDE-inspired) require more discipline.

**Constrained aesthetics (prefer these):**
- Blueprint (technical drawing feel, subtle grid background, deep slate/blue palette, monospace labels, precise borders)
- Editorial (serif headlines like Instrument Serif or Crimson Pro, generous whitespace, muted earth tones or deep navy + gold)
- Paper/ink (warm cream `#faf7f5` background, terracotta/sage accents, informal feel)
- Monochrome terminal (green/amber on near-black, monospace everything, CRT glow optional)

**Flexible aesthetics (use with caution):**
- IDE-inspired (borrow a real, named color scheme: Dracula, Nord, Catppuccin Mocha/Latte, Solarized Dark/Light, Gruvbox, One Dark, Rosé Pine) — commit to the actual palette, don't approximate
- Data-dense (small type, tight spacing, maximum information, muted colors)

**Explicitly forbidden:**
- Neon dashboard (cyan + magenta + purple on dark) — always produces AI slop
- Gradient mesh (pink/purple/cyan blobs) — too generic
- Any combination of Inter font + violet/indigo accents + gradient text

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 2. Structure

**Read the reference material** before generating. Don't memorize it — read it each time to absorb the patterns.
- For text-heavy architecture overviews (card content matters more than topology): read `./templates/architecture.html`
- For flowcharts, sequence diagrams, ER, state machines, mind maps: read `./templates/mermaid-flowchart.html`
- For data tables, comparisons, audits, feature matrices: read `./templates/data-table.html`
- For slide deck presentations (when `--slides` flag is present or `/generate-slides` is invoked): read `./templates/slide-deck.html` and `./references/slide-patterns.md`
- For prose-heavy publishable pages (READMEs, articles, blog posts, essays): read the "Prose Page Elements" section in `./references/css-patterns.md` and "Typography by Content Voice" in `./references/libraries.md`

**For CSS/layout patterns and SVG connectors**, read `./references/css-patterns.md`.

**For pages with 4+ sections** (reviews, recaps, dashboards), also read `./references/responsive-nav.md` for section navigation with sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

| Content type | Approach | Why |
|---|---|---|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control |
| Architecture (topology-focused) | **Mermaid** | Visible connections between components need automatic edge routing |
| Flowchart / pipeline | **Mermaid** | Automatic node positioning and edge routing |
| Sequence diagram | **Mermaid** | Lifelines, messages, and activation boxes need automatic layout |
| Data flow | **Mermaid** with edge labels | Connections and data descriptions need automatic edge routing |
| ER / schema diagram | **Mermaid** | Relationship lines between many entities need auto-routing |
| State machine | **Mermaid** | State transitions with labeled edges need automatic layout |
| Mind map | **Mermaid** | Hierarchical branching needs automatic positioning |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |

**Mermaid theming:** Always use `theme: 'base'` with custom `themeVariables` so colors match your page palette. Use `layout: 'elk'` for complex graphs (requires the `@mermaid-js/layout-elk` package — see `./references/libraries.md` for the CDN import). Override Mermaid's SVG classes with CSS for pixel-perfect control. See `./references/libraries.md` for full theming guide.

**Mermaid containers:** Always center Mermaid diagrams with `display: flex; justify-content: center;`. Add zoom controls (+/−/reset) to every `.mermaid-wrap` container.

**Mermaid scaling:** Complex diagrams with 10+ nodes render too small by default. Increase `fontSize` in themeVariables to 18-20px (default is 16px), or apply a CSS `transform: scale(1.3)` on the SVG. Don't let diagrams float in oversized containers with unreadable text. See `./references/css-patterns.md` "Scaling Small Diagrams".

**Mermaid layout direction:** Prefer `flowchart TD` (top-down) over `flowchart LR` (left-to-right) for complex diagrams. LR spreads horizontally and makes labels unreadable when there are many nodes. Use LR only for simple 3-4 node linear flows. See `./references/libraries.md` "Layout Direction: TD vs LR".

**Mermaid CSS class collision constraint:** Never define `.node` as a page-level CSS class. Mermaid.js uses `.node` internally on SVG `<g>` elements with `transform: translate(x, y)` for positioning. Page-level `.node` styles (hover transforms, box-shadows) leak into diagrams and break layout. Use the namespaced `.ve-card` class for card components instead. The only safe way to style Mermaid's `.node` is scoped under `.mermaid` (e.g., `.mermaid .node rect`).

### 3. Style

Apply these principles to every diagram:

**Typography is the diagram.** Pick a distinctive font pairing from the list in `./references/libraries.md`. Every page should use a different pairing from recent generations.

**Forbidden as `--font-body`:** Inter, Roboto, Arial, Helvetica, system-ui alone. These are AI slop signals.

**Good pairings (use these):**
- DM Sans + Fira Code (technical, precise)
- Instrument Serif + JetBrains Mono (editorial, refined)
- IBM Plex Sans + IBM Plex Mono (reliable, readable)
- Bricolage Grotesque + Fragment Mono (bold, characterful)
- Plus Jakarta Sans + Azeret Mono (rounded, approachable)

Load via `<link>` in `<head>`. Include a system font fallback in the `font-family` stack for offline resilience.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, and 3-5 accent colors. Each accent should have a full and a dim variant (for backgrounds). Name variables semantically when possible (`--pipeline-step` not `--blue-3`). Support both themes.

**Forbidden accent colors:** `#8b5cf6` `#7c3aed` `#a78bfa` (indigo/violet), `#d946ef` (fuchsia), the cyan-magenta-pink combination. These are Tailwind defaults that signal zero design intent.

**Good accent palettes (use these):**
- Terracotta + sage (`#c2410c`, `#65a30d`) — warm, earthy
- Teal + slate (`#0891b2`, `#0369a1`) — technical, precise
- Rose + cranberry (`#be123c`, `#881337`) — editorial, refined
- Amber + emerald (`#d97706`, `#059669`) — data-focused
- Deep blue + gold (`#1e3a5f`, `#d4a73a`) — premium, sophisticated

Put your primary aesthetic in `:root` and the alternate in the media query:

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first (neon, IDE-inspired, terminal): */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels), not dramatic color changes. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you don't.

**Backgrounds create atmosphere.** Don't use flat solid colors for the page background. Subtle gradients, faint grid patterns via CSS, or gentle radial glows behind focal areas. The background should feel like a space, not a void.

**Visual weight signals importance.** Not every section deserves equal visual treatment. Executive summaries and key metrics should dominate the viewport on load (larger type, more padding, subtle accent-tinted background zone). Reference sections (file maps, dependency lists, decision logs) should be compact and stay out of the way. Use `<details>/<summary>` for sections that are useful but not primary — the collapsible pattern is in `./references/css-patterns.md`.

**Surface depth creates hierarchy.** Vary card depth to signal what matters. Hero sections get elevated shadows and accent-tinted backgrounds (`ve-card--hero` pattern). Body content stays flat (default `.ve-card`). Code blocks and secondary content feel recessed (`ve-card--recessed`). See the depth tiers in `./references/css-patterns.md`. Don't make everything elevated — when everything pops, nothing does.

**Animation earns its place.** Staggered fade-ins on page load are almost always worth it — they guide the eye through the diagram's hierarchy. Mix animation types by role: `fadeUp` for cards, `fadeScale` for KPIs and badges, `drawIn` for SVG connectors, `countUp` for hero numbers. Hover transitions on interactive-feeling elements make the diagram feel alive. Always respect `prefers-reduced-motion`. CSS transitions and keyframes handle most cases. For orchestrated multi-element sequences, anime.js via CDN is available (see `./references/libraries.md`).

**Forbidden animations:**
- Animated glowing box-shadows (`@keyframes glow { box-shadow: 0 0 20px... }`) — this is AI slop
- Pulsing/breathing effects on static content
- Continuous animations that run after page load (except for progress indicators)

Keep animations purposeful: entrance reveals, hover feedback, and user-initiated interactions. Nothing should glow or pulse on its own.

### 4. Deliver

**Output location:** Write to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

```bash
mkdir -p ~/.agent/diagrams
```

**Open in browser:**
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

**Tell the user** the file path so they can re-open or share it.

## Diagram Types

For detailed guidance on each diagram type, see below. All types follow the rendering approach table from Step 2.

### Architecture / System Diagrams
**Text-heavy overviews** (card content matters more than connections): CSS Grid with explicit row/column placement. The reference template at `./templates/architecture.html` demonstrates this pattern.

**Topology-focused diagrams** (connections matter more than card content): **Use Mermaid.** A `graph TD` with custom `themeVariables` produces proper diagrams with automatic edge routing.

### Flowcharts / Pipelines
**Use Mermaid.** Prefer `graph TD` (top-down); use `graph LR` only for simple 3-4 node linear flows. Color-code node types with Mermaid's `classDef`.

### Sequence Diagrams
**Use Mermaid.** Use `sequenceDiagram` syntax. Style via CSS overrides on `.actor`, `.messageText`, `.activation` classes.

### Data Flow / ER / State Machine / Mind Map
**Use Mermaid.** See `./references/libraries.md` for syntax specifics per diagram type.

**`stateDiagram-v2` label caveat:** Transition labels with colons, parentheses, or special characters cause silent parse failures. Use `flowchart TD` instead with quoted edge labels for complex labels.

### Data Tables / Comparisons / Audits
Use a real `<table>` element. The reference template at `./templates/data-table.html` demonstrates all patterns: sticky `<thead>`, alternating row backgrounds, status indicators (styled `<span>`, never emoji), responsive overflow wrapper.

**Use proactively.** Any time you'd render an ASCII box-drawing table in the terminal, generate an HTML table instead.

### Timeline / Roadmap Views
Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles. Content cards branching left/right. Color progression from past (muted) to future (vivid).

### Dashboard / Metrics Overview
Card grid layout. Hero numbers large and prominent. For real charts, use **Chart.js via CDN** (see `./references/libraries.md`). KPI cards with trend indicators.

### Implementation Plans
Show **file structure with descriptions** and **key snippets only** — not full source files. See `./references/css-patterns.md` "Code Blocks" for formatting. Use collapsible sections for full code if truly needed.

### Documentation (READMEs, Library Docs, API References)
Transform prose into visual elements: feature lists become card grids, install steps become numbered flows, API references become tables.

## Slide Deck Mode

An alternative output format for presenting content as a magazine-quality slide presentation. **Opt-in only** — generate slides when the user invokes `/generate-slides`, passes `--slides` to an existing command, or explicitly asks for a slide deck.

**Before generating slides**, read `./references/slide-patterns.md` and `./templates/slide-deck.html`. Also read `./references/css-patterns.md` and `./references/libraries.md`.

**Slides are not pages reformatted.** Each slide is exactly one viewport tall (100dvh) with no scrolling. Typography is 2-3x larger. The agent composes a narrative arc (impact -> context -> deep dive -> resolution).

**Content completeness.** Every section, decision, data point from the source must appear in the deck. Add more slides rather than cutting content.

**Slide types (10):** Title, Section Divider, Content, Split, Diagram, Dashboard, Table, Code, Quote, Full-Bleed. See `./references/slide-patterns.md` for layouts.

**Compositional variety:** Consecutive slides must vary spatial approach — centered, left-heavy, right-heavy, split, edge-aligned, full-bleed.

**Curated presets:** Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean. See `./references/slide-patterns.md` for preset CSS values.

## File Structure

Every diagram is a single self-contained `.html` file. No external assets except CDN links (fonts, optional libraries):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>/* CSS custom properties, theme, layout, components */</style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- Optional: <script> for Mermaid, Chart.js, or anime.js -->
</body>
</html>
```

## Quality Checks

Before delivering, verify:
- **The squint test**: Can you still perceive hierarchy with blurred eyes?
- **The swap test**: Would a generic dark theme make this indistinguishable from a template?
- **Both themes**: Light and dark mode both look intentional
- **Information completeness**: Pretty but incomplete is a failure
- **No overflow**: Every grid/flex child needs `min-width: 0`. See `./references/css-patterns.md` Overflow Protection.
- **Mermaid zoom controls**: Every `.mermaid-wrap` must have +/-/reset and scroll zoom. See `./references/css-patterns.md`.
- **File opens cleanly**: No console errors, no broken font loads, no layout shifts

## Anti-Patterns (AI Slop)

For the complete anti-pattern checklist, see the Style section above. Quick slop test — if two or more of these are present, regenerate:

1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome

Pick a constrained aesthetic (Editorial, Blueprint, Paper/ink, or a specific IDE theme) to avoid these patterns.

## Examples

### Example 1: Architecture diagram

User says: "Show me the authentication system architecture"

Actions:
1. Read `./templates/architecture.html` and `./references/css-patterns.md`
2. Pick Blueprint aesthetic with DM Sans + Fira Code
3. Generate CSS Grid layout with auth flow cards, Mermaid dependency graph
4. Write to `~/.agent/diagrams/auth-architecture.html`
5. Open in browser, report path to user

Result: Self-contained HTML with dark/light theme support, zoom controls on Mermaid diagram

### Example 2: Proactive table rendering

User asks to compare 5 database options across 8 criteria.

Actions:
1. Detect: 5 rows x 8 columns exceeds 4+ rows / 3+ columns threshold
2. Read `./templates/data-table.html`
3. Generate HTML table with sticky headers, status badges, alternating rows
4. Write to `~/.agent/diagrams/database-comparison.html`
5. Open in browser, provide brief text summary in chat

Result: Styled HTML table instead of unreadable ASCII art

### Example 3: Slide deck

User says: `/generate-slides API Gateway Design`

Actions:
1. Read `./templates/slide-deck.html` and `./references/slide-patterns.md`
2. Pick Midnight Editorial preset, plan 15-slide narrative arc
3. Generate slides: Title, Overview, Architecture (Mermaid), 8 content slides, Summary
4. Write to `~/.agent/diagrams/api-gateway-slides.html`
5. Open in browser

Result: Magazine-quality presentation with keyboard navigation and slide transitions

## Error Handling

| Scenario | Action |
|----------|--------|
| Output directory doesn't exist | Create `~/.agent/diagrams/` with `mkdir -p` |
| Browser fails to open | Report the file path so user can open manually |
| Mermaid diagram syntax error | Check for special characters in labels; switch to `flowchart TD` if `stateDiagram-v2` fails |
| CDN fonts fail to load | System font fallback stack ensures readability |
| HTML file too large (>5MB) | Reduce inline base64 images; use simpler illustrations |
| Template file not found | Generate from memory using the patterns described in this skill |
