---
name: figma-dev-pipeline
description: >-
  Figma 디자인을 코드로 전환하는 전체 파이프라인을 오케스트레이션한다.
  디자인 추출, 스펙 생성, 코드 스캐폴딩, 구현 가이드, 검증의 5단계 파이프라인.
  Use when the user asks to "convert Figma to code", "Figma 개발 파이프라인",
  "피그마 코드 변환", "디자인 to 코드", "Figma to dev", "디자인 개발 핸드오프",
  "피그마에서 개발", "design to code pipeline", "Figma 컴포넌트 구현",
  "디자인 토큰 추출", "design handoff", or needs end-to-end Figma-to-code workflow.
  Do NOT use for tracking design system changes only (use design-system-tracker).
  Do NOT use for general code generation without Figma input.
  Do NOT use for Figma file browsing without implementation intent.
metadata:
  author: thaki
  version: "1.0.1"
  category: planning-automation
---

# Figma Dev Pipeline

Orchestrates a five-phase flow from Figma to implementation-ready code and docs.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Content pattern

**Pipeline + inversion**: Confirm Figma URL and target stack with the user, then run the five phases in order with checkpoints.

## Prerequisites

- Figma MCP authenticated.
- Target stack agreed (React/Vue/Svelte/etc.).

## Input

1. **Figma URL** (required) — File, page, or frame link.
2. **Stack** (required) — React | Vue | Svelte | HTML/CSS | React Native. If missing, stop and ask (inversion gate).
3. **CSS approach** (optional) — Tailwind | CSS Modules | Styled Components | vanilla CSS (default: Tailwind).
4. **Output path** (optional) — Default `./src/components/`.
5. **Existing design system** (optional) — Paths to tokens/components in repo.

**CRITICAL**: Do not start without Figma URL **and** stack.

## Workflow

See [references/pipeline-phases.md](references/pipeline-phases.md) for detail.

### Phase 1: Design extraction

Via Figma MCP:

- Component tree
- Tokens (color, type, spacing, shadow, radius)
- Layout (Auto Layout → flex/grid mapping)
- Assets (icons, images)

**Checkpoint 1**: Confirm extracted component and token inventory with the user.

### Phase 2: Spec generation

- Map tokens to CSS/Tailwind per [references/token-mapping.md](references/token-mapping.md).
- Per-component spec markdown.
- Optional state matrix via `prd-state-matrix`.

**Checkpoint 2**: Confirm mappings and specs.

### Phase 3: Code scaffolding

- File/folder layout
- Token files (CSS variables / Tailwind / theme object)
- Component shells (props, state, render)
- Styles wired to tokens

### Phase 4: Implementation guide

- Per-component dev notes
- Edge-case checklist
- A11y notes
- Interaction spec (hover, focus, motion)
- Optional plain-language summary via `tech-doc-translator`

### Phase 5: Verification

- Lint / typecheck
- Doc quality pass (`doc-quality-gate`) on generated docs
- Visual QA checklist (manual or browser MCP)
- Publish summary to Notion/Slack when requested

## Examples

### Example 1: Single component

User: "Build this Figma button in React + Tailwind — https://figma.com/file/..."

Phases: extract variants → map tokens + states → scaffold `Button.tsx` → handoff doc → verify.

### Example 2: Full page

User: "Convert checkout page from Figma to Vue"

Phases: extract subcomponents → layout spec → multiple `.vue` files + shared tokens → integration guide → lint + doc gate + optional Notion publish.

## Error handling

| Error | Action |
|-------|--------|
| Figma MCP not authed | Prompt `mcp_auth`; stop until connected |
| File not accessible | Ask user to fix sharing |
| Stack missing | List options; inversion gate |
| Unsupported stack | List supported stacks; offer HTML/CSS fallback |
| Very deep component (50+ layers) | Propose splitting into subcomponents |
| Token clash with existing DS | Prefer existing tokens; extend deliberately |
| Phase failure | Retry phase or roll back to prior checkpoint |
