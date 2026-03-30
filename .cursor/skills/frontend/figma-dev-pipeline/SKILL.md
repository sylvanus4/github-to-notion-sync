---
name: figma-dev-pipeline
description: >-
  Figma 디자인을 코드로 전환하거나 코드를 Figma 화면으로 생성하는 양방향 파이프라인을 오케스트레이션한다.
  디자인 추출, 스펙 생성, 코드 스캐폴딩, 구현 가이드, 검증의 5단계 파이프라인.
  Code Connect로 Figma 컴포넌트와 코드를 시맨틱하게 연결하고,
  search_design_system으로 퍼블리시된 DS 토큰/컴포넌트/스타일을 활용한다.
  Use when the user asks to "convert Figma to code", "Figma 개발 파이프라인",
  "피그마 코드 변환", "디자인 to 코드", "Figma to dev", "디자인 개발 핸드오프",
  "피그마에서 개발", "design to code pipeline", "Figma 컴포넌트 구현",
  "디자인 토큰 추출", "design handoff", "Code Connect", "코드 커넥트",
  "디자인 시스템 연결", "Figma에 화면 만들어줘", "코드에서 피그마로",
  "code to Figma", "push to Figma", "create Figma screen",
  or needs end-to-end Figma-to-code or code-to-Figma workflow.
  Do NOT use for tracking design system changes only (use design-system-tracker).
  Do NOT use for general code generation without Figma input.
  Do NOT use for Figma file browsing without implementation intent.
  Do NOT use for Code Connect mapping only without pipeline context (use figma-code-connect-components plugin skill directly).
metadata:
  author: thaki
  version: "1.1.0"
  category: planning-automation
---

# Figma Dev Pipeline

Orchestrates a **bidirectional** pipeline between Figma and code: Figma-to-code (default) and code-to-Figma. Leverages Code Connect for semantic component linking and `search_design_system` for DS-aware generation.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Content pattern

**Pipeline + inversion**: Confirm direction (Figma→Code or Code→Figma), Figma URL and target stack with the user, then run the phases in order with checkpoints.

## Prerequisites

- Figma MCP authenticated (`plugin-figma-figma` or `user-Figma`).
- Target stack agreed (React/Vue/Svelte/etc.) for Figma→Code direction.
- `search_design_system` available via Figma MCP for DS-aware extraction.
- Code Connect features require **Figma Org or Enterprise** plan. If unavailable, Code Connect steps degrade gracefully (skip with notice).
- For code-to-Figma direction: load `figma-use` plugin skill **before** any `use_figma` API call.

## Input

1. **Direction** (required) — `figma-to-code` (default) | `code-to-figma`. Infer from user intent if not explicit.
2. **Figma URL** (required for figma-to-code) — File, page, or frame link.
3. **Stack** (required for figma-to-code) — React | Vue | Svelte | HTML/CSS | React Native. If missing, stop and ask (inversion gate).
4. **CSS approach** (optional) — Tailwind | CSS Modules | Styled Components | vanilla CSS (default: Tailwind).
5. **Output path** (optional) — Default `./src/components/`.
6. **Existing design system** (optional) — Paths to tokens/components in repo.
7. **Code paths** (required for code-to-figma) — Source files/directories to generate Figma screens from.
8. **Target Figma file** (optional for code-to-figma) — Existing file URL to add screens to; otherwise create new.

**CRITICAL**: Do not start Figma→Code without Figma URL **and** stack. Do not start Code→Figma without code paths.

## Workflow — Figma → Code (default direction)

See [references/pipeline-phases.md](references/pipeline-phases.md) for detail.

### Phase 1: Design extraction

**Step 1 — DS discovery via `search_design_system`:**
- Call `search_design_system` with `includeComponents: true`, `includeVariables: true`, `includeStyles: true` to discover all published DS assets from linked Figma libraries.
- This provides the authoritative token and component inventory for the target file.

**Step 2 — Target frame extraction via `get_design_context`:**
- Use `get_design_context` with the target node/frame URL to extract the specific design being implemented.
- Use `get_metadata` for structural details when needed.

**Step 3 — Reconcile:**
- Map target frame components to discovered DS components (from Step 1).
- Identify which elements use published DS tokens vs hardcoded values.
- Flag non-DS custom elements for attention in Phase 2.

Extracted artifacts:
- Component tree (mapped to DS library entries where possible)
- Tokens (color, type, spacing, shadow, radius) — prefer DS variable names over raw values
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

**Code Connect integration (Org/Enterprise plans):**
1. After scaffolding, call `get_code_connect_suggestions` to check if Code Connect mappings already exist for the Figma components being implemented.
2. If mappings exist: use the suggested code patterns as the implementation baseline.
3. If mappings are missing: after scaffolding is complete, offer to run `send_code_connect_mappings` to link the new code components back to their Figma counterparts.
4. Reference the `figma-code-connect-components` plugin skill for detailed mapping workflows.

If Code Connect is unavailable (non-Org/Enterprise plan), skip with notice and proceed with standard scaffolding.

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

**Code Connect verification (Org/Enterprise plans):**
- Verify Code Connect mappings exist for all scaffolded components — use `get_code_connect_suggestions` to audit.
- Check DS token usage: no hardcoded hex/px values where DS variables exist (cross-reference Phase 1 DS discovery results).
- Report Code Connect coverage % in the verification summary.

- Publish summary to Notion/Slack when requested

## Workflow — Code → Figma (bidirectional mode)

When the user has code but no Figma screens, or wants to push code changes back into Figma.

### Step 1: Analyze code

- Parse source code to extract components, props, states, and token usage.
- Build a component inventory with variant and layout information.

### Step 2: DS discovery

- Call `search_design_system` to find matching published DS components, variables, and styles in the linked Figma libraries.
- Map code components to existing DS components where possible.
- Identify components that need to be created new in Figma.

### Step 3: Generate Figma screens

- **CRITICAL**: Load the `figma-use` plugin skill BEFORE any `use_figma` API call.
- Orchestrate the `figma-generate-design` plugin skill for page/screen-level generation.
- Use `search_design_system` results to import and reuse existing DS components — never recreate primitives that already exist in the library.
- Build section by section using auto-layout and DS tokens (variables, not hardcoded values).

### Step 4: DS bootstrapping (when needed)

- If the target Figma file has no design system library, use `figma-generate-library` to bootstrap tokens (colors, spacing, typography, radius, elevation) and base components from the codebase.
- Then proceed with screen generation (Step 3).

### Step 5: Code Connect linking

- After Figma screens are generated, run `send_code_connect_mappings` to create bidirectional links between the code components and the new Figma components.
- This enables future Figma→Code pipelines to recognize and reuse these components.

**Checkpoint**: Confirm generated Figma screens match code behavior; verify DS token usage.

## Plugin skill references

| Phase | Plugin skill | Purpose |
|-------|-------------|---------|
| Phase 1 (DS discovery) | `figma-generate-design` (Step 2 patterns) | Variable/style search via `search_design_system` |
| Phase 1 (Frame extraction) | `figma-implement-design` | `get_design_context` patterns for reading designs |
| Phase 3 (Code Connect) | `figma-code-connect-components` | Bidirectional Figma↔code component mapping |
| Phase 5 (DS token check) | `figma-create-design-system-rules` | DS rule generation for token compliance |
| Bidirectional Step 3 | `figma-use` | **MANDATORY** gate before any `use_figma` call |
| Bidirectional Step 3 | `figma-generate-design` | Screen generation in Figma using DS |
| Bidirectional Step 4 | `figma-generate-library` | Bootstrap DS in Figma from codebase |

## Examples

### Example 1: Single component

User: "Build this Figma button in React + Tailwind — https://figma.com/file/..."

Phases: extract variants → map tokens + states → scaffold `Button.tsx` → handoff doc → verify.

### Example 2: Full page

User: "Convert checkout page from Figma to Vue"

Phases: extract subcomponents → layout spec → multiple `.vue` files + shared tokens → integration guide → lint + doc gate + optional Notion publish.

### Example 3: Code to Figma (bidirectional)

User: "코드에서 피그마로 대시보드 화면 만들어줘" / "Push the dashboard page to Figma"

Steps: analyze `Dashboard.tsx` → `search_design_system` for DS matches → load `figma-use` → `figma-generate-design` section by section → `send_code_connect_mappings` → verify.

### Example 4: Code Connect setup

User: "Code Connect로 버튼 컴포넌트 연결해줘"

Steps: `get_code_connect_suggestions` for Button → review mappings → `send_code_connect_mappings` to link `Button.tsx` variants to Figma Button variants.

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
| Code Connect unavailable (plan) | Skip Code Connect steps with notice; proceed with standard pipeline |
| `search_design_system` returns empty | No published DS libraries linked; fall back to `get_design_context` extraction |
| `use_figma` call fails | Verify `figma-use` skill was loaded first; check node references |
| No target Figma file for code-to-Figma | Offer to create new file via `figma-create-new-file` plugin skill |
