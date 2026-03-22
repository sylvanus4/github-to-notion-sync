---
name: design-review
description: 구현된 코드를 Figma 디자인 및 화면 기획서와 대조하여 시각적 일치도, 기능 커버리지, 품질 표준을 검증합니다. 디자인 리뷰, 피그마 비교, 구현 검증, design review, compare with Figma, implement-screen 완료 후 사용합니다. Do NOT use for 코드 생성(fsd-development, implement-screen), Figma 분석(figma-to-tds), 또는 기획서 작성(screen-description).
metadata:
  version: 1.1.0
  category: review
---

# Design Review

구현된 코드를 Figma 디자인 및 화면 기획서(Screen Spec)와 대조하여 **시각적 일치도**, **기능 커버리지**, **품질 표준 준수**를 검증한다.

## Inputs

| 입력 | 소스 | 필수 |
|------|------|------|
| **구현 파일 경로** | `src/pages/{domain}/`, `src/widgets/` 등 | **필수** |
| **Figma URL** | `https://figma.com/design/...` | 선택 |
| **Screen Spec** | `docs/screens/{domain}/{screen}.md` | 선택 |
| **도메인명** | 사용자 지정 | **필수** |

하나 이상의 비교 기준(Figma 또는 Screen Spec)이 있어야 유의미한 리뷰가 가능.

---

## Workflow

### Step 1 – 컨텍스트 수집

**병렬로 수집**:
1. **구현 코드**: pages, widgets, entities, features 관련 파일
2. **Figma 데이터** (URL 있을 때): `get_design_context` + `get_screenshot`
3. **Screen Spec** (있을 때): `docs/screens/{domain}/{screen}.md`
4. **i18n 파일**: `en/{domain}.json` + `ko/{domain}.json`

### Step 2 – 시각적 일치 검증 (Figma 있을 때)

| 검증 항목 | 심각도 |
|-----------|--------|
| 레이아웃 구조 (flex, 영역 배치) | Critical |
| 간격 (gap, padding → TDS 토큰) | Critical |
| 색상 (시맨틱 토큰 매핑) | Critical |
| 타이포그래피 (폰트 크기, 굵기) | Major |
| 컴포넌트 매핑 (Figma → TDS) | Critical |
| 아이콘 | Major |

### Step 3 – 기능 커버리지 검증 (Screen Spec 있을 때)

- **인터랙션 정의**: 모든 트리거/동작/결과가 구현됨
- **상태별 화면**: 로딩/빈 상태/에러/정상 모두 처리됨
- **API 연동**: 모든 엔드포인트가 Adapter에 정의, Query/Mutation 훅 연결됨

### Step 4 – 품질 표준 검증

**항상 수행** (Figma/Spec 없어도):

- **TDS 컴포넌트**: 동등한 TDS 컴포넌트가 있는데 직접 구현 → Critical
- **스타일링**: Tailwind 기본 색상(`bg-blue-500`), 하드코딩 hex, opacity modifier → Critical
- **i18n**: 하드코딩 텍스트 → Critical, en/ko 불일치 → Critical
- **FSD 아키텍처**: 역방향 의존/형제 import → Critical
- **TypeScript**: `npx tsc --noEmit` 에러 0
- **코드 컨벤션**: `any` 타입 → Critical, `!!` 사용 → Major

### Step 5 – 리포트 생성

```markdown
## Design Review Report

### Summary
- Critical: {N}건
- Major: {N}건
- Minor: {N}건
- **판정**: PASS / FAIL (Critical 0건이면 PASS)

### Critical Issues
1. **[카테고리] 이슈 제목**
   - 위치: `src/pages/workload/WorkloadsPage.tsx:42`
   - 현재: {현재 코드/상태}
   - 기대: {기대하는 코드/상태}
   - 수정 제안: {구체적 수정 방법}

### Passed Checks
- TDS 컴포넌트 우선 사용 ✅
- 시맨틱 컬러 사용 ✅
- i18n 처리 완료 ✅
```

---

## 자동 수정 모드

사용자가 "수정해줘"라고 요청하면:
1. Critical 이슈부터 순서대로 수정
2. 수정 후 해당 항목 재검증
3. 최종 TypeScript 검증 실행

---

## Cross-reference

| 상황 | 연결 Skill / Rule |
|------|-------------------|
| implement-screen 완료 후 | `implement-screen` → Phase 5에서 이 Skill 호출 |
| Figma 데이터 수집 | `figma-to-tds` → Step 1 MCP 호출 패턴 동일 |
| TDS Props 검증 | `03-tds-essentials.mdc`(자동) + `04-tds-detail-catalog.mdc` Rule |
| FSD 구조 검증 | `fsd-development` Skill |
| i18n 검증 | Rule: `06-i18n-rules.mdc` |

## Checklist

- [ ] 구현 파일 전체 읽기 완료
- [ ] 시각적 일치 검증 (Figma 있을 때)
- [ ] 기능 커버리지 검증 (Spec 있을 때)
- [ ] TDS/스타일링/i18n/FSD/TypeScript 검증
- [ ] 리포트 출력 완료

## Examples

### Example 1: Figma + Spec 기반 풀 리뷰
User says: "workloads 목록 화면 디자인 리뷰 해줘. Figma: https://figma.com/design/abc/..."
Actions:
1. 구현 코드(pages/widgets) + Figma 데이터 + Screen Spec + i18n 파일 병렬 수집
2. 시각적 일치 검증 (레이아웃, 색상, 컴포넌트 매핑)
3. 기능 커버리지 검증 (인터랙션, 상태별 화면, API)
4. 품질 표준 검증 (TDS, 스타일링, i18n, FSD)
5. Design Review Report 출력
Result: Critical/Major/Minor 이슈가 분류된 리포트 + PASS/FAIL 판정

### Example 2: 코드 품질만 검증
User says: "template 페이지 구현 검증해줘"
Actions:
1. 구현 코드 + i18n 파일 수집 (Figma/Spec 없이)
2. 품질 표준 검증만 수행 (TDS, 스타일링, i18n, FSD, TypeScript)
3. 리포트 출력
Result: 코드 품질 중심의 검증 리포트

## Troubleshooting

### 리포트가 너무 길어 핵심이 묻힘
Cause: Minor 이슈가 과도하게 많이 보고됨
Solution: Summary 섹션의 Critical/Major 수를 먼저 확인. Critical이 0이면 PASS이므로 Minor는 참고용

### Figma 스크린샷과 실제 구현 비교가 어려움
Cause: Figma MCP 응답이 truncated되거나 노드가 너무 큼
Solution: get_metadata로 하위 노드 파악 후 섹션별로 나눠 비교. 스크린샷 + design context 병렬 확인
