---
name: code-spec-comparator
description: >-
  Compare implemented code against an existing Notion (or file) specification:
  find gaps, undocumented behavior, schema and state-transition mismatches, and
  spec-only items not present in code. Use when the user asks for "기획서 싱크",
  "스펙 코드 비교", "code vs spec", "Notion 스펙 대조", "미구현 찾기",
  "문서화 안 된 API", "스키마 불일치", "역기획 대조", "gap analysis",
  "spec-code mismatch", "기획서대로 구현됐는지", or needs audit of implementation
  vs canonical planned spec. Do NOT use for first-time reverse spec from code only
  (use code-to-spec). Do NOT use for code review or security audit (use deep-review).
  Do NOT use for formal API doc generation (use technical-writer).
metadata:
  author: thaki
  version: "1.0.1"
  category: analysis
---

# Code–Spec Comparator

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Produce a structured **gap analysis** between **what the code actually does** and **what the planned specification says**. This skill is optimized for **Notion-hosted specs** (fetch via Notion MCP) plus local or GitHub-linked code. It complements **`code-to-spec`**: run `code-to-spec` to document implementation-only truth, then this skill to diff that truth against the official spec—or diff **directly** by extracting minimal facts from code during comparison.

## Inputs

1. **Code source** — repository path, module path, PR URL, or file list (same conventions as `code-to-spec`).
2. **Canonical spec** — **Notion page URL or page ID** (preferred), or exported markdown / attached doc.
3. **Scope** (optional) — feature name, API prefix, or file glob to limit analysis.
4. **Framework hint** (optional) — if auto-detection fails.

**STOP** when scope is ambiguous: confirm repo path and spec page before scanning large trees.

## Workflow

### Step 1 — Load the spec

1. If Notion: fetch page content via **Notion MCP** (structured blocks or markdown export as available).
2. If file: read markdown/doc.
3. Parse into comparable sections: **APIs**, **states / transitions**, **business rules**, **screens/flows**, **error handling**, **data model**.

### Step 2 — Extract implementation facts

Without writing a full reverse spec unless requested, extract a **comparable inventory** from code:

- API method/path, auth, request/response shapes, status codes (see [../code-to-spec/references/api-scan-patterns.md](../code-to-spec/references/api-scan-patterns.md)).
- State enums and transitions (see [../code-to-spec/references/state-extraction-guide.md](../code-to-spec/references/state-extraction-guide.md)).
- Notable rules and validations.

Reuse extraction heuristics from **`code-to-spec`**; keep evidence as **file:line**.

### Step 3 — Structured diff

Build four primary views (empty tables if none):

| Category | Meaning |
|----------|---------|
| **Spec only** | Planned but missing or unreachable in code |
| **Code only** | Implemented but not described in spec (undocumented) |
| **Schema / contract mismatch** | Same nominal feature, different fields, types, enums, or errors |
| **State / flow mismatch** | Different transitions, ordering, or terminal states |

Severity scale:

| Level | Meaning |
|-------|---------|
| **CRITICAL** | Core capability missing or broken state machine / safety path |
| **HIGH** | Client integration or data contract impact |
| **MEDIUM** | Extra/undocumented endpoint or field; behavior drift |
| **LOW** | Naming, wording, or minor doc gaps |

Use the report scaffold in [../code-to-spec/references/diff-report-template.md](../code-to-spec/references/diff-report-template.md).

### Step 4 — Deliverables

1. **Gap Analysis Report** (Korean) with summary counts and detailed tables.
2. Optional: **reverse spec excerpt** for “code-only” items only (delegate to `code-to-spec` if full doc needed).
3. **Notion**: create or update a child page under the project space with the report; link back to the source spec page.
4. **Slack**: notify with summary table (totals by severity), Notion link, and top 3 actions.

## Examples

**Example 1** — User: “Check APIs against this Notion spec” + repo path + Notion URL.  
→ Fetch Notion → scan API layer → diff tables → Korean report + Slack + Notion page.

**Example 2** — User: “Compare schemas only” + narrow scope.  
→ Limit diff to request/response DTOs vs spec section 5.

## Error handling

| Situation | Action |
|-----------|--------|
| Notion page not found | Re-check URL/ID and sharing |
| Spec unstructured | Segment manually; list parsing assumptions |
| Code inaccessible | Request clone path or PR scope |
| Zero endpoints in scope | Widen scan or ask for controller paths |
| MCP failure | Output markdown locally; retry Notion later |

## Skill chain

| Situation | Skill |
|-----------|--------|
| Full reverse doc first | `code-to-spec` |
| Fix doc quality | `doc-quality-gate` |
| Publish markdown | `md-to-notion` |
| Visual diff story | `visual-explainer` |

## Project-Specific Overrides (AI Stock Analytics)

This skill operates under project-specific policies:

- [../references/project-overrides/project-ssot.md](../references/project-overrides/project-ssot.md) (POL-005 — artifact locations, not-used systems)
- [../references/project-overrides/project-document-standards.md](../references/project-overrides/project-document-standards.md) (POL-004 — quality gate, grading, report standards)

Key constraints:

- Treat specs as local markdown under `docs/policies/`, `docs/*.md`, and related repo paths—not Notion—as the default comparison targets unless the user provides another source.
- Compare implementation against those documents and POL-004 expectations for structure and completeness.
- Expect HTTP APIs at `/api/v1/` when diffing backend behavior against written specs.
