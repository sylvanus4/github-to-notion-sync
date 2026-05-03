---
name: design-review
description: Compare implemented code against Figma design and screen spec for visual accuracy and functional coverage.
disable-model-invocation: true
arguments: [figma_url]
---

Review implementation against Figma design at `$figma_url`.

## Review Dimensions

1. **Visual Fidelity**: Layout, spacing, colors, typography match
2. **Component Mapping**: Correct TDS components used
3. **State Coverage**: All UI states implemented (loading, empty, error, success)
4. **Responsive Behavior**: Mobile/tablet/desktop breakpoints
5. **Interaction Patterns**: Hover, focus, active states
6. **Accessibility**: WCAG AA contrast, keyboard navigation, screen reader labels
7. **i18n Readiness**: No hardcoded strings, proper locale handling

## Process

1. Fetch Figma design context via Figma MCP
2. Read implemented component code
3. Compare pixel-level layout accuracy
4. Check state coverage against spec
5. Verify responsive breakpoints

## Output

```markdown
## Design Review: [component/page]

### Visual Fidelity: [PASS/ISSUES]
### Component Mapping: [PASS/ISSUES]
### State Coverage: [PASS/ISSUES]
### Responsive: [PASS/ISSUES]
### Accessibility: [PASS/ISSUES]

## Issues Found
[Severity-ranked list with screenshots if available]

## Recommendations
[Specific fixes]
```
