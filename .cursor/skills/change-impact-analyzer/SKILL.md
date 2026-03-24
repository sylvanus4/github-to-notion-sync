---
name: change-impact-analyzer
description: >-
  Predict downstream impact when specs, policies, or designs change. Build a dependency
  view from Notion relations, code imports, and design component usage; estimate cascade
  scope, affected teams, and risk. Complements cascade sync with pre-change prediction.
  Korean triggers: "변경 영향 분석", "change impact", "영향도 예측", "downstream impact",
  "변경 범위 추정", "impact analysis", "파급 효과", "연쇄 변경". Do NOT use for
  applying automated cascade updates (use prd-cascade-sync), git-only blast radius
  without planning links (use dependency tools narrowly), or post-release incident
  analysis (use incident-focused workflows).
metadata:
  author: thaki
  version: "1.0.0"
  category: analysis
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

- Impact graph lists **concrete nodes** (pages, files, components), not vague areas.
- Risk levels include a **one-line rationale** (fan-out, revenue path, compliance).
- Comms plan names **channels** (Slack, Notion comment) without assuming private DMs.

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
6. **Estimate scope** — Count affected pages/files/components; classify effort `S/M/L` and risk `Low/Med/High` based on fan-out and critical path (auth, billing, signup).
7. **Team impact** — Map nodes to owning teams using Notion owner fields or path conventions; highlight cross-team edges.
8. **Output** — Executive summary, dependency diagram (Mermaid), ranked risk register, and recommended comms sequence.

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

1. Save the Mermaid diagram and narrative to a Notion impact memo.
2. Post Slack summary with risk emoji legend (optional team convention).
3. If High risk, propose `gws` Calendar slots in the report body for copy-paste.

## Output Structure

- Change summary and assumptions.
- Mermaid `graph TD` or `flowchart` of primary dependencies.
- Table: node, type, owner, risk, suggested validation.
- Comms checklist (who to notify, in what order).

## Examples

- **Input:** "If we rename `Organization` to `Workspace` in the PRD, what breaks?" **Output:** Korean impact map across Notion docs, 12 code modules, and 3 design components.
- **Input:** "Tightening data retention policy — downstream?" **Output:** List of features storing affected data types with risk levels.
- **Input:** "Rename design token `color.primary` — who is affected?" **Output:** Code import graph + Figma style usage summary.

## Boundaries

- Predictions are **heuristic**; they do not guarantee completeness without full graph access.
- Does **not** perform automated refactors; pairs with engineering execution tasks.

## Error Handling

- **Incomplete graph** — State uncovered areas; never imply full coverage.
- **Stale Notion links** — Flag broken relations; suggest cleanup task.
- **Monorepo ambiguity** — Prefer explicit seed paths from the user.
- **Private Figma** — Fall back to Notion-listed components only.
- **Circular references** — Detect and break cycles in the diagram with a note on the cycle set.
- **Orphan features** — If no code match, say so; suggest adding repo links to Notion rows.
