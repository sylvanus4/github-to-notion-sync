# Entity Scaffold from Swagger

Phase 1에서 추출한 Swagger 스키마를 기반으로 Entity 레이어 전체를 자동 생성하는 규칙.
기반 템플릿: `fsd-development` → `references/entity-templates.md`

---

## 1. Swagger JSON 파싱

### 1.1 스키마 추출

Swagger v2/v3에 따라 스키마 위치가 다름:

| 버전 | 스키마 경로 |
|------|-----------|
| OpenAPI 2.0 | `definitions.*` |
| OpenAPI 3.x | `components.schemas.*` |

도메인 관련 스키마 식별 기준:
1. 도메인명이 포함된 스키마 (예: `BenchmarkResponse`, `benchmark_result`)
2. 관련 엔드포인트의 Response/Request body에서 `$ref`로 참조되는 스키마

### 1.2 엔드포인트 추출

`paths` 객체에서 도메인 관련 URL 필터링:

```
필터 규칙:
  path에 /{domain}/ 또는 /{domains}/ 포함
  → 해당 path의 모든 method (get, post, put, patch, delete) 수집
```

각 엔드포인트에서 추출:
- `path`: URL 패턴 (예: `/api/v1/orgs/{org_id}/projects/{project_id}/benchmarks`)
- `method`: HTTP 메서드
- `summary` / `operationId`: 설명
- `parameters`: path/query 파라미터
- `requestBody`: Request DTO 필드 (POST/PUT/PATCH)
- `responses.200` 또는 `responses.201`: Response DTO 필드

### 1.3 필드 타입 매핑

Swagger 타입 → TypeScript 타입 변환:

| Swagger type | Swagger format | TypeScript |
|-------------|---------------|------------|
| `string` | — | `string` |
| `string` | `date-time` | `number` (Unix timestamp) |
| `string` | `uuid` | `string` |
| `string` | `enum` | union literal |
| `integer` | — | `number` |
| `integer` | `int64` | `number` |
| `number` | `float` / `double` | `number` |
| `boolean` | — | `boolean` |
| `array` | items.$ref | `{Type}[]` |
| `object` | — | `Record<string, unknown>` 또는 별도 타입 |
| `$ref` | — | 참조 타입 추출 |

### 1.4 Nullable / Optional 판단

```
필드가 required 배열에 없음 → optional (?)
필드의 nullable: true 또는 x-nullable: true → T | null
Swagger v2: 필드가 required 배열에 없으면 optional
Swagger v3: 필드가 required 배열에 없거나 nullable: true
```

---

## 2. 코드 생성 규칙

### 2.1 DTO 생성 (`infrastructure/dto/{domain}.dto.ts`)

> 기반: entity-templates.md 1.2절

**Response DTO**:
- Swagger Response 스키마의 필드를 **snake_case 그대로** 유지
- 목록 응답은 `{Domain}ListResponseDto`로 래핑 (items + total + page + page_size)
- 액션 응답(create/delete 결과)이 단건과 다른 구조면 `{Domain}ActionResponseDto` 분리

**Request DTO**:
- POST/PUT의 requestBody 스키마 → `Create{Domain}RequestDto`, `Update{Domain}RequestDto`
- GET의 query 파라미터 → `Get{Domain}ListQueryDto`
- 페이지네이션 공통 필드: `page`, `page_size`, `sort`, `order`

**중첩 구조 판단**:

```
하위 타입이 3개 이상이면:
  → model/ 폴더 분리 (entity-templates.md 1.3절)
  → DTO에서 Model import

하위 타입이 2개 이하면:
  → DTO 파일 내 인라인 정의
```

### 2.2 Domain Entity 생성 (`core/domain/{domain}.domain.ts`)

> 기반: entity-templates.md 1.1절

Response DTO → Domain Entity 변환 규칙:

| DTO 필드 패턴 | Domain 필드 | 타입 변환 |
|--------------|------------|----------|
| `snake_case` | `camelCase` | 동일 |
| `*_at` (number) | `*At` (number) | number 유지 (Mapper에서 Date 변환 처리) |
| `*_id` | `*Id` | string |
| `required` 필드 | 필수 | `T` |
| optional 필드 | 선택 | `T?` |
| nullable 필드 | nullable | `T \| null` |

### 2.3 Mapper 생성 (`mapper/{domain}.mapper.ts`)

> 기반: entity-templates.md 1.5절

자동 생성 메서드:
- `toEntity(dto)` — 단건 DTO → Domain Entity
- `toEntityList(dtos)` — DTO 배열 → Entity 배열
- `toCreateRequest(form)` — 폼 데이터 → Request DTO (폼 스키마 존재 시)

**필드 매핑 자동 생성**:

```
snake_case 필드 → camelCase 매핑 자동 추론:
  dto.created_at → entity.createdAt
  dto.owner_id → entity.ownerId
  dto.gpu_count → entity.gpuCount

*_at 필드 → unixToDate 적용:
  createdAt: dto.created_at (number 그대로 유지, 표시 시 formatDate 사용)
```

### 2.4 Adapter 생성 (`infrastructure/api/{domain}.adapter.ts`)

> 기반: entity-templates.md 1.4절

Swagger 엔드포인트 → Adapter 메서드 매핑:

| Swagger | Adapter 메서드 | 시그니처 |
|---------|---------------|---------|
| `GET /{domains}` | `getList` | `(orgId, projectId, params?) → ListResponseDto` |
| `GET /{domains}/{id}` | `getById` | `(id) → ResponseDto` |
| `POST /{domains}` | `create` | `(data) → ResponseDto \| ActionResponseDto` |
| `PUT /{domains}/{id}` | `update` | `(id, data) → ResponseDto` |
| `PATCH /{domains}/{id}` | `patch` | `(id, data) → ResponseDto` |
| `DELETE /{domains}/{id}` | `delete` | `(id) → void` |
| 커스텀 액션 | `{actionName}` | 상황에 따라 결정 |

**Scope 판단**:

```
URL에 /orgs/{org_id}/projects/{project_id}/ 포함:
  → orgId, projectId를 첫 번째/두 번째 인자로 받음
  → useScope() 훅에서 가져오는 패턴 (features 레이어에서)

URL에 scope 없음:
  → id만 인자로 받음
```

### 2.5 Query Key 생성 (`shared/constants/query-key/{domain}.query-key.ts`)

```typescript
export const {domain}QueryKeys = {
  all: ['{domain}'] as const,
  lists: () => [...{domain}QueryKeys.all, 'list'] as const,
  list: (params?: Record<string, unknown>) =>
    [...{domain}QueryKeys.lists(), params] as const,
  details: () => [...{domain}QueryKeys.all, 'detail'] as const,
  detail: (id: string) => [...{domain}QueryKeys.details(), id] as const,
};
```

### 2.6 Index 파일 생성

각 하위 폴더에 `index.ts` 생성 + Entity 루트 `index.ts` 생성.
entity-templates.md 1.8절 패턴.

---

## 3. 생성 순서

Entity 레이어의 의존성 방향에 따라 순서 고정:

```
1. infrastructure/model/ (중첩 구조일 때만)
2. infrastructure/dto/
3. core/domain/
4. mapper/
5. infrastructure/api/ (adapter)
6. types/ (Enum/상수 타입)
7. core/schema/ (폼 스키마, 필요 시)
8. shared/constants/query-key/
9. 각 폴더 index.ts
10. Entity 루트 index.ts
```

---

## 4. 자동 vs 수동 판단 기준

| 상황 | 판단 |
|------|------|
| Swagger 스키마가 명확하고 필드가 10개 이하 | **자동** — 완전 자동 생성 |
| Swagger 스키마에 $ref 중첩이 3단계 이상 | **반자동** — Model 분리 후 사용자 확인 |
| Swagger에 해당 도메인 스키마 없음 | **수동** — Checkpoint 1에서 사용자에게 알림 |
| API 응답이 프론트엔드 모델과 크게 다름 | **반자동** — DTO만 자동, Domain/Mapper는 사용자 수정 |
| allOf/oneOf/anyOf 복합 스키마 | **반자동** — 가장 유력한 해석으로 생성 + 사용자 확인 |

---

## 5. Checkpoint 1 미리보기 형식

Phase 4 실행 전, Checkpoint 1에서 Entity 미리보기를 표시:

```
Entity 생성 미리보기 (benchmark):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
entities/benchmark/
├── infrastructure/
│   ├── dto/benchmark.dto.ts
│   │   ├── BenchmarkResponseDto (7 fields: id, name, status, ...)
│   │   ├── BenchmarkListResponseDto (items + total + page)
│   │   ├── CreateBenchmarkRequestDto (3 fields: name, config, ...)
│   │   └── GetBenchmarkListQueryDto (page, page_size, sort, order, status)
│   └── api/benchmark.adapter.ts
│       ├── getList(orgId, projectId, params?)
│       ├── getById(id)
│       ├── create(data)
│       └── delete(id)
├── core/domain/benchmark.domain.ts
│   └── BenchmarkEntity (7 fields: id, name, status, ownerId, ...)
├── mapper/benchmark.mapper.ts
│   ├── toEntity (7 field mappings)
│   └── toEntityList
└── index.ts

Query Key: shared/constants/query-key/benchmark.query-key.ts
```
