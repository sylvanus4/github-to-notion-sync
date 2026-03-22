# Progress Tracking 상세

파이프라인 시작 시 **반드시 `TodoWrite` 도구**로 태스크 목록을 생성하고, 각 Phase 완료 시 상태를 업데이트한다.

---

## New Screen 시작 시

TodoWrite 호출 (`merge: false`):

| id | content | 초기 status |
|----|---------|------------|
| p0 | Phase 0: Resume 판단 | `in_progress` |
| p0.2 | Phase 0.2: Input Intake | `pending` |
| p0.5 | Phase 0.5: Auto-Discovery | `pending` |
| cp0.5 | CP 0.5: Discovery Review | `pending` |
| p1 | Phase 1: API Spec | `pending` |
| p2 | Phase 2: Screen Spec | `pending` |
| p3 | Phase 3: Figma 분석 | `pending` |
| p3.5 | Phase 3.5: 유사 컴포넌트 스캔 | `pending` |
| cp1 | CP 1: Plan Review | `pending` |
| p4 | Phase 4: Entity 생성 | `pending` |
| p5 | Phase 5: Code 생성 | `pending` |
| p6 | Phase 6: i18n | `pending` |
| p7 | Phase 7: TypeScript 검증 | `pending` |
| p7.5 | Phase 7.5: Spec Sync | `pending` |
| cp2 | CP 2: Design Review | `pending` |

## Phase 완료 시

- 현재 Phase → `completed`
- 다음 Phase → `in_progress`
- 스킵된 Phase → `cancelled` (TodoWrite content에 사유 추가)

## Design Update 시작 시

TodoWrite 호출 (`merge: false`):

| id | content | 초기 status |
|----|---------|------------|
| d1 | Spec Check: 기획서 확인 | `in_progress` |
| d1.5 | 기획서 자동 생성 (없을 때만) | `pending` |
| d2 | Figma 재분석: Phase 3 실행 | `pending` |
| d3 | 차이 식별 + 코드 수정 | `pending` |
| d4 | Phase 7: TypeScript 검증 | `pending` |
| d5 | Spec Sync: 기획서 동기화 | `pending` |
| d6 | CP 2: Design Review + Fix Loop | `pending` |

## Modification 시작 시

TodoWrite 호출 (`merge: false`):

| id | content | 초기 status |
|----|---------|------------|
| m1 | Spec Check: 기획서 확인 | `in_progress` |
| m2 | Spec Match: 요청-기획서 관계 판단 | `pending` |
| m3 | Figma Check: 디자인 변경 판단 | `pending` |
| m4 | 수정 실행 | `pending` |
| m5 | Spec Sync: 기획서 동기화 | `pending` |
