---
name: summary-template
description: Korean meeting summary output template for the meeting-digest skill.
---

# Summary Template

## Table of Contents

- [Template](#template) — Full Korean summary structure (Sections 1-6)
- [Writing Guidelines](#writing-guidelines) — Tone, specificity, language rules
- [PM Analysis Appendix](#pm-analysis-appendix) — Conditional appendix format

---

Use this template to generate the `summary.md` output file. All content
must be in Korean. Adjust section depth based on meeting complexity.

## Template

```markdown
# 회의 요약 보고서

**생성일**: {YYYY-MM-DD}
**회의 제목**: {meeting-title}
**회의 유형**: {classified-type} (discovery / strategy / gtm / sprint / operational)

---

## 1. 회의 개요

**일시**: {date and time, if available}
**참석자**: {name (role/title)} — list all identified participants
**주제**: {one-line summary of the meeting's main purpose}

---

## 2. 핵심 논의 사항

### 2.1 {Topic Title}
- **논의 내용**: {Detailed description of what was discussed. Include specific
  data points, examples, and quotes where available. Do NOT summarize away
  nuance — capture the full breadth of the discussion.}
- **결론**: {What was decided or concluded about this topic}
- **관련 참석자**: {Names of people who contributed to this discussion}

### 2.2 {Topic Title}
- **논의 내용**: {...}
- **결론**: {...}
- **관련 참석자**: {...}

{Repeat for each distinct topic discussed. Err on the side of more
granularity — split topics when they cover genuinely different subjects.}

---

## 3. 주요 결정 사항

| # | 결정 사항 | 결정 배경 | 영향 범위 | 담당자 |
|---|----------|----------|----------|--------|
| 1 | {decision} | {why this was decided} | {what it affects} | {who owns it} |
| 2 | ... | ... | ... | ... |

---

## 4. 미해결 이슈 / 오픈 질문

| # | 이슈 | 관련 담당자 | 예상 해결 시점 |
|---|------|-----------|-------------|
| 1 | {unresolved issue or open question} | {who is responsible} | {when to resolve} |

---

## 5. 액션 아이템 요약

| 우선순위 | 담당자 | 액션 | 기한 |
|---------|--------|------|------|
| 긴급 | {name} | {action} | {due date} |
| 높음 | {name} | {action} | {due date} |
| 보통 | {name} | {action} | {due date} |

> 상세 액션 아이템은 `action-items.md`를 참조하세요.

---

## 6. 다음 단계

1. {Concrete next step with responsible person and timeline}
2. {Next step}
3. {...}
```

## Writing Guidelines

1. **Completeness over brevity**: Capture every topic discussed. A missing
   topic is worse than a verbose summary.
2. **Specific over vague**: Use exact numbers, names, dates mentioned in
   the meeting. Never generalize when specifics are available.
3. **Neutral tone**: Report what was discussed without editorializing.
   Attribute viewpoints to specific participants when relevant.
4. **Participant roles**: Always identify participant roles when stated or
   inferable (e.g., "효정 (기술리드)", "소린 (재무)").
5. **Decision rationale**: For each decision, include WHY it was made,
   not just WHAT was decided.
6. **Korean language**: All content in Korean. Technical terms and proper
   nouns may remain in English (e.g., "GPU", "SWOT", "IRR").

## PM Analysis Appendix

If Phase 3 produced contextual PM analysis, append it after Section 6:

```markdown
---

## 부록: PM 분석

### {Framework Name} (e.g., SWOT 분석, 가정 검증, ICP 정의)

{Framework-specific output in Korean, formatted per the PM skill's template}
```
