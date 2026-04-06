---
name: polish
description: >-
  Systematic final quality pass for shipping-ready frontend code. Covers 13
  dimensions: visual alignment, typography, color, interaction states,
  micro-animations, content/copy, icons, forms, edge cases, responsiveness,
  performance, code quality, and accessibility. Use when the user asks to
  "polish this", "final pass", "finishing touches", "pre-launch review",
  "something looks off", "make it great", "last mile quality", "ship-ready
  check", or wants to go from functionally complete to production-polished.
  Do NOT use for building new UIs from scratch (use anthropic-frontend-design).
  Do NOT use for design system management (use tailwind-design-system).
  Do NOT use for UX audits or heuristic evaluations (use ux-expert).
  Do NOT use for frontend code review without polish intent (use frontend-expert).
  Korean triggers: "폴리시", "다듬기", "마무리", "최종 점검", "디테일 잡기",
  "출시 전 점검", "퀄리티 업".
metadata:
  author: "pbakaus/impeccable"
  version: "1.0.0"
  license: "MIT"
  category: "frontend"
---

Perform a meticulous final pass to catch all the small details that separate good work from great work. The difference between "shipped" and "polished."

**CRITICAL**: Polish is the last step, not the first. Don't polish work that's not functionally complete.

## Pre-Polish Assessment

Before touching code, understand the current state:

1. **Review completeness** — Is it functionally complete? Are there known issues to preserve (mark with TODOs)? What's the quality bar (MVP vs flagship)? When does it ship?
2. **Identify polish areas** — Visual inconsistencies, spacing/alignment issues, interaction state gaps, copy inconsistencies, edge cases, loading/transition smoothness.
3. **Load design context** — If the `anthropic-frontend-design` skill was used earlier, review its Context Gathering Protocol answers and reference docs for design direction.

## 13 Polish Dimensions

Work through these dimensions methodically. Each dimension includes specific checks.

### 1. Visual Alignment & Spacing

- Everything lines up to the grid
- All gaps use the spacing scale (no random 13px gaps)
- Optical alignment adjustments for visual weight (icons may need offset)
- Responsive consistency at all breakpoints
- Elements snap to baseline grid

**Verify**: Enable grid overlay, check with inspector, test multiple viewport sizes, look for elements that "feel" off.

### 2. Typography Refinement

- Hierarchy consistency: same elements use same sizes/weights throughout
- Line length: 45-75 characters for body text
- Line height: appropriate for font size and context
- Widows & orphans: no single words on last line
- Kerning: adjust letter spacing for headlines
- Font loading: no FOUT/FOIT flashes

### 3. Color & Contrast

- All text meets WCAG AA contrast ratios (4.5:1 body, 3:1 large text/UI)
- No hard-coded colors — all use design tokens
- Works in all theme variants
- Same colors mean same things throughout
- Focus indicators visible with sufficient contrast
- Tinted neutrals: no pure gray or pure black (add chroma ~0.01)
- Never put gray text on colored backgrounds — use a shade of that color

### 4. Interaction States

Every interactive element needs all 8 states:

| State | Purpose |
|---|---|
| Default | Resting state |
| Hover | Subtle feedback (color, scale, shadow) |
| Focus | Keyboard focus indicator (never remove without replacement) |
| Active | Click/tap feedback |
| Disabled | Clearly non-interactive |
| Loading | Async action feedback |
| Error | Validation or error state |
| Success | Successful completion |

Missing states create confusion and broken experiences.

### 5. Micro-interactions & Transitions

- All state changes animated (150-300ms)
- Consistent easing: `ease-out` exponential curves — never bounce/elastic (dated)
- 60fps: only animate `transform` and `opacity`
- Motion serves purpose, not decoration
- Respects `prefers-reduced-motion`

### 6. Content & Copy

- Consistent terminology throughout
- Consistent capitalization (Title Case vs Sentence case)
- No typos
- Not too wordy, not too terse
- Punctuation consistency (periods on sentences, not on labels)

### 7. Icons & Images

- All icons from same family or matching style
- Icons sized consistently for context
- Icons align with adjacent text optically
- All images have descriptive alt text
- Images don't cause layout shift (proper aspect ratios)
- 2x assets for high-DPI screens

### 8. Forms & Inputs

- All inputs properly labeled
- Required indicators clear and consistent
- Error messages helpful and consistent
- Tab order logical
- Auto-focus used appropriately (don't overuse)
- Validation timing consistent (on blur vs on submit)

### 9. Edge Cases & Error States

- All async actions have loading feedback
- Helpful empty states, not just blank space
- Clear error messages with recovery paths
- Confirmation of successful actions
- Handles very long content (names, descriptions)
- Handles missing data gracefully

### 10. Responsiveness

- Test mobile (375px), tablet (768px), desktop (1280px)
- Touch targets: 44x44px minimum on touch devices
- No text smaller than 14px on mobile
- No horizontal scroll
- Content adapts logically

### 11. Performance

- Optimized critical path for fast initial load
- No layout shift (CLS near zero)
- No interaction lag or jank
- Optimized image formats and sizes
- Off-screen content loads lazily

### 12. Code Quality

- No console.log debug statements
- No commented-out code
- No unused imports
- Consistent naming conventions
- No TypeScript `any` or ignored errors
- Proper semantic HTML

### 13. Accessibility

- Proper ARIA labels on interactive elements
- Semantic HTML elements (`<nav>`, `<main>`, `<article>`)
- Skip navigation link
- Screen reader testing (at minimum, check with VoiceOver/NVDA)
- Keyboard-only navigation works for all flows

## Polish Checklist

Run through systematically before declaring "done":

- [ ] Visual alignment perfect at all breakpoints
- [ ] Spacing uses design tokens consistently
- [ ] Typography hierarchy consistent
- [ ] All 8 interactive states implemented
- [ ] All transitions smooth (60fps)
- [ ] Copy is consistent and polished
- [ ] Icons consistent and properly sized
- [ ] All forms properly labeled and validated
- [ ] Error states are helpful
- [ ] Loading states are clear
- [ ] Empty states are welcoming
- [ ] Touch targets are 44x44px minimum
- [ ] Contrast ratios meet WCAG AA
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] No console errors or warnings
- [ ] No layout shift on load
- [ ] Works in all supported browsers
- [ ] Respects reduced motion preference
- [ ] Code is clean (no TODOs, console.logs, commented code)

## Anti-Patterns

- Polish before functional completion
- Spend hours polishing if it ships in 30 minutes (triage ruthlessly)
- Introduce bugs while polishing (test after every change)
- Ignore systematic issues (if spacing is off everywhere, fix the system first)
- Perfect one dimension while leaving others rough (maintain consistent quality level)

## Final Verification

Before marking as done:

1. **Use it yourself** — actually interact with the feature end-to-end
2. **Test on real devices** — not just browser DevTools
3. **Fresh eyes** — ask someone else to review
4. **Compare to design** — match intended design
5. **Check all states** — don't just test the happy path

Polish until it feels effortless, looks intentional, and works flawlessly.
