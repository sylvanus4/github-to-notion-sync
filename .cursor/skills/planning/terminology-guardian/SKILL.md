---
name: terminology-guardian
description: >-
  Three-mode terminology governance: (1) Drift Scan — enforce consistent terminology
  across PRDs, code, designs, and policies by detecting term drift and generating
  correction reports; (2) DDD Domain Grilling — interactive session that challenges a
  plan against the project's domain model, sharpens fuzzy language, cross-references
  code, and updates CONTEXT.md/ADRs inline as decisions crystallize; (3) Conversation
  Glossary Extraction — extract a DDD-style ubiquitous language glossary from the
  current conversation, flag ambiguities, propose canonical terms, and save to
  UBIQUITOUS_LANGUAGE.md. Korean triggers: "용어 점검", "terminology check", "용어 일관성",
  "glossary", "용어 사전", "terminology guardian", "용어 통일", "용어 불일치",
  "term consistency", "domain model", "DDD", "도메인 모델", "도메인 모델링", "DDD 세션",
  "도메인 언어 검증", "컨텍스트 맵", "엔티티 분석", "애그리게이트 설계",
  "ubiquitous language", "domain glossary", "도메인 용어", "유비쿼터스 언어",
  "용어 사전 추출", "DDD 글로서리", "용어 정리", "도메인 언어 추출", "grill my plan
  against domain model", "stress test domain language". Do NOT use for full document
  quality scoring (use doc-quality-gate), policy copy generation only (use
  policy-text-generator), code-vs-spec gap analysis without a glossary focus (use
  code-spec-comparator), general plan grilling without domain focus (use
  omc-deep-interview Mode B), or architecture-level improvements without DDD context
  (use deep-review).
metadata:
  author: thaki
  version: "2.0.0"
  category: review
---

# Terminology Guardian

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Single source of truth for product and technical vocabulary. Three operational modes serve different stages of the terminology lifecycle: extracting terms from discussion, stress-testing terms against the domain model, and scanning artifacts for drift.

## Mode Detection

| Signal | Mode |
|--------|------|
| User mentions "scan", "check", "drift", "consistency", "report", or provides Notion/repo/Figma targets | **A — Drift Scan** (default) |
| User mentions "domain model", "DDD", "grill", "challenge my plan", "CONTEXT.md", "bounded context", "aggregate" | **B — DDD Domain Grilling** |
| User mentions "ubiquitous language", "extract glossary", "domain terms from this conversation", "formalize terminology" | **C — Conversation Glossary Extraction** |

When ambiguous, ask: "Should I scan existing artifacts for drift, challenge your plan against the domain model, or extract a glossary from our conversation?"

---

## MODE A: Drift Scan (Default)

The original static analysis mode. Scans PRDs, code, designs, and policies to detect terminology inconsistencies.

## Prerequisites

- Agreed **canonical locale rules** (which strings must be Korean vs English).
- Access to Notion pages or databases in scope; repository read access for code scans.
- Optional: naming convention doc (camelCase API fields vs display labels).

## Success criteria

- Every drift finding cites **evidence** (quote + location).
- Glossary coverage metric is explicit; gaps list **proposed** rows, not silent edits.
- Critical/High items are distinguishable and appear first in Slack or summary sections.

## Inputs

1. **Scope** (required) — `notion` | `repo` | `figma-notes` | `mixed` (default: `mixed`).
2. **Glossary location** — Notion page or database URL for canonical terms; if missing, bootstrap a draft glossary from the scanned corpus and flag entries needing human approval.
3. **Targets** — Notion page IDs/URLs, repository paths, or Figma file keys / frame names (as available via MCP).
4. **Locale policy** — UI language rules (e.g., user-facing Korean, internal API names English).

## Procedure

1. **Load glossary** — Fetch canonical rows (term, definition, aliases, deprecated, owner) via Notion MCP. If none exists, extract candidate terms from headings and repeated nouns in supplied docs; mark confidence `low`.
2. **Inventory surfaces** — Pull text from Notion pages in scope; scan code for string literals, comments, and identifier-adjacent labels in agreed paths; capture design annotations where MCP exposes text.
3. **Normalize** — Lowercase for matching where language allows; strip punctuation; map known aliases to canonical IDs from the glossary.
4. **Detect drift** — Flag: multiple spellings, mixed KR/EN for the same UX object, deprecated terms still in use, acronym inconsistency, and "concept split" (same string used for two meanings).
5. **Score severity** — `Critical` (user-facing contradiction), `High` (API vs PRD mismatch), `Medium` (internal doc only), `Low` (style).
6. **Recommend** — For each finding: preferred term, evidence (snippet + source link or file:line), suggested replacement, owner guess (path or page author property).
7. **Report** — Executive summary, glossary gaps (missing definitions), drift table, and patch checklist. Optional: proposed Notion glossary rows for approval.

### Workflow notes

- Prefer **human-approved** glossary changes: output proposed property values, not silent writes, unless the user explicitly requests Notion updates.
- When the same Korean label maps to two English API nouns, treat as **High** until the API naming ADR or glossary resolves it.
- Re-run after large PRDs merge or major feature rename milestones to keep drift low.

## Integrations

- **Notion MCP** — Read/update glossary database or page; optionally create a child page `Terminology Report — YYYY-MM-DD` under an agreed parent.
- **Slack MCP** — Post summary to the planning-automation channel with a thread listing Critical/High items.
- **Google Workspace CLI (`gws`)** — If stakeholders review in Docs, append a summary paragraph or share the Notion link via Chat/Drive per team convention.

### Publishing checklist

1. Create or update the Notion report page with the findings table.
2. Post Slack summary + thread for Critical/High.
3. If requested, share the Notion URL via `gws` Chat or email for legal/compliance reviewers.

## Output Structure

- Summary counts (Critical/High/Medium/Low).
- Glossary coverage (% of detected concepts with a canonical row).
- Findings table: ID, severity, concept, current usage, recommended term, location, action.
- Appendix: proposed glossary additions and deprecation notices.

## Examples

- **Input:** "Scan Notion PRD X and `src/features/billing` against our glossary page." **Output:** Korean report with 12 drift items and a sorted fix list for PM and engineering.
- **Input:** "We say 'workspace' and 'tenant' interchangeably — unify." **Output:** Recommendation to pick one canonical term, list all occurrences, and suggested Notion glossary update.
- **Input:** "Quarterly glossary health check for all planning docs." **Output:** Coverage %, top deprecated terms still in use, and a prioritized cleanup backlog.

## Boundaries

- Does **not** rewrite full documents; it recommends term-level fixes.
- Does **not** replace legal review of regulated vocabulary; flag legal-sensitive terms for counsel when policy requires.

## Error Handling

- **Glossary unreachable** — Run in bootstrap mode; state that all canonical labels are provisional until approved.
- **Partial repo access** — Report scanned paths explicitly; do not infer coverage for omitted trees.
- **Figma text unavailable** — Note limitation; rely on Notion design specs and code strings for that slice.
- **Ambiguous term** — Do not auto-merge; list disambiguation questions for the owner.
- **Large corpus** — Paginate Notion reads; summarize per section to avoid token overflow; offer follow-up scoped passes.
- **Machine translation noise** — If mixed machine-translated strings appear, tag as `Low` style risk unless they contradict the glossary.

---

## MODE B: DDD Domain Grilling

An interactive, DDD-informed interview that challenges a plan or design against the project's domain model. Sharpens fuzzy language, cross-references code, and updates `CONTEXT.md` / ADRs inline as decisions crystallize.

### When to enter Mode B

The user shares a plan, design, or feature proposal and asks for domain-level validation, or explicitly mentions DDD, bounded contexts, aggregates, or domain modeling.

### Process

#### Phase 1 — Load Domain Context

1. Read `CONTEXT.md` (or equivalent domain model file) and the project glossary.
2. Identify the bounded contexts, aggregates, entities, and value objects relevant to the plan.
3. If no domain model file exists, state this gap and offer to bootstrap one from codebase analysis.

#### Phase 2 — Build Domain Decision Tree

For the plan under review, map every decision point to its domain implications:
- Does the plan introduce a new entity, or should it reuse an existing one?
- Does it cross bounded-context boundaries? If so, how is communication handled?
- Are aggregate invariants preserved?
- Does the naming align with the ubiquitous language?

#### Phase 3 — Walk Every Branch

Ask one question at a time. For each question:
1. State which domain concept is at stake.
2. Provide a recommended answer grounded in the current domain model.
3. Explain the domain-level trade-off if the user disagrees.

Rules:
- **Cross-reference code**: Before asking a question, check if the codebase already answers it. Quote the relevant file/line.
- **Sharpen language**: If the user uses a term that doesn't match the glossary, flag it immediately.
- **Resolve codebase questions silently**: Use `Grep`/`SemanticSearch` to verify claims before surfacing them.
- **Be relentless about invariants**: Never accept "we'll handle that later" for aggregate invariants.

#### Phase 4 — Update Domain Artifacts Inline

As decisions resolve during the conversation:
- Propose updates to `CONTEXT.md` (new entities, refined boundaries).
- Propose glossary additions or corrections.
- Draft ADR entries for significant domain decisions.
- Apply updates only with user approval.

#### Phase 5 — Produce Decision Summary

Output a structured summary:

```
## Domain Decisions Resolved
1. [Entity/Concept]: [Decision] — [Rationale]

## Glossary Updates
- [New/Changed term]: [Definition]

## Domain Risks
- [Unresolved boundary/invariant concerns]

## Artifact Updates Applied
- CONTEXT.md: [changes]
- Glossary: [additions]
- ADR-NNN: [created/updated]
```

### Mode B Examples

- **Input:** "We want to add a 'team workspace' concept — each team gets isolated resources."
  **Grilling:** "Your `CONTEXT.md` defines `Tenant` as the isolation boundary with `Workspace` nested under it. Is 'team workspace' a new aggregate, or a view over existing `Workspace` entities filtered by team membership? The `Workspace` entity at `src/domain/workspace.ts:L23` has no `teamId` field — are you proposing to add one?"

- **Input:** "We'll add an approval workflow for model deployments."
  **Grilling:** "I see `Deployment` lives in the `serving` bounded context while `Approval` patterns in your codebase belong to the `governance` context (`src/governance/approval.go`). This crosses a context boundary. Should the `serving` context emit a domain event that `governance` subscribes to, or should `Deployment` directly reference approval state?"

---

## MODE C: Conversation Glossary Extraction

Extracts a DDD-style ubiquitous language glossary from the current conversation. Flags ambiguous terms, proposes canonical definitions, and saves results to `UBIQUITOUS_LANGUAGE.md` (or the project glossary).

### When to enter Mode C

The user asks to formalize terms discussed in the conversation, extract a glossary, or build a ubiquitous language document from the current session.

### Process

#### Phase 1 — Scan Conversation

Review the full conversation history for:
- Domain nouns (entities, concepts, features mentioned)
- Verbs that imply domain actions or state transitions
- Adjectives that imply classification or status
- Terms used by multiple speakers with potentially different meanings

#### Phase 2 — Build Candidate Glossary

For each candidate term, produce:

| Field | Description |
|-------|-------------|
| **Term** | The canonical name (English, with Korean equivalent if applicable) |
| **Definition** | Precise 1-2 sentence definition |
| **Context** | Which bounded context or module this belongs to |
| **Aliases** | Any synonyms or informal names used in conversation |
| **Ambiguity Flag** | If the term was used inconsistently, describe the conflict |
| **Source** | Where in the conversation the term appeared |

#### Phase 3 — Detect Ambiguities

Flag and list any term that:
- Was used with two different meanings by the same or different speakers.
- Has no clear definition despite being used repeatedly.
- Conflicts with an existing glossary term.
- Maps to multiple code-level identifiers.

For each ambiguity, propose a resolution question for the user.

#### Phase 4 — Cross-Reference

Compare extracted terms against:
1. Existing glossary / `UBIQUITOUS_LANGUAGE.md` (if it exists).
2. Code identifiers in the repository.
3. `CONTEXT.md` domain model.

Flag new terms not yet in the glossary and existing terms used differently than defined.

#### Phase 5 — Output

Produce a structured document:

```markdown
# Ubiquitous Language — [Date]

## New Terms
| Term | Definition | Context | Aliases | Notes |
|------|-----------|---------|---------|-------|
| ... | ... | ... | ... | ... |

## Ambiguities Requiring Resolution
1. "[Term]" — used as [meaning A] in [context] but [meaning B] in [context]. Recommended: [pick one].

## Existing Terms Used Differently
| Term | Glossary Definition | Conversation Usage | Action |
|------|--------------------|--------------------|--------|

## Proposed Glossary Updates
[Ready-to-apply additions/changes]
```

#### Phase 6 — Persist

- If `UBIQUITOUS_LANGUAGE.md` exists, propose appending new entries.
- If it doesn't exist, offer to create it at the project root or `docs/` directory.
- If the project uses a Notion glossary, propose Notion row additions.

### Mode C Examples

- **Input:** "Extract the domain language from our conversation about the multi-tenant GPU scheduling feature."
  **Output:** 15-term glossary including "tenant", "GPU partition", "scheduling policy", "quota", "preemption priority" — with 2 ambiguities flagged ("quota" was used for both API rate limits and GPU time allocation).

- **Input:** "We keep saying 'job' and 'task' interchangeably. Formalize it."
  **Output:** Glossary entry proposing "Job" as the user-facing unit of work and "Task" as the internal scheduling unit, with code cross-references showing `Job` in the API layer and `Task` in the scheduler.
