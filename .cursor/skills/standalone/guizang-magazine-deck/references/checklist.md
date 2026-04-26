# Quality Checklist

This checklist comes from real iteration cycles. Every item is a lesson learned from actual mistakes, sorted by importance.

Read through once before generating; self-check each item after generating.

---

## P0 — Must Not Violate

### 0. Pre-generation Class Name Validation (Most Important)

**Symptom**: Pasting layout skeletons from layouts.md into a new HTML file results in completely broken styles — titles render in sans-serif, big number data looks like body text, pipeline pages collapse into a single block, images pile at browser bottom.

**Root cause**: If `template.html`'s `<style>` block doesn't define these classes, the browser falls back to defaults.

**Fix**:
- **Before generating, Read `assets/template.html`** and confirm all classes used in layouts.md are defined
- Most commonly missing classes: `h-hero / h-xl / h-sub / h-md / lead / meta-row / stat-card / stat-label / stat-nb / stat-unit / stat-note / pipeline-section / pipeline-label / pipeline / step / step-nb / step-title / step-desc / grid-2-7-5 / grid-2-6-6 / grid-2-8-4 / grid-3-3 / frame / img-cap / callout-src`
- If a class is genuinely missing, **add it to template.html's `<style>` block** — don't rewrite inline on every page
- After generating, open in browser: if you see "title in sans-serif" or "pipeline steps squished in one line" — it's almost certainly this issue

### 1. No Emoji as Icons

**Symptom**: Using emoji (fire, lightbulb, checkmark, etc.) in a magazine-style deck immediately destroys the aesthetic.

**Fix**: Use Lucide icon library via CDN:

```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
...
<i data-lucide="target" class="ico-md"></i>
...
<script>lucide.createIcons();</script>
```

Common icon names: `target / palette / search-check / compass / share-2 / crown / check-circle / x-circle / plus / arrow-right / grid-2x2 / network`

### 2. Images May Only Crop Bottom — Never Left/Right/Top

**Symptom**: Using `aspect-ratio` stretches images; grids stack or crop key identity areas (like the title bar at the top of screenshots).

**Fix**: Image containers use **fixed height + overflow hidden**, images use `object-fit:cover + object-position:top`:

```html
<figure class="frame-img" style="height:26vh">
  <img src="screenshot.png">
</figure>
```

CSS `.frame-img img` already presets `object-position:top` — crops bottom only.

**Never use this pattern** (overflows in grids):
```html
<!-- Bad example -->
<figure class="frame-img" style="aspect-ratio: 16/9">...</figure>
```

**Exception**: Single hero visual (not inside a grid) can use `aspect-ratio + max-height` since the parent container provides bounds.

### 2b. Light Pages with Dark WebGL = Washed Out Gray (Theme Switching Not Working)

**Symptom**: All light pages have a grayish overlay, even hero light pages look muddy.

**Root cause**: JS switches canvas opacity based on slide theme. If the deck starts with hero dark and nothing triggers the light-bg switch, body never gets `light-bg` class, `canvas#bg-dark` stays on top forever.

**Fix**:
- The template's `go()` function infers theme from `classList` (`light` / `dark`), so **slides must explicitly carry `light` or `dark` class**. Don't omit it, and don't use custom theme names
- Hero pages use `hero light` / `hero dark`; body pages use `light` / `dark`. Writing just `hero` without a theme is broken
- A deck must have at least one **non-hero light page** to ensure body gets `light-bg` at some point

### 2b-2. Entire Deck is All Light — No Rhythm

**Symptom**: Except for the `hero dark` cover, every other page defaults to `light` — visually flat, no breathing, wall-of-white.

**Root cause**: Layout skeletons in layouts.md default to `light`; if you just paste skeletons without adjusting themes, everything stays bright.

**Fix**:
- **Draw a "theme rhythm table" before generating**: write out `hero dark` / `hero light` / `light` / `dark` for each page, then align before coding
- **Hard rules**: 3+ consecutive same-theme pages = forbidden; 8+ page decks must have ≥1 `hero dark` + ≥1 `hero light`; can't be all `light` body pages — must include `dark` body pages
- **Choose theme by layout** (see layouts.md "Theme Rhythm Planning"):
  - Left-Text Right-Image (Layout 4), Big Quote (Layout 8), Text-Image Mixed (Layout 10) → **`light` / `dark` alternating**
  - Big Numbers, Image Grid, Pipeline, Comparison → `light` (screenshots/numbers/flowcharts need bright background)
  - Cover, Question Page → `hero dark`
  - Act Dividers → `hero dark` and `hero light` alternating
- **Post-generation check**: `grep 'class="slide' index.html`, visually confirm alternation

### 2c. Chrome and Kicker Must Not Say the Same Thing

**Symptom**: Top-left `.chrome` says "Design First" and same page `.kicker` says "Phase 01 · Design Phase" — synonymous translation, immediately reads as AI-generated.

**Fix**:
- **chrome = magazine header / nav label**: can repeat across pages (e.g., "Act II · Workflow", "Data · Result")
- **kicker = this page's unique hook**: short, has tension, is the title's "small prefix" (e.g., "BUT", "The Question")
- One describes the column, the other describes this page — never translate each other

### 3. Large Title Font Size Must Not Exceed Screen Width / Character Count

**Symptom**: Title font size set too large (e.g., 13vw) results in 1 character per line with ugly forced line breaks.

**Fix**:
- `h-hero` (largest): 10vw, **and title length ≤ 5 characters**
- `h-xl` (second largest): 6vw-7vw
- Long titles use `<br>` for manual line breaks — don't rely on auto-wrap
- Add `white-space:nowrap` when necessary

**Example**: "I'm not a programmer." (short) uses `h-xl` 7.2vw + nowrap, fits on one line.

### 4. Font Division: Titles in Serif, Body in Sans-Serif

**Fix**:
- Titles, key quotes, large numbers → **serif fonts** (Noto Serif SC + Playfair Display + Source Serif)
- Body text, descriptions, pipeline step names → **sans-serif fonts** (Noto Sans SC + Inter)
- Metadata, code, labels → **monospace fonts** (IBM Plex Mono + JetBrains Mono)

All fonts imported via Google Fonts CDN, preset in template.

### 4b. Do NOT Use `align-self:end` to Bottom-Align Images

**Symptom**: In left-text right-image layouts, adding `align-self:end` on `<figure>` to bottom-align with left-column callout causes:
- If parent isn't grid (e.g., class name undefined), `align-self` is completely ignored, image drops to document flow bottom behind browser toolbar
- Even with grid, image sticks to cell bottom, gets obscured by `.foot` and `#nav` dots on low-res screens

**Fix**:
- Text-image layouts **must use `.frame.grid-2-7-5`** (or `.grid-2-6-6`/`.grid-2-8-4`)
- Right column `<figure class="frame-img">` uses **standard ratio 16/10 or 4/3 + max-height:56vh**, naturally sticks to top
- To make left-column callout appear "bottom-aligned", add flex column + `justify-content:space-between` to the **left column** — don't modify the right column

### 4c. Do NOT Use Raw Image Aspect Ratios

**Symptom**: `aspect-ratio: 2592/1798` copied from the original image creates unpredictable whitespace or overflow across different screens.

**Fix**: Regardless of original ratio, use standard ratios only: **16/10 / 4/3 / 3/2 / 1/1 / 16/9**. Images auto-apply `object-fit:cover + object-position:top` — top preserved, bottom cropped slightly with no harm.

### 5. No Heavy Borders or Shadows on Images

**Symptom**: Adding strong shadows or black borders for "premium feel" instantly turns it into a corporate PowerPoint.

**Fix**: Maximum 1-4px subtle rounded corners + **very faint base noise** (already in template). No `box-shadow`, no `border` (except 1px very light gray).

---

## P1 — Layout Rhythm

### 6. Hero and Non-Hero Pages Must Alternate

**Recommended rhythm** (25-30 pages):
```
Hero Cover → Act Divider (hero) → 3-4 pages non-hero → Act Divider (hero)
→ 4-5 pages non-hero → Hero Question → ... → Hero Close
```

2+ consecutive hero pages cause fatigue; 4+ consecutive non-hero pages kill the rhythm.

### 7. Big Number Pages and Dense Pages Must Alternate

Big number pages (big numbers / hero question) and dense pages (pipeline / image grid) should alternate — keeps eyes from tiring.

### 8. Consistent English/Local Language Usage for Same Concepts

**Symptom**: Switching between "Skills", the translated term, and a hybrid phrase inconsistently throughout the deck.

**Fix**:
- Terms should preferably use **English words** (Skills / Harness / Pipeline / Workflow) — familiar to technical audiences
- **Don't force translations** — forced translations often sound more awkward
- One word = one spelling throughout the entire deck

### 9. Bottom Chrome Page Numbers Must Be Consistent

Use `XX / Total` format (e.g., `05 / 27`). **Don't add dynamic page numbers in the top right** (conflicts with `.chrome`).

### 9b. Animation System: Every Page Needs data-anim Markers

**Symptom**: After generating, opening in browser shows content appearing all at once ("pop") on page flip — no rhythm, magazine aesthetic relies entirely on typography with no layered reveal ceremony.

**Root cause**: No `data-anim` attributes on any elements — Motion One finds nothing to animate, entire page renders statically.

**Fix**:
- All body pages: **at minimum add `data-anim` to kicker / main title / lead / callout / stat-card / figure leaf elements**
- **Hero pages** (cover/divider/question/ending): all core blocks (kicker + large title + lead + meta-row) need it
- **Pages without special recipe**: add nothing extra, default cascade looks great
- **4 page types needing special recipe**: must add corresponding `data-animate` on `<section>`
  - Big Quote → `data-animate="quote"` + each line `<span data-anim="line" style="display:block">`
  - Before/After Comparison → `data-animate="directional"` + left column `data-anim="left"` + right column `data-anim="right"`
  - Pipeline → `data-animate="pipeline"` + each step `data-anim="step"`
  - Hero pages (auto-use hero recipe, but still need `data-anim` on elements)

**Self-check**: `grep -c 'data-anim' index.html` should show dozens of matches. Single digits means markers were missed.

### 9c. Pipeline Pages MUST Have data-animate="pipeline"

**Symptom**: Pipeline page fades in all at once, losing the "step-by-step narration" rhythm. But flipping away only goes forward — can't return to individual steps.

**Fix**: Layout 6's `<section>` must have `data-animate="pipeline"`. During presentation, pressing →/Space/scroll-down **lights up steps one by one**; only after all steps are lit does → advance to the next page. This pacing is intentional, not a bug.

---

## P2 — Visual Polish

### 10. WebGL Background Overlay Opacity

**dark hero**: overlay 12-15% (WebGL clearly visible)
**light hero**: overlay 16-20% (WebGL subtly present, doesn't overpower text)
**Regular light/dark pages**: overlay 92-95% (nearly opaque)

If a page has very little text (hero question), overlay can be even thinner; if body text is dense, overlay must be thicker for readability.

### 11. Light Hero Shader Must Not Have Strong Center Point

**Symptom**: Spiral Vortex, radial ripples on light theme are too eye-catching — looks like a Windows 98 screensaver.

**Fix**: Light hero uses FBM domain-warp driven centerless flow, base color stays silver/paper (close to #F0F0F0 / #FBF8F3), rainbow tinting stays subtle (0.05 or below).

### 12. Dark Hero Allows More Visual Impact

Dark hero can use Holographic Dispersion (titanium dispersion) and other centered-structure shaders — dark backgrounds accommodate more visual information.

### 13. Left-Text Right-Image Alignment

- Left column text group `justify-content:space-between`: title sticks to top, quote block sticks to bottom
- Right column image `align-self:end`: aligns with left column's bottom element
- Grid overall `align-items:start` (not `center` / `end`)

### 14. Subtle Image Border Radius

All `.frame-img` and `.frame-img img` get `border-radius:4px` — visually "softened" but not soft. **Do not exceed 8px** or it looks like a consumer app UI.

---

## P3 — Operational Details

### 15. Image Paths Use Relative Paths

Images go in an `images/` folder, HTML uses relative paths `images/xxx.png` — no absolute paths.

### 16. Page Numbers in `.chrome` Are Hardcoded

JS dynamically calculates total pages and extends bottom navigation dots, but `.chrome`'s `XX / N` is hardcoded. Update N manually when adding/removing pages.

### 17. Keep Navigation Intact

Template defaults support: ← → / scroll wheel / touch swipe / bottom dots / Home·End. Do not delete navigation logic from the JS.

### 18. Don't Use `height:100vh` — Use `min-height:80vh`

`100vh` makes content exactly fill the screen, but browser toolbars and tab bars consume some height, causing content overflow. Use `min-height:80vh + align-content:center` for stability.

---

## Final Self-Check Checklist

After generating the deck, check each item:

```
Pre-check (before generating)
  □ Read template.html's <style>, confirmed all needed classes exist
  □ Decided which Layout (1-10) for each page
  □ Drew a "theme rhythm table": each page explicitly hero dark / hero light / light / dark
  □ Rhythm table meets hard rules: no 3 consecutive same theme / has ≥1 hero dark + ≥1 hero light (8+ pages) / at least 1 dark body page
  □ <title> changed to actual deck title (grep "[Required]" should return nothing)

Content
  □ Page count per act is balanced (not front-heavy)
  □ No emoji used as icons
  □ Terminology usage is consistent throughout
  □ Each page has clear kicker + title + body three-level information hierarchy

Layout
  □ No large titles with 1-character-per-line forced wrapping
  □ Image grids use height:Nvh not aspect-ratio
  □ Images only crop bottom — top and sides are intact
  □ Serif/sans-serif font division follows template rules
  □ Pipeline groups have clear separation between them

Visual
  □ Hero and non-hero pages alternate
  □ WebGL background visible on hero pages
  □ Images have subtle rounded corners
  □ No heavy shadows or borders

Interaction
  □ ← → page flip works normally
  □ Bottom dot count matches total page count
  □ Chrome page numbers match actual page numbers
  □ ESC key triggers index view (if retained)

Animation
  □ assets/motion.min.js exists (local fallback)
  □ Page transitions show elements fading in one-by-one, not appearing all at once
  □ Big Quote page <section> has data-animate="quote", each line has <span data-anim="line">
  □ Before/After page <section> has data-animate="directional", left/right columns marked left/right
  □ Pipeline page <section> has data-animate="pipeline", each step has data-anim="step"
  □ grep -c 'data-anim' index.html count ≥ page count × 3 (average 3+ markers per page)
```

All items checked = a passing deck.
