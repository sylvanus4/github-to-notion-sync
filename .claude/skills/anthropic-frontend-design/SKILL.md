---
name: anthropic-frontend-design
description: >-
  Create distinctive, production-grade frontend interfaces with high design
  quality. Use when building web components, pages, dashboards, React
  components, HTML/CSS layouts, websites, landing pages, or
  styling/beautifying web UI. Generates creative, polished code that avoids
  generic AI aesthetics. Do NOT use for frontend code review (use
  frontend-expert) or UX audits (use ux-expert). Korean triggers: "프론트엔드 디자인",
  "UI 구현", "웹 디자인".
disable-model-invocation: true
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Context Gathering Protocol

Before writing a single line of code, gather or infer answers to these questions. Ask the user if the answers are ambiguous.

1. **Purpose & Audience** — What problem does this interface solve? Who uses it and in what context?
2. **Design Direction** — What aesthetic tone should this convey? (brutally minimal, maximalist, retro-futuristic, organic/natural, luxury/refined, playful, editorial/magazine, brutalist/raw, art deco, soft/pastel, industrial, etc.)
3. **Technical Constraints** — Framework, browser support, performance budget, SSR vs CSR.
4. **Reference Points** — Any existing designs, brand guidelines, competitor UIs, or mood boards to draw from?
5. **Scope Boundaries** — Single component, full page, multi-page app? What must NOT be built?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity. The one thing someone should remember about this design is _________.

## The AI Slop Test

Before delivering, run this self-check. If you answer "yes" to 3+, you've produced AI slop:

- [ ] Could this be any other project's UI with different text?
- [ ] Are you using Inter, Roboto, or Space Grotesk?
- [ ] Is the color scheme purple/blue gradient on white?
- [ ] Are all corners the same border-radius?
- [ ] Is every section the same height with centered text?
- [ ] Would it look the same if you shuffled the sections?
- [ ] Did you use a card grid as the default layout?
- [ ] Are all animations generic fade-ins?

## Frontend Aesthetics Guidelines

### Typography
→ See `references/typography.md` for full guidelines.

**DO**: Choose distinctive, characterful fonts. Pair a display font with a refined body font. Use `font-display: swap`. Use `rem`/`em` for sizing. Apply OpenType features (`tabular-nums`, `font-kerning`). Use fluid type via `clamp()` for marketing pages.

**DON'T**: Use Inter, Roboto, Arial, Open Sans, or Lato as primary fonts. Use more than 2-3 font families. Use `px` for body text. Disable user zoom. Skip fallback font definitions.

### Color & Theme
→ See `references/color-and-contrast.md` for full guidelines.

**DO**: Use OKLCH color space for perceptual uniformity. Use tinted neutrals (add brand hue at chroma 0.01). Follow 60-30-10 rule. Define semantic color tokens. Meet WCAG AA contrast ratios (4.5:1 body text, 3:1 UI components). Desaturate accents in dark mode.

**DON'T**: Use pure gray (#888) or pure black (#000) for large areas. Rely on color alone for meaning. Use purple gradients on white as default. Use heavy alpha transparency instead of explicit palette values.

### Spatial Design
→ See `references/spatial-design.md` for full guidelines.

**DO**: Use 4pt spacing base. Name tokens semantically. Use `gap` for sibling spacing. Use container queries for component layouts. Apply the squint test for hierarchy. Design generous white space OR controlled density.

**DON'T**: Use arbitrary spacing outside your scale. Default to card grids for everything. Nest cards inside cards. Make all spacing equal. Create hierarchy through size alone.

### Motion Design
→ See `references/motion-design.md` for full guidelines.

**DO**: Follow the 100/300/500ms duration rule. Use exponential ease-out for entrances, ease-in for exits. Animate only `transform` and `opacity`. Stagger list animations. Respect `prefers-reduced-motion`. One well-orchestrated page load beats scattered micro-interactions.

**DON'T**: Animate `width`, `height`, `top`, `left`, or `margin`. Use bounce/elastic curves (they feel dated). Use `ease` (it's a compromise). Exceed 500ms for UI feedback. Use animation to hide slow loading.

### Interaction Design
→ See `references/interaction-design.md` for full guidelines.

**DO**: Design all 8 interactive states (default, hover, focus, active, disabled, loading, error, success). Use `:focus-visible` for keyboard-only focus rings. Validate forms on blur. Use `<dialog>` for modals. Use Popover API for dropdowns. Prefer undo over confirmation dialogs.

**DON'T**: Remove `outline` without replacement. Use placeholder text as labels. Create touch targets under 44px. Rely on hover for critical functionality. Use arbitrary z-index values.

### Responsive Design
→ See `references/responsive-design.md` for full guidelines.

**DO**: Write mobile-first CSS (`min-width` queries). Use content-driven breakpoints. Detect input with `pointer`/`hover` media queries. Handle safe areas with `env()`. Use `srcset` and `<picture>` for images. Test on real devices.

**DON'T**: Use desktop-first CSS. Hardcode device breakpoints. Assume all mobile devices are slow. Trust DevTools alone for testing.

### UX Writing
→ See `references/ux-writing.md` for full guidelines.

**DO**: Use specific verb + object for buttons ("Save changes", not "OK"). Follow error formula: what happened + why + how to fix. Design empty states as onboarding moments. Keep terminology consistent (pick one: "Delete" vs "Remove" vs "Trash").

**DON'T**: Use "Submit", "OK", "Yes/No" for button labels. Blame the user in error messages. Use humor for error states. Use jargon without explanation.

### Backgrounds & Visual Details

**DO**: Create atmosphere and depth with gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, grain overlays. Match effects to the overall aesthetic direction.

**DON'T**: Default to solid white/gray backgrounds. Apply effects uniformly without considering the design direction. Use generic stock gradients.

## Implementation Principles

- Match complexity to the aesthetic vision: maximalist designs need elaborate animation code; minimalist designs need precision and restraint
- Build what was asked for — do not add extra pages, routes, or components beyond the request
- If the request is for a single component, deliver a single component — not a full application
- Vary between light and dark themes, different fonts, different aesthetics across generations — never converge on a single look
- Production-grade: semantic HTML, accessible, performant

## Verification

Before delivering frontend code:

1. **Syntax check**: Ensure the code runs without errors (open HTML in browser, or `npx tsc --noEmit` for TypeScript)
2. **AI Slop Test**: Run the 8-point self-check above — fix any "yes" answers
3. **Visual check**: Take a screenshot or describe the rendered result against the design intent
4. **Responsiveness**: Confirm the layout works at mobile (375px), tablet (768px), and desktop (1280px) widths

## Honest Reporting

- If the generated code has visual defects, report them with specifics
- Never claim "production-ready" without running at least a syntax check
- If a requested animation or effect is not feasible with the chosen approach, say so
