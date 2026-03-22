---
name: fsd-development
description: AI Platform Frontend의 FSD 변형 구조로 새 도메인을 생성하거나 레거시 코드를 마이그레이션합니다. entities, features, pages, widgets 작업 시, 새 도메인 추가 시, features-legacy에서 마이그레이션 시 사용합니다. Do NOT use for Figma 분석(figma-to-tds), 화면 기획서 작성(screen-description), 또는 전체 화면 구현 오케스트레이션(implement-screen).
metadata:
  version: 1.1.0
  category: execution
---

# AI Platform FE - FSD 개발 및 마이그레이션

## 핵심 원칙

**의존성 규칙 (단방향)**:

```
shared → entities → features → widgets → pages → app/routes
```

- 하위 레이어는 상위 레이어 참조 불가
- 같은 레이어 내 형제 import 금지

**Export 규칙**:

```typescript
// ❌ export * 금지!
export * from "./Button";

// ✅ 명시적 named export
export { Button } from "./Button";
export type { ButtonProps } from "./Button";
```

---

## 입력 소스 확인

| 소스 | 참조 방법 | 활용 |
|------|-----------|------|
| **화면 기획서** | `docs/screens/{domain}/{screen}.md` 읽기 | API 엔드포인트, 상태 정의, 컴포넌트 구성 |
| **Figma 분석 결과** | 오케스트레이터 Phase 2 산출물 | TDS 컴포넌트 매핑, 토큰 매핑 |
| **TDS 컴포넌트 API** | `03-tds-essentials.mdc`(자동) + `04-tds-detail-catalog.mdc` Rule | Props, variant, 패턴 |
| **테이블 패턴** | `07-table-patterns.mdc` Rule | 목록 페이지 Config/Widget 구조 |

---

## 새 도메인 생성 워크플로우

### 체크리스트

```
[ ] 1. shared/constants/query-key/{domain}.query-key.ts
[ ] 2. entities/{domain}/ (domain, dto, adapter, mapper, types, schema, index)
[ ] 3. features/{domain}/ (service, hooks, index)
[ ] 4. widgets/{type}/{domain}/ (복합 UI)
[ ] 5. pages/{domain}/ ({Domain}Page.tsx, index)
[ ] 6. app/routes/{domain}.route.ts
[ ] 7. 테스트 및 검증
```

### Step 1: Query Key (`shared/constants/query-key/{domain}.query-key.ts`)

```typescript
export const {domain}QueryKeys = {
  all: () => ['{domain}'] as const,
  lists: () => [...{domain}QueryKeys.all(), 'list'] as const,
  list: (params: Record<string, unknown>) => [...{domain}QueryKeys.lists(), params] as const,
  details: () => [...{domain}QueryKeys.all(), 'detail'] as const,
  detail: (id: string) => [...{domain}QueryKeys.details(), id] as const,
};
```

### Step 2: Entity 생성

Domain, DTO, Model(중첩 구조만), Adapter, Mapper, Types, Schema, Index를 생성합니다. 상세 템플릿은 [references/entity-templates.md](references/entity-templates.md) 참조.

### Step 3: Feature / Widget / Page / Route 생성

Service, Hooks, Widget(Card/Section), Page, Route를 생성합니다. 상세 템플릿은 [references/feature-widget-page-templates.md](references/feature-widget-page-templates.md) 참조.

---

## 레거시 마이그레이션

`features-legacy/{domain}/`에서 FSD 구조로 마이그레이션합니다. 상세 절차는 [references/legacy-migration.md](references/legacy-migration.md) 참조.

---

## 네이밍 규칙 Quick Reference

### 파일명

| 유형 | 패턴 | 예시 |
|------|------|------|
| 도메인 타입 | `{domain}.domain.ts` | `user.domain.ts` |
| DTO | `{domain}.dto.ts` | `user.dto.ts` |
| 어댑터 | `{domain}.adapter.ts` | `user.adapter.ts` |
| 매퍼 | `{domain}.mapper.ts` | `user.mapper.ts` |
| 서비스 | `{domain}.service.ts` | `user.service.ts` |
| 훅 | `use{Action}.ts` | `useLogin.ts` |
| 페이지 | `{Domain}Page.tsx` | `UserPage.tsx` |

### 타입 접미사

| 접미사 | 용도 | 예시 |
|--------|------|------|
| `Entity` | 프론트엔드 도메인 모델 (camelCase) | `UserEntity` |
| `ResponseDto` | 단건 API 응답 (snake_case) | `UserResponseDto` |
| `ApiModel` | 중첩 구조의 하위 타입 (선택적) | `NodeGpuResourceApiModel` |
| `Dto` | API 요청/응답 래퍼 | `EndpointListResponseDto` |
| `Props` | 컴포넌트 Props | `ButtonProps` |

---

## Cross-reference

| 상황 | 연결 Skill / Rule |
|------|-------------------|
| 전체 화면 구현 워크플로우 | `implement-screen` (마스터 오케스트레이터) |
| Figma 기반 구현 | `figma-to-tds` → 토큰/컴포넌트 매핑 결과 참조 |
| 기획서 참조 | `screen-description` → API, 상태, 컴포넌트 정보 확인 |
| TDS 컴포넌트 Props | `03-tds-essentials.mdc`(자동) + `04-tds-detail-catalog.mdc` Rule |
| 모달/드로어 | `overlay-layout-patterns` Skill |
| 폼 검증 (Zod+RHF) | Rule: `05-form-and-mutation.mdc` #2 |
| i18n 처리 | Rule: `06-i18n-rules.mdc` |

## 참고 코드

- **단순 Entity**: `src/entities/user/` — 단건 응답은 DTO에서 직접 정의
- **중첩 Entity**: `src/entities/node/` — 하위 타입이 많아 Model로 분리
- **다중 소스 Entity**: `src/entities/ai-model/` — 3종류 Model → 단일 Entity 매핑

## Examples

### Example 1: 새 도메인 생성
User says: "template 도메인 FSD 구조로 만들어줘"
Actions:
1. `shared/constants/query-key/template.query-key.ts` 생성
2. `entities/template/` 하위 domain, dto, adapter, mapper, types, index 생성
3. `features/template/` 하위 service, hooks 생성
4. `pages/templates/` 페이지 컴포넌트 생성
5. `app/routes/` 라우트 등록
Result: FSD 전 레이어에 걸친 도메인 코드 일체가 생성됨

### Example 2: 레거시 마이그레이션
User says: "features-legacy/workload를 FSD로 마이그레이션해줘"
Actions:
1. 레거시 코드 분석 (API, 타입, 컴포넌트 구조 파악)
2. Entity 추출 (api → adapter, models → dto, 타입 → domain)
3. Feature 추출 (queries → hooks, 로직 → service)
4. Widget/Page 분리 및 Route 업데이트
Result: `features-legacy/workload/` 의존이 0개로 줄고, FSD 구조로 전환됨

## Troubleshooting

### Query Key 하드코딩으로 캐시 무효화 실패
Cause: `queryKey: ["user", "list"]` 같이 문자열을 직접 쓰면 invalidation 범위가 어긋남
Solution: `shared/constants/query-key/` 팩토리 함수 사용. `userQueryKeys.lists()` 형태로 일관된 키 생성

### DTO와 Entity 혼용으로 snake_case 노출
Cause: Adapter 응답(DTO)을 Mapper 없이 컴포넌트에 전달
Solution: 반드시 `{Domain}Mapper.toEntity(dto)`로 변환 후 사용. Entity는 camelCase만 허용
