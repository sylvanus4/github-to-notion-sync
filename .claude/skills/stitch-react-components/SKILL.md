---
name: stitch-react-components
description: >-
  Convert Google Stitch designs into modular React + TypeScript components
  with proper data isolation, type safety, and Tailwind theme mapping.
---

# Stitch to React Components

Convert Stitch designs into modular React + TypeScript components with proper data isolation, type safety, and Tailwind CSS theme mapping.

Ported from [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) `react-components`, adapted for Cursor IDE.

## Cursor & Thaki workspace

- **Read** — Stitch output under `.stitch/designs/`, TDS rules (`.cursor/rules/frontend/03-tds-essentials.mdc`, `design-system.mdc`), and the target app’s FSD folders (`entities/`, `features/`, `pages/`, `widgets/`).
- **Write** — Place new components in the correct feature slice; keep mock data in colocated `model/` or `src/data/` per package conventions.
- **Shell** — `npm install` / `pnpm install` in the app package; run `tsc` and lint from that package.
- **Grep** / **SemanticSearch** — Reuse Thaki patterns: overlays (`overlay-layout-patterns`), tables (`07-table-patterns.mdc`), i18n keys.
- **Task** — Split large page extractions: one pass for data/types, one for presentational components.

## Triggers

Use when the user asks to "convert Stitch to React", "Stitch 디자인 React 변환", "Stitch components", "Stitch 컴포넌트 생성", "stitch-react-components", "Stitch HTML to React", "Stitch에서 리액트", "extract React from Stitch", "Stitch 코드 추출", or wants to transform Stitch-generated designs into production React code.

Do NOT use for generating designs in Stitch (use stitch-design). Do NOT use for Figma-to-code conversion (use figma-to-tds). Do NOT use for FSD entity/feature scaffolding without Stitch input (use fsd-development). Do NOT use for general React component review (use frontend-expert). Do NOT use for design QA (use anti-slop-ui-guard).

## Prerequisites

- A Stitch project with generated screens
- Stitch MCP server for retrieving design JSON
- Node.js and npm installed

## Retrieval

1. Use Stitch MCP `get_screen` to retrieve the design JSON
2. Check for existing downloads in `.stitch/designs/{page}.*`
3. Download HTML and screenshots if not present

## Architectural Rules

- **Modular components**: Break designs into independent files
- **Logic isolation**: Move event handlers into custom hooks in `src/hooks/`
- **Data decoupling**: Move static text, URLs, and lists into `src/data/mockData.ts`
- **Type safety**: Every component must have a `Readonly` TypeScript interface `[ComponentName]Props`
- **Style mapping**: Extract Tailwind config from Stitch HTML `<head>`, use theme-mapped classes instead of arbitrary hex codes

## Execution Steps

1. **Environment setup**: `npm install` if `node_modules` is missing
2. **Data layer**: Create `src/data/mockData.ts` from design content
3. **Component drafting**: Build modular React components from the design
4. **Application wiring**: Update entry point (e.g., `App.tsx`) to render new components
5. **Quality check**: Run type checking and verify against design screenshot

## Integration

- Chain after `stitch-design` for design→code workflow
- Feed output into `anti-slop-ui-guard` for design compliance validation
- Use with `stitch-loop` for autonomous build-and-convert cycles
