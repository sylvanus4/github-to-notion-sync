---
name: integration-test-migration
description: Go 백엔드 통합 테스트를 마이그레이션 스키마 기반으로 전환합니다. DDL 안티패턴(DROP TABLE/CREATE TABLE) 제거, fixture INSERT 전환, mock 타입 정합, 상태 전이 정렬을 수행합니다. "통합 테스트 고도화", "DDL 제거", "integration test 마이그레이션 기반 전환", "테스트 스키마 정합성", "테스트 DDL 리팩토링" 요청 시 사용합니다. Do NOT use for 신규 테스트 작성 from scratch, gomock 단위 테스트 수정, 프론트엔드 테스트.
---

# Go 통합 테스트 마이그레이션 스키마 전환

DDL 안티패턴(DROP/CREATE TABLE)을 제거하고, 프로덕션 마이그레이션 스키마에 의존하는 테스트로 전환하는 워크플로우.

## 전제 조건

- 로컬 PostgreSQL에 `ai_platform_db`가 존재하고 `migrate up` 완료 상태
- `TEST_DATABASE_URL` 환경변수로 접속 가능
- NATS가 필요한 테스트의 경우 `TEST_NATS_URL` 확인 (기본 4222 vs 4223 차이 주의)

## 워크플로우

```
진단 → 스키마 비교 → DDL 제거 → Fixture 전환 → Mock 정합 → 상태 전이 정렬 → 테스트 실행 → 검증
```

### Step 1: 진단 — DDL 안티패턴 탐지

대상 테스트 파일에서 DDL 사용 현황을 파악합니다.

```
검색 패턴:
  - DROP TABLE
  - CREATE TABLE
  - CREATE.*IF NOT EXISTS
  - CREATE FUNCTION
  - CREATE TRIGGER
  - CREATE INDEX (마이그레이션에 있어야 할 것)
```

**TodoWrite 체크리스트 생성**:

```
- [ ] DDL 안티패턴 탐지 (대상 파일 목록 확정)
- [ ] 프로덕션 스키마 비교
- [ ] DDL 제거 + INSERT fixture 전환
- [ ] Mock 타입 정합성 확인
- [ ] 상태 전이 정렬
- [ ] 전체 테스트 실행 및 PASS 확인
```

### Step 2: 프로덕션 스키마 비교

테스트 DDL과 마이그레이션 스키마의 **차이**를 확인합니다.

```bash
# 테이블 컬럼 확인
PGPASSWORD=password psql -h localhost -p 5432 -U postgres -d ai_platform_db \
  -c "\d+ {테이블명}"

# 제약조건 확인
PGPASSWORD=password psql -h localhost -p 5432 -U postgres -d ai_platform_db \
  -c "SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = '{테이블명}'::regclass;"

# 트리거 확인
PGPASSWORD=password psql -h localhost -p 5432 -U postgres -d ai_platform_db \
  -c "SELECT tgname, pg_get_triggerdef(oid) FROM pg_trigger WHERE tgrelid = '{테이블명}'::regclass AND NOT tgisinternal;"
```

**반드시 확인할 차이점**:

| 항목 | 흔한 불일치 | 영향 |
|---|---|---|
| 컬럼명 | `type` vs `workload_type` | INSERT 실패 |
| NOT NULL + 기본값 없음 | `organizations.domain`, `projects.owner_id` | INSERT 실패 |
| CHECK 제약조건 | `chk_organizations_domain_format` (`.` 불가), `chk_users_password_length` (60자) | 데이터 거부 |
| FK 체인 | `projects.owner_id → users.id` | FK 위반 |
| 트리거 | `trg_manage_project_k8s_namespace` → `project-{id}` 자동 설정 | 예상과 다른 값 |
| 상태 전이 트리거 | `trg_manage_workload_status` | UPDATE 거부 |

### Step 3: DDL 제거 + INSERT Fixture 전환

**제거 대상** — 다음 코드를 모두 삭제:

```go
// 이 패턴들을 모두 제거
db.Exec("DROP TABLE IF EXISTS ... CASCADE")
db.Exec("CREATE TABLE IF NOT EXISTS ...")
db.Exec("CREATE FUNCTION ...")
db.Exec("CREATE TRIGGER ...")
```

**교체 패턴** — FK 순서대로 INSERT:

```go
func setupTestFixtures(t *testing.T, db *sql.DB) {
    t.Helper()

    // 1. organizations (domain 필수, format: ^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$)
    db.Exec(`INSERT INTO organizations (id, name, domain)
             VALUES ($1, 'Test Org', $2)
             ON CONFLICT (id) DO NOTHING`, testOrgID, "test-org-domain")

    // 2. users (password CHECK: char_length >= 60 — testutil 헬퍼 사용)
    //    import "github.com/ThakiCloud/ai-platform-webui/ai-platform/backend/go/internal/testutil"
    db.Exec(`INSERT INTO users (id, name, username, email, password, organization_id)
             VALUES ($1, 'test-user', 'test-user', 'test@test.local', $2, $3)
             ON CONFLICT (id) DO NOTHING`, testUserID, testutil.TestBcryptHash(t), testOrgID)

    // 3. projects (owner_id FK → users, k8s_namespace는 트리거가 project-{id}로 설정)
    db.Exec(`INSERT INTO projects (id, organization_id, owner_id, name, k8s_namespace)
             VALUES ($1, $2, $3, 'Test Project', $4)
             ON CONFLICT (id) DO NOTHING`,
        testProjectID, testOrgID, testUserID, fmt.Sprintf("project-%s", testProjectID))

    // 4. project_members (AuthorizeProjectAccess가 멤버십 검증)
    db.Exec(`INSERT INTO project_members (project_id, user_id, role)
             VALUES ($1, $2, 'admin')
             ON CONFLICT DO NOTHING`, testProjectID, testUserID)

    // 5. 도메인 테이블 (workloads, devspaces, pipelines 등)
    // ...

    // Cleanup: 역순 삭제
    t.Cleanup(func() {
        db.Exec("DELETE FROM {도메인_테이블} WHERE organization_id = $1", testOrgID)
        db.Exec("DELETE FROM project_members WHERE project_id = $1", testProjectID)
        db.Exec("DELETE FROM projects WHERE organization_id = $1", testOrgID)
        db.Exec("DELETE FROM users WHERE organization_id = $1", testOrgID)
        db.Exec("DELETE FROM organizations WHERE id = $1", testOrgID)
        db.Close()
    })
}
```

### Step 4: Mock Repository 타입 정합성 확인

서비스가 `GetByOrgAndID` 반환값을 `*projectmodel.Project`로 타입 단언하는 패턴이 있음.
테스트용 mock이 `struct{ ID string }` 같은 익명 구조체를 반환하면 타입 단언 실패 → "Project not found".

**확인 방법**:

```
1. 서비스 코드에서 projectVal.(*projectmodel.Project) 패턴 검색
2. 테스트의 mock repository가 해당 타입을 반환하는지 확인
3. 불일치 시 DB 전체 필드를 조회하여 *projectmodel.Project 반환하도록 수정
```

**수정 템플릿**:

```go
func (r *testProjectRepo) GetByOrgAndID(ctx context.Context, orgID, projectID string) (interface{}, error) {
    var p projectmodel.Project
    var desc, groupID sql.NullString
    err := r.db.QueryRowContext(ctx,
        `SELECT id, name, COALESCE(description,''), organization_id, group_id, owner_id,
                project_type, status, k8s_namespace, COALESCE(tier,'xlarge'), created_at, updated_at
         FROM projects WHERE organization_id = $1 AND id = $2`,
        orgID, projectID,
    ).Scan(&p.ID, &p.Name, &desc, &p.OrganizationID, &groupID, &p.OwnerID,
        &p.ProjectType, &p.Status, &p.K8sNamespace, &p.Tier, &p.CreatedAt, &p.UpdatedAt)
    if err == sql.ErrNoRows {
        return nil, nil
    }
    if err != nil {
        return nil, err
    }
    if desc.Valid { p.Description = &desc.String }
    if groupID.Valid { p.GroupID = &groupID.String }
    return &p, nil
}
```

### Step 5: 상태 전이 정렬

DB 트리거가 유효한 상태 전이만 허용하는 경우, 테스트에서 `db.Exec("UPDATE ... SET status = 'running'")` 같은 직접 전환이 거부됨.

**원칙**: 상태를 바꿀 때는 유효한 전이 경로를 밟아야 한다.

```go
// ❌ 불법 전이 — 트리거가 거부
db.Exec("UPDATE workloads SET status = 'running' WHERE id = $1", wlID)

// ✅ 유효 경로를 밟아서 전이
db.Exec("UPDATE workloads SET status = 'starting' WHERE id = $1", wlID)
db.Exec("UPDATE workloads SET status = 'running' WHERE id = $1", wlID)
```

**확인 방법**: `ValidTransition` 함수 또는 DB 트리거 내 allowed_transitions 맵을 확인.

### Step 6: 테스트 실행 및 검증

```bash
cd ai-platform/backend/go

# 단일 도메인 테스트
TEST_DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_platform_db?sslmode=disable" \
TEST_NATS_URL="nats://localhost:4222" \
go test -v -count=1 -timeout=5m -tags=integration ./tests/integration/ -run 'TestIntegration_{Domain}'

# DDL 잔존 확인 (0건이어야 함)
grep -n "DROP TABLE\|CREATE TABLE" tests/integration/{domain}_test.go
```

**완료 기준**:

- [ ] 모든 테스트 PASS
- [ ] `DROP TABLE` / `CREATE TABLE` 0건
- [ ] `ON CONFLICT (id) DO NOTHING` 으로 fixture 삽입
- [ ] `t.Cleanup`으로 데이터 정리
- [ ] mock이 프로덕션 타입 반환

## 공통 함정 체크리스트

| # | 함정 | 증상 | 해결 |
|---|---|---|---|
| 1 | `organizations.domain` CHECK 제약 | `.` 포함 도메인 거부 | `test-org` 형식 사용 |
| 2 | `users.password` 60자 제약 | `'n/a'` 거부 | `testutil.TestBcryptHash(t)` 사용 |
| 3 | `projects.owner_id` FK | users 미삽입 시 FK 위반 | users INSERT 먼저 |
| 4 | `project_members` 누락 | `IsProjectMember` false → 403 | fixture에 추가 |
| 5 | `k8s_namespace` 트리거 | `project-{id}` 자동 설정, 테스트 하드코딩과 불일치 | `fmt.Sprintf("project-%s", projectID)` |
| 6 | NATS 포트 | 기본값 4223 vs 실제 4222 | `TEST_NATS_URL` 명시 |
| 7 | `workload_events.published_at` CHECK | status='published' 시 published_at 필수 | `EXTRACT(EPOCH FROM NOW())::BIGINT` 설정 |
| 8 | 상태 전이 트리거 | 불법 전이 거부 | 유효 경로 순차 UPDATE |
| 9 | migration 133 force | 빈 DB에서 data migration 실패 | `migrate force 133` 후 계속 |

## 관련 규칙

- **제약조건 규칙**: `go-integration-test-guard.mdc` 섹션 8 (DB 스키마: 마이그레이션 기반 필수)
- **안티패턴 금지**: `go-integration-test-guard.mdc` 섹션 9 (DB 스키마 파괴)
- **gomock 품질**: `go-gomock-false-positive-guard.mdc`
