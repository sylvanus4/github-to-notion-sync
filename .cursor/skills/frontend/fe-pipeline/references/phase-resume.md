# Phase Resume 규칙

Phase 0에서 기존 산출물을 스캔하여 이미 완료된 Phase를 자동 스킵하는 증분 실행 시스템.
Phase 0 완료 후, Phase 0.2(Input Intake)에서 보유 자료를 확인한 뒤, 입력이 부족하면 Phase 0.5(Auto-Discovery)가 실행됨. 상세: [auto-discovery.md](auto-discovery.md)

## 산출물 경로 규약

모든 경로는 `ai-platform/frontend/` 기준 상대 경로.

| Phase | 산출물 경로 | 검증 방법 |
|-------|-----------|----------|
| 1 – API Spec | `docs/api/{domain}/{domain}-api-spec.md` | 파일 존재 |
| 2 – Screen Spec | `docs/screens/{domain}/*.md` | 폴더 내 .md 1개 이상 |
| 3 – Figma 분석 | 메모리 (산출물 없음) | **스킵 불가** |
| 4 – Entity | `src/entities/{domain}/infrastructure/` | 폴더 존재 |
| 5 – Page 코드 | `src/pages/{domain}/*Page.tsx` | *Page.tsx 1개 이상 |
| 6 – i18n | `src/shared/libs/i18n/locales/en/{domain}.json` + `ko/{domain}.json` | 양쪽 모두 존재 |

## 스킵 판단 의사코드

```
function determinePhases(domain, swaggerUrl, figmaUrl, description):
  basePath = "ai-platform/frontend"
  phases = []

  # Phase 1 – API Spec
  if swaggerUrl AND NOT exists("{basePath}/docs/api/{domain}/*-api-spec.md"):
    phases.push(1)

  # Phase 2 – Screen Spec
  if NOT exists("{basePath}/docs/screens/{domain}/*.md"):
    phases.push(2)

  # Phase 3 – Figma 분석 (스킵 불가)
  if figmaUrl:
    phases.push(3)
    phases.push(3.5)
  else:
    phases.push(3.5)  # Figma 없어도 유사 컴포넌트 스캔은 실행

  # Phase 4 – Entity
  if swaggerUrl AND NOT exists("{basePath}/src/entities/{domain}/infrastructure/"):
    phases.push(4)

  # Phase 5 – Page
  if NOT exists("{basePath}/src/pages/{domain}/*Page.tsx"):
    phases.push(5)

  # Phase 6 – i18n
  if NOT exists("{basePath}/src/shared/libs/i18n/locales/en/{domain}.json") OR
     NOT exists("{basePath}/src/shared/libs/i18n/locales/ko/{domain}.json"):
    phases.push(6)

  # Phase 7 – tsc 검증 (항상 실행)
  phases.push(7)

  return phases
```

## 사용자 표시 형식

```
Resume 분석 결과:
- Phase 1 (API Spec): SKIP ✅ - docs/api/{domain}/{domain}-api-spec.md 존재
- Phase 2 (Screen Spec): RUN 🔄 - docs/screens/{domain}/ 없음
- Phase 3 (Figma): RUN 🔄 - Figma URL 제공됨
- Phase 3.5 (유사 컴포넌트): RUN 🔄
- Phase 4 (Entity): RUN 🔄 - src/entities/{domain}/ 없음
- Phase 5 (Code): RUN 🔄 - src/pages/{domain}/ 없음
- Phase 6 (i18n): RUN 🔄 - en/{domain}.json 없음
- Phase 7 (tsc): RUN 🔄 - 항상 실행
```

## 입력 분기 결정

| Swagger | Figma | 기획서 | 실행 Phase |
|---------|-------|--------|-----------|
| ✅ | ✅ | ✅ | 0 → (스킵) → 3 → 3.5 → CP1 → 4~7 → CP2 |
| ✅ | ✅ | ❌ | 0 → 1 → 2 → 3 → 3.5 → CP1 → 4~7 → CP2 |
| ✅ | ❌ | ❌ | 0 → 1 → 2 → (Figma 없음: Phase 3 미실행) → 3.5 → CP1 → 4~7 → CP2 |
| ❌ | ✅ | ✅ | 0 → (스킵1) → 3 → 3.5 → CP1 → 5~7 → CP2 |
| ❌ | ❌ | ✅ | 0 → (스킵1,3) → 3.5 → CP1 → 5~7 → CP2 |
| ❌ | ❌ | ❌ | 0 → **0.5(Auto-Discovery)** → CP0.5 → 1(자동) → 2(자동) → 3.5 → CP1 → 4~7 → CP2 |

## 부분 실행 시나리오

### 시나리오 A: 새 대화에서 이어서 진행
이전 대화에서 Phase 4까지 완료 후 컨텍스트 초과.
→ 새 대화에서 동일 입력 제공 → Phase 0이 Phase 1-4 산출물 감지 → Phase 5부터 실행.

### 시나리오 B: Entity만 재생성
Entity 구조를 수정하고 싶을 때.
→ `src/entities/{domain}/` 삭제 후 재실행 → Phase 4만 다시 실행.

### 시나리오 C: Figma 업데이트 후 검증
기존 화면이 모두 구현된 상태에서 Figma만 변경됨.
→ Phase 0이 모든 산출물 존재 확인 → Phase 3(Figma 재분석) + Checkpoint 2(Design Review)만 실행.

### 시나리오 D: API 변경으로 Entity 재생성 필요
Swagger 스키마가 바뀐 경우.
→ `docs/api/{domain}/` + `src/entities/{domain}/` 삭제 → Phase 1, 4 재실행.
