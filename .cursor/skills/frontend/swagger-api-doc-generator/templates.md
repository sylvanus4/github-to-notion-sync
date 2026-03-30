# API Documentation Templates

## 문서 헤더 템플릿

```markdown
# {API Name} API Specification

> **Source**: `{swagger_url}`
>
> 이 문서는 Swagger JSON 스키마를 기반으로 작성되었습니다.

## 인증

모든 API는 Bearer Token 인증이 필요합니다.

\`\`\`
Authorization: Bearer {access_token}
\`\`\`

---
```

## API 개요 템플릿

```markdown
## API 구조 개요

{API Name} API는 다음 Base URL을 사용합니다:

| 구분        | Base URL          | 설명           |
| ----------- | ----------------- | -------------- |
| **{Type1}** | `/api/v1/{path1}` | {Description1} |
| **{Type2}** | `/api/v1/{path2}` | {Description2} |

---
```

## Endpoints 목록 템플릿

```markdown
## 전체 Endpoints 목록 ({N}개)

### {Category} API ({M}개)

| Method | Endpoint       | Description |
| ------ | -------------- | ----------- |
| GET    | `/{path}`      | {summary}   |
| POST   | `/{path}`      | {summary}   |
| PATCH  | `/{path}/{id}` | {summary}   |
| DELETE | `/{path}/{id}` | {summary}   |

---
```

## API 상세 템플릿

### GET (목록 조회)

```markdown
## {N}. {API 이름}

### Request

\`\`\`
GET /api/v1/{path}
\`\`\`

### Path Parameters

| Parameter | Type   | Required | Description   |
| --------- | ------ | -------- | ------------- |
| {param}   | string | ✅       | {description} |

### Query Parameters

| Parameter  | Type    | Required | Description                   |
| ---------- | ------- | -------- | ----------------------------- |
| q          | string  | ❌       | 검색 키워드                   |
| page       | integer | ❌       | 페이지 번호 (기본값: 1)       |
| page_size  | integer | ❌       | 페이지당 항목 수 (기본값: 10) |
| sort_by    | string  | ❌       | 정렬 기준                     |
| sort_order | string  | ❌       | 정렬 순서 (`asc`, `desc`)     |

### Response

\`\`\`typescript
{
"data": {ItemDTO}[],
"pagination": PaginationDTO
}
\`\`\`

---
```

### POST (생성)

```markdown
## {N}. {API 이름}

### Request

\`\`\`
POST /api/v1/{path}
\`\`\`

### Request Body: `{CreateRequest}`

| Field       | Type   | Required | Description |
| ----------- | ------ | -------- | ----------- |
| name        | string | ✅       | 이름        |
| description | string | ❌       | 설명        |

### Response: `{CreateResponse}`

\`\`\`typescript
{
"data": {ItemDTO},
"meta": {}
}
\`\`\`

---
```

### PATCH (수정)

```markdown
## {N}. {API 이름}

### Request

\`\`\`
PATCH /api/v1/{path}/{id}
\`\`\`

### Request Body: `{UpdateRequest}`

| Field       | Type   | Required | Description      |
| ----------- | ------ | -------- | ---------------- |
| name        | string | ❌       | 이름             |
| description | string | ❌       | 설명 (`""`=null) |

### Response: `{UpdateResponse}`

\`\`\`typescript
{
"data": {ItemDTO},
"meta": {}
}
\`\`\`

---
```

### DELETE (삭제)

```markdown
## {N}. {API 이름}

### Request

\`\`\`
DELETE /api/v1/{path}/{id}
\`\`\`

### Response

\`\`\`
HTTP 200 OK (성공)
HTTP 404 Not Found (리소스 없음)
\`\`\`

---
```

## Schema 템플릿

```markdown
### Response Schema: `{SchemaName}`

| Field      | Type    | Description                | Example          |
| ---------- | ------- | -------------------------- | ---------------- |
| id         | string  | 고유 ID                    | `"550e8400-..."` |
| name       | string  | 이름                       | `"My Item"`      |
| created_at | integer | 생성 시간 (Unix timestamp) | `1640995200`     |
| updated_at | integer | 수정 시간 (Unix timestamp) | `1640995200`     |

---
```

## 에러 응답 템플릿

```markdown
# 에러 응답

## HTTP Status Codes

| Status Code | Description                    |
| ----------- | ------------------------------ |
| 200         | 성공                           |
| 201         | 생성 성공                      |
| 400         | 잘못된 요청 (유효성 검사 실패) |
| 401         | 인증 실패                      |
| 403         | 권한 없음                      |
| 404         | 리소스를 찾을 수 없음          |
| 409         | 충돌 (중복 등)                 |
| 500         | 서버 내부 오류                 |

## Error Response Format

\`\`\`typescript
{
"error": {
"code": string,
"message": string,
"details"?: object
}
}
\`\`\`

---
```

## Enum 정의 템플릿

```markdown
# Appendix: Type Definitions

## Enum Values

### {enum_name}

\`\`\`typescript
type {EnumName} = "{value1}" | "{value2}" | "{value3}";
\`\`\`

---
```

## Pagination 템플릿

```markdown
### PaginationDTO

| Field       | Type    | Description           |
| ----------- | ------- | --------------------- |
| page        | integer | 현재 페이지           |
| page_size   | integer | 페이지당 항목 수      |
| total       | integer | 전체 항목 수          |
| total_pages | integer | 전체 페이지 수        |
| has_next    | boolean | 다음 페이지 존재 여부 |
| has_prev    | boolean | 이전 페이지 존재 여부 |

---
```

## 문서 푸터 템플릿

```markdown
---

**문서 생성일**: {YYYY-MM-DD}
**Swagger Source**: `{swagger_url}`
```
