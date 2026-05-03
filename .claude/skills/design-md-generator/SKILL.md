---
name: design-md-generator
description: >-
  Analyze the project's frontend codebase and design-system.mdc to generate a
  structured DESIGN.md in the awesome-design-md format, optimized for AI-agent
  UI generators like Google Stitch and Cursor.
disable-model-invocation: true
---

# Design MD Generator

Analyze the project's frontend codebase and `.cursor/rules/design-system.mdc` to generate a structured `DESIGN.md` file in the [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) format, optimized for AI-agent UI generators like Google Stitch and Cursor.

Adapted from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `design-md` skill, tailored for the ThakiCloud AI Platform's Refined Swiss design system.

## Triggers

Use when the user asks to "generate DESIGN.md", "create design document", "design-md", "DESIGN.md 생성", "디자인 문서 생성", "AI용 디자인 시스템 문서", "awesome-design-md", "Stitch 디자인 문서", "디자인 토큰 문서화", "디자인 시스템 문서화", "머신 리더블 디자인 문서", "AI 에이전트 디자인 문서", "디자인 MD 생성", "DESIGN.md 갱신", or needs a machine-readable design system document for AI agent consumption.

Do NOT use for design QA of existing code (use design-qa-checklist). Do NOT use for Figma-to-code workflows (use figma-dev-pipeline). Do NOT use for creating UI components (use fsd-development). Do NOT use for design system tracking (use design-system-tracker). Do NOT use for design system rule authoring (edit design-system.mdc directly). Do NOT use for anti-pattern scanning (use anti-slop-ui-guard).

## Workflow

### Phase 1 — Source Analysis

1. Read `.cursor/rules/design-system.mdc` as the authoritative design system source
2. Scan `frontend/src/index.css` for CSS custom property definitions
3. Scan `tailwind.config.js` / `tailwind.config.ts` for extended theme tokens
4. Sample 5-10 representative components from `frontend/src/` to extract usage patterns

### Phase 2 — Token Extraction

Extract and categorize all design tokens:

#### Colors
- Surface palette (bg-surface, bg-surface-card, bg-surface-elevated)
- Foreground palette (text-foreground, text-foreground-secondary, text-foreground-muted)
- Border palette (border-border, border-border-strong)
- Brand palette (brand-50 through brand-900)
- Accent palette (accent-400, accent-500, accent-600)
- Feedback palettes (error, success, warning — surface, surface-strong, text variants)
- Skeleton palette (bg-skeleton, bg-skeleton-muted)

#### Typography
- Font families (Inter for sans, Fira Code for mono)
- Size scale (text-2xs through text-xl)
- Weight scale (normal, medium, semibold, bold)
- Heading hierarchy (h1, h2, h3, caption)

#### Spacing & Layout
- Page padding (p-3 md:p-6)
- Card padding (p-4)
- Max-width values (max-w-6xl default, max-w-3xl reading, etc.)
- Grid patterns (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4)

#### Effects
- Shadows (shadow-sm default, shadow-xl modal)
- Border radius (rounded-lg standard, rounded-xl modal, rounded-full badge/icon-btn)
- Animations (fade-in-up, fade-in, scale-in, slide-in-right)
- Z-index scale (auto, 10, 30, 40, 50, 60)

### Phase 3 — Component Pattern Catalog

Document each component variant with exact Tailwind classes:

- **Buttons**: Primary, CTA, Secondary, Danger, Ghost, Icon
- **Cards**: Default, Flush, Modal, Elevated
- **Badges**: Success, Error, Warning, Brand, Neutral
- **Form Inputs**: Text input, label, placeholder
- **Tabs**: Container, active tab, inactive tab
- **Dropdowns**: Trigger, container, menu item
- **Modals**: Overlay, content (with size presets)
- **Loading**: Skeleton, spinner, text
- **Empty States**: Container, text pattern
- **Pagination**: Container, info text, buttons
- **Progress Bar**: Track, fill
- **Tables**: Header, row, wrapper

### Phase 4 — Anti-Pattern Registry

List all prohibited patterns from the design system with their corrections:

```yaml
anti_patterns:
  - pattern: "rounded-md on buttons"
    correction: "Use rounded-lg"
  - pattern: "Hard-coded hex colors"
    correction: "Use semantic Tailwind tokens"
  - pattern: "dark:bg-gray-* overrides"
    correction: "Use semantic tokens that auto-switch"
  # ... all 25+ anti-patterns from design-system.mdc
```

### Phase 5 — DESIGN.md Generation

Output a single `DESIGN.md` file at the project root with this structure:

```markdown
# DESIGN.md — Refined Swiss

> Machine-readable design system for AI-agent UI generators.
> Source of truth: `.cursor/rules/design-system.mdc`

## Design Direction
[Refined Swiss description]

## Color Tokens
[Structured color tables with CSS custom property names, hex values, and usage]

## Typography
[Font families, size scale, weight scale, heading hierarchy]

## Spacing
[Padding, margin, gap conventions]

## Layout
[Page types, max-width values, grid patterns]

## Components
[Each component with variant classes]

## Icons
[lucide-react conventions, size scale]

## Animation
[Entry animations, continuous animations, rules]

## Accessibility
[WCAG AA requirements, ARIA patterns, touch targets]

## Anti-Patterns
[Complete list with corrections]

## Theme
[Light/dark mode management]
```

### Phase 6 — Validation

Verify the generated DESIGN.md:
1. Every token referenced in DESIGN.md exists in design-system.mdc
2. No invented tokens appear
3. All anti-patterns from design-system.mdc are listed
4. Component classes match the canonical definitions exactly

## Output

Save the file to `DESIGN.md` at the project root (or a user-specified path).

## Integration

The generated DESIGN.md can be used by:
- Google Stitch for design-aware UI generation
- `refined-swiss-prompt-enhancer` as a machine-readable reference
- `anti-slop-ui-guard` for automated design compliance checking
- Any AI agent that needs to generate UI code aligned with the project's design system
