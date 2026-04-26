# Page Layout Library (Layouts)

This document contains 10 commonly used page layout skeletons. Each is a complete, paste-ready `<section class="slide ...">...</section>` code block — just replace the copy and images.

---

## Pre-flight Checklist (Read Before Generating)

### A. Class Names Must Come from template.html

All classes used in layouts.md (`h-hero` / `h-xl` / `h-sub` / `h-md` / `lead` / `meta-row` / `stat-card` / `stat-label` / `stat-nb` / `stat-unit` / `stat-note` / `pipeline-section` / `pipeline-label` / `pipeline` / `step` / `step-nb` / `step-title` / `step-desc` / `grid-2-7-5` / `grid-2-6-6` / `grid-2-8-4` / `grid-3-3` / `grid-6` / `grid-3` / `grid-4` / `frame` / `frame-img` / `img-cap` / `callout` / `callout-src` / `kicker`) are pre-defined in the `<style>` block of `assets/template.html`.

**Do not invent new class names.** If customization is needed, use `style="..."` inline. Before generating, grep template.html to confirm a class exists if unsure.

### B. Image Aspect Ratio Rules (Critical)

**Always use standard ratios** — never raw image ratios like `aspect-ratio: 2592/1798`:

| Scenario | Recommended Ratio | Syntax |
|----------|------------------|--------|
| Left-text right-image main image | 16:10 or 4:3 | `aspect-ratio:16/10; max-height:54vh` |
| Image grid (multi-image comparison) | Uniform | **Fixed `height:26vh`, no aspect-ratio** |
| Small left image + right text | 1:1 or 3:2 | `aspect-ratio:1/1; max-width:40vw` |
| Full-screen hero visual | 16:9 | `aspect-ratio:16/9; max-height:64vh` |
| Mixed text-image small inset | 3:2 | `aspect-ratio:3/2; max-width:30vw` |

Images must be wrapped in `<figure class="frame-img">`. The inner `<img>` automatically gets `object-fit:cover + object-position:top center` — crops bottom only, never top/left/right.

### C. Image Positioning (Avoid Images Piling at Page Bottom)

**Wrong approaches** (known pitfalls):
- Using `align-self:end` outside grid/flex: `align-self` has no effect outside flex/grid, images fall to document flow bottom
- Using `position:absolute + bottom:0`: gets obscured by `.foot` and `#nav` dots
- Single images with only `height:Nvh` without `max-height`: overflows viewport on low-res screens

**Correct approaches:**
- Text-image layouts **must use `.frame.grid-2-7-5`** (or `.grid-2-6-6` / `.grid-2-8-4`) grid structure
- Grid containers default to `align-items:start` (set in template), images naturally stick to cell top
- To align "image bottom with left-column callout": **use flex column + `justify-content:space-between` on the left column** (lets callout stick to left column bottom), **right column figure stays with align-items:start** — do NOT add `align-self:end`
- All grid parent containers should add inline `style="padding-top:6vh"` for title breathing room

### D. Theme Colors and Theme Rhythm

- Theme colors come from `references/themes.md` — 5 preset palettes, no custom hex values allowed
- Theme rhythm (which page uses light / dark / hero light / hero dark) has hard rules in the "Theme Rhythm Planning" section below — read before generating
- Both decisions must be made before picking layouts to avoid rework

### E. Animation System (Enabled by Default — Motion One Powered)

**Core mechanism**: The module script at the bottom of template.html triggers entrance animations on page flip. All elements with `data-anim` start invisible and are revealed one-by-one by Motion One when the page becomes current.

**Animation strategy**: Add `data-animate="<recipe>"` on `<section>` to choose animation style; add `data-anim` (with optional value: `left` / `right` / `line` / `step`) to each element that needs entrance animation.

| Recipe | Usage | Suitable Layouts |
|--------|-------|-----------------|
| Default (cascade) | Add nothing, auto cascade fade-in | Most body pages (Layout 3/4/5/10) |
| `hero` | Auto-enabled for `.hero` pages, slower ceremonial rhythm | Layout 1/2/7 (all hero pages) |
| `quote` | Line-by-line reveal, slow rhythm (550ms stagger) | Layout 8 big quote |
| `directional` | Left-in → divider → right-in, for comparison | Layout 9 Before/After |
| `pipeline` | Manual advance, press →/Space to light up steps one-by-one | Layout 6 pipeline |

**Graceful degradation**: If motion.min.js fails to load from both local and CDN, the script force-sets all `data-anim` elements to `opacity:1` — content is always readable.

**No-animation pages**: To skip animation entirely on a page, simply don't add any `data-anim` attributes — Motion One only affects marked elements.

---

## 0. Base Structure (Same for All Slides)

```html
<section class="slide [light|dark|hero light|hero dark]">
  <div class="chrome">
    <div>Context Label · Sub-label</div>
    <div>ACT · Page / Total</div>
  </div>
  <!-- Main content -->
  <div class="foot">
    <div>Page Description</div>
    <div>— · —</div>
  </div>
</section>
```

- Non-hero pages should use `light` or `dark`; hero pages use `hero light` or `hero dark` (participates in WebGL theme interpolation)
- `chrome` and `foot` are optional but recommended corner metadata
- **Hero pages are for chapter covers / opening / closing / transitions**, non-hero pages are for body content

### Chrome vs Kicker — Never Duplicate Content

This is the most common content repetition problem. They serve entirely different semantic roles:

| Position | Role | Content Nature | Example |
|----------|------|---------------|---------|
| `.chrome` top-left | **Magazine header / nav metadata** | Stable "column name" or "chapter category", can repeat across pages | "Act II · Workflow" / "Data · Result" |
| `.chrome` top-right | **Page number + act number** | Fixed format | "Act II · 15 / 25" |
| `.kicker` | **This page's unique hook line** | A "small prefix" above the title, like a magazine headline kicker — should differ per page | "BUT" / "The Question" / "Phase 01 · Design" |

**Anti-pattern**: chrome says "Design First" and kicker says "Phase 01 · Design Phase" — semantically duplicated, immediately reads as AI-generated.

**Correct approach**: chrome is a **column label** (stable, reusable across pages); kicker is **this page's hook** (short, dramatic). They complement each other, never translate each other.

### Theme Rhythm Planning (Required — Do Before Generating)

**Core mechanism**: Each page `<section>` must carry `light` / `dark` / `hero light` / `hero dark`. JS infers the theme from class and decides whether to add `light-bg` to body, switching which WebGL canvas is in front. Missing theme or custom names = fallback error.

#### Default Theme by Layout

| Layout | Default Theme | Reason |
|--------|--------------|--------|
| 1. Opening Cover | `hero dark` | Ceremonial impact, dark base |
| 2. Act Divider | `hero dark` and `hero light` **must alternate** | Breathing rhythm |
| 3. Big Numbers (Data) | `light` | Numbers need paper-white; occasionally `dark` in multi-act runs |
| 4. Left-Text Right-Image | **`light` / `dark` alternating** | Main body rhythm driver |
| 5. Image Grid | `light` | Screenshots need bright background |
| 6. Pipeline | `light` | Flowcharts need clarity |
| 7. Question Page | `hero dark` | Strong visual impact by default |
| 8. Big Quote | **`dark` preferred**, occasionally `light` | Key quotes need dark ceremonial feel |
| 9. Comparison Page | `light` | Dual columns need clarity |
| 10. Text-Image Mixed | **`light` / `dark` alternating** | Rhythm |

#### Rhythm Hard Rules (Self-check After Generating)

- **FORBIDDEN**: 3+ consecutive pages with the same theme (including light stacking and dark stacking)
- **FORBIDDEN**: Decks with 8+ pages without at least 1 `hero dark` + 1 `hero light`
- **FORBIDDEN**: Entire deck with only `light` body pages and no `dark` body pages — flat and breathless
- **RECOMMENDED**: Insert 1 hero page every 3-4 body pages (cover/divider/question/quote)

#### 8-Page Rhythm Template (Ready to Use)

| Page | Theme | Layout | Notes |
|------|-------|--------|-------|
| 1 | `hero dark` | Cover | Opening |
| 2 | `light` | Big Numbers | Data punch |
| 3 | `dark` | Left-Text Right-Image | Contrast/story |
| 4 | `light` | Pipeline | Process |
| 5 | `hero light` | Act Divider | Breathing |
| 6 | `dark` | Left-Text Right-Image or Big Quote | |
| 7 | `hero dark` | Question Page | Suspense close |
| 8 | `light` | Big Quote / Ending | Wrap up |

**Draw this table first, then start writing slides.** Skipping rhythm planning = all light pages.

---

## Layout 1: Opening Cover (Hero Cover)

```html
<section class="slide hero dark">
  <div class="chrome">
    <div>A Talk · 2026.04.22</div>
    <div>Vol.01</div>
  </div>
  <div class="frame" style="display:grid; gap:4vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Private Session · Speaker Name</div>
    <h1 class="h-hero" data-anim>Main Title</h1>
    <h2 class="h-sub" data-anim>Subtitle Line</h2>
    <p class="lead" style="max-width:60vw" data-anim>
      A compelling one-sentence description of the talk's premise and what makes it worth watching.
    </p>
    <div class="meta-row" data-anim>
      <span>Author Name</span><span>·</span><span>Title / Affiliation</span>
    </div>
  </div>
  <div class="foot">
    <div>A talk about Topic · Domain · Theme</div>
    <div>— 2026 —</div>
  </div>
</section>
```

**Key points**:
- Use `hero dark` to let WebGL background show through most of the area
- `h-hero` is the largest font size (10vw), used as the title hero visual
- Use `min-height:80vh + align-content:center` to vertically center all content
- No page numbers needed in `.chrome` — cover page stands alone

---

## Layout 2: Act Divider (Chapter Cover)

```html
<section class="slide hero light">
  <div class="chrome">
    <div>Act One · Hard Data</div>
    <div>Act I · 01 / 25</div>
  </div>
  <div class="frame" style="display:grid; gap:6vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Act I</div>
    <h1 class="h-hero" style="font-size:8.5vw" data-anim>Hard Data</h1>
    <p class="lead" style="max-width:55vw" data-anim>
      Numbers first, methods second.
    </p>
  </div>
  <div class="foot">
    <div>Act One Introduction</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Ultra-minimal: only kicker + large title + one-line lead
- Alternate between `hero light` / `hero dark` across act covers to create rhythm
- `h-hero` font size can be adjusted from 10vw to 8.5vw for longer titles

---

## Layout 3: Big Numbers Grid (Data Billboard)

```html
<section class="slide light">
  <div class="chrome">
    <div>Past 64 Days · Development</div>
    <div>Act I / Dev · 02 / 25</div>
  </div>
  <div class="frame" style="padding-top:6vh">
    <div class="kicker" data-anim>What one person built.</div>
    <h2 class="h-xl" data-anim>Past 64 Days</h2>
    <p class="lead" style="margin-bottom:5vh" data-anim>From zero to open-source product.</p>

    <div class="grid-6" style="margin-top:6vh">
      <div class="stat-card" data-anim>
        <div class="stat-label">Duration</div>
        <div class="stat-nb">64 <span class="stat-unit">days</span></div>
        <div class="stat-note">From scratch to now</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">Lines of Code</div>
        <div class="stat-nb">110K+</div>
        <div class="stat-note">Written line by line</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">GitHub Stars</div>
        <div class="stat-nb">5,166</div>
        <div class="stat-note">One open-source repo</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">Downloads</div>
        <div class="stat-nb">41K+</div>
        <div class="stat-note">Installed on tens of thousands of machines</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">AI Providers</div>
        <div class="stat-nb">19</div>
        <div class="stat-note">Cross-platform integration</div>
      </div>
      <div class="stat-card" data-anim>
        <div class="stat-label">Commits</div>
        <div class="stat-nb">608+</div>
        <div class="stat-note">No collaborators</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Project · CodePilot | github.com/codepilot</div>
    <div>Act I · Dev Numbers</div>
  </div>
</section>
```

**Key points**:
- 3×2 or 4×2 grid works best (see `.grid-6`)
- Each `stat-card` has a fixed structure: label (monospace small text) → nb (large number) → note (description)
- Numbers should be 2-3 characters (too long will overflow); use K / M abbreviations
- Leave 5vh+ top buffer so the title area captures attention first

---

## Layout 4: Left-Text Right-Image (Quote + Image)

```html
<section class="slide light">
  <div class="chrome">
    <div>The Identity Twist</div>
    <div>03 / 25</div>
  </div>
  <div class="frame grid-2-7-5" style="padding-top:6vh">
    <!-- Left column: title + body + callout, flex column lets callout stick to column bottom -->
    <div style="display:flex; flex-direction:column; justify-content:space-between; gap:3vh">
      <div>
        <div class="kicker" data-anim>BUT</div>
        <h2 class="h-xl" style="white-space:nowrap; font-size:7.2vw" data-anim>
          I'm not a programmer.
        </h2>
        <p class="lead" style="margin-top:3vh" data-anim>
          Haven't written a single line of code since graduating. The past decade was UI design and AI effects.
        </p>
      </div>
      <div class="callout" data-anim>
        "This would have taken<br>
        a ten-person team a full year,<br>
        just three years ago."
        <div class="callout-src">— An observer's assessment</div>
      </div>
    </div>
    <!-- Right column: image with standard 16/10 ratio + max-height, no align-self:end -->
    <figure class="frame-img" style="aspect-ratio:16/10; max-height:56vh" data-anim>
      <img src="images/product.png" alt="Product screenshot">
      <figcaption class="img-cap">Product · Screenshot</figcaption>
    </figure>
  </div>
  <div class="foot">
    <div>Page 03 · The Twist</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Use `grid-2-7-5` (left 7 parts, right 5 parts), `align-items:start` is preset in template
- **Left column** uses flex column + `justify-content:space-between`: title sticks to top, callout naturally sticks to bottom
- **Right column image** — **do NOT add `align-self:end`**. It causes the image to slide to cell bottom, gets obscured by browser toolbar on low-res screens
- Image must use **standard ratio 16/10 or 4/3 + `max-height:56vh`** — never raw image ratios

---

## Layout 5: Image Grid (Multi-Image Comparison)

```html
<section class="slide light">
  <div class="chrome">
    <div>Platform Proof</div>
    <div>Act I / Ops · 05 / 27</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker" data-anim>Proof · Evidence</div>
    <h2 class="h-xl" data-anim>10 Platforms · 6 Screenshots</h2>

    <div class="grid-3-3" style="margin-top:4vh">
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-1.png" alt="Platform 1 · 289K">
        <figcaption class="img-cap">Platform 1 · 289K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-2.png" alt="Platform 2 · 137K">
        <figcaption class="img-cap">Platform 2 · 137K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-3.png" alt="Platform 3 · 96K">
        <figcaption class="img-cap">Platform 3 · 96K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-4.png" alt="Platform 4 · 26K">
        <figcaption class="img-cap">Platform 4 · 26K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-5.png" alt="Platform 5 · 19K">
        <figcaption class="img-cap">Platform 5 · 19K</figcaption>
      </figure>
      <figure class="frame-img" style="height:26vh" data-anim>
        <img src="images/platform-6.png" alt="Platform 6 · 10K">
        <figcaption class="img-cap">Platform 6 · 10K</figcaption>
      </figure>
    </div>
  </div>
  <div class="foot">
    <div>Screenshot Date · 2026.04</div>
    <div>Page 05 · Evidence</div>
  </div>
</section>
```

**Key points**:
- Critical: each `frame-img` must have a fixed `height:NNvh` (do NOT use `aspect-ratio`) or the grid will overflow
- Images auto-apply `object-fit:cover + object-position:top`, cropping bottom only
- Use `.grid-3-3` (3×2) or `.grid-3` (3×1) as container

---

## Layout 6: Pipeline (Two-Column Flow)

```html
<section class="slide light" data-animate="pipeline">
  <div class="chrome">
    <div>My Workflow</div>
    <div>Act II · 15 / 27</div>
  </div>
  <div class="frame">
    <div class="kicker">Pipeline · Workflow</div>
    <h2 class="h-xl">Two Pipelines</h2>

    <!-- Group 1: Text Pipeline -->
    <div class="pipeline-section">
      <div class="pipeline-label">Text Pipeline</div>
      <div class="pipeline">
        <div class="step" data-anim="step">
          <div class="step-nb">01</div>
          <div class="step-title">Draft</div>
          <div class="step-desc">AI drafts the initial version</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">02</div>
          <div class="step-title">Polish</div>
          <div class="step-desc">AI refines and removes AI-ness</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">03</div>
          <div class="step-title">Morph</div>
          <div class="step-desc">AI adapts for Twitter / LinkedIn</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">04</div>
          <div class="step-title">Illustrate</div>
          <div class="step-desc">AI generates infographics</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">05</div>
          <div class="step-title">Distribute</div>
          <div class="step-desc">One-click publish to 9 platforms</div>
        </div>
      </div>
    </div>

    <!-- Group 2: Video Pipeline -->
    <div class="pipeline-section">
      <div class="pipeline-label">Visual · Video Pipeline</div>
      <div class="pipeline">
        <div class="step" data-anim="step">
          <div class="step-nb">06</div>
          <div class="step-title">Cut</div>
          <div class="step-desc">AI handles editing</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">07</div>
          <div class="step-title">Wrap</div>
          <div class="step-desc">AI handles packaging</div>
        </div>
        <div class="step" data-anim="step">
          <div class="step-nb">08</div>
          <div class="step-title">Cover</div>
          <div class="step-desc">AI generates thumbnails</div>
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 15 · Content Factory</div>
    <div>Workflow</div>
  </div>
</section>
```

**Key points**:
- Use `.pipeline-section` for grouping + `.pipeline-label` for group titles
- Groups separated by 3.6vh spacing + top dashed border (preset in CSS)
- Each step has a fixed structure: nb → title → desc
- Max ~5 steps per pipeline row; overflow into a second pipeline group
- **Animation**: `<section>` gets `data-animate="pipeline"`, each `.step` gets `data-anim="step"`. Steps start at `opacity:.15` on page entry; press →/Space/scroll to light them up one-by-one; **all steps must be revealed before the page advances** — creates interactive presentation feel

---

## Layout 7: Hero Question (Suspense Close)

```html
<section class="slide hero dark">
  <div class="chrome">
    <div>A Question For You</div>
    <div>24 / 27</div>
  </div>
  <div class="frame" style="display:grid; gap:8vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>The Question</div>
    <h1 class="h-hero" style="font-size:7vw; line-height:1.15">
      <span data-anim style="display:block">Which roles in your company</span>
      <span data-anim style="display:block">were never meant</span>
      <span data-anim style="display:block">to be done by humans?</span>
    </h1>
    <p class="lead" style="max-width:50vw" data-anim>
      This isn't a technology question. It's an architecture question.
    </p>
  </div>
  <div class="foot">
    <div>Page 24 · The Question</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Hero pages should have maximum whitespace — only one question
- `h-hero` font size adjusts by length: 7vw for 3 lines, 10vw for 1 line
- Use `<span style="display:block">` for manual line breaks at semantic points
- Optionally add a `lead` line at the end as the reveal

---

## Layout 8: Big Quote (Serif Key Quote)

```html
<section class="slide light" data-animate="quote">
  <div class="chrome">
    <div>The Takeaway · Key Quote</div>
    <div>18 / 25</div>
  </div>
  <div class="frame" style="display:grid; gap:5vh; align-content:center; min-height:80vh">
    <div class="kicker" data-anim>Quote</div>
    <blockquote style="font-family:var(--serif-en); font-weight:700; font-size:5.8vw; line-height:1.2; letter-spacing:-.01em; max-width:72vw">
      <span data-anim="line" style="display:block">"Without the handoff,</span>
      <span data-anim="line" style="display:block">everyone builds."</span>
    </blockquote>
    <p class="lead" style="max-width:55vw; opacity:.65" data-anim>
      And that makes all the difference.
    </p>
    <div class="meta-row" data-anim>
      <span>— Luke Wroblewski</span><span>·</span><span>2026.04.16</span>
    </div>
  </div>
  <div class="foot">
    <div>Page 18 · Key Quote</div>
    <div>— · —</div>
  </div>
</section>
```

**Key points**:
- Full-page whitespace, only a big quote + attribution
- `<blockquote>` uses inline style for enlargement (5-6vw) — do NOT use `h-hero` (that's reserved for page main titles)
- Follow with a secondary line (lead · opacity:.65) to create hierarchy
- Use `meta-row` for attribution + date

---

## Layout 9: Side-by-Side Comparison (Before vs After)

```html
<section class="slide light" data-animate="directional">
  <div class="chrome">
    <div>Old vs New · The Shift</div>
    <div>12 / 25</div>
  </div>
  <div class="frame" style="padding-top:5vh">
    <div class="kicker" data-anim>Before / After · Paradigm Shift</div>
    <h2 class="h-xl" style="margin-bottom:4vh" data-anim>From Handoff to Co-building</h2>

    <div class="grid-2-6-6" style="gap:5vw 4vh">
      <!-- Left column: Before -->
      <div data-anim="left" style="padding:3vh 2vw; border-left:3px solid currentColor; opacity:.55">
        <div class="kicker" style="opacity:.9">Before · Old Model</div>
        <h3 class="h-md" style="margin-top:2vh">Design → Develop → Handoff</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-cjk); font-size:max(14px,1.1vw); line-height:1.55">
          <li>Designer creates mockups in Figma</li>
          <li>Developer translates pixels from file</li>
          <li>Repeated PR alignment rounds</li>
          <li>Non-technical people can't touch code</li>
        </ul>
      </div>
      <!-- Right column: After -->
      <div data-anim="right" style="padding:3vh 2vw; border-left:3px solid currentColor">
        <div class="kicker" style="opacity:.9">After · New Model</div>
        <h3 class="h-md" style="margin-top:2vh">Same Tool · Parallel · Co-build</h3>
        <ul style="margin-top:3vh; padding-left:1.2em; display:flex; flex-direction:column; gap:1.4vh; font-family:var(--sans-cjk); font-size:max(14px,1.1vw); line-height:1.55">
          <li>Three roles work simultaneously</li>
          <li>agents.md serves as shared context</li>
          <li>Agents handle alignment / conflicts</li>
          <li>Anyone can safely contribute code</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot">
    <div>Page 12 · Paradigm Shift</div>
    <div>Before / After</div>
  </div>
</section>
```

**Key points**:
- Use `.grid-2-6-6` (1:1) for even left-right split
- Left column gets `opacity:.55` to visually de-emphasize "old"; right column stays full brightness for "new"
- Both columns use `border-left:3px solid` + `padding-left` for blockquote feel
- Each column follows unified structure: `kicker` → `h-md` → `<ul>` bullet points, consistent rhythm

---

## Layout 10: Text-Image Mixed (Lead Image + Side Text)

```html
<section class="slide light">
  <div class="chrome">
    <div>Design First</div>
    <div>08 / 16</div>
  </div>
  <div class="frame grid-2-8-4" style="padding-top:6vh">
    <!-- Left column: long-form text + quote -->
    <div>
      <div class="kicker" data-anim>Phase 01 · Design Phase</div>
      <h2 class="h-xl" style="margin-top:1vh; margin-bottom:3vh" data-anim>Design First · 2 Weeks</h2>

      <p class="lead" style="margin-bottom:3vh" data-anim>
        Complete visual exploration and design system in Figma — grids, typography, color tokens, reusable components, desktop and mobile iterations.
      </p>

      <p data-anim style="font-family:var(--sans-cjk); font-size:max(14px,1.15vw); line-height:1.75; opacity:.78; margin-bottom:2.4vh">
        Within two weeks, visual style, rough structure, and directional content all stabilized. This is a solid traditional design process — nothing new here yet.
      </p>

      <div class="callout" style="margin-top:3vh" data-anim>
        "This phase was pretty standard.<br>Just a solid Web design process."
        <div class="callout-src">— Luke Wroblewski</div>
      </div>
    </div>
    <!-- Right column: supplementary image, portrait or square -->
    <figure class="frame-img" style="aspect-ratio:3/4; max-height:60vh" data-anim>
      <img src="images/design-system.png" alt="Design system">
      <figcaption class="img-cap">Figma · Design System</figcaption>
    </figure>
  </div>
  <div class="foot">
    <div>Page 08 · Design First</div>
    <div>~2 weeks</div>
  </div>
</section>
```

**Key points**:
- `.grid-2-8-4` (8:4) gives text the dominant share, image as supplement
- Left column contains multiple information layers: kicker → large title → lead → body paragraph → callout (quote)
- Right column image uses **portrait 3:4** or square 1:1 to avoid competing with left column text for attention
- This layout suits **information-dense pages** (unlike Layout 4 which has only a single key quote)

---

## Appendix: Common Grid Templates

| Class | Ratio | Usage |
|-------|-------|-------|
| `.grid-2-6-6` | 6:6 (1:1) | Even split |
| `.grid-2-7-5` | 7:5 | Text-dominant + supplementary image |
| `.grid-2-8-4` | 8:4 (2:1) | Long-form text + small image/data |
| `.grid-3` | 1:1:1 | 3-item parallel (cases/screenshots) |
| `.grid-3-3` | 3×2 | 6-image matrix |
| `.grid-6` | 3×2 | 6 data cards |

All grids have preset `gap: 3vw 4vh` (horizontal 3vw, vertical 4vh), which can be individually overridden.

---

## Page Rhythm Recommendations

For a 25-30 page presentation, recommended rhythm:

1. **Hero Cover** (page 1)
2. **Act Divider** (act one opening, hero light or hero dark)
3. **Big Numbers** (hard data for initial impact)
4. **Quote + Image** (identity twist / hook)
5. **Image Grid** (evidence)
6. **Hero Question** (act close, suspense)
7. ... Acts two and three follow the same rhythm ...
8. **Hero Close** (final page, question or acknowledgment)

Hero and non-hero pages should alternate at a **2-3 : 1 ratio** — no more than 3 consecutive non-hero pages, no more than 2 consecutive hero pages.
