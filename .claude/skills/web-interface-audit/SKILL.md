---
name: web-interface-audit
description: >-
  Audit UI code against 16 dimensions of web interface quality —
  accessibility, focus states, forms, animation, typography, content handling,
  images, performance, navigation, touch, safe areas, dark mode, i18n,
  hydration safety, hover states, and content copy. Includes 12 anti-pattern
  detectors. Self-contained rules; no external fetching required. Adapted from
  Vercel's Web Interface Guidelines.
---

# Web Interface Audit

**16 audit dimensions · 12 anti-pattern detectors · code-level UI review**

Read target files, check against rules below. Output concise, grouped by
file.  Use `file:line` format (VS Code clickable). High signal-to-noise.

---

## How to Use

When invoked, the agent should:

1. Identify target files (from user input, git diff, or explicit paths).
2. Read each file.
3. Check every rule below against the code.
4. Output findings grouped by file, one line per issue.
5. Mark clean files with `✓ pass`.

---

## Audit Rules

### 1. Accessibility

- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`)
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates (toasts, validation) need `aria-live="polite"`
- Use semantic HTML (`<nav>`, `<main>`, `<article>`, `<section>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link for main content
- `scroll-margin-top` on heading anchors

### 2. Focus States

- Interactive elements need visible focus: `focus-visible:ring-*` or equivalent
- Never `outline-none` / `outline: none` without focus replacement
- Use `:focus-visible` over `:focus` (avoid focus ring on click)
- Group focus with `:focus-within` for compound controls

### 3. Forms

- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onPaste` + `preventDefault`)
- Labels clickable (`htmlFor` or wrapping control)
- Disable spellcheck on emails, codes, usernames (`spellCheck={false}`)
- Checkboxes/radios: label + control share single hit target (no dead zones)
- Submit button stays enabled until request starts; spinner during request
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern
- `autocomplete="off"` on non-auth fields to avoid password manager triggers
- Warn before navigation with unsaved changes (`beforeunload` or router guard)

### 4. Animation

- Honor `prefers-reduced-motion` (provide reduced variant or disable)
- Animate `transform`/`opacity` only (compositor-friendly)
- Never `transition: all`—list properties explicitly
- Set correct `transform-origin`
- SVG: transforms on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`
- Animations interruptible—respond to user input mid-animation

### 5. Typography

- `…` not `...`
- Curly quotes `"` `"` not straight `"`
- Non-breaking spaces: `10 MB`, `⌘ K`, brand names
- Loading states end with `…`: `"Loading…"`, `"Saving…"`
- `font-variant-numeric: tabular-nums` for number columns/comparisons
- Use `text-wrap: balance` or `text-pretty` on headings (prevents widows)

### 6. Content Handling

- Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words`
- Flex children need `min-w-0` to allow text truncation
- Handle empty states—don't render broken UI for empty strings/arrays
- User-generated content: anticipate short, average, and very long inputs

### 7. Images

- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold images: `loading="lazy"`
- Above-fold critical images: `fetchpriority="high"`

### 8. Performance

- Large lists (>50 items): virtualize (`virtua`, `content-visibility: auto`)
- No layout reads in render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop`)
- Batch DOM reads/writes; avoid interleaving
- Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke
- Add `<link rel="preconnect">` for CDN/asset domains
- Critical fonts: `<link rel="preload">` with `font-display: swap`

### 9. Navigation & State

- URL reflects state—filters, tabs, pagination, expanded panels in query params
- Links use `<a>`/`<Link>` (Cmd/Ctrl+click, middle-click support)
- Deep-link all stateful UI (if uses `useState`, consider URL sync via `nuqs` or similar)
- Destructive actions need confirmation modal or undo window—never immediate

### 10. Touch & Interaction

- `touch-action: manipulation` (prevents double-tap zoom delay)
- `-webkit-tap-highlight-color` set intentionally
- `overscroll-behavior: contain` in modals/drawers/sheets
- During drag: disable text selection, `inert` on dragged elements
- `autoFocus` sparingly—desktop only, single primary input; avoid on mobile

### 11. Safe Areas & Layout

- Full-bleed layouts need `env(safe-area-inset-*)` for notches
- Avoid unwanted scrollbars: `overflow-x-hidden` on containers, fix content overflow
- Flex/grid over JS measurement for layout

### 12. Dark Mode & Theming

- `color-scheme: dark` on `<html>` for dark themes (fixes scrollbar, inputs)
- `<meta name="theme-color">` matches page background
- Native `<select>`: explicit `background-color` and `color` (Windows dark mode)

### 13. Locale & i18n

- Dates/times: use `Intl.DateTimeFormat` not hardcoded formats
- Numbers/currency: use `Intl.NumberFormat` not hardcoded formats
- Detect language via `Accept-Language` / `navigator.languages`, not IP
- Brand names, code tokens, identifiers: wrap with `translate="no"` to prevent garbled auto-translation

### 14. Hydration Safety

- Inputs with `value` need `onChange` (or use `defaultValue` for uncontrolled)
- Date/time rendering: guard against hydration mismatch (server vs client)
- `suppressHydrationWarning` only where truly needed

### 15. Hover & Interactive States

- Buttons/links need `hover:` state (visual feedback)
- Interactive states increase contrast: hover/active/focus more prominent than rest

### 16. Content & Copy

- Active voice: "Install the CLI" not "The CLI will be installed"
- Title Case for headings/buttons (Chicago style)
- Numerals for counts: "8 deployments" not "eight"
- Specific button labels: "Save API Key" not "Continue"
- Error messages include fix/next step, not just problem
- Second person; avoid first person
- `&` over "and" where space-constrained

---

## Anti-Patterns (Always Flag)

These patterns should always be flagged with `⚠️`:

| Anti-Pattern | Why It's Bad |
|---|---|
| `user-scalable=no` or `maximum-scale=1` | Disables zoom — accessibility violation |
| `onPaste` with `preventDefault` | Blocks paste — breaks password managers |
| `transition: all` | Animates unintended properties — jank |
| `outline-none` without `focus-visible` replacement | Invisible focus — keyboard users lost |
| Inline `onClick` navigation without `<a>` | Breaks Cmd+click, middle-click, crawlers |
| `<div>` or `<span>` with click handlers | Should be `<button>` — no keyboard/a11y |
| Images without dimensions | Causes CLS (Cumulative Layout Shift) |
| Large arrays `.map()` without virtualization | Slow initial render for 50+ items |
| Form inputs without labels | Screen readers can't identify fields |
| Icon buttons without `aria-label` | Screen readers read nothing |
| Hardcoded date/number formats | Breaks for non-US locales — use `Intl.*` |
| `autoFocus` without justification | Disorienting on mobile; unexpected scroll |

---

## Output Format

Group by file. Use `file:line` format. Terse findings.

```text
## src/components/Button.tsx

src/components/Button.tsx:42 - icon button missing aria-label
src/components/Button.tsx:18 - input lacks label
src/components/Button.tsx:55 - animation missing prefers-reduced-motion
src/components/Button.tsx:67 - transition: all → list properties

## src/components/Modal.tsx

src/components/Modal.tsx:12 - missing overscroll-behavior: contain
src/components/Modal.tsx:34 - "..." → "…"

## src/components/Card.tsx

✓ pass
```

State issue + location. Skip explanation unless fix non-obvious. No preamble.
