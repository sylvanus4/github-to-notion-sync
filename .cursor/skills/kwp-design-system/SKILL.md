---
name: kwp-design-system
description: >-
  Design system tokens and patterns for the frontend — Refined Swiss. Reference
  this rule when creating or editing any UI component. Do NOT use for tasks
  outside the design domain. Korean triggers: "디자인 시스템", "디자인 토큰".
metadata:
  author: "anthropic-kwp"
  version: "1.0.0"
  category: "workflow"
---
# Design System Guide — Refined Swiss

Canonical design tokens for `frontend/`. Every component MUST follow these conventions.

## Design Direction

**Refined Swiss** — A flat, data-dense dashboard style built on a trust-blue brand, cool gray neutrals, and Inter typeface. Optimised for SaaS readability, WCAG AA compliance, and minimal migration overhead. Orange accent for CTAs creates clear visual hierarchy.

## Typography

- **Primary font**: `font-sans` → "Inter" — used for all text (headings, body, labels, buttons)
- **Monospace font**: `font-mono` → "Fira Code" — used for code snippets, data values, and metric displays

## Semantic Color Tokens (CSS Custom Properties)

The project uses CSS custom properties defined in `frontend/src/index.css` that automatically switch between light and dark mode. These are registered as Tailwind colors in `tailwind.config.js`.

### Surface Colors (cool gray)
| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `bg-surface` | #F9FAFB (gray-50) | #111827 (gray-900) | Page backgrounds |
| `bg-surface-card` | #FFFFFF (white) | #1F2937 (gray-800) | Cards, panels, modals |
| `bg-surface-elevated` | #FFFFFF (white) | #1F2937 (gray-800) | Elevated surfaces |

### Foreground Colors
| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `text-foreground` | #111827 (gray-900) | #F3F4F6 (gray-100) | Primary text, headings |
| `text-foreground-secondary` | #4B5563 (gray-600) | #9CA3AF (gray-400) | Labels, secondary text |
| `text-foreground-muted` | #6B7280 (gray-500) | #9CA3AF (gray-400) | Captions, hints, timestamps |

### Border Colors
| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `border-border` | #E5E7EB (gray-200) | #4B5563 (gray-600) | Default borders |
| `border-border-strong` | #D1D5DB (gray-300) | #6B7280 (gray-500) | Input borders, stronger dividers |

### Brand Colors (trust blue)
| Token | Value | Use |
|-------|-------|-----|
| `brand-50` | #eff6ff | Light brand tints (hover bg) |
| `brand-100` | #dbeafe | Selected/active backgrounds |
| `brand-200` | #bfdbfe | Light outlines |
| `brand-300` | #93c5fd | Subtle accents |
| `brand-400` | #60a5fa | Secondary brand |
| `brand-500` | #3b82f6 | Focus rings, light accent |
| `brand-600` | #2563eb | Primary buttons, active states |
| `brand-700` | #1d4ed8 | Hover states |
| `brand-800` | #1e40af | Strong emphasis |
| `brand-900` | #1e3a8a | Darkest brand |

### Accent Colors (orange CTA)
| Token | Value | Use |
|-------|-------|-----|
| `accent-400` | #fb923c | Light accent, hover |
| `accent-500` | #f97316 | CTA buttons, action highlights |
| `accent-600` | #ea580c | CTA hover |

### Skeleton/Loading Colors
| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `bg-skeleton` | #E5E7EB (gray-200) | #374151 (gray-700) | Skeleton loaders, progress bar tracks |
| `bg-skeleton-muted` | #F3F4F6 (gray-100) | #1F2937 (gray-800) | Lighter skeleton elements, neutral badges |

**Always prefer semantic tokens over hardcoded gray values.** Use `bg-surface-card` instead of `bg-white`, `text-foreground` instead of `text-gray-900`, etc.

## Typography Scale

| Token | Size | Use |
|-------|------|-----|
| `text-2xs` | 10px | Timestamps, confidence scores only. **A11y warning**: 10 px is below the recommended 12 px minimum — use sparingly, never for critical information, and ensure the container does not block user zoom. |
| `text-xs` | 12px | Table headers, badges, captions, icon-button labels |
| `text-sm` | 14px | Body text, form labels, button labels, table cells, descriptions |
| `text-base` | 16px | Reserved (call timer only) |
| `text-lg` | 18px | Section headings (h2/h3 inside pages) |
| `text-xl md:text-2xl` | 20-24px | Page titles (h1) |

## Font Weight

| Token | Use |
|-------|-----|
| `font-normal` | Body text, descriptions |
| `font-medium` | Labels, badges, button text, table cells with emphasis |
| `font-semibold` | Section headings (h2, h3) |
| `font-bold` | Page titles (h1) only |

## Heading Hierarchy

```
h1  text-xl md:text-2xl font-bold text-foreground
h2  text-lg font-semibold text-foreground
h3  text-sm font-semibold text-foreground-secondary
caption  text-xs text-foreground-muted
```

Anchored headings (those with `id` for deep-linking) MUST include `scroll-mt-16` (or a value matching the sticky header height) to prevent content from being hidden behind the header on scroll.

### Numeric Display

Use `tabular-nums` (Tailwind class) on table cells, metric values, counters, and any column where numbers are compared vertically. This ensures digits are monospaced and columns align. For code-like data, also add `font-mono`.

## Button Variants

Every interactive button MUST include `focus-visible:outline-none focus-visible:ring-2`.
All touch targets MUST meet `min-h-[44px]`.

### Primary
```
rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white
hover:bg-brand-700 disabled:opacity-50
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
transition-colors
```

### CTA (Accent)
```
rounded-lg bg-accent-500 px-4 py-2 text-sm font-medium text-white
hover:bg-accent-600 disabled:opacity-50
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-400 focus-visible:ring-offset-2
transition-colors
```

### Secondary
```
rounded-lg border border-border-strong px-4 py-2 text-sm font-medium text-foreground-secondary
hover:bg-surface disabled:opacity-50
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
transition-colors
```

### Danger
```
rounded-lg bg-error-600 px-4 py-2 text-sm font-medium text-white
hover:bg-error-700 disabled:opacity-50
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-error-500 focus-visible:ring-offset-2
transition-colors
```

### Ghost
```
rounded-lg px-3 py-1.5 text-sm font-medium text-foreground-secondary
hover:bg-surface disabled:opacity-50
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2
transition-colors
```

### Icon Button
```
flex items-center justify-center rounded-full min-h-[44px] min-w-[44px]
text-foreground-muted hover:bg-surface
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500
transition-colors
```

### Inline Link
```
text-xs font-medium hover:underline
focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500
```
Color varies by context: `text-success-600`, `text-error-600`, `text-warning-600`.

## Card Variants

| Variant | Classes |
|---------|---------|
| Default | `rounded-lg border border-border bg-surface-card p-4 shadow-sm` |
| Flush | `rounded-lg border border-border bg-surface-card` (no padding — for table wrappers) |
| Modal | `rounded-xl border border-border bg-surface-card p-6 shadow-xl` |
| Elevated | `rounded-lg border border-border bg-surface-card p-4 shadow-sm hover:shadow-md transition-shadow` (interactive cards ONLY — do NOT apply `hover:shadow-md` to default cards) |

## Badge

Base: `inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium`

| Semantic | Color classes |
|----------|-------------|
| Success | `bg-success-100 text-success-800` |
| Error | `bg-error-100 text-error-800` |
| Warning | `bg-warning-100 text-warning-700` |
| Brand | `bg-brand-100 text-brand-700` |
| Neutral | `bg-skeleton-muted text-foreground-secondary` |

## Form Inputs

```
min-h-[44px] w-full rounded-lg border border-border bg-surface-card px-3 py-2
text-sm text-foreground shadow-sm transition-colors
placeholder:text-foreground-muted
focus-visible:border-brand-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500
```

Labels: `block text-sm font-medium text-foreground-secondary mb-1`

## Page Layout

Every page rendered inside `Layout` MUST use one of these two layout modes:

### Full-Bleed Workspace

Use for multi-panel interactive pages (side-by-side panels, real-time feeds).
Only `ActiveCallView` and `ConversationInbox` should use this pattern.

```
Root wrapper      flex h-full flex-col
```

### Contained Page (Default)

Use for all other pages. Content is centered with max-width for readability.

```
Outer wrapper     h-full overflow-y-auto
Inner container   p-3 md:p-6 max-w-6xl mx-auto
```

Exception: `SummaryReview` uses `max-w-3xl` for long-form reading comfort.

### Allowed `max-w-*` Values (non-page contexts)

| Width | Use |
|-------|-----|
| `max-w-6xl` | Default page container |
| `max-w-3xl` | Long-form reading (SummaryReview) |
| `max-w-2xl` | Wizard dialogs |
| `max-w-lg` | Form dialogs |
| `max-w-md` | Info modals, help popups |
| `max-w-sm` | Confirm dialogs, login form |
| `max-w-xs` | Compact elements |
| `max-w-[80%]` / `max-w-[85%]` | Chat bubbles |

Do NOT use `max-w-7xl`, `max-w-5xl`, `max-w-4xl`, or `max-w-screen`.

### Standard Header Row

```
Header row    flex flex-wrap items-center justify-between gap-3 mb-6
Title (h1)    text-xl md:text-2xl font-bold text-foreground
```

### Layout Anti-Patterns

- Full-width layout for form/table/settings pages (use Contained Page)
- `max-w-6xl` on workspace pages like Call or Inbox (use Full-Bleed)
- Mixing `overflow-y-auto` with `max-w-6xl` on the same element (separate into outer scroll + inner container)
- Using `max-w-7xl`, `max-w-5xl`, or other non-standard widths (use `max-w-6xl`)

## Responsive Conventions

- Page padding: `p-3 md:p-6`
- Card padding: `p-4`
- Metric grids: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`
- Table wrapper: `overflow-x-auto rounded-lg border border-border`
- Table header row: `text-xs uppercase bg-surface text-foreground-muted` with `scope="col"` on every `<th>`
- Table row border: `border-b border-border`
- Flex containers where children may overflow on narrow screens: add `flex-wrap` (fixed-layout rows like input + button or icon + label that should never wrap are exempt)
- Font size: page titles scale with `text-xl md:text-2xl`

## Theme Management

- Theme state is managed by `useThemeStore` in `frontend/src/stores/themeStore.ts`
- Use `useThemeStore((s) => s.theme)` to read the current theme
- Use `useThemeStore((s) => s.toggleTheme)` to toggle
- FOUC is prevented by an inline script in `index.html`
- Pages outside Layout (e.g. LoginPage) can import `useThemeStore` directly

## Tabs

Container: `flex flex-wrap gap-1 border-b border-border` with `role="tablist"` and `aria-label`

```
Tab button    flex min-h-[44px] items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-colors
Active        bg-brand-100 text-brand-700 shadow-sm
Inactive      text-foreground-secondary hover:bg-surface
```

Every tab MUST include `role="tab"`, `aria-selected`, `aria-controls`, and a matching `id`.
The tab panel MUST include `role="tabpanel"`, `aria-labelledby`, and `id`.

## Dropdown / Popover

```
Trigger       button with aria-expanded, aria-haspopup="true"
Container     absolute [position] top-full z-50 mt-2 w-[width] animate-scale-in rounded-xl border border-border bg-surface-card p-3 shadow-sm
Menu item     flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-foreground-secondary hover:bg-surface transition-colors
```

Close on click-outside and Escape key. Positioning is `absolute right-0 top-full` or `absolute left-0 top-full` depending on trigger location.

## Modal / Dialog

```
Overlay       fixed inset-0 z-50 flex items-center justify-center bg-foreground/20 backdrop-blur-sm animate-fade-in
Content       mx-4 w-full max-w-[size] animate-scale-in rounded-xl border border-border bg-surface-card p-6 shadow-xl
```

Size presets: `max-w-sm` (confirm), `max-w-md` (info), `max-w-lg` (form), `max-w-2xl` (wizard).

Every modal MUST include:
- `role="dialog"` and `aria-modal="true"` on content
- `aria-labelledby` pointing to the title element
- Focus trap (tab cycling within modal)
- Escape key to close
- Click-outside to close (unless destructive action in progress)

## Loading States

```
Skeleton      animate-pulse motion-reduce:animate-none rounded bg-skeleton
Skeleton alt  animate-pulse motion-reduce:animate-none rounded bg-skeleton-muted
Spinner       <Loader2 aria-hidden="true" size={14} className="animate-spin motion-reduce:animate-none" />
Text          <p className="text-sm text-foreground-muted">{t("common.loading")}</p>
```

Full-page skeleton containers use `aria-busy="true"` and `role="status"`.
ALL `animate-pulse` and `animate-spin` MUST include `motion-reduce:animate-none`.

## Empty States

```
Container     flex flex-1 items-center justify-center p-4
Text          text-sm text-foreground-muted
```

Pattern: `<p className="text-sm text-foreground-muted">{t("feature.noData")}</p>`
For feature-level empty states (no items created yet), consider adding a relevant icon above the text.

## Pagination

```
Container     mt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-foreground-muted
Info text     <span className="tabular-nums"> for alignment
Buttons       secondary button style (rounded-lg border border-border-strong px-3 py-1.5 text-sm font-medium)
Disabled      disabled:opacity-50 disabled:cursor-not-allowed
```

## Progress Bar

```
Track         h-2 rounded-full bg-skeleton (or bg-skeleton-muted)
Fill          h-2 rounded-full bg-brand-500 with inline style={{ width }}
```

For interactive progress (audio scrubber): add `role="slider"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and `cursor-pointer`.

## Icon Conventions

Library: `lucide-react` exclusively.
Default attribute: `aria-hidden="true"` on decorative icons.
Icon-only buttons MUST have `aria-label`.

### Size Scale

| Size | Use |
|------|-----|
| 12px | Inline with `text-xs` (tabs, badges, small labels) |
| 14px | Inline with `text-sm` (buttons, table cells, body text) |
| 16px | Standalone actions (nav, primary icons) |
| 20px | Mobile nav, feature headers |
| 24–28px | Hero/feature illustrations only |

### Color

Inherit from parent text color. Use `text-foreground-muted` for secondary icons, `text-brand-600` for brand accent, semantic colors (`text-success-500`, `text-error-600`, `text-warning-500`) for status.

## Z-Index Scale

| Level | Value | Use |
|-------|-------|-----|
| Base content | auto | Default stacking |
| Floating | z-10 | Tooltips, minor overlays |
| Mobile nav | z-30 | Bottom tab bar |
| Overlay | z-40 | Mobile admin menu overlay, chat FAB |
| Modal | z-50 | All modals, dialogs, popovers, dropdowns |
| Skip link | z-[60] | Skip-to-content link |

Do NOT introduce new z-index values. Use the scale above.

## Animation

### Entry Animations (use sparingly)

- Page/section content: `animate-fade-in-up` (with optional `animationDelay`)
- Overlays: `animate-fade-in`
- Modals/popovers: `animate-scale-in`
- Side content: `animate-slide-in-right`

### Continuous Animations

- Loading pulse: `animate-warm-pulse` or `animate-pulse`
- Spinner: `animate-spin`

### Rules

- ALL continuous animations (`animate-pulse`, `animate-spin`, `animate-warm-pulse`) MUST include `motion-reduce:animate-none`
- Entry animations are covered by the global `prefers-reduced-motion` rule in `index.css`
- Transition utility: prefer `transition-colors` for interactive states; use `transition-all duration-200` only when multiple properties change
- Do NOT use `transition-all` without explicit `duration-*`

## Feedback Colors (Semantic)

These tokens auto-switch between light and dark mode via CSS custom properties.

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `bg-error-surface` | #fef2f2 | #450a0a | Error background |
| `bg-error-surface-strong` | #fee2e2 | #7f1d1d | Error emphasis bg |
| `text-error-text` | #b91c1c | #fca5a5 | Error text |
| `bg-success-surface` | #f0fdf4 | #052e16 | Success background |
| `bg-success-surface-strong` | #dcfce7 | #14532d | Success emphasis bg |
| `text-success-text` | #166534 | #86efac | Success text |
| `bg-warning-surface` | #fffbeb | #2e2602 | Warning background |
| `bg-warning-surface-strong` | #fef3c7 | #713f12 | Warning emphasis bg |
| `text-warning-text` | #b45309 | #fde047 | Warning text |

Prefer these over `bg-error-100` / `bg-success-50` + `dark:` overrides for feedback banners. For borders in feedback banners, use `border-[semantic]-surface-strong` when available.

## Inline Feedback

For temporary status messages (e.g., "Copied!" on a button):

```
Container     role="status" aria-live="polite"
Pattern       Swap button text/icon for 1.5–2s, then revert via setTimeout
```

Do NOT use toast/snackbar for inline copy-to-clipboard or single-action confirmations.

## Mobile Conventions

- Bottom nav bar: `fixed inset-x-0 bottom-0 z-30 lg:hidden` with `pb-safe`
- Main content padding: `pb-14 lg:pb-16` to clear bottom nav
- Chat FAB position: `bottom-20 right-4 md:bottom-6 md:right-6`
- Desktop-only elements: `hidden lg:flex` or `hidden lg:block`
- Mobile-only elements: `lg:hidden`
- Sidebar to full-width: `w-full lg:w-96` with conditional `hidden lg:flex` when detail is selected
- Touch targets: `min-h-[44px] min-w-[44px]` on all interactive elements (WCAG 2.5.8)
- Safe area: use `pb-safe` utility for bottom-anchored elements on notched devices

## Anti-Patterns (DO NOT use)

- `rounded-md` on buttons (use `rounded-lg`)
- `focus:outline-none` without `focus-visible:` replacement
- `disabled:opacity-60` or `disabled:opacity-40` (use `disabled:opacity-50`)
- `px-5`, `px-6`, `py-2.5` on standard buttons (use `px-4 py-2`)
- `text-2xs` on badges (use `text-xs`)
- Hard-coded hex colors (use Tailwind tokens)
- Hard-coded gray colors without semantic tokens (use `text-foreground`, `bg-surface-card`, etc.)
- Missing dark mode support (every surface MUST use semantic tokens)
- `dark:bg-gray-*` / `dark:text-gray-*` overrides (use semantic tokens instead)
- `shadow-md` / `shadow-lg` on regular cards (use `shadow-sm`; `hover:shadow-md` is only for Elevated variant)
- `<th>` without `scope="col"`
- Tables without `overflow-x-auto` wrapper
- Teal/stone color values (use blue brand + gray neutrals)
- Serif fonts for headings (use `font-sans` Inter)
- `font-serif` usage anywhere (removed from this design system)
- `animate-spin` or `animate-pulse` without `motion-reduce:animate-none`
- `transition-all` without explicit `duration-*`
- `dark:bg-*` / `dark:text-*` overrides when semantic tokens exist (use feedback surface tokens)
- New z-index values outside the defined scale (auto, 10, 30, 40, 50, 60)
- Icon libraries other than `lucide-react`
- Icon-only buttons without `aria-label`
- Modals without `role="dialog"`, `aria-modal="true"`, or focus trap

## Examples

### Example 1: Typical request

**User says:** "I need help with design system"

**Actions:**
1. Ask clarifying questions to understand context and constraints
2. Apply the domain methodology step by step
3. Deliver structured output with actionable recommendations

### Example 2: Follow-up refinement

**User says:** "Can you go deeper on the second point?"

**Actions:**
1. Re-read the relevant section of the methodology
2. Provide detailed analysis with supporting rationale
3. Suggest concrete next steps
## Error Handling

| Issue | Resolution |
|-------|-----------|
| Missing required context | Ask user for specific inputs before proceeding |
| Skill output doesn't match expectations | Re-read the workflow section; verify inputs are correct |
| Conflict with another skill's scope | Check the "Do NOT use" clauses and redirect to the appropriate skill |