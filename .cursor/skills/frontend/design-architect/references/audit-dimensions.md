# Audit Dimensions — 14-Point Design Review

Detailed checklist for each dimension in the Full Audit step. Apply every question to every screen.

---

## 1. Visual Hierarchy

- Does the eye land where it should? Is the most important element the most prominent?
- Can a user understand the screen in 3 seconds?
- Is the primary action unmistakable without scanning?
- Are secondary elements clearly subordinate — not competing for attention?
- Do colors reinforce hierarchy and meaning? Is the palette cohesive?
- Are semantic colors used consistently (error = red, success = green, warning = amber)?
- Is color ever the only indicator of meaning? (accessibility violation)
- Are all colors from design system tokens — no hardcoded hex values?
- Does the hierarchy hold at every viewport width?

## 2. Spacing and Rhythm

- Is whitespace consistent and intentional? Do all elements breathe?
- Are spacing values from the design system token scale — no arbitrary pixel values?
- Is there a visible vertical rhythm (consistent gaps between sections)?
- Does the spacing create logical groupings (related items closer, unrelated items farther)?
- Are there areas where elements feel squeezed or floating?

## 3. Typography

- Are font sizes establishing a clear hierarchy (title, heading, body, caption)?
- Are font weights used purposefully — not scattered randomly?
- Is line height comfortable for reading (1.5-1.75 for body)?
- Is line length controlled (65-75 characters per line for body text)?
- Does the type feel calibrated and intentional, not default?
- Are all sizes from the typography scale defined in the design system?

## 4. Alignment and Grid

- Do elements sit on a consistent grid?
- Is anything off by 1-2 pixels? The eye detects misalignment before the brain names it.
- Do elements align with their visual weight, not just their bounding box?
- Are form labels, inputs, and buttons aligned on the same baseline?
- Is the grid consistent across all pages, or does each page invent its own layout?

## 5. Components

- Are similar elements styled identically across screens?
- Is there an element that appears in two variations when it should be one component?
- Are all interactive elements recognizable as interactive (buttons look like buttons)?
- Do components use design system tokens exclusively?
- Are there ad-hoc styled elements that should be extracted into shared components?

## 6. Icons

- Are icons consistent in style, weight, and visual metaphor?
- Do they come from a single icon library (e.g., lucide-react)?
- Do icons reinforce meaning or just decorate?
- Are icon sizes consistent within context (inline with text, standalone, nav)?
- Are decorative icons marked `aria-hidden="true"`?
- Do icon-only buttons have `aria-label`?

## 7. Motion and Transitions

- Do transitions feel natural and purposeful?
- Is there motion that exists for no reason? Remove it.
- Does the app feel responsive to touch and click interactions?
- Are animation durations appropriate (150-300ms for micro-interactions)?
- Are animations using performant properties (transform, opacity) — not layout properties?
- Does `prefers-reduced-motion` disable continuous animations?

## 8. Empty States

- Are empty screens designed, not just blank?
- Do empty states communicate what happens next (e.g., "Create your first...")?
- Is there visual interest (icon, illustration) or just plain text?
- Are empty states consistent in pattern across the app?
- Do they guide the user toward the primary action?

## 9. Loading States

- Are skeleton screens, spinners, or placeholders consistent?
- Does the app feel alive while loading, or frozen?
- Is there a loading state for every async operation?
- Do loading states match the shape of the content they replace?
- Are loading animations marked with `aria-busy="true"` and `role="status"`?
- Do all `animate-pulse` and `animate-spin` include `motion-reduce:animate-none`?

## 10. Error States

- Are error messages elegant — not raw technical strings?
- Do they offer friendly guidance ("Try again" / "Check your connection")?
- Is there a consistent error pattern across the app?
- Are inline errors positioned near the source of the problem?
- Do form validation errors prevent confusion (specific messages, not generic)?
- No screen should show a harsh, unstyled error.

## 11. Dark Mode

- Does dark mode feel intentional — not just color-inverted?
- Are shadows replaced with subtle borders or elevation changes?
- Are borders and highlights reworked for dark backgrounds?
- Do images and illustrations look correct on dark backgrounds?
- Is contrast sufficient (WCAG AA: 4.5:1 for text, 3:1 for UI)?
- Are all surfaces using semantic tokens that auto-switch?

## 12. Density

- Can anything be removed without losing meaning?
- Are there redundant elements saying the same thing twice?
- Does every element earn its place on screen?
- Is information density appropriate for the context (data-dense dashboard vs. marketing page)?
- Are there sections where less content would communicate more?

## 13. Responsiveness

- Does every screen work at mobile (375px), tablet (768px), and desktop (1440px)?
- Are layouts truly redesigned for each breakpoint — not just stacked?
- Is there horizontal scroll at any viewport? (Critical failure)
- Are touch targets at least 44x44 CSS pixels on mobile?
- Do tables transform or scroll gracefully on small screens?
- Is the font size readable at every viewport (minimum 16px body on mobile)?

## 14. Accessibility

- Keyboard navigation: Can every interactive element be reached via Tab?
- Focus indicators: Are focus rings visible and not suppressed?
- ARIA: Are roles, labels, and states used correctly?
- Color contrast: >= 4.5:1 for normal text, >= 3:1 for large text and UI components
- Screen reader flow: Is the reading order logical?
- Headings: Single `<h1>` per page, logical hierarchy
- Forms: Every input has an associated `<label>` or `aria-label`
- Images: Meaningful `alt` text or `alt=""` for decorative
