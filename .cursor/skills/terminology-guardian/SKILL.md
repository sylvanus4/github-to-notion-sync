---
name: terminology-guardian
description: >-
  Enforce consistent terminology across PRDs, code, designs, and policies. Maintain a
  project-wide glossary, detect term drift across Notion docs, code, and Figma notes,
  suggest corrections, and generate terminology reports cross-referenced to the glossary.
  Korean triggers: "용어 점검", "terminology check", "용어 일관성", "glossary", "용어 사전",
  "terminology guardian", "용어 통일", "용어 불일치", "term consistency". Do NOT use for
  full document quality scoring (use doc-quality-gate), policy copy generation only
  (use policy-text-generator), or code-vs-spec gap analysis without a glossary focus
  (use code-spec-comparator).
metadata:
  author: thaki
  version: "1.0.0"
  category: review
---

# Terminology Guardian

**All outputs MUST be in Korean (한국어). Technical terms may remain in English.**

## Purpose

Single source of truth for product and technical vocabulary. Aligns artifacts so one concept maps to one preferred term, surfaces synonyms and deprecated labels, and produces actionable correction lists for authors and implementers.

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
