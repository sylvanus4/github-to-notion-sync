---
name: report-template
description: Final Korean summary report template for Phase 6.
---

# Report Template

Use this template to generate `report.md` in Phase 6.

## Template

```markdown
# 스프린트 회고 → GitHub 이슈 변환 보고서

**생성일**: {YYYY-MM-DD}
**회의 제목**: {meeting_title}
**Notion 원본**: [{meeting_title}]({notion_url})

---

## 1. 파이프라인 실행 요약

| 항목 | 값 |
|------|-----|
| 실행 시작 | {started_at} |
| 실행 완료 | {completed_at} |
| 총 소요 시간 | {elapsed} |
| 전체 상태 | {overall_status} |
| 경고 | {warnings_count}건 |

### 단계별 상태

| 단계 | 이름 | 상태 | 소요 시간 |
|------|------|------|----------|
| 1 | 수집 (Collect) | {status} | {elapsed} |
| 2 | 분석 (Analyze) | {status} | {elapsed} |
| 3 | 추출 (Extract) | {status} | {elapsed} |
| 4 | 비판 (Critique) | {status} | {elapsed} |
| 5 | 이슈 생성 (Create) | {status} | {elapsed} |
| 6 | 보고 (Report) | {status} | {elapsed} |

---

## 2. 회의 개요

**참석자**: {participant_count}명
**트랜스크립트 크기**: {content_size_kb}KB
**회의 유형**: 스프린트 회고

### 주요 논의 주제
{for each topic in key_findings:}
- {topic}
{end for}

---

## 3. 액션 아이템 요약

**총 항목**: {total_items}개
**우선순위 분포**: P0({p0_count}) | P1({p1_count}) | P2({p2_count})
**크기 분포**: XS({xs}) S({s}) M({m}) L({l}) XL({xl})
**총 스토리 포인트**: {total_estimate}pt

### 생성된 이슈 목록

| # | ID | 제목 | 담당자 | 우선순위 | 크기 | GitHub 이슈 |
|---|-----|------|--------|---------|------|------------|
{for each issue in created_issues:}
| {n} | {action_id} | {title} | @{assignee_github} | {priority} | {size} | [#{issue_number}]({issue_url}) |
{end for}

---

## 4. 품질 검사 결과

| 항목 | 값 |
|------|-----|
| 통과 | {passed}개 |
| 보완 후 통과 | {rewritten}개 |
| 병합 | {merged}개 |
| 플래그 | {flagged}개 |
| 평균 품질 점수 | {average_score}/5.0 |

### 갭 경고
{if gap_warnings:}
{for each warning in gap_warnings:}
- ⚠️ {warning}
{end for}
{else}
✅ 모든 논의 주제가 액션 아이템으로 커버됨
{end if}

---

## 5. 프로젝트 필드 설정

모든 이슈가 **ThakiCloud Project #5**에 추가되었으며, 다음 필드가 설정되었습니다:
- ✅ Status (상태)
- ✅ Priority (우선순위)
- ✅ Size (크기)
- ✅ Estimate (추정치)
- ✅ Sprint (스프린트)

---

## 6. 다음 단계

1. GitHub Project #5 보드에서 이슈 확인: https://github.com/orgs/ThakiCloud/projects/5
2. 각 이슈의 담당자 확인 (Owner-to-GitHub 매핑 기반 자동 배정됨)
3. 스프린트 플래닝에서 우선순위 조정
4. 의존성 이슈 간 링크 추가
```

## Writing Guidelines

1. All content in Korean; technical terms and URLs in English.
2. Include clickable GitHub issue links for every created issue.
3. Report quality scores honestly — do not inflate.
4. Gap warnings should reference specific retro topics that lack action items.
5. Phase timing should be approximate (seconds or minutes).
