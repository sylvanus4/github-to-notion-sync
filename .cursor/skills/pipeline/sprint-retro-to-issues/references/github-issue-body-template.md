---
name: github-issue-body-template
description: Template for GitHub issue body created from sprint retro action items (Phase 5).
---

# GitHub Issue Body Template

## Template

Use this template when rendering each action item into a `gh issue create --body` argument.

```markdown
## 개요

{item.description}

## 배경 및 맥락

이 이슈는 **{meeting_title}** 스프린트 회고에서 도출되었습니다.

**출처**: {item.source}
**원문**: "{item.source_quote}"

### 추가 배경 정보

{AI가 알고 있는 프로젝트/조직/기술적 맥락에서 이 이슈가 왜 중요한지, 현재 상태가 어떤지, 관련 히스토리나 의존성 등 개발자가 작업 시작 전 알아야 할 배경 정보를 상세히 기술}

## 완료 기준

{for each criterion in item.acceptance_criteria:}
- [ ] {criterion}
{end for}

## 실행 계획

{for each step in item.description_steps (if available):}
1. {step}
{end for}

## 메타데이터

| 항목 | 값 |
|------|-----|
| 우선순위 | {item.priority} |
| 크기 | {item.size} ({item.estimate}pt) |
| 카테고리 | {item.category} |
| 스프린트 | {item.sprint_target} |
| 담당자 | @{item.assignee_github} |
| 의존성 | {item.dependencies or "없음"} |

---

> 이 이슈는 `sprint-retro-to-issues` 파이프라인에 의해 자동 생성되었습니다.
> 회고 ID: {item.id} | 생성일: {date}
```

## Title Format

Issue title should be the action item's Korean title as-is:

```
{item.title}
```

Do NOT add prefixes like `[Retro]` or `[SRI-001]` — use labels for categorization.

## Labels

Always apply the `sprint-retro` label. Additionally apply category-specific labels if they exist:

| Category | Additional Label |
|----------|-----------------|
| bug | `bug` |
| feature | `enhancement` |
| improvement | `enhancement` |
| tech-debt | `tech-debt` |
| process | `process` |
| documentation | `documentation` |

## Rendering Rules

1. **Escape heredoc-unsafe characters**: Replace any `EOF` in content with `END_OF_CONTENT`.
2. **No raw HTML**: GitHub renders markdown; avoid `<br>` or `<table>`.
3. **Korean content**: Issue title and body must be entirely in Korean. Section headers, field labels, and metadata are all Korean.
4. **Link dependencies**: If `item.dependencies` references another SRI item, add a note: "관련 이슈: #{other_issue_number}" after creation.
