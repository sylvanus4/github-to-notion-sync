---
name: change-impact-analyzer
description: >-
  Predict downstream impact when specs, policies, or designs change. Build a
  dependency view from Notion relations, code imports, and design component
  usage; estimate cascade scope, affected teams, and risk. Complements cascade
  sync with pre-change prediction. Korean triggers: "변경 영향 분석", "change
  impact", "영향도 예측", "downstream impact", "변경 범위 추정", "impact analysis", "파급
  효과", "연쇄 변경". Do NOT use for applying automated cascade updates (use
  prd-cascade-sync), git-only blast radius without planning links (use
  dependency tools narrowly), or post-release incident analysis (use
  incident-focused workflows).
---

# Change Impact Analyzer

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Before editing a canonical artifact, forecast who and what breaks downstream. Turns implicit dependencies into a ranked impact map for scheduling and communication.

## Prerequisites

- Clear statement of the **proposed change** (even if tentative).
- Seed anchors the user provides (Notion page, path, component, or endpoint).
- Optional stakeholder map: team names or Notion person properties.

## Success criteria

- **Mermaid dependency graph (mandatory)** — You MUST include a Mermaid diagram (`graph TD` or `flowchart`) showing **named nodes**, **edge direction** (cascade/downstream), and **relationship types** (e.g. relation, import, token usage). A table alone does not satisfy E1; the diagram is required unless the user explicitly declines visuals.
- Impact graph lists **concrete nodes** (pages, files, components), not vague areas.
- Risk levels include a **one-line rationale** that **names at least one signal** drawn from [references/impact-criteria.md](references/impact-criteria.md) (e.g. auth/billing path, fan-out band, PII/retention, breaking vs additive API) — not intuition-only labels.
- Comms plan uses the **checklist template** below with **named teams or roles**, **channels**, and **timing** — no placeholder-only rows.

## Inputs

1. **Change proposal** — What will change (spec section, policy clause, Figma component, API field) and intended direction.
2. **Anchors** — Notion page IDs, feature keys, component names, API path, or repo module paths.
3. **Depth** — `1-hop` (direct links only) | `2-hop` | `full` (best-effort within time box).
4. **Stakeholder map** (optional) — Team tags on Notion or manual list for routing.

## Procedure

1. **Normalize change unit** — Express as one or more stable IDs (feature slug, component key, endpoint, policy clause ref).
2. **Graph from Notion** — Traverse relations: PRD ↔ design spec ↔ decision log ↔ policy; record each edge with link and relation type.
3. **Graph from code** — From seed paths, follow imports, shared types, API clients, feature flags, and config keys tied to the change unit.
4. **Graph from design** — List instances of renamed components or tokens (via Figma MCP when available); else use Notion design references.
5. **Merge graphs** — Deduplicate nodes; tag source `notion` | `code` | `design`.
6. **Estimate scope** — Count affected pages/files/components; classify effort `S/M/L` and risk `Low/Med/High` using **only** the concrete signal tables in [references/impact-criteria.md](references/impact-criteria.md) (risk bands, effort bands, cascade probability). For each `Low/Med/High` row, tie the rationale to a **specific criterion line** (e.g. “High: touches auth/payments per risk table”, “Med: 4–12 dependents per risk table”).
7. **Team impact** — Map nodes to owning teams using Notion owner fields or path conventions; highlight cross-team edges.
8. **Output** — Executive summary, **Mermaid dependency graph (required)**, ranked risk register (with criteria-backed rationale), and comms checklist from the template below.

### Workflow notes

- Cap **full** depth with a time box; when truncated, print `frontier` nodes explicitly.
- Separate **breaking** vs **additive** API changes in the risk register.
- For policy changes, include **data retention** and **notification** touchpoints when mentioned in Notion.

## Integrations

- **Notion MCP** — Query databases for backlinks and relations; create an impact memo page.
- **Slack MCP** — DM or channel ping for High-risk changes with @mention guidance per team norms.
- **GitHub MCP** — List likely affected files or recent PRs touching seeds.
- **Google Workspace CLI (`gws`)** — Optional calendar holds for alignment meetings when impact is cross-team.

### Publishing checklist

Analysis-only: **do not** create or edit Notion pages, Slack posts, or calendar events unless the user explicitly asks for that separate step; the default deliverable is the **report body** they can copy. If they request publish, then: (1) save the Mermaid diagram and narrative to a Notion impact memo, (2) post Slack summary with risk emoji legend where applicable, (3) if High risk, propose `gws` Calendar slots in the report for copy-paste.

### Anti-patterns (boundary)

- **Do NOT** modify repository code, run refactors, or apply automated document/PRD updates — this skill is **prediction and analysis only**; cascade application is **prd-cascade-sync**.
- **Do NOT** substitute a bullet list of “affected areas” for the **Mermaid graph** when the user asked for impact analysis (E1).
- **Do NOT** assign risk from gut feel without referencing **impact-criteria.md** signals (E2).

## Output Structure

- Change summary and assumptions.
- **Mermaid** `graph TD` or `flowchart`: every **downstream node** in scope appears as a named vertex; edges show direction and type; if depth is truncated, include **`frontier`** pseudo-nodes or an annotated note on the diagram.
- Table: node, type, owner, risk, **criterion reference** (which row/signal from impact-criteria.md), suggested validation.
- **Communication checklist** (copy this table; replace placeholders with real names — E3):

| Team / Role | Channel (e.g. Slack `#channel`, Notion comment, email) | When (e.g. before PRD edit, after design handoff, T-24h) | What (one line: decision, ask, risk level) |
|-------------|----------------------------------------------------------|--------------------------------------------------------|---------------------------------------------|
| …           | …                                                        | …                                                      | …                                           |

Order rows by recommended notification sequence (earliest first).

## Examples

- **Input:** "If we rename `Organization` to `Workspace` in the PRD, what breaks?" **Output:** Korean impact map across Notion docs, 12 code modules, and 3 design components.
- **Input:** "Tightening data retention policy — downstream?" **Output:** List of features storing affected data types with risk levels.
- **Input:** "Rename design token `color.primary` — who is affected?" **Output:** Code import graph + Figma style usage summary.

## Boundaries

- Predictions are **heuristic**; they do not guarantee completeness without full graph access.
- **Analysis only (E4):** Do not edit Notion, code, Figma, or policies as part of this skill; output is forecasts, graphs, risk register, and comms recommendations. Execution and cascade sync live in other skills/workflows.
- Does **not** perform automated refactors or auto-apply spec changes; pairs with engineering execution tasks and **prd-cascade-sync** when updates are needed.

### When to use which (overlap)

- **change-impact-analyzer** — **PRE-change prediction**: forecast who/what may break before the edit lands; ranked map and comms plan.
- **prd-cascade-sync** — **POST-change propagation**: after a spec/decision changes, sync and update dependent PRD nodes and downstream docs with approval workflows.
- **change-impact-analyzer** — **Single proposed change** or narrow blast radius from one anchor set.
- **cross-domain-sync-checker** — **Comprehensive multi-artifact state comparison** (Notion, Figma, code, policy) for drift and sync status, not only one change’s forward impact.

## Error Handling

- **Incomplete graph** — State uncovered areas; never imply full coverage.
- **Stale Notion links** — Flag broken relations; suggest cleanup task.
- **Monorepo ambiguity** — Prefer explicit seed paths from the user.
- **Private Figma** — Fall back to Notion-listed components only.
- **Circular references** — Detect and break cycles in the diagram with a note on the cycle set.
- **Orphan features** — If no code match, say so; suggest adding repo links to Notion rows.

## Evolution

Binary eval hooks (pass/fail per run):

- **E1 — Dependency graph completeness**: **Mermaid** graph present with named nodes, edge direction, relationship types, and sources (`notion` / `code` / `design`); truncated depth shows explicit `frontier` nodes.
- **E2 — Risk assessment accuracy**: Each `Low/Med/High` row cites **specific signals** from [references/impact-criteria.md](references/impact-criteria.md) (not intuition-only).
- **E3 — Communication checklist actionability**: Table uses **Team \| Channel \| When \| What**; named teams/channels and ordering; no generic “notify stakeholders” only.
- **E4 — Boundary respect**: No code/doc auto-apply; heuristic limits stated; does not substitute for **prd-cascade-sync** or **cross-domain-sync-checker** where those scopes apply.
