---
name: clone-website
description: >-
  Reverse-engineer and rebuild any website as a pixel-perfect Next.js 16 clone
  using browser automation (cursor-ide-browser MCP), component-level CSS
  extraction, parallel builder subagents in git worktrees, and visual QA diff.
  Produces a deployable Next.js 16 + shadcn/ui + Tailwind CSS v4 project with
  real assets, exact design tokens, and interaction behaviors.
  Use when the user asks to "clone a website", "replicate a site",
  "rebuild this page", "reverse-engineer this website", "pixel-perfect copy",
  "make a copy of this site", "copy this website", "website cloner",
  "clone-website", or provides a URL with intent to recreate the site.
  Do NOT use for general web scraping without rebuild intent (use scrapling
  or defuddle). Do NOT use for screenshot-only capture (use agent-browser).
  Do NOT use for design token extraction without full rebuild (use
  figma-dev-pipeline). Do NOT use for testing existing web apps (use
  e2e-testing or qa-dogfood).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "development"
  composable_with:
    - agent-browser
    - anthropic-frontend-design
    - visual-explainer
  triggers_korean:
    - "웹사이트 클론"
    - "사이트 복제"
    - "웹사이트 복사"
    - "페이지 재현"
    - "사이트 따라 만들기"
    - "웹 클로닝"
---

# Clone Website

Reverse-engineer and rebuild a target website as a pixel-perfect clone. This is a **foreman on a job site** pattern — as you inspect each section, you write a detailed specification file, then dispatch a specialist builder subagent with everything it needs. Extraction and construction happen in parallel.

## Input

The user provides:
1. **Target URL** — the website to clone (required)
2. **Scope** (optional) — which pages to replicate, fidelity level
3. **Output directory** (optional) — defaults to a new project directory

## Pre-Flight

1. **cursor-ide-browser MCP is required.** Test it immediately by navigating to the target URL. If it is not available, stop and tell the user to enable it — this skill cannot work without browser automation.
2. Create or verify a `TARGET.md` in the project root using the template from [references/target-template.md](references/target-template.md). Fill in the user's URL and scope.
3. Verify the base project builds. The output stack is **Next.js 16 (App Router, React 19, TypeScript strict) + shadcn/ui + Tailwind CSS v4 + Lucide React**. If the scaffold does not exist, create it:

```bash
npx create-next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir --use-npm
cd <project-name>
npx shadcn@latest init -d
```

4. Create output directories: `docs/research/`, `docs/research/components/`, `docs/design-references/`, `scripts/`.

## Guiding Principles

These truths separate a successful clone from a "close enough" mess.

### 1. Completeness Beats Speed

Every builder subagent must receive **everything** it needs: screenshot, exact CSS values from `getComputedStyle()`, downloaded assets with local paths, real text content, component structure. If a builder has to guess anything, extraction failed.

### 2. Small Tasks, Perfect Results

When a subagent gets "build the entire features section," it glosses over details. When it gets a single focused component with exact CSS values, it nails it.

**Complexity budget:** If a builder prompt exceeds ~150 lines of spec content, the section is too complex for one subagent. Break it into smaller pieces.

### 3. Real Content, Real Assets

Extract actual text, images, videos, and SVGs from the live site. This is a clone, not a mockup. Download every `<img>` and `<video>`, extract inline `<svg>` as React components. **Layered assets matter** — a section that looks like one image is often multiple layers (background gradient, foreground PNG, overlay icon). Inspect each container's full DOM tree.

### 4. Foundation First

Nothing can be built until the foundation exists: global CSS with the target's design tokens (colors, fonts, spacing), TypeScript types, and global assets. This is sequential and non-negotiable. Everything after is parallel.

### 5. Extract Appearance AND Behavior

A website is not a screenshot. Elements move, change, appear, and disappear in response to scrolling, hovering, clicking, resizing, and time. Extract **appearance** (exact computed CSS) AND **behavior** (what changes, what triggers it, how the transition happens).

Behaviors to watch for (illustrative, not exhaustive):
- Navbar shrinks/changes on scroll
- Elements animate into view on viewport intersection
- Scroll-snap sections
- Parallax layers
- Hover state transitions (duration, easing)
- Dropdowns, modals, accordions with enter/exit animations
- Auto-playing carousels or cycling content
- Theme transitions between page sections
- Tabbed content that cycles
- Scroll-driven tab/accordion switching (IntersectionObserver)
- Smooth scroll libraries (Lenis, Locomotive Scroll)

### 6. Identify the Interaction Model Before Building

Before building any interactive section, answer: **Is this driven by clicks, scrolls, hovers, time, or a combination?**

1. Don't click first. Scroll slowly and observe if things change.
2. If they do, it's scroll-driven. Extract the mechanism.
3. If nothing changes on scroll, then test click/hover.
4. Document the interaction model explicitly in the component spec.

### 7. Extract Every State, Not Just the Default

For tabbed/stateful content: click each tab via browser MCP, extract content per state, record transitions. For scroll-dependent elements: capture styles at position 0, scroll past trigger, capture again, diff.

### 8. Spec Files Are the Source of Truth

Every component gets a specification file in `docs/research/components/` BEFORE any builder is dispatched. See [references/component-spec-template.md](references/component-spec-template.md) for the template.

### 9. Build Must Always Compile

Every builder subagent must verify `npx tsc --noEmit` passes. After merging worktrees, verify `npm run build` passes.

## Phase 1: Reconnaissance

Navigate to the target URL with `cursor-ide-browser` MCP.

### Screenshots
- Take **full-page screenshots** at desktop (1440px) and mobile (390px) viewports
- Save to `docs/design-references/` with descriptive names

### Global Extraction

**Fonts** — Inspect `<link>` tags for Google Fonts or self-hosted fonts. Check computed `font-family` on key elements. Configure in `src/app/layout.tsx` using `next/font/google` or `next/font/local`.

**Colors** — Extract the site's color palette from computed styles. Update `src/app/globals.css` with the target's actual CSS variables.

**Favicons & Meta** — Download favicons, apple-touch-icons, OG images to `public/seo/`. Update `layout.tsx` metadata.

**Global UI patterns** — Identify site-wide CSS/JS: custom scrollbar hiding, scroll-snap, global keyframe animations, backdrop filters, smooth scroll libraries.

### Asset Discovery Script

Run via `cursor-ide-browser` MCP to enumerate all assets:

```javascript
JSON.stringify({
  images: [...document.querySelectorAll('img')].map(img => ({
    src: img.src || img.currentSrc, alt: img.alt,
    width: img.naturalWidth, height: img.naturalHeight,
    parentClasses: img.parentElement?.className,
    siblings: img.parentElement ? [...img.parentElement.querySelectorAll('img')].length : 0,
    position: getComputedStyle(img).position, zIndex: getComputedStyle(img).zIndex
  })),
  videos: [...document.querySelectorAll('video')].map(v => ({
    src: v.src || v.querySelector('source')?.src,
    poster: v.poster, autoplay: v.autoplay, loop: v.loop, muted: v.muted
  })),
  backgroundImages: [...document.querySelectorAll('*')].filter(el => {
    const bg = getComputedStyle(el).backgroundImage;
    return bg && bg !== 'none';
  }).map(el => ({
    url: getComputedStyle(el).backgroundImage,
    element: el.tagName + '.' + el.className?.split(' ')[0]
  })),
  svgCount: document.querySelectorAll('svg').length,
  fonts: [...new Set([...document.querySelectorAll('*')].slice(0, 200).map(el => getComputedStyle(el).fontFamily))],
  favicons: [...document.querySelectorAll('link[rel*="icon"]')].map(l => ({ href: l.href, sizes: l.sizes?.toString() }))
});
```

### Mandatory Interaction Sweep

After screenshots, before anything else — discover every behavior:

**Scroll sweep:** Scroll top to bottom via browser MCP. At each section, pause and observe header changes, viewport-triggered animations, scroll-snap points, sidebar auto-switching.

**Click sweep:** Click every interactive element (buttons, tabs, pills, links, cards). Record what happens for each.

**Hover sweep:** Hover over buttons, cards, links, images, nav items. Record what changes.

**Responsive sweep:** Test at 1440px, 768px, 390px viewports. Note layout changes and breakpoints.

Save all findings to `docs/research/BEHAVIORS.md`.

### Page Topology

Map every distinct section top to bottom. Document visual order, fixed/sticky overlays, page layout, dependencies, interaction models. Save as `docs/research/PAGE_TOPOLOGY.md`.

## Phase 2: Foundation Build

Sequential (not delegated to subagents):

1. Update fonts in `layout.tsx`
2. Update `globals.css` with target's color tokens, spacing, keyframes, scroll behaviors
3. Create TypeScript interfaces in `src/types/`
4. Extract SVG icons as React components in `src/components/icons.tsx`
5. Write and run a Node.js asset download script (`scripts/download-assets.mjs`)
6. Verify: `npm run build` passes

## Phase 3: Component Specification & Dispatch

Core loop for each section in the page topology:

### Step 1: Extract

For each section, use `cursor-ide-browser` MCP to extract:

1. **Screenshot** the section in isolation
2. **Extract CSS** for every element using the per-component extraction script:

```javascript
(function(selector) {
  const el = document.querySelector(selector);
  if (!el) return JSON.stringify({ error: 'Element not found: ' + selector });
  const props = [
    'fontSize','fontWeight','fontFamily','lineHeight','letterSpacing','color',
    'textTransform','textDecoration','backgroundColor','background',
    'padding','paddingTop','paddingRight','paddingBottom','paddingLeft',
    'margin','marginTop','marginRight','marginBottom','marginLeft',
    'width','height','maxWidth','minWidth','maxHeight','minHeight',
    'display','flexDirection','justifyContent','alignItems','gap',
    'gridTemplateColumns','gridTemplateRows',
    'borderRadius','border','borderTop','borderBottom','borderLeft','borderRight',
    'boxShadow','overflow','overflowX','overflowY',
    'position','top','right','bottom','left','zIndex',
    'opacity','transform','transition','cursor',
    'objectFit','objectPosition','mixBlendMode','filter','backdropFilter',
    'whiteSpace','textOverflow','WebkitLineClamp'
  ];
  function extractStyles(element) {
    const cs = getComputedStyle(element);
    const styles = {};
    props.forEach(p => { const v = cs[p]; if (v && v !== 'none' && v !== 'normal' && v !== 'auto' && v !== '0px' && v !== 'rgba(0, 0, 0, 0)') styles[p] = v; });
    return styles;
  }
  function walk(element, depth) {
    if (depth > 4) return null;
    const children = [...element.children];
    return {
      tag: element.tagName.toLowerCase(),
      classes: element.className?.toString().split(' ').slice(0, 5).join(' '),
      text: element.childNodes.length === 1 && element.childNodes[0].nodeType === 3 ? element.textContent.trim().slice(0, 200) : null,
      styles: extractStyles(element),
      images: element.tagName === 'IMG' ? { src: element.src, alt: element.alt, naturalWidth: element.naturalWidth, naturalHeight: element.naturalHeight } : null,
      childCount: children.length,
      children: children.slice(0, 20).map(c => walk(c, depth + 1)).filter(Boolean)
    };
  }
  return JSON.stringify(walk(el, 0), null, 2);
})('SELECTOR');
```

3. **Extract multi-state styles** — capture both states, diff them
4. **Extract real content** — all text, alt attributes, aria labels
5. **Identify assets** — downloaded images/videos, icon components
6. **Assess complexity** — how many distinct sub-components?

### Step 2: Write the Component Spec File

Create a spec file per section/sub-component in `docs/research/components/`. Use the template from [references/component-spec-template.md](references/component-spec-template.md).

### Step 3: Dispatch Builder Subagents

Use the **Task tool** with `subagent_type="best-of-n-runner"` for worktree isolation, or `subagent_type="generalPurpose"` for simpler components.

**Simple section** (1-2 sub-components): One subagent.
**Complex section** (3+ sub-components): One subagent per sub-component, plus one for the wrapper.

Every builder subagent receives:
- Full contents of its component spec file (inline in the prompt)
- Path to the section screenshot
- Which shared components to import
- Target file path
- Instruction to verify with `npx tsc --noEmit`
- Responsive breakpoints and changes

**Don't wait.** Dispatch builders for one section, then move to extracting the next. Builders work in parallel.

### Step 4: Merge

As subagents complete:
- Merge worktree branches into main
- Resolve conflicts
- After each merge: `npm run build`

## Phase 4: Page Assembly

After all sections built and merged, wire everything in `src/app/page.tsx`:
- Import all section components
- Implement page-level layout from topology doc
- Connect real content to props
- Implement page-level behaviors (scroll snap, scroll-driven animations, smooth scroll)
- Verify: `npm run build` passes

## Phase 5: Visual QA Diff

Do NOT declare the clone complete without this pass:

1. Take side-by-side screenshots at desktop (1440px) and mobile (390px)
2. Compare section by section
3. For each discrepancy: check spec → re-extract if spec wrong → fix component if builder wrong
4. Test all interactive behaviors
5. Verify animations, transitions, scroll feel

## Pre-Dispatch Checklist

Before dispatching ANY builder subagent:

- [ ] Spec file written with ALL sections filled
- [ ] Every CSS value is from `getComputedStyle()`, not estimated
- [ ] Interaction model identified (static / click / scroll / time)
- [ ] Stateful components: every state captured
- [ ] Scroll-driven components: trigger, before/after styles, transition recorded
- [ ] Hover states: before/after values and timing recorded
- [ ] All images identified (including overlays and layers)
- [ ] Responsive behavior documented for desktop and mobile
- [ ] Text content verbatim from the site
- [ ] Builder prompt under ~150 lines of spec

## What NOT to Do

- Don't build click-based tabs when the original is scroll-driven (or vice versa)
- Don't extract only the default state
- Don't miss overlay/layered images
- Don't build mockup components for content that is actually video/animation
- Don't approximate CSS — extract exact computed values
- Don't build everything in one monolithic commit
- Don't reference external docs from builder prompts — inline everything
- Don't skip asset extraction
- Don't give a builder subagent too much scope
- Don't bundle unrelated sections into one subagent
- Don't skip responsive extraction
- Don't forget smooth scroll libraries
- Don't dispatch builders without a spec file

## Examples

### Example 1: Full single-page clone

User says: "Clone https://linear.app"

Actions:
1. Navigate to URL with cursor-ide-browser MCP, take full-page screenshots
2. Extract fonts (Inter via Google Fonts), colors (#5E6AD2 primary), favicons
3. Run interaction sweep: sticky nav, scroll-triggered animations, hover effects on cards
4. Map page topology: Hero, Features Grid, Integrations, Testimonials, CTA, Footer
5. Build foundation: layout.tsx fonts, globals.css tokens, download assets
6. For each section: extract CSS, write spec file, dispatch builder subagent
7. Assemble page.tsx, verify `npm run build`
8. Visual QA: side-by-side comparison at 1440px and 390px

Result: Deployable Next.js 16 project replicating the target site's appearance and behavior

### Example 2: Scoped multi-page clone

User says: "Replicate only the pricing and docs pages from stripe.com"

Actions:
1. Create TARGET.md with scope limited to `/pricing` and `/docs`
2. Reconnaissance on both pages — shared nav/footer noted
3. Build foundation with Stripe's design tokens
4. Build shared components first (navbar, footer), then page-specific sections
5. Wire routing in App Router with two page files
6. Visual QA both pages

Result: Two-page Next.js clone with shared layout and page-specific content

## Error Handling

| Error | Action |
|-------|--------|
| cursor-ide-browser MCP unavailable | Stop immediately — skill cannot operate without browser automation. Tell user to enable it in Cursor MCP settings. |
| Target URL returns 403/blocked | Try with different viewport, or ask user for authenticated access or a staging URL |
| `npx create-next-app` fails | Check Node.js version (>= 18 required), verify npm is available |
| Asset download fails (CORS/403) | Try downloading manually via curl with referer header; fall back to placeholder image with TODO comment |
| `npm run build` fails after merge | Check TypeScript errors with `npx tsc --noEmit`, resolve import conflicts from parallel worktrees |
| Builder subagent produces incorrect output | Re-read spec file, verify CSS values were from `getComputedStyle()` not estimated, re-dispatch with corrected spec |
| Scroll-driven behavior not captured | Re-run interaction sweep with slower scroll speed, capture at multiple scroll positions |
| Site uses anti-bot/Cloudflare protection | Ask user for alternative access (staging URL, local dev server, or pre-captured HAR file) |

## Completion

When done, report:
- Total sections built
- Total components created
- Total spec files written
- Total assets downloaded
- Build status (`npm run build` result)
- Visual QA results
- Known gaps or limitations

## References

- [Inspection Guide](references/inspection-guide.md)
- [Component Spec Template](references/component-spec-template.md)
- [Target Template](references/target-template.md)
