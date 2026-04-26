# Component Reference

This is the component manual for the `guizang-magazine-deck` skill. The template.html already defines all styles — this document only describes "what each component looks like and how to use it."

## Table of Contents

- [Base Slide Shell](#base-slide-shell)
- [Typography](#typography)
- [Chrome & Foot](#chrome--foot)
- [Callout (Quote Block)](#callout-quote-block)
- [Stat (Number Matrix)](#stat-number-matrix)
- [Platform Card](#platform-card)
- [Rowline (Table Row)](#rowline-table-row)
- [Pillar Card](#pillar-card)
- [Tag & Kicker](#tag--kicker)
- [Figure (Image Frame)](#figure-image-frame)
- [Icons](#icons)
- [Ghost (Giant Background Text)](#ghost-giant-background-text)
- [Highlight](#highlight)
- [Motion (Animation System)](#motion-animation-system)

---

## Base Slide Shell

Every page is a `<section class="slide ...">`. The slide must include a theme class — JS uses it to switch backgrounds on page flip.

```html
<section class="slide light">          <!-- Light page -->
<section class="slide dark">           <!-- Dark page -->
<section class="slide light hero">     <!-- Hero page: light + thin overlay reveals WebGL -->
<section class="slide dark hero">      <!-- Hero page: dark + thin overlay -->
```

**light vs dark usage: alternate** every 2-3 pages. The WebGL background smoothly interpolates between two shaders on page transitions.

**hero class usage**: Only for visually-dominant pages (cover, key quote, chapter transition, ending). Adding `hero` reduces the overlay to 12-16%, letting the WebGL background show prominently — don't put too much text on hero pages.

---

## Typography

Font division is the most important rule in this template. Mixing is strictly forbidden.

| Class | Purpose | Font |
|-------|---------|------|
| `.display` | Extra-large English (Hero pages) | Playfair Display 700, 11vw |
| `.display-cjk` | Extra-large CJK title | Noto Serif SC 700, 7.8vw |
| `.h1-cjk` | Page main title | Noto Serif SC 700, 4.6vw |
| `.h2-cjk` | Subtitle | Noto Serif SC 600, 3.2vw |
| `.h3-cjk` | Pipeline step title | Noto Serif SC 500, 1.9vw |
| `.lead` | Lead paragraph (larger than body) | Noto Serif SC 400, 1.9vw |
| `.body-cjk` | **Body text (sans-serif)** | Noto Sans SC 400, 1.22vw |
| `.body-serif` | Body text (serif) | Noto Serif SC 400, 1.3vw |
| `.kicker` | Section hint (above title) | IBM Plex Mono, 12px uppercase |
| `.meta` | Metadata labels | IBM Plex Mono, 0.88vw uppercase |
| `.big-num` | Giant numbers | Playfair Display 800, 10vw |
| `.mid-num` | Medium numbers | Playfair Display 700, 5.5vw |

**Core rules**:
- **Serif** (`serif-cjk` / `serif-en`): titles, key quotes, large numbers — "visual accent"
- **Sans-serif** (`sans-cjk`): body descriptions, dense reading content — "information density"
- **Monospace** (`mono`): kicker, meta, foot labels — "decorative rhythm"

**Emphasis techniques**:
- `<em class="en">English word</em>` — renders English in Playfair Display italic (elegant)
- `<em style="opacity:.65">phrase</em>` — fades the second half of a title, creating rhythm

---

## Chrome & Foot

Top and bottom metadata bars on every page. Almost all pages should have them.

```html
<div class="chrome">
  <div class="left">
    <span>Act One · Hard Data</span>
    <span class="sep"></span>
    <span>Act I</span>
  </div>
  <div class="right"><span>02 / 27</span></div>
</div>

<!-- ... page body ... -->

<div class="foot">
  <div class="title">Project Name · CodePilot | github.com/codepilot</div>
  <div>Act I · Dev Numbers</div>
</div>
```

**Rules**:
- `chrome.right` always shows page number `NN / TOTAL` (TOTAL = total page count)
- `foot.title` is the descriptive text, `foot.right` is the act marker
- Chrome and foot together create the magazine-style "header and footer"

---

## Callout (Quote Block)

Display key quotes / core observations / third-party citations.

```html
<div class="callout" style="max-width:80vw">
  <div class="q-big">"This would have taken a ten-person team<br>a full year, just three years ago."</div>
  <div class="callout-src">— An observer's assessment</div>
</div>
```

Variants:
- Without source attribution: remove the `<div class="callout-src">` element
- With English quote: `<em class="en">"Thin Harness, Fat Skills."</em>`
- On hero pages: add `style="position:relative;z-index:2"` to the outer div (avoids overlay covering)

---

## Stat (Number Matrix)

Display data metrics, commonly paired with `.grid-6` / `.grid-4`.

```html
<div class="grid-6">
  <div class="stat-card">
    <div class="stat-label">Duration</div>
    <div class="stat-nb">64 <span class="stat-unit">days</span></div>
    <div class="stat-note">From scratch to now</div>
  </div>
  <!-- ... more stat-card ... -->
</div>
```

Three-part structure: `.stat-label` monospace label → `.stat-nb` giant number (with optional `.stat-unit` for units) → `.stat-note` description.

**Common layout containers**:
- `.grid-6` — 3×2 grid (most common, 6 stats)
- `.grid-4` — 2×2 grid (4 stats)
- `.grid-3` — 3-column single row (3 stats / pillars)

---

## Platform Card

Display social platforms / channels + follower counts.

```html
<div class="plat">
  <div class="sub">Twitter</div>
  <div class="name">X / Twitter</div>
  <div class="nb">137K</div>
</div>
```

Optional fourth line (supplementary note):
```html
<div class="body-cjk" style="font-size:max(11px,.8vw);opacity:.5;margin-top:.6vh">
  Includes cross-posted content
</div>
```

**"Also On" variant** (supplementary platforms):
```html
<div class="plat" style="border-top-style:dashed;opacity:.72">
  <div class="sub">Also On</div>
  <div class="body-cjk" style="font-weight:600;margin-top:.8vh">
    YouTube · LinkedIn
  </div>
</div>
```

---

## Rowline (Table Row)

List-style content, one entry per row.

```html
<div class="rowline">
  <div class="k">CLAUDE.md</div>
  <div class="v">How to do things — behavior rules + work preferences + prohibitions</div>
  <div class="m">EMPLOYEE · HANDBOOK</div>
</div>
```

Three-column structure: `.k` serif keyword · `.v` body description · `.m` monospace label (right-aligned). First and last rowline automatically get top/bottom borders.

**2-column variant**: `style="grid-template-columns:1fr 3fr"` and omit `.m` column.

---

## Pillar Card

Three-pillar structure, commonly used for "parallel concepts" pages.

```html
<div class="grid-3">
  <div class="pillar">
    <div class="ic">01</div>
    <div class="t">Three-Layer<br>Documentation</div>
    <div class="d">CLAUDE.md<br>+ Project Knowledge Base<br>+ Guardrails</div>
  </div>
  <!-- ... more pillars ... -->
</div>
```

**Pillar with icon (for emphasis pages)**:
```html
<div class="pillar" style="padding:4vh 2vw;border:1px solid currentColor;border-color:rgba(10,10,11,.2)">
  <div class="ic"><i data-lucide="compass" class="ico-lg"></i></div>
  <div class="t">Judgment</div>
  <div class="d">Authority over decisions and direction.<br>Trade-offs, taste, sense of direction.</div>
</div>
```

`.ic` can be a sequence number (`01 / 02 / 03` or `A. / B. / C.`) or a Lucide icon.

---

## Tag & Kicker

**Kicker** is the small hint text above a title (monospace, uppercase, small):
```html
<div class="kicker">Past 64 Days · Development</div>
<div class="h1-cjk">What one person built.</div>
```

**Tag** is a standalone label capsule (with border):
```html
<div style="display:flex;gap:1.6vw;flex-wrap:wrap">
  <div class="tag">Wakes up at 10am</div>
  <div class="tag">Gym on Tue / Thu afternoons</div>
  <div class="tag">Still watches shows · plays games at night</div>
</div>
```

---

## Figure (Image Frame)

**This is the most error-prone component — follow these rules strictly.**

### Base Structure (v2 API)

```html
<figure class="frame-img" style="height:26vh" data-anim>
  <img src="images/xxx.png" alt="Description">
  <figcaption class="img-cap">Twitter · 137K</figcaption>
</figure>
```

The `<figure>` itself carries the `frame-img` class. The `<img>` goes directly inside (no wrapping `<div>`). Use `.img-cap` for a simple monospace caption.

### Rich Caption Variant

For structured captions with styled sub-elements, use `.frame-cap` inside the `<figure>`:

```html
<figure class="frame-img" style="height:26vh" data-anim>
  <img src="images/xxx.png" alt="Description">
  <figcaption class="frame-cap">
    <span class="pf">Twitter</span>
    <span class="nb">137K</span>
  </figcaption>
</figure>
```

Sub-elements: `.pf` (platform name, serif bold) · `.nb` (number, serif italic) · `.idx` (index, mono faded).

### Critical Constraints (Hard-Won Lessons)

1. **Must use `height:Nvh` for fixed height** — do NOT use `aspect-ratio`.
   - Reason: `aspect-ratio` in grids overflows parent containers, causing image stacking.
   - Recommended sizes: `height:18vh` (compact strip) / `22vh` (standard grid) / `26vh` (featured) / `28vh` (large).

2. **`object-position:top center` (preset in CSS)** — only bottom gets cropped.
   - Cropping left/right/top is strictly forbidden — that's the image's core identity area.

3. **For multiple images in a grid, use inline grid instead of `.grid-3`**:
   ```html
   <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1vh 1.2vw">
     <figure class="frame-img">...</figure>
     <figure class="frame-img">...</figure>
     <figure class="frame-img">...</figure>
   </div>
   ```

4. **Aligning images with other layout elements**: Use `align-self:end` on the figure to bottom-align.

### Image Placeholder (Design-Phase Placeholder)

When images aren't ready yet, use a dashed-border placeholder:
```html
<div class="img-slot r-4x3">  <!-- r-4x3 / r-16x9(default) / r-3x2 / r-1x1 -->
  <span class="plus">+</span>
  <span class="label">GitHub screenshot placeholder</span>
</div>
```

---

## Icons

**Emoji is strictly forbidden.** Use Lucide via CDN (already imported in template.html).

```html
<i data-lucide="compass" class="ico-lg"></i>     <!-- Large icon (for pillars) -->
<i data-lucide="target" class="ico-md"></i>      <!-- Medium icon (for list items) -->
<i data-lucide="check-circle" class="ico-sm"></i>  <!-- Small icon (for inline) -->
```

**Common Lucide icon names** (grouped by meaning):

- Judgment: `compass`, `target`, `crosshair`, `search-check`
- Relationships: `share-2`, `users`, `network`, `link`, `handshake`
- Brand: `crown`, `gem`, `award`, `star`, `badge-check`
- Process: `workflow`, `route`, `arrow-right-left`, `repeat`
- Data: `grid-2x2`, `bar-chart-3`, `trending-up`, `activity`
- Aesthetics: `palette`, `brush`, `eye`, `sparkles`
- Pass/Fail: `check-circle`, `x-circle`, `check`, `x`
- Direction: `arrow-right`, `arrow-up-right`, `corner-down-right`

**Icon + text inline combo**:
```html
<div class="h3-cjk" style="display:flex;align-items:center;gap:.8em">
  <i data-lucide="target" class="ico-md"></i>
  Judgment — What's worth writing
</div>
```

---

## Ghost (Giant Background Text)

Used as "decorative background text" at extremely low opacity, creating magazine feel.

```html
<div class="ghost" style="right:-6vw;top:-8vh">BUT</div>
<div class="ghost" style="left:-8vw;bottom:-18vh;font-style:italic">Harness</div>
```

- Font size 34vw, opacity 0.06
- Common positions: `right:-6vw;top:-8vh` (top-right overflow) / `left:-8vw;bottom:-18vh` (bottom-left overflow)
- Content: English words or numbers (chapter numbers 01/02/03, keywords BUT/NOW/HERE)

**Note**: On pages using ghost, other content needs `position:relative;z-index:2` to avoid being layered below.

---

## Highlight

Inline "highlighter pen" effect for short phrases:

```html
<span class="hi">not</span>
<span class="hi">a one-time burst</span>
```

Generates a semi-transparent highlight bar at the text bottom. Dark theme uses bright bar, light theme uses dark bar (CSS handles this).

**Suitable for**: Only use on 1-3 key words — don't apply broadly.

---

## Motion (Animation System)

The entire deck has page-entry animations enabled by default, powered by Motion One (~4KB vanilla Framer Motion).

### Loading Strategy

The module script at the bottom of `assets/template.html` first tries **local** `assets/motion.min.js`, then falls back to **jsdelivr CDN**. Both failing triggers a force-set of all `data-anim` elements to `opacity:1` — content is always readable, presentations don't depend on network.

```js
// Core loader in template (don't modify)
let motion;
try { motion = await import('./assets/motion.min.js'); }
catch(e1) {
  try { motion = await import('https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm'); }
  catch(e2) {
    document.querySelectorAll('[data-anim]').forEach(el=>{el.style.opacity='1';el.style.transform='none'});
  }
}
```

### Data-Attribute Driven

You only need two attributes in HTML:

```html
<!-- 1. Choose recipe on section (optional; defaults to cascade / hero auto-detected) -->
<section class="slide light" data-animate="quote">

<!-- 2. Add data-anim to elements that need entrance animation (optional values: left/right/line/step/divider) -->
<h1 class="h-xl" data-anim>Big Title</h1>
<div class="stat-card" data-anim>...</div>
<div data-anim="left">Left column content</div>
<span data-anim="line" style="display:block">Quote first line</span>
```

### 5 Recipe Overview

| Recipe | Trigger | Behavior | Representative Layout |
|--------|---------|----------|----------------------|
| `cascade` (default) | Don't add `data-animate` | All `data-anim` elements stagger fade-in, 75ms/step | Layout 3/4/5/10 |
| `hero` | Auto-used on `.hero` slides | Slower stagger, more ceremonial, 160ms/step | Layout 1/2/7 |
| `quote` | `data-animate="quote"` | Other elements appear first, `data-anim="line"` lines reveal at 550ms intervals | Layout 8 |
| `directional` | `data-animate="directional"` | `data-anim="left"` slides from left → divider → `data-anim="right"` slides from right | Layout 9 |
| `pipeline` | `data-animate="pipeline"` | On page entry, steps stay at 15% opacity; press →/Space/scroll to light up one step at a time; page only advances after all steps are revealed | Layout 6 |

### Recipe Decision Tree

1. **Is it a `.hero` slide?** → Don't add `data-animate`, auto-uses `hero`
2. **Is it a big quote page?** → `data-animate="quote"`, each line uses `<span data-anim="line" style="display:block">`
3. **Is it a left-right Before/After comparison?** → `data-animate="directional"`, left column `data-anim="left"`, right column `data-anim="right"`
4. **Is it a step-by-step pipeline?** → `data-animate="pipeline"`, each step `data-anim="step"`
5. **All other body pages** → Add nothing, auto-uses `cascade`

### Which Elements Should Get `data-anim`?

- Each semantically independent block: kicker / h1 / h-xl / lead / callout / stat-card / figure / tag / rowline
- Each column in multi-column structures, so they fade in column-by-column rather than all at once
- Do NOT add to containers (`.grid-6` / `.frame`) — only add to leaf elements
- Do NOT add to every `<li>` — adding to the `<ul>` level is usually sufficient
- To skip animation on a page entirely, don't add any `data-anim` attributes — Motion One only affects marked elements

### Common Questions

- **Image flashes then appears?** Expected behavior — animation triggers at mid-transition (450ms mark)
- **Pipeline page stuck, can't advance?** Correct — press → to light up steps one by one; only after all steps are lit does the next → advance the page
- **Content invisible even when static?** Check if motion.min.js exists in `assets/`; or check browser console for errors
