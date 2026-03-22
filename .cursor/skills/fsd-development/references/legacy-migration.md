# 레거시 마이그레이션 워크플로우

## 마이그레이션 체크리스트

```
[ ] 1. 분석: features-legacy/{domain}/ 구조 파악
[ ] 2. Entity 추출: API, 타입, 모델 분리
[ ] 3. Feature 추출: 비즈니스 로직 분리
[ ] 4. Widget 추출: 복합 UI 분리
[ ] 5. Page 생성: 페이지 컴포넌트 분리
[ ] 6. Route 업데이트: 새 경로로 변경
[ ] 7. 레거시 import 제거 확인
[ ] 8. 테스트
```

## Step 1: 레거시 코드 분석

```bash
ls -la src/features-legacy/{domain}/
cat src/features-legacy/{domain}/api/*.ts
cat src/features-legacy/{domain}/components/*.tsx
```

**확인 사항**:

- API 호출 패턴 (axios/httpClient)
- 타입 정의 위치
- 비즈니스 로직 위치
- UI 컴포넌트 구조

## Step 2: Entity 추출

| 레거시 위치       | 새 위치                                 |
| ----------------- | --------------------------------------- |
| `api/*.api.ts`    | `entities/{domain}/infrastructure/api/` |
| `api/*.models.ts` | `entities/{domain}/infrastructure/dto/` |
| 타입 정의         | `entities/{domain}/types/`              |
| 도메인 로직       | `entities/{domain}/core/domain/`        |

## Step 3: Feature 추출

| 레거시 위치        | 새 위치                      |
| ------------------ | ---------------------------- |
| `api/*.queries.ts` | `features/{domain}/hooks/`   |
| 비즈니스 로직      | `features/{domain}/service/` |
| 유틸 함수          | `features/{domain}/helper/`  |

## Step 4: Widget 추출

복합 UI 컴포넌트를 widgets/로 이동:

- 여러 컴포넌트 조합
- 레이아웃 관련 복합체
- 재사용 가능한 UI 블록

## Step 5: Route 업데이트

```typescript
// 변경 전 (레거시 참조)
component: lazy(() => import('@/features-legacy/{domain}').then(...))

// 변경 후 (새 구조 참조)
component: lazy(() => import('@/pages/{domain}').then(...))
```
