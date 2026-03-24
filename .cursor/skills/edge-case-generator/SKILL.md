---
name: edge-case-generator
description: >-
  Generate a structured edge-case matrix from PRD/spec documents: states, boundaries,
  concurrency, errors, permissions, validation limits, network failures, and
  cross-feature interactions; output is planner-ready and traceable to spec sections.
  Korean triggers: "엣지 케이스 생성", "예외 상황 도출", "경계값 분석", "엣지 케이스 매트릭스".
  English triggers: "edge case generator", "edge cases", "boundary analysis",
  "missing edge cases from PRD".
  Do NOT use as a full document quality gate (use doc-quality-gate), code-level reverse
  engineering (use code-to-spec), or formal test-case execution planning alone.
metadata:
  version: "1.0.0"
  category: analysis
  author: thaki
---

# Edge Case Generator

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

From an existing **PRD / spec** (file or Notion page), systematically surface **missing or under-specified edge cases** and deliver an **edge-case matrix** suitable for review with PM/Design/Eng.

## Prerequisites

- Source document accessible (path or **Notion MCP** URL).
- Optional: related policy doc for permission/data rules.

## Procedure

1. **Ingest** — Load full text. If Notion: fetch via **Notion MCP**; preserve heading hierarchy in notes.

2. **Extract baseline** — List stated functional requirements, states, transitions, roles, data fields, external dependencies, SLAs, and non-goals.

3. **Generate dimensions** — For each area below, propose cases **not clearly covered**; mark each as explicit / partial / missing **using Korean labels** in the matrix with cite (section heading or quote fragment):

   - **State machine**: illegal transitions, double-submit, stale UI after async completion
   - **Boundary values**: min/max length, empty collections, timezone, large files
   - **Concurrency**: two tabs, duplicate requests, optimistic UI rollback
   - **Permissions**: role changes mid-session, expired token, partial revoke
   - **Validation**: unicode, whitespace-only, copy-paste anomalies
   - **Network / infra**: timeout, offline, 4xx/5xx, partial success
   - **Cross-feature**: notifications, deep links, feature flags inconsistent
   - **Compliance / policy**: consent withdrawal, retention, audit logging

4. **Build matrix** — Suggested columns (headers and cells **in Korean** in the output):

   | ID | Scenario | Preconditions | Expected behavior (per spec) | Spec reference | Gap level | Recommended action |
   |----|----------|---------------|------------------------------|----------------|-----------|---------------------|

5. **Prioritize** — Tag severity: `P0` (data loss/safety), `P1` (broken core flow), `P2` (degraded UX), `P3` (polish).

6. **Handoff** — Optional: create **Notion** subpage via MCP; or **Slack** summary with matrix link.

7. **Traceability pass** — Re-read the matrix: every row marked missing should have a **testable question** for the author.

## Dimension deep-dive (prompting aid)

- **State machine**: list illegal transitions implied by UI (e.g., checkout complete → cart edit).
- **Boundary values**: numeric fields, string length, pagination limits, file upload size, rate limits.
- **Concurrency**: double clicks, repeated form submit, parallel API calls, cache invalidation timing.
- **Permissions**: role elevation, session expiry, org switching, guest vs member.
- **Validation**: special characters, emoji, leading/trailing spaces, IME composition edge cases.
- **Network / infra**: retries, idempotency, partial responses, webhook duplication.
- **Cross-feature**: analytics events, SEO states, deep links, feature flags, experiments.

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

## Quality checklist

- No fabricated requirements: if the spec is silent, label as missing **in Korean** and propose a question.
- Severity tags align with user impact, not implementation difficulty.
- Korean output uses consistent terminology with the source doc where possible.

## Error handling

- **Source too vague**: Produce matrix with an assumptions column filled; list minimal clarification questions **in Korean**.
- **Notion sync issues**: Fall back to user-exported markdown; note timestamp.
- **Contradictions in spec**: Add contradiction rows **in Korean**; do not auto-resolve.
