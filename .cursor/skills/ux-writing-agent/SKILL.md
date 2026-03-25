---
name: ux-writing-agent
description: >-
  Generate, review, audit, and quality-check UX copy for cloud UIs — labels,
  tooltips, errors, modals, empty states, CTAs, notifications, onboarding — with
  policy enforcement, cloud tone guides, and a 5-dimension rubric. Native English
  UI strings; Korean for analysis/reports unless copy is English. Use when:
  "write UI copy", "audit UI strings", "UX writing", "UX 라이팅", "에러 메시지",
  "툴팁", "모달", "빈 상태", "CTA", "톤앤보이스", "문구 일관성".
  Do NOT use for: ADRs/API docs/changelogs (technical-writer); prompts
  (prompt-transformer); decks (presentation-strategist); marketing/landing copy
  (pm-marketing-growth); brand voice guidelines (kwp-brand-voice-guideline-generation).
metadata:
  author: "thaki"
  version: "2.1.0"
  category: "generation"
---

# UX Writing Agent

Policy-driven UX copy generation, review, consistency auditing, and quality
scoring for product teams. Covers the full surface area of cloud and SaaS UIs
with professional tone, natural English for on-screen strings, and structured
workflows backed by reference guides.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English. For this skill: analysis, rationale, tables, audit reports, score cards, and usage notes follow that rule unless the user explicitly requests English. On-screen UX copy follows `--lang` / product locale (English UI → native English strings; Korean UI → Korean strings).

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| Sub-skill | Yes | One of: `generate`, `review`, `audit`, `quality-check` |
| Context | Yes | Product area, feature name, screen, or policy document |
| Copy / strings | Varies | Existing copy for `review` / `audit` / `quality-check` |
| `--category` | No | `label`, `tooltip`, `error`, `description`, `confirmation`, `empty-state`, `status`, `onboarding`, `modal`, `notification`, `cta` |
| `--context` | No | Where the copy appears, user state, preceding action |
| `--tone` | No | `formal`, `neutral`, `friendly` (default: `neutral`) — see [references/cloud-tone-matrix.md](references/cloud-tone-matrix.md) |
| `--lang` | No | `en` (default for UI strings), `ko`, or `both` for paired EN/KO |
| `--review` | No | Force review mode on provided text |
| `--batch` | No | Process multiple related strings in one table |
| `--variants` | No | Number of alternatives (1–3) with tradeoff notes |
| Custom tone guide | No | If absent, use [references/tone-and-voice-guide.md](references/tone-and-voice-guide.md) + cloud matrix |

## Reference map

| Purpose | File |
|---------|------|
| General tone (non-cloud-specific) | [references/tone-and-voice-guide.md](references/tone-and-voice-guide.md) |
| Cloud voice + tone-by-category | [references/cloud-tone-matrix.md](references/cloud-tone-matrix.md) |
| Cloud structural patterns + lengths | [references/cloud-copy-patterns.md](references/cloud-copy-patterns.md) |
| AWS/GCP/Azure-style conventions | [references/cloud-service-conventions.md](references/cloud-service-conventions.md) |
| Approved terms | [references/cloud-terminology-glossary.md](references/cloud-terminology-glossary.md) |
| 10-point validation | [references/cloud-validation-checklist.md](references/cloud-validation-checklist.md) |
| Legacy patterns (optional) | [references/ux-copy-patterns.md](references/ux-copy-patterns.md) |
| Terminology / casing consistency | [references/consistency-rules.md](references/consistency-rules.md) |
| 5-dimension scoring | [references/quality-rubric.md](references/quality-rubric.md) |

## Sub-skill index

| Sub-skill | Routing condition | Primary references |
|-----------|-------------------|-------------------|
| `generate` | New copy from policy, spec, or flow | cloud-tone-matrix, cloud-copy-patterns, cloud-service-conventions, glossary |
| `review` | Fix tone, grammar, clarity, naturalness | cloud-tone-matrix, consistency-rules, cloud-validation-checklist |
| `audit` | Batch consistency (terms, casing, voice) | consistency-rules, quality-rubric, glossary |
| `quality-check` | Numeric 5-dimension score + fixes | quality-rubric |

## Workflow

### Step 1: Route

Map intent to one sub-skill. If ambiguous, ask whether the user wants to
generate, review, audit, or score quality.

### Step 2: Gather context

- **generate**: Policy or spec, target elements, user flow, optional `--category`, `--variants`
- **review**: Strings + UI placement + optional `--review`
- **audit**: String set (JSON, CSV, or list) + scope
- **quality-check**: Copy + audience + product context

For cloud UIs, always cross-check
[references/cloud-terminology-glossary.md](references/cloud-terminology-glossary.md)
and [references/cloud-validation-checklist.md](references/cloud-validation-checklist.md).

### Step 3: Execute

#### generate — policy-based generation

1. Classify category (label, tooltip, error, modal, empty state, etc.).
2. Apply [references/cloud-tone-matrix.md](references/cloud-tone-matrix.md) for formality, urgency, depth.
3. Use [references/cloud-copy-patterns.md](references/cloud-copy-patterns.md) structure and length limits.
4. Apply [references/cloud-service-conventions.md](references/cloud-service-conventions.md) for lifecycle, async ops, quotas, permissions.
5. Replace disallowed terms per glossary.
6. Run cloud validation checklist before delivery.
7. Output: **English UI strings** (or KO if requested) + **Korean** rationale,
   usage notes, character counts, and accessibility notes.

#### review — correction and improvement

1. Check grammar, tone, clarity, naturalness (English copy should read native).
2. Enforce consistency rules and cloud validation.
3. Output: before/after table + **Korean** change rationale.

```markdown
| # | Location | Before | After | Rationale (Korean in deliverable) |
|---|----------|--------|-------|-----------------------------------|
```

#### audit — consistency analysis

1. Scan for terminology conflicts, casing, punctuation, voice/person shifts.
2. Optional: score sample strings with the rubric.
3. Output: **Korean** audit summary with severity groups.

#### quality-check — 5-dimension rubric

1. Use [references/quality-rubric.md](references/quality-rubric.md):
   - **Clarity** (25%), **Consistency** (25%), **Actionability** (20%),
   - **Tone** (15%), **Naturalness** (15%).
2. Gate: 8.0+ PASS; 6.0–7.9 REVIEW; below 6.0 FAIL.
3. Output: **Korean** score card with per-dimension breakdown.

### Step 4: Deliver

Use tables for structured comparisons. Offer `md-to-notion` or spreadsheet
export via `anthropic-xlsx` when useful.

## Cloud-specific rules (summary)

- Use **resource** as the generic cloud object term when type-agnostic.
- Separate **destructive** vs **reversible** actions in confirmations; name
  resources in errors and confirmations.
- State **time estimates** for async operations when appropriate.
- Use **progressive disclosure**: short inline text + descriptive “Learn more” links
  (never bare “click here”).

## Integration

- **Inputs**: PRDs (`pm-execution`), design handoff, policy docs, `policy-text-generator` output
- **Outputs**: `md-to-notion`, Slack, `anthropic-xlsx`
- **Related**: `technical-writer` (non-UI docs), `sentence-polisher` (final Korean polish for reports)

## Examples

### Example 1: Generate payment errors (English copy, Korean delivery)

User: English payment failure strings.

Actions: `generate` → error pattern → 3-part structure → validate → deliver
table of English strings with Korean usage notes.

### Example 2: Review a confirmation modal

User: Provides modal title/body/buttons.

Actions: `review` → flag vague “OK”, passive voice → specific verb labels →
Korean rationale table.

### Example 3: Audit button labels

User: Mixed-case batch.

Actions: `audit` → casing + verb patterns → Korean report with Critical/High/Medium.

### Example 4: Quality-check onboarding English

User: Paste onboarding paragraph.

Actions: `quality-check` → score dimensions → Korean REVIEW/FAIL verdict with fixes.

## Error handling

| Situation | Action |
|-----------|--------|
| Ambiguous sub-skill | Ask which of generate / review / audit / quality-check |
| No tone guide | Use default + cloud tone matrix; or ask for 3–5 tone attributes |
| Mixed languages in input | Process each language group separately |
| Very large set (>200 strings) | Batches of 50; cumulative Korean summary |
| Custom terminology list | Merge with glossary; user terms win |
| User overrides a suggestion | Accept; record as team convention |
| UI element type unknown | Infer or ask: error, tooltip, modal, label, etc. |

<!-- autoskill-merge anchor — do not remove -->
