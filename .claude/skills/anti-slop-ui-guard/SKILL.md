---
name: anti-slop-ui-guard
description: >-
  Detect and reject generic, template-looking, or design-system-violating UI
  code. Scans TSX/CSS for 35+ anti-patterns defined by the Refined Swiss
  design system and produces a severity-ranked violation report with auto-fix.
---

# Anti-Slop UI Guard

Detect and reject generic, template-looking, or design-system-violating UI code before it enters the codebase. Scans TSX/CSS for 35+ anti-patterns defined by the Refined Swiss design system and produces a severity-ranked violation report with auto-fix suggestions.

Adapted from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `taste-design` anti-pattern enforcement, tailored for the ThakiCloud AI Platform's Refined Swiss design system.

## Triggers

Use when the user asks to "check UI slop", "UI 슬롭 점검", "design anti-pattern scan", "디자인 안티패턴 검사", "anti-slop", "UI 품질 검사", "generic UI check", "디자인 위반 검사", "taste check", "is this UI good enough", "does this follow our design system", "디자인 시스템 준수 확인", "UI 코드 맛 검사", "디자인 토큰 위반", "안티 슬롭 가드", "UI 위반 스캔", "디자인 규칙 점검", "코드 디자인 검증", or after generating UI code that needs design compliance validation.

Do NOT use for code logic review (use deep-review or simplify). Do NOT use for AI code slop cleanup without UI focus (use omc-ai-slop-cleaner). Do NOT use for full design QA with screenshots (use design-qa-checklist). Do NOT use for UX heuristic evaluation (use ux-expert). Do NOT use for accessibility-only audits (use kwp-design-accessibility-review). Do NOT use for Tailwind class sorting or formatting only (use linters). Do NOT use for design system documentation generation (use design-md-generator).

## Violation Categories

### Category A — Token Violations (Severity: HIGH)

These break dark mode, theming, and design consistency.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| A1 | Hard-coded hex colors | `/#[0-9a-fA-F]{3,8}/` in className | Replace with semantic token |
| A2 | `dark:bg-gray-*` overrides | `dark:bg-gray` or `dark:text-gray` | Use semantic token that auto-switches |
| A3 | Non-semantic gray values | `bg-gray-*`, `text-gray-*` without semantic wrapper | Use `bg-surface`, `text-foreground`, etc. |
| A4 | Missing dark mode support | Surface/text without semantic token | Swap to CSS custom property token |

### Category B — Component Shape Violations (Severity: HIGH)

These break visual consistency across the application.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| B1 | `rounded-md` on buttons | `rounded-md` in button-like elements | Use `rounded-lg` |
| B2 | Wrong button padding | `px-5`, `px-6`, `py-2.5` on standard buttons | Use `px-4 py-2` |
| B3 | Wrong disabled opacity | `disabled:opacity-60` or `disabled:opacity-40` | Use `disabled:opacity-50` |
| B4 | Wrong shadow on cards | `shadow-md` or `shadow-lg` on non-elevated cards | Use `shadow-sm` |
| B5 | `hover:shadow-md` on default cards | Elevated hover on non-interactive cards | Remove or use Elevated card variant |
| B6 | Wrong badge size | `text-2xs` on badges | Use `text-xs` |
| B7 | Non-standard max-width | `max-w-7xl`, `max-w-5xl`, `max-w-4xl`, `max-w-screen` | Use `max-w-6xl` or other allowed values |

### Category C — Accessibility Violations (Severity: HIGH)

These break WCAG AA compliance.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| C1 | Missing focus-visible | `focus:outline-none` without `focus-visible:` | Add `focus-visible:outline-none focus-visible:ring-2` |
| C2 | Small touch targets | Interactive elements without `min-h-[44px]` | Add `min-h-[44px]` |
| C3 | Icon-only button without label | `<button>` with only icon child, no `aria-label` | Add `aria-label` |
| C4 | `<th>` without scope | `<th>` missing `scope="col"` | Add `scope="col"` |
| C5 | Table without overflow wrapper | `<table>` not inside `overflow-x-auto` | Wrap in `overflow-x-auto rounded-lg border border-border` |
| C6 | Modal without ARIA | Modal missing `role="dialog"` or `aria-modal="true"` | Add required ARIA attributes |
| C7 | Tabs without ARIA | Tab elements missing `role="tab"`, `aria-selected` | Add required tab ARIA attributes |

### Category D — Animation Violations (Severity: MEDIUM)

These cause motion sickness for users with vestibular disorders.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| D1 | `animate-spin` without motion-reduce | `animate-spin` without `motion-reduce:animate-none` | Add `motion-reduce:animate-none` |
| D2 | `animate-pulse` without motion-reduce | `animate-pulse` without `motion-reduce:animate-none` | Add `motion-reduce:animate-none` |
| D3 | `transition-all` without duration | `transition-all` without `duration-*` | Add explicit `duration-200` or similar |

### Category E — Typography Violations (Severity: MEDIUM)

These break the typographic hierarchy.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| E1 | Serif fonts | `font-serif` anywhere | Remove; use `font-sans` (Inter) |
| E2 | Wrong heading weight | `font-bold` on h2/h3 | Use `font-semibold` for h2/h3, `font-bold` for h1 only |
| E3 | Wrong icon library | Import from non-lucide-react icon lib | Replace with `lucide-react` equivalent |

### Category F — Design Taste Violations (Severity: LOW)

These produce "generic AI" aesthetics.

| ID | Pattern | Detection | Fix |
|----|---------|-----------|-----|
| F1 | Teal/stone colors | `teal-*`, `stone-*` in classes | Use blue brand + gray neutrals |
| F2 | Gratuitous gradients | `bg-gradient-*` on non-hero elements | Use flat semantic colors |
| F3 | Excessive shadows | Multiple shadow layers on simple elements | Use `shadow-sm` |
| F4 | Rainbow status colors | Non-semantic status colors | Use success/error/warning tokens |
| F5 | New z-index values | z-index outside (auto, 10, 30, 40, 50, 60) | Use the defined scale |

## Scan Process

### Step 1 — Scope Selection

Accept one of:
- `--diff`: Scan only `git diff` changed files (default)
- `--files <paths>`: Scan specific files
- `--full`: Scan entire `frontend/src/`

Filter to `*.tsx`, `*.ts`, `*.css` files only.

### Step 2 — Pattern Matching

For each file, run all violation detectors. Use:
- Grep/regex for class-based patterns (A1-A4, B1-B7, D1-D3, E1-E3, F1-F5)
- AST-aware checks for structural patterns (C1-C7) via SemanticSearch when needed

### Step 3 — Report Generation

Produce a structured report:

```markdown
# Anti-Slop UI Guard Report

## Summary
- Files scanned: N
- Violations found: N (HIGH: N, MEDIUM: N, LOW: N)
- Pass/Fail: [PASS if 0 HIGH violations, FAIL otherwise]

## Violations

### [file.tsx]

| ID | Severity | Line | Pattern | Fix |
|----|----------|------|---------|-----|
| A1 | HIGH | 42 | `#3b82f6` hard-coded | Use `brand-500` |
| B1 | HIGH | 55 | `rounded-md` on button | Use `rounded-lg` |
| D1 | MEDIUM | 78 | `animate-spin` without motion-reduce | Add `motion-reduce:animate-none` |

## Auto-Fix Available
[List of violations that can be auto-fixed with StrReplace]
```

### Step 4 — Auto-Fix (Optional)

When invoked with `--fix`, apply safe auto-fixes for deterministic replacements:
- `rounded-md` → `rounded-lg` on buttons
- Add `motion-reduce:animate-none` next to `animate-spin`/`animate-pulse`
- Add `scope="col"` to `<th>` elements
- Replace `disabled:opacity-60` → `disabled:opacity-50`

Skip ambiguous fixes that require human judgment (e.g., choosing the right semantic color token).

## Integration

- Run as part of `design-qa-checklist` for comprehensive design QA
- Run as part of `ui-design-harness` for the full UI quality pipeline
- Run before `ship` or `release-commander` to catch design violations pre-merge
- Run after `implement-screen` or `fsd-development` to validate generated code
