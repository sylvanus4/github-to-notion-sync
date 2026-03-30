---
name: action-items-template
description: Korean action items document template for the meeting-digest skill.
---

# Action Items Template

## Table of Contents

- [Template](#template) — Full Korean action items structure with dashboard
- [Extraction Rules](#extraction-rules) — What qualifies as an action item
- [Priority Assignment](#priority-assignment) — 4-tier priority criteria
- [Action Item ID Format](#action-item-id-format) — Sequential numbering rules
- [Dependency Tracking](#dependency-tracking) — Cross-action dependencies
- [Writing Guidelines](#writing-guidelines) — Titles, details, success criteria

---

Use this template to generate the `action-items.md` output file. All content
must be in Korean.

## Template

```markdown
# 액션 아이템 상세 문서

**생성일**: {YYYY-MM-DD}
**출처 회의**: {meeting title}

---

## 우선순위: 긴급 (높음)

### AI-001: {Action Title}

- **담당자**: {name}
- **기한**: {YYYY-MM-DD}
- **우선순위**: 긴급
- **상태**: 미시작
- **관련 회의**: {meeting title}
- **배경**: {2-3 sentences explaining WHY this action is needed, referencing
  the specific discussion point that generated it}
- **상세 내용**:
  1. {Concrete execution step 1}
  2. {Concrete execution step 2}
  3. {Concrete execution step 3}
- **성공 기준**: {Measurable criteria for completion}
- **의존성**: {Prerequisites or related action items, e.g., "AI-002"}
- **비고**: {Additional notes, quotes, or context}

---

## 우선순위: 높음 (중간)

### AI-002: {Action Title}

- **담당자**: {name}
- **기한**: {YYYY-MM-DD}
- **우선순위**: 높음
- **상태**: 미시작
- **관련 회의**: {meeting title}
- **배경**: {...}
- **상세 내용**:
  1. {...}
- **성공 기준**: {...}
- **의존성**: {...}
- **비고**: {...}

---

## 우선순위: 보통 (낮음)

### AI-003: {Action Title}
...

---

## 액션 아이템 대시보드

| ID | 액션 | 담당자 | 기한 | 우선순위 | 상태 | 의존성 |
|----|------|--------|------|---------|------|--------|
| AI-001 | {short desc} | {name} | {date} | 긴급 | 미시작 | - |
| AI-002 | {short desc} | {name} | {date} | 높음 | 미시작 | AI-001 |
| AI-003 | {short desc} | {name} | {date} | 보통 | 미시작 | - |
```

## Extraction Rules

### What qualifies as an action item

1. **Explicit commitments**: Anything stated as "we need to", "someone
   should", "let's do", "will handle", "by next week" — extract directly
2. **Implicit follow-ups**: Decisions that require implementation work
   even if not explicitly assigned — extract and mark owner as "미정"
   if not stated
3. **Blocked items**: Items that depend on external input, other teams,
   or future events — mark dependencies clearly
4. **Time-sensitive items**: Items with stated deadlines get higher priority

### Priority assignment

| Priority | Criteria |
|----------|----------|
| **긴급** | Explicit deadline within 3 days, or blocks other work |
| **높음** | Deadline within 1 week, or significant business impact |
| **보통** | Deadline beyond 1 week, or lower urgency stated |
| **낮음** | No deadline, exploratory, or "nice to have" |

### Action item ID format

- Sequential: `AI-001`, `AI-002`, `AI-003`...
- Group by priority (긴급 first, then 높음, 보통, 낮음)
- Numbering is continuous across priority groups

### Dependency tracking

- If action B cannot start until action A is complete, record
  `의존성: AI-{A's number}` in action B
- If an action depends on external input (not another action item),
  note it in 비고 instead

### Writing guidelines

1. **Action titles**: Start with a verb (작성, 검토, 산출, 정리, 설계)
2. **상세 내용**: Break into 3-6 concrete, sequential steps
3. **성공 기준**: Must be verifiable — avoid "잘 되면" type criteria
4. **배경**: Reference the specific discussion point from the meeting
   that generated this action, including relevant participant quotes
   when impactful
5. **Owner attribution**: Use the participant's name as stated in the
   meeting. If multiple owners, list the primary owner first
