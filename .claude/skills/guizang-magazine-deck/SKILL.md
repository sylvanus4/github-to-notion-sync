---
name: guizang-magazine-deck
description: >-
  Generate "magazine x electronic ink" horizontal-swipe HTML decks
  (single-file) with WebGL fluid backgrounds, serif + sans-serif + monospace
  type hierarchy, 10 editorial layouts, 5 locked color themes, and Motion One
  page-transition animations. Use when the user asks to create a
  magazine-style presentation, horizontal swipe deck, editorial magazine
  slides, guizang deck, or mentions "잡지 스타일 PPT", "매거진 덱", "가로 넘김 프레젠테이션",
  "에디토리얼 슬라이드", "magazine deck", "horizontal swipe deck", "editorial magazine
  presentation", "guizang", "magazine-style slides", "e-ink presentation
  deck", "guizang-magazine-deck". Do NOT use for technical explainer pages
  with vertical scroll-snap (use visual-explainer). Do NOT use for interactive
  React prototypes with JSX (use expert-html-designer). Do NOT use for
  presentation content strategy only without slide generation (use
  presentation-strategist). Do NOT use for PowerPoint .pptx file output (use
  anthropic-pptx). Do NOT use for production web applications (use
  anthropic-frontend-design). Do NOT use for simple Mermaid diagrams or data
  charts (use visual-explainer or infographic).
---

# Magazine Web Deck

## What This Skill Does

Generates a **single-file HTML** horizontal-swipe presentation deck with:

- **Magazine x Electronic Ink** hybrid aesthetic
- **WebGL fluid / contour / dispersion backgrounds** (visible on hero pages)
- **Serif titles** (Noto Serif SC + Playfair Display) + **sans-serif body** (Noto Sans SC + Inter) + **monospace metadata** (IBM Plex Mono)
- **Lucide line icons** (no emoji allowed)
- **Horizontal left/right navigation** (keyboard arrows, scroll wheel, touch swipe, dot pagination, ESC index overlay)
- **Smooth theme interpolation**: colors and shaders transition smoothly when flipping to hero pages
- **Page-entry animations** (Motion One driven, 5 recipes auto-matched to layouts, local + CDN dual fallback, offline-safe)

The aesthetic is NOT "corporate PowerPoint" or "consumer app UI" — it looks like *Monocle* magazine fused with code.

## 6-Step Workflow

### Step 1 — Requirements Clarification

Ask the user these 6 questions before starting:

1. **Audience** — Who will view this? (conference, internal share, investor pitch, personal blog)
2. **Page count** — Rough estimate? (8-page quick share, 15-20 standard talk, 25-30 deep dive)
3. **Source material** — Any existing text, outline, or notes to work from?
4. **Images** — Does the user have screenshots/photos, or should we use placeholder slots?
5. **Theme** — Show the 5 preset options from `references/themes.md` and let the user pick (or recommend based on content)
6. **Constraints** — Any branding, language, or layout preferences?

### Step 2 — Template Setup

1. Read `assets/template.html` with the Read tool
2. Copy the full template content into a new file (e.g., `output/magazine-deck.html`) using the Write tool
3. Replace `<title>[REQUIRED] Replace with Deck Title</title>` with the actual deck title
4. If the user chose a non-default theme, replace the `:root` CSS variables block with the chosen theme's values from `references/themes.md`

### Step 3 — Content Population

1. Read `references/layouts.md` and select appropriate layouts for each page
2. **Plan the theme rhythm FIRST** — create a table mapping each page to its theme class (`hero dark` / `hero light` / `light` / `dark`). Enforce rhythm hard-rules:
   - No 3+ consecutive pages with the same theme
   - Decks with 8+ pages must have at least 1 `hero dark` AND 1 `hero light`
   - Must include at least 1 `dark` body page (not all `light`)
   - Insert a hero page every 3-4 body pages
3. For each page, pick a layout (1-10), populate content, and add `data-anim` attributes to leaf elements (kicker, titles, lead, callout, stat-card, figure)
4. For special layouts, add the correct `data-animate` recipe on the `<section>`:
   - Big Quote → `data-animate="quote"` with `<span data-anim="line">`
   - Before/After → `data-animate="directional"` with `data-anim="left"` / `data-anim="right"`
   - Pipeline → `data-animate="pipeline"` with `data-anim="step"`
5. Reference `references/components.md` for component markup patterns

### Step 4 — Self-Check

Run the quality checklist from `references/checklist.md`. All **P0 items must pass** before preview:

- Verify all CSS class names exist in the template's `<style>` block
- Confirm no emoji icons (Lucide only)
- Confirm image containers use `height:Nvh` (not `aspect-ratio` in grids)
- Confirm theme rhythm has no 3+ consecutive same-theme pages
- Confirm `chrome` and `kicker` text are not duplicates of each other
- Confirm every page has `data-anim` attributes on leaf elements
- Confirm Pipeline pages have `data-animate="pipeline"`

### Step 5 — Preview

Open the generated HTML file in the browser via `cursor-ide-browser` MCP for visual verification:
- Check that WebGL backgrounds render on hero pages
- Verify horizontal swipe navigation works (arrows, dots, ESC index)
- Confirm Motion One animations trigger on page transitions
- Verify theme switching (light/dark canvas transitions)

### Step 6 — Iterate

Based on preview feedback, make inline adjustments:
- Font sizes (use `style="font-size:Nvw"` overrides)
- Spacing (adjust `padding-top`, `margin-top`, `gap` values)
- Image heights (tune `height:Nvh` values)
- Theme rhythm (swap `light`/`dark` classes if visual balance is off)

## Reference Files

| File | Purpose |
|------|---------|
| `references/layouts.md` | 10 page layout skeletons with HTML, pre-flight rules, and theme rhythm guidance |
| `references/themes.md` | 5 curated CSS variable sets — no custom colors allowed |
| `references/components.md` | Component manual: slide shell, typography, chrome/foot, callout, stat, pipeline, figure, icons, ghost text, highlight, motion system |
| `references/checklist.md` | Quality gate with P0 (must fix) through P3 (cosmetic) severity levels |
| `assets/template.html` | Complete seed HTML template with CSS, WebGL shaders, navigation JS, and Motion One animation engine |

## Constraints

**Freedom level: LOW** — This skill enforces strict aesthetic guardrails.

- **Single-file HTML only** — one `.html` file, no external CSS/JS bundles, no build step
- **5 locked themes only** — never invent custom hex/rgb values; if the user insists on a custom palette, decline and explain the 5 presets
- **10 layout templates only** — do not invent new layout class names; compose pages from the 10 layouts in `references/layouts.md`
- **No emoji** — all icons must be Lucide SVG references
- **No `aspect-ratio` in grid images** — use `height:Nvh` instead (see Image Rules below)
- **No framework dependencies** — no React, Vue, Svelte; plain HTML + inline CSS + vanilla JS only
- **Maximum 30 pages** — if the user requests more, split into multiple decks

## Output Format

The final deliverable is a **single `.html` file** that can be opened directly in any modern browser (Chrome, Firefox, Safari, Edge). No server, no build tool, no npm required.

- Default output path: `output/magazine-deck.html` (or user-specified path)
- File should be self-contained: all CSS in `<style>`, all JS in `<script>`, WebGL shaders inline
- External dependencies loaded via CDN with local fallback: Google Fonts, Lucide icons, Motion One

## Gotchas

1. **Class names must exist in template CSS** — The #1 failure mode. If you write `<section class="slide hero fancy-new-class">`, the page will render broken. Always verify class names against `assets/template.html` `<style>` block before using them.
2. **WebGL canvas only renders on hero pages** — Adding `hero` class to too many pages creates visual fatigue. Limit hero pages to 1 per 3-4 body pages.
3. **Theme rhythm violations are invisible until preview** — Three consecutive `light` pages look washed out; three consecutive `dark` pages feel oppressive. Plan the rhythm table in Step 3 before writing any HTML.
4. **Motion One CDN can fail** — The template includes a fallback that makes all `[data-anim]` elements visible. Never rely on animations for conveying critical information.
5. **`object-position: top center`** — The template crops images from the bottom. If the user provides a portrait photo where the face is centered, it will look fine. But if the subject is at the bottom of the image, it will be cropped out. Warn the user about this.
6. **Pipeline layout blocks page advance** — The `data-animate="pipeline"` recipe reveals steps sequentially and blocks arrow-key/swipe navigation until all steps are shown. Users may think navigation is broken — this is by design.
7. **Font loading delay** — Google Fonts load from CDN. On slow connections, a flash of unstyled text (FOUT) is expected for ~1-2 seconds. This is acceptable.

## Edge Cases

- **Short decks (< 5 pages)**: Skip the hero rhythm rule; use 1 hero cover + all body pages
- **Image-heavy decks**: Prefer Image Grid and Left-Text Right-Image layouts; warn user about file size if many high-res images are embedded as base64
- **Text-heavy / data-heavy decks**: Use Data Billboard and Pipeline layouts; consider splitting into multiple decks if exceeding 30 pages
- **No-image decks**: Big Quote, Suspense Question, and Chapter Cover layouts work without images; remove `<figure>` blocks entirely rather than leaving empty placeholders
- **Offline viewing**: All critical features (navigation, layout, typography) work offline; only Google Fonts and Lucide icons require network — fallback system fonts and no icons appear gracefully

## Anti-Gold-Plating Rules

- Do NOT add features the user did not request (e.g., print stylesheet, PDF export, speaker notes)
- Do NOT create custom WebGL shader variants — use only the Holographic Dispersion (dark) and Spiral Vortex (light) shaders from the template
- Do NOT tweak theme CSS variables "just a little" — use the exact values from `references/themes.md`
- If the generated deck meets all P0 checklist items and the user hasn't requested changes, STOP — do not iterate for cosmetic polish unless asked

## Honest Reporting

- If content doesn't fit well into any of the 10 layouts, say so — suggest splitting or restructuring rather than forcing content into a bad layout
- If the user's image quality is too low for hero pages (< 1200px wide), report this directly rather than silently using it
- If the theme rhythm cannot satisfy all hard-rules with the given page count, explain the constraint and propose alternatives

## Key Design Rules

### Typography Hierarchy (Strict — No Mixing)
- **Serif** (Noto Serif SC / Playfair Display): titles, key quotes, large numbers — "visual accent"
- **Sans-serif** (Noto Sans SC / Inter): body text, descriptions — "information density"
- **Monospace** (IBM Plex Mono): kicker, meta labels, footer — "decorative rhythm"

### Theme System (5 Presets Only — No Custom Colors)
1. **Ink Classic** (default) — pure black + warm cream, universal
2. **Indigo Porcelain** — deep indigo + porcelain white, tech/research
3. **Forest Ink** — forest green + ivory, nature/culture
4. **Kraft Paper** — deep brown + warm cream, humanities/vintage
5. **Dune** — charcoal + sand, art/design/creative

### Image Rules
- Grid images: use `height:Nvh`, never `aspect-ratio`
- Single images: `aspect-ratio` + `max-height` is acceptable
- Always wrap in `<figure class="frame-img">`
- `object-position: top center` — crops bottom only, never top/sides
- No heavy borders or box-shadows (max 4px border-radius)

### Animation System (Motion One)
- All `[data-anim]` elements start hidden, animate in on page entry
- 5 recipes: `cascade` (default), `hero` (auto for `.hero`), `quote`, `directional`, `pipeline`
- Pipeline recipe blocks page advance until all steps are revealed
- Graceful degradation: if Motion One fails to load, all content becomes visible

### Navigation
- Keyboard: ← → arrows, Page Up/Down, Home/End
- Scroll wheel: horizontal page flip
- Touch: swipe left/right
- Dot pagination: bottom center
- ESC: index overlay with page thumbnails

## Rationalization Detection

If you catch yourself thinking any of the following, STOP and follow the constraint:

| Thought | Rule |
|---------|------|
| "This theme is close enough, I'll just adjust one variable" | Use exact theme values from `references/themes.md` — no exceptions |
| "I'll add a quick custom layout for this content" | Use one of the 10 layouts — restructure the content to fit |
| "An emoji here would be clearer than an icon" | No emoji — use Lucide or no icon at all |
| "The user probably wants a print view too" | Only build what was requested — see Anti-Gold-Plating Rules |
| "This image is a bit small but it'll be fine" | Report the image quality issue — see Honest Reporting |
| "Three dark pages in a row looks fine to me" | Theme rhythm rules are non-negotiable — swap at least one to `light` |
