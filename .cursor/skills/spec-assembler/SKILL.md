---
name: spec-assembler
description: >-
  회의록, 정책서, 디자인 시안, 기존 기획 파편 등 다양한 소스를 통합하여 완성된
  기획서/PRD를 자동 조립합니다. 소스 간 충돌을 감지하고 일관된 문서를 생성합니다.
  Use when the user asks to "assemble a spec", "create PRD from sources",
  "combine meeting notes into spec", "기획서 자동 조립", "여러 자료에서 기획서
  만들어줘", "회의록 기반 PRD", "자료 통합해서 스펙 만들어줘", "기획서 자동화",
  "spec-assembler", or wants to automatically generate planning documents from
  multiple scattered sources.
  Do NOT use for PRD writing from scratch without sources (use pm-execution create-prd).
  Do NOT use for meeting transcript analysis only (use meeting-digest).
  Do NOT use for document quality checking (use doc-quality-gate).
  Do NOT use for single-source feature spec (use kwp-product-management-feature-spec).
  Korean triggers: "기획서 자동 조립", "PRD 자동화", "자료 통합 기획서",
  "소스 통합 스펙", "회의록에서 PRD", "기획서 자동 생성".
metadata:
  author: "thaki"
  version: "1.0.1"
  category: "execution"
---

# Spec Assembler

Merge multiple sources (meeting notes, policies, design notes, Slack threads, doc fragments) into one coherent PRD/spec. Detect conflicts, flag gaps, and preserve provenance.

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| `<sources>` | Yes | Paths, Notion IDs, URLs, or pasted text (multiple allowed) |
| `--template` | No | `prd` \| `spec` \| `policy` \| `brief` (default: `prd`) |
| `--fill-gaps` | No | Attempt to infer missing items (default: false) |
| `--conflict-strategy` | No | `ask` \| `latest` \| `flag` (default: `flag`) |
| `--notion-parent` | No | Notion parent page ID for upload |

## Workflow

```
Phase 1: Collect    → Load sources
Phase 2: Extract    → Pull planning elements
Phase 3: Reconcile  → Detect/resolve conflicts
Phase 4: Assemble   → Fill template
Phase 5: Validate   → Completeness + gap scan
Phase 6: Deliver    → Write outputs
```

### Phase 1: Collect

| Source type | How to load |
|-------------|-------------|
| Local (.md, .docx, .pdf) | Read / doc skills |
| Notion | Notion MCP |
| Meeting transcript | meeting-digest chain |
| Slack | Slack MCP history |
| Figma | Figma MCP |
| URL | WebFetch or defuddle |
| Pasted text | Use as-is |

Tag provenance: `[S1: meeting 2026-03-20]`, `[S2: policy v2.1]`, etc.

### Phase 2: Extract

Extract from each source:

- Goals / background / problem
- User needs / stories
- Functional requirements (must/should)
- Non-functional requirements
- Business rules / policy conditions
- States / edge cases
- Design decisions
- Timeline / milestones
- Dependencies / constraints
- Decisions (resolved vs open)

Keep source tags on every extracted atom.

### Phase 3: Reconcile

Conflict types:
- **Numeric mismatch** (e.g. deadlines differ)
- **Scope mismatch** for same feature
- **Priority mismatch** across sources
- **Terminology mismatch**

Strategies (`--conflict-strategy`):
- `ask`: pause for user choice
- `latest`: prefer newest source
- `flag`: embed `⚠️ conflict` with both versions

### Phase 4: Assemble

See [references/spec-templates.md](references/spec-templates.md) for templates.

Default PRD skeleton (assemble content into Korean per output rule):

```markdown
# [Product/feature] PRD

## 1. Overview
### Background
### Problem
### Goals & KPIs

## 2. User scenarios
### Target users
### Primary flows
### Edge cases

## 3. Requirements
### Functional (MoSCoW)
### Non-functional
### Policy constraints

## 4. Detailed design
### States
### Screen flow
### Data needs

## 5. Schedule & milestones

## 6. Dependencies & risks

## 7. Open questions
[Unresolved decisions by source]

## Appendix: Source map
[Traceability table]
```

### Phase 5: Validate

- Required sections present
- Extracted facts missing from doc → gap list
- If `--fill-gaps true`, infer gaps and tag inferred items per the output-language rule (localized label)
- Self-check against doc-quality-gate “required sections” expectations

### Phase 6: Deliver

1. Save markdown: `output/specs/[name]-[date].md`
2. If `--notion-parent`: md-to-notion
3. Include source-mapping table

## Output contract (quality gate)

1. **Traceability** — major claims carry `[SN]` tags
2. **Conflict log** — all conflicts listed (resolved or not)
3. **Open items** — unresolved decisions isolated
4. **Completeness score** — checklist coverage
5. **Inference labels** — mark inferred items with the localized tag required by the output-language rule

## Skill chain

| Situation | Skill | Role |
|-----------|-------|------|
| Meeting preprocessing | meeting-digest | Structured extraction |
| Quality pass | doc-quality-gate | Seven-dimension review |
| Policy parsing | policy-text-generator | Rule extraction |
| Code as source | code-to-spec | Implementation facts |
| Notion publish | md-to-notion | Publishing |

## Examples

### Example 1: Meeting + policy → PRD

User: "Merge last meeting notes and refund policy into a PRD"  
→ Load both → extract → assemble → Korean PRD output.

### Example 2: Three Notion pages

User: "Combine these three Notion pages into one spec"  
→ Fetch → detect conflicts → unified doc.

### Example 3: Gap fill

User: "Assemble and infer missing parts" `--fill-gaps`  
→ Merge → detect gaps → infer with inference tags per output language rule.

## Error Handling

| Situation | Action |
|-----------|--------|
| No sources | Ask for at least one |
| Source unreachable | Process what works; report failures |
| Severe contradictions | Prefer `--conflict-strategy ask` |
| Too many sources (>10) | Prioritize core sources first |
| Mixed languages | Unify to Korean in deliverable; cite originals if needed |

## Evolution

### Eval criteria (binary)

| ID | Eval | Pass condition |
|----|------|----------------|
| E1 | Information retention | ≥90% of core source facts appear in output |
| E2 | Conflict detection | Detect ≥2/3 injected conflicts |
| E3 | Traceability | ≥80% of major bullets have source tags |
| E4 | Template compliance | All required sections for chosen template |
| E5 | Open issues split | Undecided items listed under open questions |

### Autoimprove hook

- **Test inputs**: meeting+policy, three Notion pages, code+design (3 scenarios)
- **Baseline target**: E1–E5 pass rate ≥ 80%
- **Mutation focus**: extraction patterns, conflict rules, template shape
