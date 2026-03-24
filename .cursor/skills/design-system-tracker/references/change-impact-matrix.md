# Change Impact Matrix

Impact analysis matrix for design system changes. Use during **Impact Analysis** phase of `design-system-tracker`.

## Impact by change type — tokens

| Token type | Engineering | Design | Planning |
|------------|-------------|--------|----------|
| Color (Primary) | CSS variables / theme updates | Full palette review | Brand guide refresh |
| Color (Semantic) | Component style fixes | State color review | None |
| Typography (Font family) | Font load / build config | Full type scale | Content reflow possible |
| Typography (Size/Weight) | Possible layout breaks | Visual hierarchy review | None |
| Spacing | Layout fixes | Spacing guide refresh | None |
| Border/Shadow | Component style fixes | Visual style review | None |
| Breakpoint | Responsive logic changes | Responsive redesign | Mobile scenario review |

## Impact by change type — components

| Change kind | Engineering | Design | Planning |
|-------------|-------------|--------|----------|
| Optional prop added | No code change required | New option awareness | None |
| Required prop added | All call sites must update | Reflect new property | Scenario review possible |
| Prop removed | All call sites must update | Find alternative | Feature change check |
| Prop renamed | Bulk refactor | Figma update | None |
| Variant added | No code change required | New variant design | New use cases possible |
| Variant deleted | Call sites need replacement | Map to alternate variant | Affected scenarios |
| Style change | Visual testing | Confirm intent | None (minor) |
| Behavior change | Logic updates | Interaction updates | User flow review |
| Component deleted | Migrate to replacement | Replacement design | Full feature review |
| New component | Implementation work | Usage guide | Applicable scenarios |

## Migration difficulty

| Level | Criteria | Typical effort |
|-------|----------|----------------|
| S | Simple rename, 1–2 files | Under 1 hour |
| M | ≤10 files, no logic change | Half day |
| L | 10–50 files, partial logic | 1–2 days |
| XL | 50+ files or core logic | 3+ days |

## Codebase search patterns

1. **Imports**: `import.*{ComponentName}`
2. **Token refs**: search token names in CSS/JS
3. **Styles**: CSS variables, Tailwind classes, styled-components
4. **Tests**: component name in test files
5. **Storybook**: stories using the component
