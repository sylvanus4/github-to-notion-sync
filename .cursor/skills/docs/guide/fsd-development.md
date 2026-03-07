## 개요

FSD(Feature-Sliced Design) 변형 구조로 새 도메인을 생성하거나 레거시 코드를 마이그레이션하는 스킬이다. "새 도메인 추가해줘"라고 요청하면 에이전트가 Entity부터 Route까지 필요한 파일을 일괄 생성한다.

> 트리거 키워드: entities, features, pages, widgets, 새 도메인 추가, features-legacy 마이그레이션

## 사전 조건

- `ai-platform/frontend/src/` 디렉토리 구조가 FSD 레이어를 따르고 있어야 한다
- 기존 도메인 참고 코드: `src/entities/user/` (단순 구조), `src/entities/node/` (중첩 구조)

## 절차

### 1. 새 도메인 생성

새로운 API 리소스에 대한 프론트엔드 코드가 필요할 때 요청한다.

```
"volume 도메인 추가해줘"
"endpoint entity 만들어줘"
"inference 도메인 Entity부터 Page까지 생성해줘"
```

에이전트가 생성하는 파일 (volume 도메인 예시):
- `entities/volume/` — 도메인 타입, DTO, 어댑터, 매퍼
- `features/volume/` — 서비스, React Query 훅
- `widgets/card/volume/` — 카드 위젯 (필요시)
- `pages/volume/` — 페이지 컴포넌트
- `app/routes/volume/` — 라우트 설정

### 2. 특정 레이어만 생성

전체가 아닌 특정 레이어만 필요할 때도 요청할 수 있다.

```
"volume entity만 만들어줘"
"inference feature 훅 추가해줘"
"model 도메인 widget section 만들어줘"
```

### 3. 레거시 마이그레이션

`features-legacy/` 에 있는 코드를 새 FSD 구조로 옮길 때 요청한다.

```
"features-legacy/storage를 FSD로 마이그레이션해줘"
"storage 레거시 코드 새 구조로 옮겨줘"
```

에이전트가 수행하는 작업:
- 레거시 디렉토리 구조 분석
- `api/*.api.ts` → `entities/{domain}/infrastructure/api/`
- `api/*.models.ts` → `entities/{domain}/infrastructure/dto/`
- `api/*.queries.ts` → `features/{domain}/hooks/`
- 복합 UI → `widgets/{type}/{domain}/`
- 기존 import 경로를 새 경로로 업데이트

### 4. API 연동 추가

기존 도메인에 새 API 엔드포인트를 추가할 때 요청한다.

```
"volume entity에 resize API 추가해줘"
"endpoint 도메인에 로그 조회 훅 만들어줘"
```

## 검증

- 에이전트가 생성한 파일들의 import 경로가 정상인지 확인
- `shared → entities → features → widgets → pages` 의존성 방향이 지켜졌는지 확인
- `index.ts`에서 `export *` 대신 명시적 named export를 사용했는지 확인

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| 순환 참조 에러 | 레이어 의존성 규칙 위반 | 하위 레이어에서 상위 레이어 import가 없는지 확인 |
| Query Key 충돌 | 하드코딩된 Query Key | `shared/constants/query-key/` 팩토리 함수 사용 요청 |
| snake_case가 UI에 노출 | 매퍼 누락 | "매퍼 추가해줘" 요청, DTO → Entity 변환 확인 |
| 레거시 import 남아있음 | 마이그레이션 불완전 | "레거시 import 정리해줘" 요청 |
