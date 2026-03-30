---
name: user-flow-mapper
description: >-
  Generate visual user-flow diagrams from PRDs, code, or specs: navigation, decisions,
  errors, and success paths. Output Mermaid diagrams, markdown flowcharts, or HTML via
  visual-explainer; cover happy path and key edge cases.
  Korean triggers: "사용자 플로우", "user flow", "플로우 다이어그램", "user flow mapper",
  "화면 흐름도", "flow diagram", "사용자 여정 맵", "유저 플로우". Do NOT use for
  market-level customer journey maps only (use pm-market-research journey tools), code
  reverse spec tables without diagrams (use code-to-spec), or interactive prototype
  building (manual design tools).
metadata:
  author: thaki
  version: "1.0.0"
  category: analysis
---

# User Flow Mapper

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Make navigable, testable flows explicit for reviews, QA, and onboarding. Converts narrative specs or code routes into diagrams planners and engineers share.

## Prerequisites

- One primary **source** (Notion PRD, code map, or narrative).
- Named **actor** and whether admin/support paths are in scope.
- Chosen **output format** (Mermaid default unless HTML requested via visual-explainer).

## Success criteria

- Happy path is **one continuous** path from entry to success state.
- Each **decision** shows at least one non-happy branch when depth is `standard` or `deep`.
- Open assumptions are listed, not hidden.

## Inputs

1. **Source** — Notion PRD URL, pasted requirements, repository route map, or demo URL description.
2. **Actor** — Primary user role; optional secondary actors (admin, support).
3. **Depth** — `happy-path` | `standard` (happy + top errors) | `deep` (+ permission variants).
4. **Output format** — `mermaid` | `markdown` | `html` (invoke visual-explainer for rich HTML when user wants a standalone page).

## Procedure

1. **Extract steps** — Identify screens, modals, branches, and terminal states from the source; label each with a stable step ID.
2. **Decision points** — Conditions (validation failure, empty data, denied permission, network error) become diamonds or labeled edges.
3. **Parallelism** — Note async operations (polling, background jobs) as annotations, not false linear sequences.
4. **Cross-feature hooks** — Show entry/exit to other flows (login, settings, billing) as subgraphs or labeled off-ramps.
5. **Edge coverage** — For `standard` and `deep`, ensure at least one recovery path per critical error class mentioned in the spec.
6. **Diagram** — Build Mermaid `flowchart TD` or `stateDiagram-v2` when states dominate; keep labels concise Korean with English proper nouns allowed.
7. **Narrative** — Short Korean walkthrough under the diagram: preconditions, success criteria, known gaps.
8. **Traceability** — Map nodes to spec section headings or source files when available.

### Workflow notes

- Prefer **verbs on edges** (`submit`, `retry`, `cancel`) for clarity in reviews.
- Collapse repeated loops (pagination) into a note unless the user asks for full detail.
- When code and spec disagree, draw **two** dashed variants labeled `spec` vs `code` and explain.

## Integrations

- **Notion MCP** — Fetch PRD content; publish flow as a child page or embed in the spec.
- **Slack MCP** — Share Mermaid in a fenced block or link to Notion/HTML artifact.
- **Browser MCP** — When a URL is provided, verify steps against visible UI (note deviations).
- **visual-explainer skill** — Produce a polished HTML diagram page when requested.

### Publishing checklist

1. Paste Mermaid into Notion code block or attach HTML link from visual-explainer.
2. Slack: send overview diagram + link to full doc for long flows.
3. Optional: add the diagram URL to the PRD properties if the team tracks artifacts there.

## Output Structure

- Actor and scope statement.
- Primary diagram (Mermaid or equivalent).
- Edge-case addendum list (if not all rendered).
- Open questions / assumptions.

## Examples

- **Input:** "Map checkout from our Notion PRD section 4." **Output:** Korean-labeled Mermaid flow with payment failure branch.
- **Input:** "Show admin invite flow from code routes." **Output:** Flowchart with file references on edges.
- **Input:** "Deep flow for payment including 3DS and network errors." **Output:** Expanded subgraph with labeled recovery paths.

## Boundaries

- Not a **replacement** for automated E2E tests; diagrams aid humans, not CI.
- Does **not** include analytics funnel definitions unless the user supplies them.

## Error Handling

- **Contradictory spec** — Draw tentative flow; list conflicts for resolution.
- **Missing states** — Mark `TBD` nodes rather than guessing UX.
- **Huge flows** — Split into per-episode diagrams plus a high-level overview diagram.
- **Unreadable source** — Request minimal bullet outline from user before mapping.
- **Mermaid size limits** — Split into `Part A/B` diagrams with a master overview node.
- **Concurrent edits** — If live collab changes the spec mid-run, timestamp the diagram context.

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:

- `.cursor/skills/references/project-overrides/project-terminology-glossary.md` (POL-001 — product name, domain terms, forbidden terms)
- `.cursor/skills/references/project-overrides/project-ssot.md` (POL-005 — artifact locations, not-used systems)

Key constraints:

- Prefer **financial-domain** journey examples when illustrating flows (e.g. stock screening → signal detection → order preview → execution → P&L tracking).
- Label nodes and branches using POL-001 terminology and forbidden-term rules.
- When linking artifacts, follow POL-005 for canonical doc and output locations.
