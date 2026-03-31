---
name: screen-description
description: 러프한 사용자 입력을 받아 구조화된 화면 설명 문서(Markdown)를 생성/업데이트합니다. 화면 설명, 기획서, 화면 기획, 스크린 디스크립션, UI 명세, 화면 스펙 작성 시 사용합니다. Do NOT use for 코드 생성(fsd-development), Figma 디자인 변환(figma-to-tds).
metadata:
  version: 1.1.1
  category: generation
---

# Screen Description Generator

Turn rough notes into structured screen-spec Markdown (create or update).

## Output language

All outputs MUST be in Korean (한국어). Technical terms may remain in English.

## Storage path

```
ai-platform/frontend/docs/screens/
├── workloads/
│   ├── workloads-list.md
│   └── workloads-detail.md
├── templates/
│   ├── templates-list.md
│   └── templates-create.md
└── ...
```

- Folder: page domain (kebab-case)
- File: `{domain}-{screen}.md`

## Workflow

### Step 0 — Figma data (optional)

Only if a Figma URL is provided. Reuse `figma-to-tds` Steps 1–3 pattern:

1. Figma MCP: `get_design_context` + `get_screenshot` in parallel
2. Extract layout, components, tokens
3. Feed Step 2 sections **Layout** and **Components**

### Step 1 — Analyze input

1. Identify target screen and core intent
2. Check existing docs under `ai-platform/frontend/docs/screens/{domain}/`
3. If code exists, read `src/pages/{domain}/` for as-built hints
4. If Swagger/OpenAPI is provided, pre-fill **API integration**

### Step 2 — Create or update

- **New**: scaffold from [references/document-template.md](references/document-template.md)
- **Update**: patch only affected sections + changelog
- **With Figma**: fill layout/component sections from Step 0

### Step 3 — Confirm with user

Show a short summary and ask if further edits are needed.

## Section rules

| Section | Required | When |
|---------|----------|------|
| Screen overview | **Yes** | Always |
| Layout | Recommended | Layout discussed |
| Components | Optional | Implementation detail discussed |
| Interactions | Recommended | Events/behaviors discussed |
| Per-state UI | Recommended | State branching discussed |
| API integration | Optional | APIs mentioned |
| i18n | Optional | i18n mentioned |
| Accessibility | Optional | a11y mentioned |

Rough inputs → fill required + recommended; others use `{TODO: define later}`.
Rich inputs → fill every applicable section.

## Naming

- **Folder**: align with route (e.g. `src/pages/workload/` → `docs/screens/workloads/`)
- **File**: `{domain}-{action}.md` (e.g. `workloads-list.md`)
- **Composite screens**: tabs/modals as subsections inside the main file

## Update rules

1. Do **not** delete existing content unless the user explicitly asks
2. Touch only changed sections
3. Append **changelog** table rows
4. Refresh `last updated` date

## Cross-reference

| Situation | Skill |
|-----------|-------|
| Figma URL present | `figma-to-tds` (Step 0) |
| After spec → code | `implement-screen` |
| i18n keys | Rule `06-i18n-rules.mdc` if present |

## Checklist

- [ ] Target screen identified
- [ ] Save path confirmed (`docs/screens/{domain}/{file}.md`)
- [ ] Checked for existing doc
- [ ] Required overview section present
- [ ] Changelog updated on edits

## Examples

### Example 1: Rough text → new spec

User: "Spec for workload list — table view with create/delete"

Actions: create `docs/screens/workloads/workloads-list.md` with overview, layout, interactions; TODO placeholders elsewhere.

### Example 2: Figma refresh

User: "Update templates-create.md from Figma https://figma.com/design/..."

Actions: read existing doc + Figma MCP → update layout/components → changelog entry.

## Troubleshooting

### Accidental overwrite

Cause: rewrote entire file.
Fix: follow update rules — delta edits only, never drop prior sections without explicit approval.

### Figma not reflected

Cause: skipped Step 0 or MCP error.
Fix: always run Step 0 when URL exists; on MCP failure, continue text-only and state the gap.
