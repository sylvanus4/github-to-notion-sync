---
name: implement-screen
description: 화면 기획서와 Figma 디자인을 기반으로 FSD 구조의 프로덕션 코드를 생성하는 마스터 오케스트레이터. 화면 구현, 페이지 만들어줘, 화면 개발, Figma URL + screen spec으로 코드 생성 시 사용합니다. Do NOT use for 기획서만 작성(screen-description), Figma 분석만 수행(figma-to-tds), 또는 디자인 리뷰만 수행(design-review).
metadata:
  version: 1.1.0
  category: orchestrator
---

# Screen Implementation Orchestrator

화면 기획서(Screen Spec)와 Figma 디자인을 기반으로, FSD 구조의 프로덕션 코드를 생성하는 **마스터 워크플로우**. 개별 Skills를 올바른 순서로 체이닝한다.

## Input types

| 입력 | 소스 | 필수 |
|------|------|------|
| **도메인명** | 사용자 지정 (예: `workload`, `template`) | **필수** |
| **화면 기획서** | `docs/screens/{domain}/{screen}.md` | 권장 |
| **Figma URL** | `https://figma.com/design/...` | 선택 |
| **Swagger/API 명세** | URL 또는 문서 | 선택 |

---

## Workflow

### Phase 0 – 입력 수집 및 검증

```
Task Progress:
- [ ] Phase 0: 입력 수집 및 검증
- [ ] Phase 1: 화면 기획서 준비
- [ ] Phase 2: Figma 디자인 분석
- [ ] Phase 3: FSD 코드 생성
- [ ] Phase 4: i18n 다국어 처리
- [ ] Phase 5: 검증 및 마무리
```

1. **도메인명 확인** — 없으면 사용자에게 질문
2. **화면 기획서 확인** — `docs/screens/{domain}/` 경로에서 검색
3. **Figma URL 확인** — 사용자 입력에 URL 포함 여부 확인
4. **기존 코드 확인** — `src/pages/{domain}/`, `src/entities/{domain}/` 존재 여부

**분기 결정**:

| 기획서 | Figma | 행동 |
|--------|-------|------|
| ✅ | ✅ | Phase 2 → 3 → 4 → 5 |
| ✅ | ❌ | Phase 3 → 4 → 5 |
| ❌ | ✅ | Phase 1 → 2 → 3 → 4 → 5 |
| ❌ | ❌ | Phase 1 → 3 → 4 → 5 |

---

### Phase 1 – 화면 기획서 준비

> **Skill**: `screen-description`

기획서가 없거나 불완전한 경우에만 실행. Figma URL/Swagger URL이 있으면 해당 정보를 기획서에 반영.

**산출물**: `docs/screens/{domain}/{screen}.md`

---

### Phase 2 – Figma 디자인 분석

> **Skill**: `figma-to-tds`

Figma URL이 제공된 경우에만 실행. **코드 생성 없이** 분석 결과(컴포넌트 맵, 토큰 맵)만 다음 Phase로 전달.

**산출물** (메모리에 유지): Component Map + Token Map

---

### Phase 3 – FSD 코드 생성

> **Skill**: `fsd-development`
> **Rule**: `03-tds-essentials.mdc`(자동), `04-tds-detail-catalog.mdc`(상세), `07-table-patterns.mdc`

기획서 + Figma 분석 결과를 바탕으로 FSD 레이어 순서대로 코드 생성:

```
shared/constants/query-key → entities → features → widgets → pages → routes
```

**핵심 확인**:
- [ ] TDS 컴포넌트 우선 사용
- [ ] 모든 텍스트 `t()` 처리
- [ ] 시맨틱 컬러만 사용
- [ ] Overlay 필요 시 → `overlay-layout-patterns` Skill 참조

---

### Phase 4 – i18n 다국어 처리

> **Rule**: `06-i18n-rules.mdc` (`.tsx/.ts` 편집 시 자동 적용)

Phase 3에서 사용한 모든 `t()` 키에 대해 en/ko 동시 추가. 공통 텍스트는 `tCommon('button.*')`, 도메인 전용은 `t('key')`.

---

### Phase 5 – 검증 및 마무리

> **Skill**: `design-review`

1. **TypeScript 검증**: `npx tsc --noEmit`
2. **기획서 커버리지**: 레이아웃/컴포넌트/인터랙션/상태별 화면/API 연동 검증
3. **Figma 매칭** (URL 있을 때): 레이아웃, 타이포그래피, 색상 토큰 매핑 확인
4. **i18n 완성도**: 하드코딩 문자열 0개, en/ko 동기화
5. **산출물 요약**: 생성/수정 파일 목록 보고

---

## Cross-reference: Skills & Rules

| Phase | Skill / Rule | 역할 |
|-------|--------------|------|
| 1 | `screen-description` | 기획서 생성/업데이트 |
| 2 | `figma-to-tds` | Figma 분석 + TDS 토큰/컴포넌트 매칭 |
| 3 | `fsd-development` | FSD 레이어 구조 + 코드 템플릿 |
| 3 | `03-tds-essentials.mdc` + `04-tds-detail-catalog.mdc` | TDS 필수 규칙(자동) + 상세 Props/API |
| 3 | `overlay-layout-patterns` | 모달/드로어 패턴 |
| 4 | Rule: `06-i18n-rules.mdc` | 다국어 키 관리 |
| 5 | `design-review` | 시각/기능/품질 검증 |

## Examples

### Example 1: Figma + 기획서 모두 있을 때
User says: "workloads 목록 화면 구현해줘. Figma: https://figma.com/design/abc/... 기획서: docs/screens/workloads/workloads-list.md"
Actions:
1. Phase 0: 기획서 ✅, Figma ✅ → Phase 2부터 시작
2. Phase 2: Figma 분석 (컴포넌트 맵 + 토큰 맵)
3. Phase 3: FSD 코드 생성 (entities → features → widgets → pages)
4. Phase 4: i18n 처리
5. Phase 5: 검증 + 산출물 보고
Result: 전 FSD 레이어에 걸친 프로덕션 코드 + i18n 완료

### Example 2: 러프한 설명만 있을 때
User says: "템플릿 목록 페이지 만들어줘. SelectableTable로 목록 보여주고, 생성/삭제 기능 필요해"
Actions:
1. Phase 0: 기획서 ❌, Figma ❌ → Phase 1부터 시작
2. Phase 1: 사용자 설명 기반 기획서 생성
3. Phase 3: FSD 코드 생성
4. Phase 4 → 5: i18n + 검증
Result: 기획서 + 코드 + i18n이 모두 생성됨

## Troubleshooting

### Phase 간 데이터가 전달되지 않음
Cause: Phase 2의 Figma 분석 결과를 Phase 3에서 참조하지 않아 TDS 매핑이 누락
Solution: Phase 2 산출물(Component Map, Token Map)을 Phase 3 시작 시 명시적으로 참조

### 기획서와 코드 불일치
Cause: 기획서 업데이트 후 코드를 재생성하지 않음
Solution: 기획서 변경 시 Phase 5(검증)의 기획서 커버리지 체크를 실행하여 차이점 식별
