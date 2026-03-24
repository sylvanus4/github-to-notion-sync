---
name: prd-auto-generator
description: >-
  미팅·슬랙·기존 문서 등 다중 소스에서 PRD를 자동 생성. 상태/엣지 체크리스트,
  API 스펙 연계, 디자인 시스템 컴포넌트 참조, 실행 모드에서는 Edge 매트릭스·상태 정의서·
  정책 체크리스트까지 포함한 개발 착수용 기획서까지 지원.
  Use when the user asks to "generate PRD from meeting", "auto PRD",
  "PRD 자동 생성", "기획서 자동화", "회의록에서 PRD 만들어줘", "슬랙에서 PRD 추출",
  "PRD from transcript", "실행 기획서 작성", "상세 PRD", "Edge Case 포함 기획서",
  "상태 정의서 포함 PRD", "개발 착수용 기획서", "정책 반영 기획서",
  "implementation-ready spec", "detailed PRD with edge cases".
  Do NOT use for simple PRD from scratch only (use pm-execution create-prd).
  Do NOT use for feature spec only (use kwp-product-management-feature-spec).
  Do NOT use for code reverse spec (use code-to-spec; Notion 대조는 code-spec-comparator).
  Do NOT use for full research PRD with human verification gates (use prd-research-factory)
  when the user needs the complete research pipeline — this skill may still reference it in strategic mode.
metadata:
  author: "thaki"
  version: "2.0.1"
  category: "generation"
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

<!-- autoskill-merge anchor — do not remove -->
