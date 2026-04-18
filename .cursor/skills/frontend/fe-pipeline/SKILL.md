---
name: fe-pipeline
description: "자연어 한 줄부터 Swagger+Figma 풀세트까지, 프로젝트 내 API·화면 패턴을 자동 발견하여 기획서·Entity·Feature/Widget/Page·i18n·검증을 체크포인트 기반으로 자동 진행합니다. 새 화면 생성뿐 아니라 기존 화면 수정/버그픽스도 기획서 대조 기반으로 처리합니다. Use when 화면 구현해줘, 페이지 만들어줘, 화면 개발, 새 화면 추가, 기존 화면 수정, 버그 수정, UI 변경 요청 시. Do NOT use for 개별 스킬 단독 작업 — API 문서만(swagger-api-doc-generator), 기획서만(screen-description), Figma 분석만(figma-to-tds), 디자인 리뷰만(design-review), Entity만(fsd-development)."
metadata:
  version: "2.0.0"
  category: orchestrator
---

# Frontend Pipeline

자연어 한 줄 → 요청 분류 → 기획서 대조 → 자동 발견 → Entity → Code → i18n → 검증. 체크포인트 기반 자동 진행.

## Inputs

| 입력                          | 필수     | 비고                                           |
| ----------------------------- | -------- | ---------------------------------------------- |
| **도메인명 또는 자연어 설명** | **필수** | `"벤치마크 목록 화면 만들어줘"` 한 줄이면 충분 |
| Swagger URL                   | 선택     | 없으면 프로젝트 내 swagger.json 자동 탐색      |
| Figma URL                     | 선택     | 없으면 기존 유사 화면 패턴으로 대체            |
| 기획서 경로                   | 선택     | 없으면 자동 생성                               |
| `--with-pge`                  | 선택     | PGE 루브릭 평가 활성화 (CP2.5)                 |

## Request Classification (최우선)

**모든 요청은 먼저 유형을 분류**한 뒤, 유형에 맞는 플로우를 따른다.

| 유형              | 판단 기준                                      | 플로우                      |
| ----------------- | ---------------------------------------------- | --------------------------- |
| **New Screen**    | "화면 만들어줘", "페이지 추가", 새 도메인      | Full Pipeline (Phase 0 → 7) |
| **Modification**  | "수정해줘", "버그", "추가해줘", 기존 화면 변경 | Modification Flow           |
| **Design Update** | "Figma 업데이트", "디자인 변경" + Figma URL    | Design Update Flow          |

---

## Design Update Flow (Figma 디자인 업데이트)

Figma 디자인이 변경되었을 때, 기존 코드와 기획서를 새 디자인에 맞게 갱신하는 플로우.

```
1. Spec Check ─── docs/screens/{domain}/ 기획서 존재 확인
   ├─ 기획서 있음 → 읽기 → Step 2로
   └─ 기획서 없음 → 기획서 자동 생성:
       1) 기존 코드(pages/{domain}/, widgets/)에서 구조 파악
       2) screen-description 스킬로 기획서 생성
       3) 사용자 알림: "기획서가 없어서 코드 기반으로 생성했습니다."
2. Figma 재분석 ── Phase 3(figma-to-tds) 실행 → 새 Component/Token Map 생성
3. 차이 식별 ──── 새 Figma 매핑 ↔ 기존 코드 비교 → 변경 필요한 부분 식별
4. 코드 수정 ──── 차이점에 해당하는 코드만 선택적 수정
5. 검증 ──────── Phase 7(TypeScript 검증)
6. Spec Sync ──── 코드 변경 내용을 기획서에 반영 + 변경 이력 기록
7. CP 2 ──────── Design Review (design-review 스킬) → Fix Loop (Critical 자동 수정)
```

### Design Update와 Modification의 차이

| 항목       | Design Update             | Modification        |
| ---------- | ------------------------- | ------------------- |
| 트리거     | Figma URL + "업데이트"    | 텍스트 요청         |
| 기준       | 새 Figma 디자인           | 기획서              |
| 변경 대상  | UI 레이아웃·컴포넌트·토큰 | 로직·데이터·UI 혼합 |
| Figma 분석 | 항상 실행                 | 필요 시만           |

---

## Modification Flow (기존 화면 수정/버그픽스)

기존 화면의 수정·버그 수정·부분 기능 추가 시 이 플로우를 따른다.

```
1. Spec Check ─── docs/screens/{domain}/ 기획서 존재 확인
   ├─ 기획서 있음 → 읽기 → Step 2(Spec Match)로
   └─ 기획서 없음 → 역추론 모드:
       1) 기존 코드(pages/{domain}/, widgets/)에서 구조 파악
       2) 사용자 알림: "기획서가 없습니다. 코드 기반으로 수정 진행할까요?"
       3) 수정 완료 후 → 기획서 자동 생성 (screen-description 스킬)
       4) Spec Sync로 코드↔기획서 일치 확인
2. Spec Match ─── 요청이 기획서와 어떤 관계인지 판단
   ├─ (a) 기획서에 정의된 동작의 구현 누락 (버그)
   │     → 기획서 근거 제시 후 바로 수정
   ├─ (b) 기획서에 없는 새 동작/UI 추가
   │     → 사용자에게 확인: "기획서에 이 동작이 없는데 추가할까요?"
   └─ (c) 기획서 내용과 다른 변경 요청
         → 사용자에게 확인: "기획서에는 A인데 B로 변경할까요?"
3. Figma Check ── 디자인 관련 변경인지 판단 (아래 기준표)
4. 수정 실행
5. Spec Sync ─── 변경 이력 기록 + 기획서 업데이트 (필요 시)
```

### Figma 질문 판단 기준

| 변경 유형                         | Figma 질문 | 이유             |
| --------------------------------- | ---------- | ---------------- |
| 조건 분기 버그 (데이터 미노출 등) | ❌ 불필요  | 디자인 변경 없음 |
| API 연동 오류 / 로직 수정         | ❌ 불필요  | 디자인 변경 없음 |
| i18n 누락 / 번역 수정             | ❌ 불필요  | 디자인 변경 없음 |
| 새 컬럼·필드·섹션 UI 추가         | ✅ 질문    | 레이아웃 영향    |
| 레이아웃·간격·색상 변경           | ✅ 질문    | 디자인 기준 필요 |
| 컴포넌트 교체·추가                | ✅ 질문    | 디자인 기준 필요 |

---

## Core Principle: Spec–Code Sync

> **기획서(`docs/screens/`)는 구현 코드의 진실(Source of Truth)과 항상 일치해야 한다.**

코드가 기획서와 달라지는 **모든 시점**에서 기획서를 자동 업데이트:

- Phase 5 완료 후, Design Update 수정 후, Fix Loop 수정 후, 파이프라인 외 코드 변경 시
- 동기화 범위: 상태별 화면, 인터랙션 정의, 컴포넌트 구성, 레이아웃 구조, 변경 이력

규칙:

1. 기획서에 없는 동작을 코드에 추가 → 기획서에도 즉시 추가
2. 기획서와 코드가 다름 → 기획서를 코드 기준으로 수정
3. 변경 이력 테이블에 날짜와 변경 요약을 항상 기록

---

## Full Pipeline Workflow (New Screen)

```
Phase 0:   Resume 판단 (산출물 스캔 → 스킵 결정)
Phase 0.2: Input Intake (보유 자료 확인 — 사용자에게 질문)
Phase 0.5: Auto-Discovery (API·화면패턴·도메인 자동 발견)
━━━ CHECKPOINT 0.5: Discovery Review ━━━
Phase 1+2: API Spec + Screen Spec ← ⚡ 병렬 가능 (독립적 산출물)
Phase 3:   Figma + TDS 매핑 (figma-to-tds)
Phase 3.5: 유사 컴포넌트 스캔 (Skeleton 포함)
━━━ CHECKPOINT 1: Plan Review ━━━
Phase 4:   Entity 자동 생성 (Swagger → DTO/Adapter/Mapper)
Phase 5:   Code 생성 — Sub-phases:
  5.1: Feature (Service + Query/Mutation 훅)
  5.2: Widget (화면 유형별 — Table/Card/Form/Section)
  5.3: Page (Widget 조합 + 상태 분기)
  5.4: Route 등록
  5.5: Overlay/Drawer (기획서에 모달/드로어 정의 시)
Phase 6:   i18n (Rule: 11-i18n-namespace-pattern.mdc)
Phase 7:   TypeScript 검증
Phase 7.5: Spec Sync (코드 ↔ 기획서 동기화)
━━━ CHECKPOINT 2: Design Review ━━━
Fix Loop:  Critical 자동 수정 → 재검증 → Spec Sync (최대 3회)
━━━ CHECKPOINT 2.5: PGE Evaluation (Optional, --with-pge) ━━━
PGE Loop:  workflow-eval-opt + pge-rubric.yaml 4차원 채점 (최대 2회)
```

### Phase Summary

| Phase                 | Skill                                 | 산출물                   |
| --------------------- | ------------------------------------- | ------------------------ |
| 1 API Spec            | `swagger-api-doc-generator`           | `docs/api/{domain}/`     |
| 2 Screen Spec         | `screen-description`                  | `docs/screens/{domain}/` |
| 3 Figma               | `figma-to-tds`                        | Component/Token Map      |
| 4 Entity              | —                                     | `src/entities/{domain}/` |
| 5 Code                | `fsd-development`                     | features/widgets/pages/  |
| 6 i18n                | Rule: `11-i18n-namespace-pattern.mdc` | en/ko JSON               |
| 7 tsc + 7.5 Spec Sync | —                                     | 검증 + 기획서 동기화     |

Phase별 Fallback 전략과 실패 복구: [error-recovery](references/error-recovery.md) | Phase 5 상세: [code-generation](references/code-generation.md)

### Checkpoints

- **CP 0.5** (Discovery): API/화면/참조 패턴 확인 → 사용자 승인 (Degraded 항목 보고)
- **CP 1** (Plan): TDS 매핑 + 유사 컴포넌트 + Entity 미리보기 + 생성 파일 목록 → 승인
- **CP 2** (Design Review): `design-review` 스킬 → Critical 자동 수정 ([Fix Loop](references/fix-loop.md))
- **CP 2.5** (PGE Evaluation, Optional): `--with-pge` 플래그 시, `workflow-eval-opt` + `pge-rubric.yaml` 기반 4차원 루브릭 채점 → 미달 시 Phase 5 복귀 (최대 2회)

상세: [Phase 0 Resume](references/phase-resume.md) | [Phase 0.2 Input Intake](references/input-intake.md) | [Phase 0.5 Auto-Discovery](references/auto-discovery.md) | [Entity Scaffold](references/entity-scaffold-from-swagger.md) | [Phase 5 Code Generation](references/code-generation.md) | [Error Recovery](references/error-recovery.md)

---

## Examples

### Example 1: 새 화면 (자연어 한 줄)

User says: "벤치마크 화면 만들어줘"
Actions:

1. Classification → **New Screen**
2. Phase 0(Resume) → 0.2(Intake 질문) → 0.5(Discovery) → CP0.5
3. Phase 1-7 → CP2 → Fix Loop
   Result: 전체 파이프라인 완료

### Example 2: 버그 수정 (기획서에 정의된 동작의 구현 누락)

User says: "워크로드 테이블에서 GPU 선택 시 데이터 노출이 CPU와 동일해"
Actions:

1. Classification → **Modification**
2. Spec Check → `workloads-list.md` 읽기 → "GPU 타입 시만 노출" 정의 발견
3. Spec Match → (a) 기획서 정의 대비 구현 누락 버그 → 근거 제시 후 바로 수정
4. Figma Check → 로직 버그 → Figma 질문 **불필요**
5. 수정 실행 → Spec Sync(변경 이력 기록)
   Result: 기획서 근거 제시 + 코드 수정 + 변경 이력

### Example 3: 기획서에 없는 기능 추가

User says: "워크로드 테이블에 GPU 온도 컬럼 추가해줘"
Actions:

1. Classification → **Modification**
2. Spec Check → `workloads-list.md`에 GPU 온도 컬럼 없음
3. Spec Match → (b) 새 동작 → **사용자 확인**: "기획서에 GPU 온도 컬럼이 없습니다. 추가할까요?"
4. Figma Check → UI 추가 → **"Figma URL 있나요?"** 질문
5. 수정 실행 → Spec Sync(기획서에 컬럼 추가 + 변경 이력)
   Result: 확인 후 코드 + 기획서 동시 업데이트

### Example 4: Figma 디자인 업데이트 (기획서 있음)

User says: "template 화면 Figma 업데이트됐어. Figma: https://..."
Actions:

1. Classification → **Design Update**
2. Spec Check → `docs/screens/template/` 존재 → 기획서 읽기
3. Figma 재분석 → 새 Component/Token Map 생성
4. 기존 코드와 비교 → 변경된 컴포넌트·레이아웃·토큰 식별
5. 차이점 코드 수정 → Phase 7(tsc 검증)
6. Spec Sync → 기획서에 변경 내용 반영 + 변경 이력 기록
7. CP 2(Design Review) → Fix Loop
   Result: 변경된 디자인만 선택적 반영 + 기획서 자동 동기화

### Example 5: Figma 디자인 업데이트 (기획서 없음)

User says: "devspace 화면 Figma 업데이트됐어. Figma: https://..."
Actions:

1. Classification → **Design Update**
2. Spec Check → `docs/screens/devspace/` 없음 → 역추론 모드
3. 기존 코드에서 구조 파악 → screen-description 스킬로 기획서 자동 생성
4. 사용자 알림: "기획서가 없어서 코드 기반으로 생성했습니다."
5. Figma 재분석 → 기존 코드 비교 → 차이점 수정
6. Spec Sync → 기획서 업데이트 + 변경 이력
7. CP 2 → Fix Loop
   Result: 기획서 자동 생성 + 디자인 반영 + 기획서 동기화

### Example 6: 최초 메시지에 URL 포함 → Intake 스킵

User says: "benchmark 화면 구현해줘. Swagger: http://... Figma: https://..."
Actions:

1. Classification → **New Screen** → Intake 스킵 (URL 이미 제공)
2. Phase 1-3 → CP1 → Phase 4-7 → CP2
   Result: Figma 픽셀 매칭 + API 연동

---

## Troubleshooting

### 기획서 대조 없이 수정 진행

Cause: Modification Flow의 Spec Check 단계를 건너뜀
Solution: 모든 수정 요청은 반드시 `docs/screens/{domain}/` 확인 후 진행. 기획서 없으면 그 사실을 사용자에게 알림

### Figma 질문을 해야 할 때 안 한 경우

Cause: UI/레이아웃 변경인데 Figma Check 판단 기준표를 적용하지 않음
Solution: 새 UI 요소 추가, 레이아웃 변경, 컴포넌트 교체 시 항상 Figma URL 질문

### swagger.json 자동 발견했지만 오래된 경우

Cause: 정적 swagger.json이 `swag init` 이후 미갱신
Solution: CP 0.5에서 수정일 표시. `make swagger-gen` 실행 후 재시도

### Fix Loop 3회 초과

Cause: 구조적 문제로 자동 수정 불가
Solution: 자동 수정 중단, 남은 이슈 목록과 수동 수정 제안 리포트 전달

### 파이프라인 외 코드 변경 시 기획서 미동기화

Cause: fe-pipeline 밖에서 정책/상태/UI 변경이 발생했으나 기획서 미업데이트
Solution: Spec–Code Sync 원칙 적용. 코드 변경과 동시에 `docs/screens/{domain}/` 업데이트 + 변경 이력 기록
