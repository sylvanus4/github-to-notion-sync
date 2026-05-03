---
name: shadcn-ui
description: >-
  Expert guidance for integrating and building applications with shadcn/ui
  components — discovery, installation, customization, and best practices with
  Radix UI or Base UI primitives and Tailwind CSS.
---

# shadcn/ui Component Integration

Expert guidance for integrating and building applications with shadcn/ui — a collection of accessible, customizable components built with Radix UI or Base UI and Tailwind CSS that you copy into your project.

Ported from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `shadcn-ui`, adapted for Cursor IDE.

## Cursor & Thaki workspace

- **Shell** — Run `npx shadcn@latest init` / `add` in the correct package root (`thaki-ui/`, `ai-suite/`, `ai-platform-webui/`, etc.); never assume the repo root without checking `package.json` and `components.json`.
- **Read** — Inspect `tailwind.config`, `src/index.css` / `app/globals.css`, and existing `components/ui/` before adding or forking components.
- **Grep** — Locate existing `cn(`, cva patterns, and Radix usage to match project conventions.
- **Write** — Add or extend files only in the target app or shared package; follow FSD layout for feature code (`features/`, `entities/`) per `01-fsd-architecture.mdc` when applicable.
- **SemanticSearch** — Find how sibling pages use tables, forms, and overlays before composing new shadcn blocks.

## Triggers

Use when the user asks to "add shadcn component", "shadcn/ui 컴포넌트 추가", "install shadcn", "shadcn 설치", "shadcn setup", "shadcn 설정", "shadcn component", "shadcn 컴포넌트", "radix ui component", "customize shadcn", "shadcn 커스터마이즈", "shadcn blocks", "shadcn 블록", "shadcn-ui", "init shadcn", "browse shadcn components", "shadcn 레지스트리", or needs help with shadcn/ui component discovery, installation, or customization.

Do NOT use for project-specific TDS components (@thakicloud/shared) (follow 03-tds-essentials.mdc). Do NOT use for Tailwind CSS v4 design system creation (use tailwind-design-system). Do NOT use for Figma component implementation (use figma-to-tds). Do NOT use for general React component architecture (use react-composition-guide). Do NOT use for design system token management (use design-md-generator).

## Core Principles

shadcn/ui is NOT a component library — it's a collection of reusable components you copy into your project:
- **Full ownership**: Components live in your codebase, not node_modules
- **Complete customization**: Modify styling, behavior, and structure freely
- **No version lock-in**: Update components selectively
- **Zero runtime overhead**: No library bundle

## Component Discovery & Installation

### Browse Components
Use the shadcn MCP tools if available:
- `list_components` — Complete catalog
- `get_component_metadata` — Props, dependencies, usage
- `get_component_demo` — Implementation examples

### Installation

```bash
# Recommended: CLI installation
npx shadcn@latest add [component-name]

# Project initialization (new projects)
npx shadcn@latest init
```

### Required Dependencies
- React 18+
- Tailwind CSS 3.0+
- Radix UI or Base UI primitives
- `class-variance-authority` (variant styling)
- `clsx` + `tailwind-merge` (class composition)

## The `cn()` Utility

```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Customization Best Practices

### Theme Customization
Edit CSS variables in `globals.css` for light/dark mode theming.

### Component Variants
Use `class-variance-authority` (cva) for variant logic — define variant, size, and default variants.

### Extending Components
Create wrapper components in `components/` (not `components/ui/`) for project-specific extensions.

## Blocks
shadcn/ui provides complete UI blocks (auth forms, dashboards, sidebars). Use `list_blocks` and `get_block` via MCP.

## Accessibility
Built on Radix UI primitives with keyboard navigation, screen reader support, focus management, and proper ARIA attributes.

## Validation Checklist
1. `tsc --noEmit` — Type check
2. Linter pass
3. Light/dark mode visual QA
4. Responsive breakpoint verification
5. Accessibility tools (axe DevTools)
