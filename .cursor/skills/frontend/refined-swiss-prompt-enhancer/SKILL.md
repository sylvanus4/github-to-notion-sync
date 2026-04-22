---
name: refined-swiss-prompt-enhancer
description: >-
  Transform vague UI descriptions into structured, design-system-aligned
  implementation prompts enriched with Refined Swiss tokens, component
  patterns, and anti-pattern guardrails.
metadata:
  author: thaki
  version: "1.1.0"
  category: frontend
  origin: google-labs-code/stitch-skills (enhance-prompt + taste-design)
---

# Refined Swiss Prompt Enhancer

Transform vague UI descriptions into structured, design-system-aligned implementation prompts enriched with Refined Swiss tokens, component patterns, and anti-pattern guardrails.

Adapted from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `enhance-prompt` and `taste-design` skills, tailored for the ThakiCloud AI Platform's Refined Swiss design system.

## Triggers

Use when the user asks to "enhance UI prompt", "UI 프롬프트 개선", "refine UI description", "make this UI spec precise", "design-system-aware prompt", "refined-swiss-prompt", "UI 설명 다듬기", "프롬프트 보강", "디자인 토큰 적용 프롬프트", "UI 프롬프트 변환", "디자인 시스템 프롬프트", "UI 명세 생성", "프롬프트 디자인 토큰", "Swiss 프롬프트", "UI 스펙 정교화", "컴포넌트 명세 프롬프트", or provides a rough UI description that needs to be converted into an implementation-ready specification with correct design tokens.

Do NOT use for general prompt optimization without UI context (use prompt-architect). Do NOT use for code generation from a finalized spec (use fsd-development or implement-screen). Do NOT use for design QA of existing code (use design-qa-checklist). Do NOT use for Figma-to-code workflows (use figma-dev-pipeline). Do NOT use for Stitch MCP direct screen generation (use stitch-design). Do NOT use for general text/copywriting prompt improvement (use prompt-transformer).

## Workflow

### Phase 1 — Intent Extraction

Read the user's raw UI description. Identify:

1. **Component type**: page, modal, card, form, table, empty state, etc.
2. **Data model**: what entities and fields are displayed or mutated
3. **User actions**: CRUD operations, navigation, filtering, sorting
4. **Edge cases**: loading, empty, error, overflow, permission-denied states

### Phase 2 — Design Token Injection

Map every visual element to Refined Swiss tokens from `.cursor/rules/design-system.mdc`:

| Element | Token to inject |
|---------|----------------|
| Page background | `bg-surface` |
| Card wrapper | `rounded-lg border border-border bg-surface-card p-4 shadow-sm` |
| Primary button | `rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700` |
| CTA button | `rounded-lg bg-accent-500 px-4 py-2 text-sm font-medium text-white hover:bg-accent-600` |
| Secondary button | `rounded-lg border border-border-strong px-4 py-2 text-sm font-medium text-foreground-secondary` |
| Page title (h1) | `text-xl md:text-2xl font-bold text-foreground` |
| Section heading (h2) | `text-lg font-semibold text-foreground` |
| Body text | `text-sm font-normal text-foreground` |
| Secondary text | `text-sm text-foreground-secondary` |
| Muted text | `text-xs text-foreground-muted` |
| Form input | `min-h-[44px] w-full rounded-lg border border-border bg-surface-card px-3 py-2 text-sm` |
| Badge (success) | `inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium bg-success-100 text-success-800` |
| Table header | `text-xs uppercase bg-surface text-foreground-muted` with `scope="col"` |
| Skeleton loader | `animate-pulse motion-reduce:animate-none rounded bg-skeleton` |
| Empty state | `flex flex-1 items-center justify-center p-4` + `text-sm text-foreground-muted` |
| Icon | `lucide-react` only, `aria-hidden="true"` on decorative icons |

### Phase 3 — Anti-Pattern Guard

Before finalizing the prompt, verify NONE of these patterns appear:

- `rounded-md` on buttons → must be `rounded-lg`
- `focus:outline-none` without `focus-visible:` → must use `focus-visible:outline-none focus-visible:ring-2`
- Hard-coded hex colors → must use semantic tokens
- `dark:bg-gray-*` overrides → must use semantic tokens
- `shadow-md` / `shadow-lg` on regular cards → must use `shadow-sm`
- `animate-spin` or `animate-pulse` without `motion-reduce:animate-none`
- `transition-all` without explicit `duration-*`
- Missing `scope="col"` on `<th>`
- Tables without `overflow-x-auto` wrapper
- Touch targets below `min-h-[44px]`
- Icon-only buttons without `aria-label`
- Modals without `role="dialog"`, `aria-modal="true"`, or focus trap

### Phase 4 — Structured Output

Produce a structured prompt with these sections:

```markdown
## Component: [Name]

### Layout
- Page type: Contained Page | Full-Bleed Workspace
- Container: [max-w-* + padding tokens]

### Data Model
- Entity: [name]
- Fields: [list with types]

### Visual Specification
- [Element]: [exact Tailwind classes from design system]
- ...

### States
- Default: [description]
- Loading: [skeleton pattern]
- Empty: [empty state pattern]
- Error: [error feedback pattern]

### Interactions
- [Action]: [behavior + transition tokens]

### Accessibility
- [ARIA attributes required]
- [Keyboard navigation]
- [Touch target compliance]

### Anti-Pattern Checklist
- [ ] No rounded-md on buttons
- [ ] No hard-coded colors
- [ ] All animations have motion-reduce
- [ ] All touch targets ≥ 44px
- [ ] All icons from lucide-react
```

## Design System Reference

Read `.cursor/rules/design-system.mdc` before every invocation to ensure token accuracy. The design system is the single source of truth — never invent tokens.

## Integration

The enhanced prompt can be passed to:
- `implement-screen` for full page implementation
- `fsd-development` for entity/feature scaffolding
- `figma-to-tds` for Figma-based implementation
- `fe-pipeline` for end-to-end frontend pipeline
