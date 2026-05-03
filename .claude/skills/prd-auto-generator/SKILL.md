---
name: prd-auto-generator
description: >-
  Three-mode PRD generator. **Strategic mode**: discovery + positioning +
  market framing from meetings, Slack, docs. **Implementation-ready mode**:
  full PRD + edge-case matrix + state spec + policy checklist for dev handoff.
  **Conversation-capture mode** (`--capture`): synthesize the current
  conversation context and codebase understanding into a PRD without
  interviewing the user — identifies deep modules, files as GitHub issue,
  captures contradictions. Use when the user asks to "generate PRD from
  meeting", "auto PRD", "PRD 자동 생성", "기획서 자동화", "회의록에서 PRD 만들어줘", "슬랙에서 PRD
  추출", "PRD from transcript", "실행 기획서 작성", "상세 PRD", "Edge Case 포함 기획서", "상태
  정의서 포함 PRD", "개발 착수용 기획서", "정책 반영 기획서", "implementation-ready spec",
  "detailed PRD with edge cases", "to PRD", "make a PRD from this", "PRD로
  만들어", "대화에서 PRD", "지금까지 정리해서 PRD", "PRD 이슈로", "컨텍스트 PRD", "capture this as
  PRD", "conversation to PRD". Do NOT use for simple PRD from scratch only
  (use pm-execution create-prd). Do NOT use for feature spec only (use
  kwp-product-management-feature-spec). Do NOT use for code reverse spec (use
  code-to-spec; Notion 대조는 code-spec-comparator). Do NOT use for full research
  PRD with human verification gates (use prd-research-factory) when the user
  needs the complete research pipeline — this skill may still reference it in
  strategic mode.
---

# PRD Auto-Generator

Assembles product requirements documents from **heterogeneous sources** (meeting
transcripts, Slack threads, Notion pages, pasted text) with optional deep
enrichment: state coverage, edge cases, API links, design-system references,
and policy alignment.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Modes

| Mode | Purpose | Differentiators |
|------|---------|-----------------|
| `strategic` | Discovery + positioning + market framing | Problem, goals, user stories, **market context**, **competitive landscape** summary, open questions; lighter implementation detail unless user asks |
| `implementation-ready` | Handoff to engineering | Full PRD + **edge-case matrix** + **state spec** + **policy checklist** + optional **Figma state cross-check** + **doc-quality-gate** + export **DOCX** / **Notion** |

Default if unspecified: infer from user wording (implementation / dev handoff / edge cases → `implementation-ready`; strategy / market / competition → `strategic`). Korean trigger phrases are listed in the YAML description. When unclear, ask once.

**Note:** For exhaustive research, fidelity gates, and multi-layer verification, orchestrate with `prd-research-factory` **after** or **instead of** `strategic` when the user explicitly needs that pipeline.

## Input

1. **`mode`** — `strategic` \| `implementation-ready`
2. **Source type** — `meeting` / `slack` / `doc` / `manual`
3. **Source data** — transcript text, Slack thread URL, Notion page ID, or pasted content
4. **Feature name** — product feature or initiative name
5. **Optional enrichments** (defaults ON unless disabled):
   - `api_link` — tie requirements to APIs (code-to-spec / code-spec-comparator output when available)
   - `design_ref` — design system components per screen/flow
   - `policy_check` — policy alignment; use `policy-text-generator` for copy-level checks in implementation-ready
   - `state_checklist` — state/edge matrices
6. **implementation-ready only:**
   - Policy doc URL/file (optional)
   - Figma URL (optional)
   - Output targets: `notion` | `docx` | `both` (default: `both` when publishing)

## Workflow (shared)

### Step 1: Extract requirements

From sources, extract:

1. Problem statement
2. Goals / objectives / success metrics
3. Functional requirements (flows, interactions)
4. Non-functional requirements (performance, security, accessibility)
5. Assumptions
6. Open questions / conflicts

For meetings, reuse `meeting-digest`-style cues: decisions, action items, requirements.

### Step 2: Strategic mode additions

- Add **market context** (segment, problem urgency, trends) at appropriate depth from sources + light web research if user allows.
- Add **competitive analysis** summary (table: competitor / positioning / gap / implication).
- Keep state/edge matrices **abbreviated** unless user requests implementation-ready.

### Step 3: State and edge coverage

Always use [references/state-edge-case-checklist.md](references/state-edge-case-checklist.md) as the base checklist.

For **`implementation-ready`**, also generate full artifacts from:

- [references/edge-case-matrix-template.md](references/edge-case-matrix-template.md)
- [references/state-spec-template.md](references/state-spec-template.md)

Flag uncovered states and missing edge categories explicitly in a **gap section** (Korean heading in deliverable).

### Step 4: Cross-reference enrichment

**API linking** (`api_link`):

- Link endpoints to requirements; flag requirements without API traces.

**Design references** (`design_ref`):

- Map UI requirements to design-system components; flag gaps.

**Policy** (`policy_check`):

- List applicable policies; flag conflicts.
- In **implementation-ready**, run **policy copy alignment** via `policy-text-generator` for error/consent strings; record mismatches and proposed text.

### Step 5: Implementation-ready pipeline extras

When `mode: implementation-ready`:

1. Build PRD skeleton using `pm-execution` PRD patterns (problem, stories, NFRs, metrics).
2. Attach **edge-case matrix** and **state spec** per feature/screen.
3. If **Figma URL** present: compare design variants vs state spec; list missing error/empty/loading.
4. Run **`doc-quality-gate`** on the assembled doc; append scores/findings as an **appendix** (Korean section title in deliverable).
5. Publish **Notion** via `md-to-notion`; generate **DOCX** via `anthropic-docx` when requested.
6. Optional: `design-system-tracker` only if the user needs DS change linkage (not default).

```text
Functional requirements → PRD skeleton → edge matrix → state spec
  → policy-text-generator (copy alignment) → optional Figma cross-check
  → doc-quality-gate → anthropic-docx + md-to-notion
```

### Step 6: Assemble PRD

Use [references/prd-template.md](references/prd-template.md). For implementation-ready, ensure sections include:

- Functional requirements (per item: state matrix, linked APIs, design components)
- **Edge-case matrix** (dedicated section or appendix)
- **State specification**
- **Policy compliance** table + validation summary

### Step 7: Publish

1. Write markdown locally.
2. `md-to-notion` under the agreed PRD parent.
3. Optional Slack summary (high-level goals + open questions + gap count).

## Integration

| Skill | Role |
|-------|------|
| `meeting-digest` | Meeting parsing patterns |
| `pm-execution` | PRD scaffolding |
| `policy-text-generator` | Policy copy sync (implementation-ready) |
| `doc-quality-gate` | Final quality (implementation-ready) |
| `anthropic-docx` | Word export |
| `md-to-notion` | Notion publish |
| `prd-research-factory` | Deeper strategic + research + gates when explicitly required |

## Examples

### Example 1: Meeting → implementation-ready

User: meeting-notes URL + request for implementation-ready PRD.

Actions: Extract requirements → full edge + state → API/design refs → policy pass → doc-quality-gate → Notion + DOCX.

### Example 2: Slack → strategic

User: Slack thread URL + request for strategic PRD draft.

Actions: Extract decisions → market/competitive sections → short checklist → Notion.

### Example 3: Multi-source merge

User: meeting notes + existing Notion doc.

Actions: Merge, dedupe conflicts into an **open issues** section → mode per user.

## Error handling

| Error | Action |
|-------|--------|
| Requirements not extractable | Ask for bullet list or narrower scope |
| Source too short (<500 chars) | Request more context |
| API link fails | Continue without links; note manual follow-up |
| Notion publish fails | Save local MD; retry instructions |
| Conflicting requirements | List conflicts under open issues; do not silently merge |
| Policy/Figma inaccessible | Mark sections TBD; continue other sections |

## Conversation-Capture Mode (`--capture`)

Activate when the user says "to PRD", "make a PRD from this", "capture this as
PRD", "대화에서 PRD", "지금까지 정리해서 PRD", "컨텍스트 PRD", or uses
`--capture` flag.

### Core Principle

**Do NOT interview the user.** Everything needed is already in the current
conversation context and codebase. Synthesize, don't interrogate.

### Workflow

#### 1. Harvest Conversation Context

Scan the entire conversation history for:
- Stated goals, constraints, and requirements
- Decisions made (and their rationale)
- Contradictions or unresolved tensions
- Technical discoveries from codebase exploration
- User corrections or preference signals

#### 2. Deep Module Identification

Analyze the codebase (via SemanticSearch/Grep) to find:
- **Deep modules**: small interface hiding significant complexity (GOOD)
- **Shallow modules**: large interface with thin implementation (FLAG)
- Existing patterns the PRD should reference or extend

For each candidate deep module, note:
- Interface surface area (method/prop count)
- Hidden complexity (what callers don't see)
- Reuse potential across features

#### 3. Synthesize PRD

Use `references/prd-template.md` as the scaffold. Fill sections from harvested
context only — leave sections genuinely unknown as `TBD (not discussed)` rather
than hallucinating content.

Required sections:
1. **Problem Statement** — from user's stated goals
2. **Proposed Solution** — from conversation decisions
3. **Deep Module Candidates** — from codebase analysis (Step 2)
4. **Contradictions & Open Questions** — unresolved tensions found in Step 1
5. **Technical Context** — relevant codebase patterns discovered
6. **Scope Boundaries** — what was explicitly excluded in conversation

#### 4. Contradiction Handling

When contradictions are found between:
- Earlier vs later statements → note both, mark which is more recent
- User intent vs codebase reality → flag with evidence
- Multiple stakeholder signals → list as open question

Never silently resolve contradictions. Surface them in a dedicated section.

#### 5. File as GitHub Issue (optional, `--file-issue`)

When `--file-issue` is specified:

```bash
gh issue create \
  --title "PRD: <feature-name>" \
  --body "$(cat prd-output.md)" \
  --label "prd,auto-generated" \
  --project "ThakiCloud #5"
```

### Example: Conversation → PRD

User has been discussing a new notification system for 20 messages. Context
includes: requirements, rejected alternatives, codebase exploration results.

Actions: Harvest all 20 messages → identify notification service as deep module
candidate → synthesize PRD with contradictions section → file as issue.

<!-- autoskill-merge anchor — do not remove -->
