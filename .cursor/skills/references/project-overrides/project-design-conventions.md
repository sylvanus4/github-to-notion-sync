# Project Design Conventions — AI Stock Analytics

> Override for TDS / @thakicloud/shared references.
> Source: `docs/policies/02-uiux-design-policy.md` (POL-002)

## Design System

| Item | Value |
|------|-------|
| Theme | Refined Swiss |
| CSS Framework | Tailwind CSS v4 |
| Component Library | Radix UI (headless) |
| Icons | lucide-react (only — no other icon libs) |
| Fonts | Inter (body), Fira Code (numbers/code) |
| Dark mode | CSS Custom Properties auto-switch |
| Accessibility | WCAG 2.1 AA |
| Token source | `.cursor/rules/design-system.mdc` |

## NOT Used

- `@thakicloud/shared` (TDS)
- `@tabler/icons-react`
- Figma
- Code Connect

## Color Tokens

### Brand (Trust Blue)
- `brand-500`: #3b82f6 (focus ring)
- `brand-600`: #2563eb (primary button, active)
- `brand-700`: #1d4ed8 (hover)
- `brand-100`: #dbeafe (selected background)

### Accent (Orange CTA)
- `accent-500`: #f97316 (CTA button)
- `accent-600`: #ea580c (CTA hover)

### Financial Domain Colors
- **Gain/Profit**: `text-success-text` (green)
- **Loss**: `text-error-text` (red)
- **Neutral**: `text-foreground-muted`
- **BUY signal**: `brand-600` bg + white text
- **SELL signal**: `error-600` bg + white text

## Component Quick Reference

| Component | Framework | Key Classes |
|-----------|-----------|-------------|
| Button (Primary) | HTML+Tailwind | `bg-brand-600 text-white rounded-lg min-h-[44px]` |
| Button (CTA) | HTML+Tailwind | `bg-accent-500 text-white rounded-lg` |
| Card | HTML+Tailwind | `rounded-lg border border-border bg-surface-card p-4 shadow-sm` |
| Table | HTML+Tailwind | `overflow-x-auto rounded-lg border border-border` |
| Form Input | Radix+Tailwind | `min-h-[44px] border border-border focus-visible:ring-2` |
| Dialog/Modal | Radix Dialog | `@radix-ui/react-dialog` |
| Select | Radix Select | `@radix-ui/react-select` |
| Tabs | Radix Tabs | `@radix-ui/react-tabs` |
| Chart | Recharts | Transparent bg, grid = border-border |

## Anti-Patterns

| Forbidden | Use Instead |
|-----------|-------------|
| Hardcoded hex in components | Semantic tokens |
| `dark:bg-gray-*` manual override | CSS Custom Properties |
| `rounded-md` on buttons | `rounded-lg` |
| `@thakicloud/shared` import | Local Tailwind + Radix |
| Figma reference | `design-system.mdc` |
| serif fonts | Inter only |
