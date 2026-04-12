---
name: action-item-template
description: Structured action item format for sprint retro extraction (Phase 3).
---

# Action Item Template

## JSON Schema

Each action item extracted in Phase 3 MUST conform to this schema:

```json
{
  "id": "SRI-{NNN}",
  "title": "{한국어 제목 — 반드시 한국어로, 동사형으로 시작. 영어 금지}",
  "description": "{상세 설명: 배경, 현재 상태, 성공 기준 포함. 최소 100자 이상}",
  "assignee_github": "{Owner-to-GitHub Mapping에서 resolve한 GitHub username. 미매핑 시 sylvanus4}",
  "priority": "P0|P1|P2",
  "size": "XS|S|M|L|XL",
  "estimate": 1,
  "category": "{bug|feature|improvement|tech-debt|process|documentation}",
  "source": "{summary|transcript|retro-table|pm-analysis}",
  "source_quote": "{원문 인용 또는 참조}",
  "acceptance_criteria": [
    "{구체적이고 검증 가능한 완료 조건 1}",
    "{완료 조건 2}"
  ],
  "dependencies": ["SRI-XXX"],
  "sprint_target": "current|next"
}
```

## Priority Definitions

| Priority | Definition | Examples |
|----------|-----------|---------|
| P0 (Critical) | 서비스 장애, 보안 취약점, 데이터 손실 위험 | 프로덕션 버그, 인증 실패 |
| P1 (High) | 이번 스프린트 반드시 완료, 사용자 직접 영향 | 핵심 기능 개선, 성능 병목 |
| P2 (Medium) | 중요하지만 긴급하지 않음, 다음 스프린트 가능 | 리팩토링, 문서화, 테스트 추가, UX 미세 조정 |

> **Note**: GitHub Project #5 only has P0-P2. Low-priority / nice-to-have items should be mapped to P2.

## Size Definitions (Auto-Size Rules)

> **기준**: 1 story point = 8시간 = 1일 = 1 스프린트 (AI 기반 개발). 웬만해서는 estimate 1을 초과하지 않는다.

| Size | Time Estimate (AI-assisted) | Story Points | Criteria |
|------|----------------------------|-------------|----------|
| XS | < 1h | 0.1 | 설정 변경, 오타 수정, 한 줄 수정, 템플릿 적용 |
| S | 1-2h | 0.25 | 단일 파일 수정, 간단한 기능 추가, 정책 문서화 |
| M | 2-4h | 0.5 | 여러 파일 수정, 테스트 포함, 설계 문서화 |
| L | 4-8h (1일) | 1 | 새 컴포넌트/모듈, 통합 작업, 복합 조사 |
| XL | > 8h | 분해 필수 (max 2) | 대규모 리팩토링, 새 시스템 → 더 작은 이슈로 분할 |

## Category Definitions

| Category | Description |
|----------|------------|
| `bug` | 기존 기능의 오동작 수정 |
| `feature` | 새로운 기능 추가 |
| `improvement` | 기존 기능의 개선 (UX, 성능 등) |
| `tech-debt` | 기술 부채 해소 (리팩토링, 의존성 업데이트) |
| `process` | 팀 프로세스/워크플로우 개선 |
| `documentation` | 문서 작성 또는 업데이트 |

## Markdown Output Format

When writing `action-items.md`, use this format:

```markdown
# 스프린트 회고 액션 아이템

**생성일**: {YYYY-MM-DD}
**출처**: {meeting title}
**총 항목**: {N}개

---

## 우선순위: P0 (Critical)

### SRI-001: {Action Title}

- **담당자**: {name} (@{assignee_github})
- **기한**: {YYYY-MM-DD}
- **크기**: {size} ({estimate}pt)
- **카테고리**: {category}
- **출처**: {source}
- **배경**: {2-3 sentences explaining WHY this action is needed}
- **상세 내용**:
  1. {구체적인 실행 단계 1}
  2. {구체적인 실행 단계 2}
  3. {구체적인 실행 단계 3}
- **완료 조건**:
  - [ ] {검증 가능한 조건 1}
  - [ ] {검증 가능한 조건 2}
- **의존성**: {Prerequisites or related items}
- **원문 참조**: "{relevant quote from retro}"

---

## 우선순위: P1 (High)

### SRI-002: ...

{Repeat for each priority group}
```

## Extraction Rules

1. **One action per commitment**: If a participant says "I'll do A and B", create TWO items.
2. **Implicit commitments count**: "We should probably..." in a retro context = action item.
3. **Retro improvements are actionable**: Every "improvement idea" in the retro table should map to at least one item unless it's purely aspirational.
4. **Technical debt from discussion**: Mentions of "we need to fix", "this keeps breaking" → tech-debt items.
5. **No orphan topics**: Every major discussion topic should have at least one resulting action item.
