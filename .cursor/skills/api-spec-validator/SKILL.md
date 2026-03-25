---
name: api-spec-validator
description: >-
  Validate implemented APIs (from repository code or OpenAPI/Swagger) against planned
  specifications on Notion: endpoints, schemas, errors, auth, rate limits. Produces a
  gap report answering whether code matches the spec.
  Korean triggers: "API 검증", "api spec validator", "API 스펙 대조", "코드 스펙 비교",
  "API 정합성", "api validation", "기획서 API 비교", "스웨거 대조". Do NOT use for
  first-time reverse documentation from code only (use code-to-spec), generic code review
  (use deep-review), or publishing formal API reference docs (use technical-writer).
metadata:
  author: thaki
  version: "1.0.0"
  category: analysis
---

# API Spec Validator

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Close the loop between planning documents and shipped HTTP APIs. Surfaces mismatches early with traceable evidence for PM and engineering.

## Prerequisites

- A **single spec source of truth** on Notion (page or database) for the API slice under review.
- Implementation reference: OpenAPI file/URL or identifiable route code in the repository.
- Agreement on **auth model** (Bearer, cookies, mTLS) to compare consistently.

## Success criteria

- Every endpoint row in the matrix has a **decisive** status or explicit `ambiguous` with questions.
- Field-level mismatches name **both** spec location and code/OpenAPI pointer.
- Live probes (if any) are **read-only** and documented in the report.

## Inputs

1. **Spec source** (required) — Notion page(s) or database rows describing endpoints, payloads, errors, auth, and limits.
2. **Implementation source** — Git paths for route handlers/controllers, or a Swagger/OpenAPI URL or file in the repo.
3. **Environment** — Optional base URL for probing (read-only GETs only unless user approves).
4. **Version focus** — v1, v2, or delta since a given date/PR.

## Procedure

1. **Extract planned contract** — Parse Notion content into a structured list: method, path, query/body schema summary, success shape, error codes/messages, auth scheme, pagination, idempotency, rate limits.
2. **Extract actual contract** — From OpenAPI: use declared paths and schemas. Else: infer from framework route decorators, validation middleware, and response serializers; note confidence level.
3. **Align inventory** — Match by normalized path template and method; flag spec-only and code-only endpoints.
4. **Compare dimensions** — Request fields (required/optional, types), response fields, status codes, error model, auth requirements, deprecation headers, breaking vs additive changes.
5. **Behavioral hints** — If safe probes allowed, note discrepancies between live status codes and documentation (document probe scope).
6. **Gap report** — For each item: `match` | `partial` | `missing_in_code` | `missing_in_spec` | `ambiguous`; include remediation owner suggestion.
7. **Action items** — Ordered backlog: contract tests, spec update, code fix, or joint clarification meeting.

### Workflow notes

- Normalize paths (`/users/{id}`) before comparison; treat trailing slash policy explicitly.
- When Notion tables are informal, extract **intent** and mark inferred fields clearly.
- Prefer **contract tests** or OpenAPI as the long-term sync mechanism when drift is recurring.

## Integrations

- **Notion MCP** — Read spec pages; optionally append a linked "API Validation — YYYY-MM-DD" subpage under the feature PRD.
- **Slack MCP** — Notify with summary counts and link to Notion detail.
- **GitHub MCP** — Reference PRs or files for code locations when validating recent changes.
- **Google Workspace CLI (`gws`)** — Optional: share the gap table with tech leads via Doc or Chat.

### Publishing checklist

1. Append validation summary to the Notion spec or linked validation page.
2. Slack: counts of `missing_in_code` vs `missing_in_spec` + link.
3. Optional: schedule review via `gws` Calendar when breaking changes appear.

## Output Structure

- Spec vs implementation coverage %.
- Matrix: endpoint × dimension × status.
- Detailed findings with code/file or OpenAPI pointer and Notion section anchor.
- Risk callouts for breaking changes.

## Examples

- **Input:** "Compare Notion API section for Orders with `openapi.yaml`." **Output:** Korean matrix showing three `partial` mismatches on error schema.
- **Input:** "Did we implement `/v2/invoices` as specified?" **Output:** Focused pass/fail with field-level diff narrative.
- **Input:** "Diff OpenAPI against Notion error model for Auth APIs." **Output:** Table of status codes and payload shapes with gaps.

## Boundaries

- Not a **security audit**; auth presence is structural, not penetration-tested here.
- Does **not** replace consumer SDK generation; focuses on truth between spec and server.

## Error Handling

- **Ambiguous Notion formatting** — List questions back to authors; do not invent fields.
- **Generated OpenAPI missing** — Fall back to static analysis; label inferred entries `inferred`.
- **No authentication to probe** — Skip live probes; rely on static comparison.
- **Version skew** — If spec says v2 but code defaults v1, flag as Critical mismatch.
- **Undocumented middleware** — Global validators may alter bodies; note possible hidden constraints.
- **Pagination variants** — cursor vs offset; if both appear, mark `ambiguous` until unified.

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:

- [../references/project-overrides/project-ssot.md](../references/project-overrides/project-ssot.md) (POL-005 — artifact locations, not-used systems)
- [../references/project-overrides/project-tech-stack.md](../references/project-overrides/project-tech-stack.md) (POL-001 — frontend/backend libraries)

Key constraints:

- Use FastAPI interactive docs at `/docs` as the live OpenAPI surface; do not require committed `openapi.yaml` / static Swagger files in-repo.
- Validate routes and schemas against `backend/app/api/v1/` implementations and the stack notes in project tech-stack overrides.
