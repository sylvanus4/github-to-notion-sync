---
name: docs-tutor
description: >-
  Interactive quiz tutor for the project's StudyVault. Tracks concept-level
  proficiency with badges, drills weak areas, and updates a learning dashboard.
  Use when the user wants to "quiz me", "test my knowledge", "study the docs",
  "docs-tutor", "학습", "퀴즈", "평가", or review specific platform topics. Do NOT use
  for generating the StudyVault (use docs-tutor-setup) or for general
  documentation reading.
metadata:
  version: "1.0.0"
  category: "learning"
  author: "thaki"
---
# Docs Tutor — Interactive Quiz for Platform Knowledge

Quiz-based tutor that tracks what the user knows and doesn't know at the **concept level**. The goal is helping users discover blind spots in their platform knowledge through targeted questions.

## Allowed Tools

Read, Write, Glob, Grep, AskQuestion

## File Structure

```
StudyVault/
├── 00-Dashboard/
│   ├── *study-map*         ← MOC with section map and learning path
│   └── *dashboard*         ← Compact overview: proficiency table + stats
├── 01-<Section>/
│   ├── concept notes...
│   └── practice questions...
├── ...
└── concepts/
    ├── {section-name}.md   ← Per-section concept tracking (attempts, status, error notes)
    └── ...
```

- **Dashboard**: Only aggregated numbers. Links to concept files. Stays small forever.
- **Concept files**: One per section. Tracks each concept with attempts, correct count, date, status, and error notes. Grows proportionally to unique concepts tested (bounded).

---

## Workflow

### Phase 0: Detect Language

Detect user's language from their message → `{LANG}`. All output and file content in `{LANG}`.

### Phase 1: Discover Vault

1. Glob `**/StudyVault/` in project root.
2. List section directories (numbered folders).
3. Glob `**/StudyVault/00-Dashboard/*dashboard*` to find dashboard.
4. If found, read it. Preserve existing file path regardless of language.
5. If not found, create from template (see Dashboard Template below).

If no StudyVault exists, inform user: "StudyVault가 없습니다. 먼저 `/docs-tutor-setup`을 실행하여 학습 자료를 생성하세요." and stop.

### Phase 2: Ask Session Type

**MANDATORY**: Use AskQuestion to let the user choose what to do.

Read the dashboard proficiency table and build context-aware options:

1. If unmeasured sections (⬜) exist → include **"진단 평가"** option targeting those sections
2. If weak sections (🟥/🟨) exist → include **"약점 집중 학습"** option naming the weakest section(s)
3. Always include **"섹션 선택"** option so the user can pick any section
4. If all sections are 🟩/🟦 → include **"하드 모드 복습"** option

Present these via AskQuestion with concise descriptions showing which sections each option targets. The user MUST select before proceeding.

### Phase 3: Build Questions

1. Read concept notes and practice question files in target section(s).
2. If drilling weak area: also read `concepts/{section}.md` to find 🔴 unresolved concepts — rephrase these in new contexts (don't repeat the same question).
3. Craft exactly **4 questions** following [quiz-rules.md](references/quiz-rules.md).

**CRITICAL**: Read `references/quiz-rules.md` before crafting ANY question. Zero hints allowed.

### Phase 4: Present Quiz

Use AskQuestion:
- 4 questions, 4 options each, single-select
- Header format: `"Q1. <Topic>"` (max 12 chars)
- Descriptions: neutral, no hints, no "(Recommended)" tags

### Phase 5: Grade & Explain

1. Show results table:

   | Question | Correct Answer | Your Answer | Result |
   |----------|---------------|-------------|--------|
   | Q1 | B | A | ❌ |
   | Q2 | C | C | ✅ |
   | ... | ... | ... | ... |

2. Wrong answers: provide concise explanation of the correct answer and why the selected option is wrong.
3. Map each question to its section for tracking.

### Phase 6: Update Files

#### 1. Update concept file (`concepts/{section}.md`)

For each question answered:
- **New concept**: Add row to table. If wrong, add error note under `### 오답 메모`.
- **Existing 🔴 concept answered correctly**: Increment attempts & correct, change status to 🟢, keep error note (learning history).
- **Existing 🟢 concept answered wrong again**: Increment attempts, change status back to 🔴, update error note.

Table format:
```markdown
| Concept | Attempts | Correct | Last Tested | Status |
|---------|----------|---------|-------------|--------|
| concept name | 2 | 1 | 2026-03-04 | 🔴 |
```

Error notes format (only for wrong answers):
```markdown
### 오답 메모

**concept name**
- 혼동: what the user mixed up
- 핵심: the correct understanding
```

#### 2. Update dashboard

- Recalculate per-section stats from concept files (sum attempts/correct across all concepts in that section).
- Update proficiency badges: 🟥 0-39% · 🟨 40-69% · 🟩 70-89% · 🟦 90-100% · ⬜ no data
- Update stats: total questions, cumulative rate, unresolved/resolved counts, weakest/strongest section.

Dashboard stays compact — no session logs, no per-question details.

---

## Dashboard Template

Create when no dashboard exists. Filename: `학습-대시보드.md` (Korean) or `learning-dashboard.md` (English).

```markdown
# 학습 대시보드

> 개념 수준 메타인지 추적. 상세 내용은 링크된 파일을 참조하세요.

---

## 섹션별 숙련도

| Section | Correct | Wrong | Rate | Level | Details |
|---------|---------|-------|------|-------|---------|
(one row per section, last column = [[concepts/{section}]] link)
| **Total** | **0** | **0** | **-** | ⬜ Unmeasured | |

> 🟥 Weak (0-39%) · 🟨 Fair (40-69%) · 🟩 Good (70-89%) · 🟦 Mastered (90-100%) · ⬜ Unmeasured

---

## Stats

- **Total Questions**: 0
- **Cumulative Rate**: -
- **Unresolved Concepts (🔴)**: 0
- **Resolved Concepts (🟢)**: 0
- **Weakest Section**: -
- **Strongest Section**: -
```

## Concept File Template

Create per section when first question is asked. Filename: `{section-name}.md`.

```markdown
# {Section Name} — Concept Tracker

| Concept | Attempts | Correct | Last Tested | Status |
|---------|----------|---------|-------------|--------|

### 오답 메모

(added as concepts are missed)
```

---

## Important Reminders

- ALWAYS read `references/quiz-rules.md` before creating questions
- NEVER include hints in option labels or descriptions
- NEVER use "(Recommended)" on any option
- Randomize correct answer position across questions
- After grading, ALWAYS update both concept file AND dashboard
- Communicate in user's detected language
- If user wants to continue, loop back to Phase 2 (ask session type again)
- Keep dashboard compact — never append session logs or per-question history

## Examples

### Example 1: Standard usage
**User says:** "docs tutor" or request matching the skill triggers
**Actions:** Execute the skill workflow as specified. Verify output quality.
**Result:** Task completed with expected output format.

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Unexpected input format | Validate input before processing; ask user for clarification |
| External service unavailable | Retry with exponential backoff; report failure if persistent |
| Output quality below threshold | Review inputs, adjust parameters, and re-run the workflow |
