---
name: code-to-spec
description: >-
  Reverse-engineer planning documents from implementations: extract states, edge
  cases, API contracts, business rules, UI flows, and policy mappings from
  frontend/backend code, PR diffs, or demos. Produces structured specs with
  state matrix, user flows, and API tables. Use when the user asks for
  "코드 역기획", "코드에서 스펙 추출", "역기획서 생성", "코드 분석해서 기획서",
  "reverse plan from code", "reverse engineer spec", "code to spec",
  "extract states from code", "edge case 분석", "API 스펙 역추출", "PR 기반 기획서",
  "what does this API actually do", "구현에서 스펙", "코드 기획서", "배포된 기능 문서화",
  or needs planning documentation from existing code without comparing to a canonical Notion spec
  (for spec-vs-code gap analysis use code-spec-comparator). Do NOT use for code review
  (use deep-review). Do NOT use for writing new PRDs from scratch (use pm-execution or
  prd-auto-generator). Do NOT use for formal API reference docs (use technical-writer).
  Do NOT use for test scenarios only (use pm-execution test-scenarios).
metadata:
  author: thaki
  version: "2.0.1"
  category: analysis
---

# Code-to-Spec (Unified)

## Output language

All outputs MUST be in Korean (한국어). Technical terms (API paths, HTTP methods, class names, field names, framework names) may remain in English. Use localized Korean labels for uncertainty tags when writing deliverables (see tag names below as logical keys).

Reverse-engineer structured planning documents from code and related artifacts. This skill merges former workflows for component/API/screen analysis, PR-based extraction, backend API inventory, state-machine documentation, policy traceability, and optional lightweight comparison with an informal spec. For **systematic diff against an existing Notion specification** (gaps, undocumented behavior, schema drift), use **`code-spec-comparator`** instead or after generating the reverse spec.

## Mental model

**Reviewer + Generator**: read the implementation (Reviewer), extract planner-relevant facts with file:line evidence (Generator), then assemble a single structured document. Never invent product intent; tag uncertainty with `[NEEDS_CONFIRMATION]`, `[INFERRED]`, `[CANNOT_INFER]` per [references/spec-template.md](references/spec-template.md) (render with Korean labels in output).

## Inputs (multi-source)

| Source | How to ingest |
|--------|----------------|
| **Frontend / app code** | Local paths; classify components, routes, conditional UI, client state |
| **Backend code** | Local paths; scan routes, handlers, DTOs/schemas, entities (see [references/api-scan-patterns.md](references/api-scan-patterns.md)) |
| **PR diffs** | GitHub MCP: changed files + diff; focus on behavioral change |
| **Git diff / patch** | Parse as scope boundary for incremental reverse spec |
| **Pasted snippet** | Treat as narrow scope; state limitations |
| **Running demo** | User description, screenshots, short screen recording notes, or browser/Playwright observation when available—document **observed** behavior separately from **code-derived** facts |

Optional inputs:

- **Scope** — `component` \| `screen` \| `api` \| `module` \| `feature` \| `full` (auto-detect if omitted)
- **Output depth** — `spec` \| `state-map` \| `edge-report` \| `api-spec` \| `full` (default: `full`)
- **Existing draft spec** — markdown or Notion URL for a **quick** alignment table (not a full audit; use `code-spec-comparator` for that)
- **Policy documents** — for policy-to-code mapping (optional section)

**CRITICAL**: Before deep analysis, map the repository or file set (entry points, routing, major modules). If **10+ files** are in scope, propose narrowing to the most relevant paths unless the user insists on full coverage.

## Workflow

### Phase 1 — Ingest and structure

1. Resolve input type (local tree, PR URL, diff, paste, demo notes).
2. Detect stack (package manifests, folder conventions, framework patterns).
3. Build a **structural map**: modules, import/dependency edges, entry points (routes, controllers, main views).
4. For PRs: list changed files and classify (API, UI, state, schema, config).

### Phase 2 — Extract (planner-facing)

Use [references/extraction-patterns.md](references/extraction-patterns.md) and [references/state-extraction-guide.md](references/state-extraction-guide.md).

1. **State extraction** — UI/data/auth/business states; enums/unions; switches; reducers; DB status fields; state machines (e.g. XState). List transitions, triggers, terminal and orphan states. Prefer a **state matrix** + `mermaid` stateDiagram.
2. **Edge case analysis** — try/catch, guards, validation, HTTP errors, empty/null paths, concurrency (race, idempotency), timeouts. Include **suspected missing** edge cases (what the code does not handle).
3. **API contract extraction** — method, path, auth, request/response shapes, status and app error codes, idempotency when visible.
4. **Business logic mapping** — rules expressed as conditionals, limits, pricing, permissions, feature flags, quotas.
5. **Component / screen analysis** (frontend) — routes → screens; conditional rendering → state-specific UI; modals, forms, navigation.
6. **Policy mapping** (if policy docs supplied) — requirement vs implementation row table; unimplemented or partial items.

Severity for edge cases: **Critical / High / Medium / Low** (see [references/state-extraction-guide.md](references/state-extraction-guide.md)).

### Phase 3 — Synthesize

Assemble **one** structured planning document. Templates and tables:

- Master layout: [references/spec-template.md](references/spec-template.md)
- Screen-heavy flows: [references/document-template.md](references/document-template.md)
- Self-check for state coverage: [references/state-checklist.md](references/state-checklist.md)

Required sections (use `N/A` with reason if not applicable):

1. Overview (scope, sources, summary)
2. User flows / scenarios (happy + alternate paths)
3. State matrix + state diagram(s)
4. Edge cases (handled + suspected gaps)
5. Business rules (with code references)
6. API specs (endpoint tables + per-endpoint detail when in scope)
7. Data model (entities/fields when visible)
8. Policy mapping (only if policies provided)
9. Code reference index (files/functions)
10. Open questions — items tagged `[NEEDS_CONFIRMATION]` / `[CANNOT_INFER]` (localized in Korean output)

**Quality gate**: distinguish **`[FACT]`** (directly observed in code) vs **`[INFERRED]`**; every substantive claim should tie to **file:line** or demo observation.

### Phase 4 — Optional quick alignment

If the user supplied an existing spec (Notion or file): produce a **short** mismatch table (planned vs implemented). For full gap analysis, severity rollups, and Notion-centric reporting, hand off or rerun with **`code-spec-comparator`**.

### Phase 5 — Publish and notify

1. Save markdown locally under `output/reverse-spec/` or the user’s path when requested.
2. **Notion**: publish via Notion MCP (page create/update) or **`md-to-notion`** as child pages under the agreed parent.
3. **Slack**: post a short summary (what was analyzed, link to Notion, count of states/APIs/edge cases, number of open confirmation items) in the planning automation channel or thread as per team convention.

### Multi-agent prompts (optional)

For large scopes, sub-prompt patterns live in [references/agent-prompts.md](references/agent-prompts.md). Subagents must still follow the output-language rule.

## Skill chain

| Next step | Skill | Purpose |
|-----------|--------|---------|
| Spec vs Notion audit | `code-spec-comparator` | Gaps, undocumented APIs, schema/state drift |
| Quality pass | `doc-quality-gate` | Completeness and consistency |
| Diagrams | `visual-explainer` | Rich state/flow HTML |
| Formal PRD | `pm-execution` | Rewrite into forward PRD format |
| Audience soften | `tech-doc-translator` | Non-engineer summary |

## Examples

**Example 1 — React checkout folder**  
User provides `src/components/Checkout/`. Scan → extract order/payment states, validation and error paths, price rules → one reverse spec with mermaid state diagram and edge-case table in Korean.

**Example 2 — PR**  
User provides a GitHub PR URL. Use GitHub MCP → diff-limited reverse spec → list behavioral deltas vs main.

**Example 3 — Backend module**  
User provides API repo path. Use [references/api-scan-patterns.md](references/api-scan-patterns.md) → endpoint inventory → per-endpoint request/response/error tables → combined state transitions for entities that mutate state.

## Error handling

| Situation | Action |
|-----------|--------|
| Path not found | Confirm path; suggest glob or parent directory listing |
| No GitHub access | Fall back to local clone or pasted diff |
| Unsupported or obfuscated code | Generic pattern scan (conditionals, errors); state limitations |
| Scope too large | Propose module boundaries; phased deliverables |
| Notion unreachable | Deliver markdown only; retry publish later |
| No state machine in code | Say so explicitly; emphasize rules and API behavior |
| Demo vs code conflict | Report both; mark which source each row uses |

## Evolution (binary eval)

| ID | Eval | Pass condition |
|----|------|----------------|
| E1 | State extraction | Named states + transitions + diagram or matrix |
| E2 | Edge cases | ≥3 handled paths from code OR documented “none found” with scan notes |
| E3 | Honest tagging | `[NEEDS_CONFIRMATION]` / `[INFERRED]` used where intent unclear |
| E4 | Document skeleton | All required sections present or marked N/A |
| E5 | Code grounding | Claims traceable to code or explicit demo observation |
| E6 | API inventory (backend scope) | Endpoint table matches routed handlers for analyzed scope |

**Autoimprove hook**: test inputs — React feature module, REST/NestJS controller slice, Vue screen, GitHub PR, service-layer-only package; target E1–E6 pass rate at least 80%.
