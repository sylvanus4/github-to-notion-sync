# Auto-Discovery 상세 규칙

Phase 0.5에서 실행되는 자동 발견 로직. 입력이 부족할 때 프로젝트 내부에서 소스를 찾아 후속 Phase에 전달.

---

## 1. 도메인 해석

### 1.1 자연어 → 영문 도메인명

1. 사용자 입력에서 도메인 키워드 추출
2. `src/entities/` 디렉토리 스캔 → 기존 도메인 목록 구성
3. 매칭 규칙:
   - 정확한 영문 일치: `"benchmark"` → `benchmark`
   - 한글 → 영문 추론: `"벤치마크"` → `benchmark`, `"워크로드"` → `workload`
   - 복수형 처리: `"templates"` → `template`
4. 매칭 실패 시 사용자에게 확인: `"영문 도메인명을 {추론값}으로 하면 될까요?"`

### 1.2 신규 vs 기존 도메인

| 상황 | 판단 | 동작 |
|------|------|------|
| `src/entities/{domain}/` 존재 | 기존 도메인 | Phase 4 스킵 가능 |
| 존재하지 않음 | 신규 도메인 | Phase 4 필수 실행 |

---

## 2. API 자동 발견

### 2.1 탐색 체인

Swagger URL 미제공 시 순서대로 시도:

```
Step 1: curl -s http://localhost:3000/swagger/doc.json
  → HTTP 200: 라이브 스웨거 사용
  → 실패: Step 2로

Step 2: 정적 파일 읽기
  경로: ai-platform/backend/go/docs/swagger/swagger.json
  → 파일 존재: 정적 스웨거 사용 (수정일 기록)
  → 파일 없음: Step 3으로

Step 3: API 없이 진행
  → Phase 1, 4 스킵
  → Checkpoint 0.5에서 알림
```

### 2.2 도메인 필터링

발견된 Swagger JSON에서 도메인 관련 엔드포인트만 추출:

```
필터 규칙:
  paths에서 /{domain}/ 또는 /{domains}/ 포함하는 경로
  definitions 또는 components.schemas에서 {Domain} 포함하는 스키마
```

### 2.3 신뢰도 표시

| 소스 | 신뢰도 | Checkpoint 표시 |
|------|--------|----------------|
| 라이브 서버 (localhost) | 높음 | `✅ 라이브 서버에서 확인` |
| 정적 swagger.json (7일 이내) | 보통 | `⚠️ 정적 파일 (수정일: YYYY-MM-DD)` |
| 정적 swagger.json (7일 초과) | 낮음 | `⚠️ 오래된 정적 파일 — make swagger-gen 권장` |

---

## 3. 화면 유형 추론

### 3.1 키워드 → 화면 유형

| 키워드 (한/영) | 화면 유형 | 생성 페이지 |
|---------------|----------|-----------|
| 목록, 리스트, list, 테이블, table | List | `{Domain}ListPage` |
| 상세, 디테일, detail, 조회 | Detail | `{Domain}DetailPage` |
| 생성, 만들기, create, 새로 | Create | `{Domain}CreatePage` |
| 수정, 편집, edit, update | Edit | `{Domain}EditPage` |
| 대시보드, dashboard, 통계, 모니터링 | Dashboard | `{Domain}DashboardPage` |
| 키워드 없음 | CRUD 세트 | List + Detail + Create |

### 3.2 유사 화면 탐색

추론된 화면 유형과 매칭되는 기존 화면을 참조 템플릿으로 사용:

```
탐색 순서:
1. docs/screens/ 에서 같은 유형의 기획서 (예: *-list.md)
2. src/pages/ 에서 같은 유형의 페이지 컴포넌트
3. src/widgets/ 에서 같은 유형의 위젯

우선순위: API 구조가 유사한 도메인 > 화면 유형만 같은 도메인
```

### 3.3 화면 유형별 기본 TDS 구성

| 유형 | 기본 레이아웃 |
|------|-------------|
| List | ActionBar + FilterSearchInput + SelectableTable + Pagination |
| Detail | DetailPageHeader + DetailCard + Tabs |
| Create | CreateLayout + Fieldset + FormField |
| Edit | CreateLayout (기존값 채움) + Fieldset + FormField |
| Dashboard | Layout.Grid + FloatingCard + 차트 영역 |

---

## 4. Figma 대체 전략

Figma URL 없을 때 Phase 3를 스킵하되, Phase 5에 레이아웃 가이드를 전달.

### 4.1 레이아웃 레퍼런스 구성

유사 화면의 Page 컴포넌트를 읽어서:
1. import된 위젯/컴포넌트 목록 추출
2. JSX 구조(레이아웃 계층) 추출
3. 사용된 TDS 컴포넌트 패턴 추출
→ 레이아웃 레퍼런스로 Phase 5에 전달

### 4.2 Checkpoint 1 표시 차이

| Figma 있을 때 | Figma 없을 때 |
|-------------|-------------|
| TDS Component Map (Figma 매칭) | 레이아웃 레퍼런스 (유사 화면 기반) |
| TDS Token Map (색상/간격) | TDS 기본 토큰 사용 |
| Checkpoint 2에서 스크린샷 비교 가능 | 스크린샷 비교 불가 |

---

## 5. Checkpoint 0.5 표시 형식

```
━━━ Discovery Review ━━━

🔍 도메인: benchmark (entities/benchmark/ 기존 도메인)

📡 API 발견 ({소스}, {수정일})
  GET    /api/v1/.../benchmarks         → 목록 조회
  GET    /api/v1/.../benchmarks/:id     → 상세 조회
  POST   /api/v1/.../benchmarks         → 생성
  DELETE /api/v1/.../benchmarks/:id     → 삭제
  POST   /api/v1/.../benchmarks/:id/run → 실행 (커스텀)

📄 화면 유형
  - BenchmarkListPage (목록)
  - BenchmarkDetailPage (상세)
  - BenchmarkCreatePage (생성)

📐 유사 화면 참조
  - workloads (API 구조 유사도 높음)
  - docs/screens/workloads/workloads-list.md → 목록 기획서 참조
  - src/pages/workload/WorkloadListPage.tsx → 목록 코드 참조

🎨 Figma: 없음 → workloads 레이아웃 패턴 참조

선택: [진행] [Swagger URL 직접 제공] [화면 구성 수정] [Figma URL 추가]
```

---

## 6. 입력 조합별 Phase 분기

Phase 0.2(Input Intake)에서 확인된 보유 자료에 따라 분기.
최초 메시지에 URL/경로가 하나라도 포함되어 있으면 Intake 스킵 (첫 행만 Intake 실행).

| Swagger | 기획서(경로) | Figma | Intake | 실행 Phase |
|---------|-------------|-------|--------|-----------|
| ❌ | ❌ | ❌ | 필요 | 0 → 0.2 → 0.5(전체 발견) → CP0.5 → 1(자동) → 2(자동) → 3.5 → CP1 → 4~7 → CP2 |
| ✅ | ❌ | ❌ | 스킵 | 0 → 0.5(도메인·화면만) → 1 → 2(자동) → 3.5 → CP1 → 4~7 → CP2 |
| ✅ | ✅ | ❌ | 스킵 | 0 → 1 → 3.5 → CP1 → 4~7 → CP2 |
| ✅ | ✅ | ✅ | 스킵 | 0 → 1 → 3 → 3.5 → CP1 → 4~7 → CP2 |
| ❌ | ✅ | ✅ | 스킵 | 0 → 0.5(API 발견) → CP0.5 → 1(자동) → 3 → 3.5 → CP1 → 4~7 → CP2 |
| ❌ | ❌ | ✅ | 스킵 | 0 → 0.5(API 발견) → CP0.5 → 1(자동) → 2(자동) → 3 → 3.5 → CP1 → 4~7 → CP2 |
| ❌ | ✅ | ❌ | 스킵 | 0 → 0.5(API 발견) → CP0.5 → 1(자동) → 3.5 → CP1 → 4~7 → CP2 |
