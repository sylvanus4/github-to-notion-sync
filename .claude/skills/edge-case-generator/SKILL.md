---
name: edge-case-generator
description: >-
  Generate a structured edge-case matrix from PRD/spec documents: states,
  boundaries, concurrency, errors, permissions, validation limits, network
  failures, and cross-feature interactions; output is planner-ready and
  traceable to spec sections. Korean triggers: "엣지 케이스 생성", "예외 상황 도출", "경계값
  분석", "엣지 케이스 매트릭스". English triggers: "edge case generator", "edge cases",
  "boundary analysis", "missing edge cases from PRD". Do NOT use as a full
  document quality gate (use doc-quality-gate), code-level reverse engineering
  (use code-to-spec), or formal test-case execution planning alone.
disable-model-invocation: true
---

# Edge Case Generator

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

From an existing **PRD / spec** (file or Notion page), systematically surface **missing or under-specified edge cases** and deliver an **edge-case matrix** suitable for review with PM/Design/Eng.

## Prerequisites

- Source document accessible (path or **Notion MCP** URL).
- Optional: related policy doc for permission/data rules.

## Procedure

For dimension deep-dive details, see [references/edge-dimensions.md](references/edge-dimensions.md).

1. **Ingest** — Load full text. If Notion: fetch via **Notion MCP**; preserve heading hierarchy in notes.

2. **Extract baseline** — List stated functional requirements, states, transitions, roles, data fields, external dependencies, SLAs, and non-goals.

3. **Generate dimensions** — For each dimension in the deep-dive reference, propose cases **not clearly covered**; mark each as explicit / partial / missing **using Korean labels** in the matrix with cite (section heading or quote fragment).

4. **Build matrix** — Suggested columns (headers and cells **in Korean** in the output):

   | ID | Scenario | Preconditions | Expected behavior (per spec) | Spec reference | Gap level | Recommended action |
   |----|----------|---------------|------------------------------|----------------|-----------|---------------------|

5. **Prioritize** — Tag severity: `P0` (data loss/safety), `P1` (broken core flow), `P2` (degraded UX), `P3` (polish).

6. **Handoff** — Optional: create **Notion** subpage via MCP; or **Slack** summary with matrix link.

7. **Traceability pass** — Re-read the matrix: every row marked missing should have a **testable question** for the author.

## Notion MCP ingestion

- Pull page content with headings intact; preserve bullet hierarchy in working notes.
- If the PRD spans multiple linked pages, include linked pages up to user cap (default: 3 pages).

## Slack MCP distribution

- Post `P0/P1` count in the main message; full matrix in thread or Notion link to avoid noise.

## Output structure (sections must be written in Korean)

1. Document summary (scope and assumptions)
2. Edge-case matrix (table)
3. P0/P1 discussion list
4. Spec revision suggestions (by section)
5. Validation questions (engineering/design/policy)

## Examples

- **Checkout PRD** — Surfaces partial payment retry, idempotency key missing, cart merge across devices.

- **Permissions PRD** — Surfaces admin vs member invite flows, token expiry, and audit log gaps.

## Boundaries

- **edge-case-generator** — Comprehensive **gap hunting** from a PRD/spec: matrix of missing/partial coverage and testable questions.
- **prd-state-matrix** — **Extract and organize existing** states and transitions into a structured matrix from the document; use when the primary goal is state inventory consolidation, not broad edge discovery.

## Quality checklist

- No fabricated requirements: if the spec is silent, label as missing **in Korean** and propose a question.
- Severity tags align with user impact, not implementation difficulty.
- Korean output uses consistent terminology with the source doc where possible.

## Error Handling

- **Source too vague**: Produce matrix with an assumptions column filled; list minimal clarification questions **in Korean**.
- **Notion sync issues**: Fall back to user-exported markdown; note timestamp.
- **Contradictions in spec**: Add contradiction rows **in Korean**; do not auto-resolve.

## Evolution

Binary eval hooks (pass/fail per run):

- **E1 — Matrix completeness**: Table includes all columns from **Procedure step 4**; each row has scenario, gap level, and spec reference or explicit “silent in spec”.
- **E2 — Severity accuracy**: P0–P3 tags match user-impact definitions in **Procedure step 5**, not implementation difficulty alone.
- **E3 — Spec traceability**: Every non-assumption row cites section heading or short quote fragment from the source.
- **E4 — No fabrication**: No row presents invented requirements as stated facts; silent spec areas are labeled missing and phrased as questions.
