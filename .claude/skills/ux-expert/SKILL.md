---
name: ux-expert
description: >-
  Conduct UX audits, heuristic evaluations (Nielsen's 10), accessibility checks
  (WCAG 2.1 AA), and design-system consistency reviews. Use when asked for a UX
  review, usability analysis, accessibility audit, or design-system alignment check.
---

# UX Expert

Perform user-experience reviews for a React + Tailwind CSS application.

## Review Workflow

1. **Scope** -- Identify the pages/components under review.
2. **Heuristic Evaluation** -- Apply Nielsen's 10 usability heuristics.
3. **Accessibility Audit** -- Check WCAG 2.1 Level AA compliance.
4. **Design-System Consistency** -- Verify Tailwind token usage, component naming, spacing/color consistency.
5. **User-Flow Analysis** -- Trace critical paths (happy path + error states).
6. **Report** -- Produce the structured output below.

## Nielsen's 10 Heuristics

| # | Heuristic | What to check |
|---|-----------|---------------|
| 1 | Visibility of system status | Loading states, progress indicators, toast feedback |
| 2 | Match between system and real world | Domain language, icons, metaphors |
| 3 | User control and freedom | Undo/redo, cancel, back navigation |
| 4 | Consistency and standards | Design tokens, component library reuse |
| 5 | Error prevention | Form validation, confirmation dialogs, disabled states |
| 6 | Recognition over recall | Labels, placeholders, breadcrumbs |
| 7 | Flexibility and efficiency | Keyboard shortcuts, power-user paths |
| 8 | Aesthetic and minimalist design | Visual noise, information density |
| 9 | Help users recover from errors | Error messages with guidance, retry actions |
|10 | Help and documentation | Tooltips, onboarding, contextual help |

## Accessibility Checklist (WCAG 2.1 AA)

- [ ] Color contrast ratio >= 4.5:1 (text), >= 3:1 (large text/UI)
- [ ] All interactive elements reachable via keyboard (Tab, Enter, Escape)
- [ ] Focus indicators visible and not suppressed
- [ ] Images have meaningful `alt` text (or `alt=""` for decorative)
- [ ] Form inputs have associated `<label>` or `aria-label`
- [ ] ARIA roles used correctly (no redundant roles on semantic HTML)
- [ ] Page has a single `<h1>`, heading hierarchy is logical
- [ ] Motion/animation respects `prefers-reduced-motion`
- [ ] Touch targets >= 44x44 CSS pixels on mobile

## Design-System Checks

- Tailwind utility classes used instead of raw CSS values
- Color palette from `tailwind.config` -- no hard-coded hex
- Spacing scale consistent (no arbitrary `px` values)
- Typography uses project-defined font-size/weight tokens
- Shared components preferred over ad-hoc markup

## Output Format

```
UX Audit Report
================
Scope: [pages/components reviewed]

1. Heuristic Evaluation
   Overall: [Pass / Needs Attention / Fail]
   Findings:
   - H[N] [Heuristic Name]: [Issue] -> [Recommendation]

2. Accessibility (WCAG 2.1 AA)
   Compliance: [XX%]
   Critical:
   - [Element/Component]: [Issue] -> [Fix]
   Warnings:
   - [Element/Component]: [Issue] -> [Fix]

3. Design-System Consistency
   Violations: [count]
   - [File:Line]: [Violation] -> [Correct token/component]

4. User-Flow Analysis
   Flow: [Flow name]
   Steps: [Step 1] -> [Step 2] -> ...
   Issues:
   - [Step N]: [Problem] -> [Suggestion]

5. Summary
   Priority fixes: [top 3 items]
   Estimated effort: [Low/Medium/High]
```

## Test Invocation

```
/ux-expert
/ux-expert src/features/dashboard/
/ux-expert accessibility check for login page
```
