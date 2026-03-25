---
name: doc-quality-gate
description: >-
  Unified planning-document quality gate: scores PRDs, feature specs, policy docs,
  and design docs on seven weighted dimensions, assigns A–D grades, and auto-approves
  or rejects using a configurable threshold with actionable, severity-ranked feedback.
  Korean triggers: "문서 품질 점검", "PRD 검수", "기획서 완성도", "상태 커버리지",
  "Edge Case 누락", "정책 정합성", "doc quality gate", "spec review",
  "inspect document quality", "review PRD quality".
  Do NOT use for: doc-review-orchestrator (review workflows); cross-domain-sync-checker
  (design/code sync audits); code review tools or agents; prd-state-matrix only;
  policy-text-generator (copy compliance only); meeting-digest; content marketing
  quality (appropriate content gate skill).
metadata:
  author: thaki
  version: "2.1.0"
  category: review
---

# Doc Quality Gate (Unified)

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

Single skill combining weighted 7-dimension scoring (formerly `doc-quality-checker`), binary sub-checks and gate workflow (formerly `doc-quality-gate`), and checklist / sync / collaboration guidance (formerly `doc-quality-inspector`).

## Inputs

1. **Document** (required) — File path, Notion page URL, or pasted content.
2. **Document type** (optional) — `prd` | `feature-spec` | `spec` | `policy` | `design` | `design-spec` | `guideline` | `postmortem` | `research` | `general` | `custom`. Default: auto-detect from headings and keywords.
3. **Policy source** (optional) — Notion URL or file for **Policy compliance** dimension; if omitted, that dimension is scored as **N/A** (excluded from weighted average; document in the report).
4. **Comparison targets** (optional) — Code path and/or design URL for optional **sync spot-checks** (design–code, spec–design). If inaccessible, skip sync sections and note in the report.
5. **Scope** (optional) — `full` | `quick`. Quick: required sections, state coverage, edge cases, and severity scan only.
6. **Gate configuration** (optional):
   - `approval_min_score` — Minimum **weighted overall score** (0–100) for **APPROVED**. Default: **75**.
   - `approval_min_dimensions` — Minimum count of dimensions with score ≥ **60** (excluding N/A). Default: **6** (out of 7 applicable).
   - `dimension_pass_line` — Per-dimension “pass” floor for the dimension table. Default: **60**.
   - `custom_checklist_path` — Override default checklist; else use [references/quality-checklist.md](references/quality-checklist.md) and type-specific lists under [references/quality-checklists/](references/quality-checklists/).

## The seven dimensions (unified framework)

Each dimension is scored **0–100**. Compute a **weighted overall score** (0–100) using the weights below. Dimensions marked **N/A** (e.g. policy source missing for policy compliance) are **omitted from the weight denominator**; renormalize remaining weights to sum to 100%.

| # | Dimension | Weight | What to verify |
|---|-----------|--------|----------------|
| 1 | **Required sections** | 20% | Type-specific mandatory sections present and non-placeholder; includes clarity/actionability expectations (unambiguous requirements, owners/deadlines where applicable, acceptance criteria for specs). See [references/completeness-checklist.md](references/completeness-checklist.md), [references/checklist.md](references/checklist.md), [references/quality-rubric.md](references/quality-rubric.md). |
| 2 | **State coverage** | 20% | UI/flows: default, loading, error, empty; plus disabled/success where relevant; state transitions and permission variants. See checker-style state matrix expectations in [references/quality-rubric.md](references/quality-rubric.md). |
| 3 | **Edge cases** | 15% | Input/network/concurrency/permission/data/environment edge cases addressed. |
| 4 | **Policy compliance** | 15% | Copy and data practices vs supplied policy; contradictions; legal/consent alignment. N/A if no policy supplied. |
| 5 | **Terminology consistency** | 10% | One concept → one term; acronym rules; KR/EN consistency; contradictions across sections. |
| 6 | **API alignment** | 10% | API contracts referenced or specified; endpoints, errors, versioning; alignment with data model mentions; traceability to technical sources. |
| 7 | **Design references** | 10% | Figma/design links, components/tokens, related PRD/spec links, test/QA doc links, decision/version history. |

**Sub-rubric (legacy gate, binary hints):** Use the six pass/fail lenses from [references/quality-rubric.md](references/quality-rubric.md) (Completeness, Clarity, Consistency, Actionability, Traceability, Compliance) as *signals* when arguing scores for dimensions 1, 5, 6, and 7 — they are not separate scored axes in v2.

**Checklist depth:** Apply type-specific items from [references/quality-checklist.md](references/quality-checklist.md) and [references/quality-checklists/](references/quality-checklists/). Use [references/ambiguity-patterns.md](references/ambiguity-patterns.md) and [references/common-gaps.md](references/common-gaps.md) for findings. Optional collaboration depth: [references/collaboration-structure-guide.md](references/collaboration-structure-guide.md).

## Scoring and grades

**Weighted overall score** (0–100): Each non-N/A dimension has a score 0–100 and a weight from the table. Let **W** = sum of weights for non-N/A dimensions only.

```
overall_score = (sum of (dimension_score × weight)) / W
```

(Optionally also show a **legacy binary diagnostic**: count PASS among the six lenses in [references/quality-rubric.md](references/quality-rubric.md) Part B, e.g. `4/6`, for teams calibrating against the v1 gate.)

**Letter grade** (overall score):

| Grade | Range | Interpretation |
|-------|-------|----------------|
| **A** | 90–100 | Ready for implementation / publication |
| **B** | 75–89 | Minor fixes |
| **C** | 60–74 | Major gaps |
| **D** | 0–59 | Rework recommended |

**Verdict:**

- **APPROVED** only if `overall_score >= approval_min_score` **and** count(dimensions ≥ 60, excluding N/A) `>= approval_min_dimensions` **and** no **Critical** unresolved issue (document Critical items explicitly).
- Otherwise **NEEDS REVISION**.

## Workflow

### Step 1 — Load document

- **Notion:** read page via Notion MCP (e.g. `read_page` / workspace fetch tools per your environment).
- **File:** read from workspace.
- **Inline:** use pasted text.

If the document is empty, stop with an error message. If very short (&lt; ~100 characters), run a limited structural check and warn. If very long (&gt; ~10k words), sample by major sections and state that full pass may require follow-up.

### Step 2 — Score all applicable dimensions

For each dimension, produce: score 0–100, short rationale, and findings list with **Critical / High / Medium / Low**.

### Step 3 — Optional sync spot-check

If comparison targets were provided:

- Compare design/spec components and states vs code (high level): list matches, gaps, and **sync coverage %** if quantifiable.
- If target inaccessible: skip and record **Skip** with reason.

### Step 4 — Gate decision

Apply configurable thresholds; set **Verdict** to APPROVED or NEEDS REVISION.

### Step 5 — Integrations

- **Notion:** If the user requests it, create or update a child page or status properties with verdict, score, grade, and link to the report summary.
- **Slack:** Post a short summary (title, verdict, score, grade, top 3 issues) to the channel or thread the user specifies; put details in a thread or attached doc.

### Step 6 — Output report

Write the full gate report in Korean. Required sections: title; summary (document name, type, weighted score /100, letter grade, APPROVED vs NEEDS REVISION, review timestamp); per-dimension score table (all seven dimensions with weight, contribution, N/A where applicable); dimension-level failure narratives when below threshold (issue, location, fix, before/after example); prioritized findings (Critical → Low); optional sync spot-check summary when comparison targets were provided; follow-ups (Notion/Slack actions).

## Per-dimension failure template (from legacy gate)

For any failing dimension, also include when helpful:

```markdown
### [Dimension] — FAIL

**Issue**: [Specific problem]
**Location**: [Section or evidence]
**Fix**: [Concrete action]
**Example**: [Before → After]
```

## Error handling

| Situation | Action |
|-----------|--------|
| Document not found | Ask for correct path or URL. |
| Unknown type | Default to `general` or `custom`; note uncertainty. |
| Policy unavailable | Score policy dimension **N/A**; renormalize weights. |
| Checklist override missing | Fall back to bundled references; warn user. |
| Mixed languages | Score in primary language; note secondary sections. |
| Notion/Slack not configured | Complete report locally; say what would be posted. |

## Skill chain

| Step | Tool / skill | Purpose |
|------|----------------|---------|
| 1 | Notion MCP | Fetch source page |
| 2 | (this skill) | Score, grade, verdict |
| 3 | md-to-notion | Publish full report as sub-page (optional) |
| 4 | policy-text-generator | Deep policy copy checks (optional follow-up) |
| 5 | cross-domain-sync-checker | After approval, broader SSoT drift check (optional) |

## Examples

**Example 1 — PRD gate (Notion)**  
User provides a PRD URL. Fetch → score seven dimensions → overall 78 (B) → 6/7 dimensions ≥ 60 → `approval_min_score` 75 → **APPROVED** with two High follow-ups listed.

**Example 2 — Spec + policy**  
User attaches policy doc. Policy dimension scored; contradiction on data collection → Policy dimension 45 → **NEEDS REVISION** despite high overall score if Critical policy conflict exists.

**Example 3 — Design spec + code path**  
Run full dimension scoring plus sync spot-check; report match rates for components/states.

## References (bundled)

- [references/quality-rubric.md](references/quality-rubric.md) — Dimension detail, legacy binary rubric, document-type sections.
- [references/quality-checklist.md](references/quality-checklist.md) — Replaceable master checklist (Reviewer pattern).
- [references/checklist.md](references/checklist.md) — Weighted section tables (PRD / policy / feature spec).
- [references/completeness-checklist.md](references/completeness-checklist.md) — Severity-weighted completeness.
- [references/quality-checklists/prd.md](references/quality-checklists/prd.md), [feature-spec.md](references/quality-checklists/feature-spec.md), [policy.md](references/quality-checklists/policy.md) — Typed scoring checklists.
- [references/ambiguity-patterns.md](references/ambiguity-patterns.md), [references/common-gaps.md](references/common-gaps.md), [references/collaboration-structure-guide.md](references/collaboration-structure-guide.md) — Deep inspection aids.
