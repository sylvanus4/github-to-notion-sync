# Create New Database Sync Script

GitHub 프로젝트 데이터를 지정된 Notion 페이지 하위에 **새로운 데이터베이스를 생성**하여 동기화하는 스크립트입니다.

## 📖 개요

`create_new_database_sync.py`는 `complete_resync.py`를 기반으로 하지만, 기존 데이터베이스를 수정하는 대신 **새로운 데이터베이스를 생성**합니다. 이는 다음과 같은 경우에 유용합니다:

- 🧪 테스트용 데이터베이스를 별도로 생성하고 싶을 때
- 💾 기존 데이터를 유지하면서 백업용 데이터베이스를 만들고 싶을 때
- 📊 여러 버전의 프로젝트 스냅샷을 관리하고 싶을 때
- 🔄 다른 워크스페이스나 페이지에 동일한 구조의 데이터베이스를 생성하고 싶을 때

## 🚀 주요 기능

### 1. 새 데이터베이스 자동 생성
- 지정된 Notion 페이지 하위에 새 데이터베이스 생성
- `field_mappings.yml` 설정 기반 properties schema 자동 구성
- Title, Status, Priority, 담당자 등 모든 필드 자동 생성

### 2. GitHub 프로젝트 동기화
- GitHub Projects v2의 모든 아이템을 새 데이터베이스로 동기화
- 이슈, PR, Draft Issue 모두 지원
- 본문 내용 및 댓글까지 포함

### 3. 유연한 필터링
- Sprint 기준 필터링 지원
- Batch 처리로 대용량 데이터 안정적 처리

### 4. 안전한 실행
- Dry-run 모드로 사전 확인 가능
- 상세한 로깅으로 진행 상황 추적

## 📋 사용법

### 기본 사용법

```bash
# 새 데이터베이스 생성 및 동기화
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "GitHub Project Sync"
```

### Dry-run 모드 (권장: 먼저 테스트)

```bash
# 실제 생성 없이 미리보기
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "GitHub Sync Test" \
  --dry-run
```

### Sprint 필터링

```bash
# 특정 스프린트의 아이템만 동기화
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "Sprint 4 Snapshot" \
  --sprint-filter "25-10-Sprint4"
```

### 배치 크기 조정

```bash
# 배치 크기를 조정하여 처리 속도 제어
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "GitHub Project Sync" \
  --batch-size 30
```

### Quiet 모드

```bash
# 에러만 출력
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "GitHub Project Sync" \
  --quiet
```

## 🔧 파라미터 설명

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `--parent-page-id` | ✅ | - | 데이터베이스를 생성할 부모 페이지 ID |
| `--database-title` | ❌ | "GitHub Project Sync" | 새로 생성할 데이터베이스의 제목 |
| `--dry-run` | ❌ | False | 실제 생성 없이 미리보기만 실행 |
| `--batch-size` | ❌ | 50 | 한 번에 처리할 아이템 개수 |
| `--sprint-filter` | ❌ | None | 특정 스프린트만 필터링 (예: "25-10-Sprint4") |
| `--quiet` | ❌ | False | 에러 메시지만 출력 |

## 📝 Notion 페이지 ID 찾기

1. Notion에서 원하는 페이지를 열기
2. 페이지 URL 확인:
   ```
   https://notion.so/2939eddc34e68064b505c66d3c22b27a
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      이 부분이 페이지 ID
   ```
3. 하이픈(-) 있어도 자동으로 제거되므로 그대로 사용 가능

## 💡 사용 예시

### 예시 1: 백업용 데이터베이스 생성

```bash
# 현재 프로젝트 상태를 백업
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "백업 - $(date +%Y%m%d)"
```

### 예시 2: Sprint 별 스냅샷 생성

```bash
# Sprint 4의 모든 아이템을 별도 데이터베이스로 저장
python scripts/create_new_database_sync.py \
  --parent-page-id 2939eddc34e68064b505c66d3c22b27a \
  --database-title "Sprint 4 Archive" \
  --sprint-filter "25-10-Sprint4"
```

### 예시 3: 테스트 환경 구축

```bash
# 1. Dry-run으로 확인
python scripts/create_new_database_sync.py \
  --parent-page-id abc123def456 \
  --database-title "Test DB" \
  --dry-run

# 2. 문제없으면 실제 생성
python scripts/create_new_database_sync.py \
  --parent-page-id abc123def456 \
  --database-title "Test DB"
```

### 예시 4: 여러 워크스페이스에 배포

```bash
# 개발 환경
python scripts/create_new_database_sync.py \
  --parent-page-id dev-page-id \
  --database-title "Dev - GitHub Sync"

# 프로덕션 환경
python scripts/create_new_database_sync.py \
  --parent-page-id prod-page-id \
  --database-title "Prod - GitHub Sync"
```

## ⚙️ 동작 원리

### 1. 데이터베이스 Schema 생성

스크립트는 `config/field_mappings.yml` 파일을 읽어서 자동으로 properties schema를 생성합니다:

```yaml
# field_mappings.yml 예시
github_to_notion:
  title:
    notion_property: "피드백 제목"
    type: "title"
  
  status:
    notion_property: "진행 상태"
    type: "status"
    value_mappings:
      "Todo": "시작 전"
      "In Progress": "진행 중"
      "Done": "완료"
```

### 2. 동기화 프로세스

```
1. 📦 field_mappings.yml 로드
2. 🏗️  Properties schema 자동 생성
3. 🆕 Notion 데이터베이스 생성
4. 📊 GitHub 프로젝트 아이템 조회
5. 🔄 각 아이템을 Notion 페이지로 생성
6. 📝 본문 및 댓글 동기화
7. ✅ 완료 리포트 출력
```

### 3. 출력 예시

```
Starting new database creation and sync...
Step 1: Creating new Notion database...
Successfully created database: a1b2c3d4e5f6...
Database properties: 8 properties

Step 2: Syncing GitHub items to new Notion database...
Found 127 items in GitHub project
Processing batch 1/3 (50 items)
Created 10/127 pages...
Created 20/127 pages...
...
Successfully created 127 pages in new Notion database

New database sync completed!
Duration: 245.67 seconds
Database created: True
New database ID: a1b2c3d4e5f6789012345678901234ab
GitHub items processed: 127
Notion pages created: 127

✅ New database created with ID: a1b2c3d4e5f6789012345678901234ab
   View at: https://notion.so/a1b2c3d4e5f6789012345678901234ab
```

## 🆚 complete_resync.py와의 차이점

| 기능 | complete_resync.py | create_new_database_sync.py |
|-----|-------------------|---------------------------|
| 기존 DB 사용 | ✅ 환경변수의 NOTION_DB_ID 사용 | ❌ 사용 안 함 |
| 새 DB 생성 | ❌ | ✅ 파라미터로 지정한 페이지에 생성 |
| 기존 페이지 삭제 | ✅ 모든 페이지 삭제 후 재생성 | ❌ 기존 DB 건드리지 않음 |
| Page ID 지정 | ❌ | ✅ --parent-page-id로 지정 |
| DB Title 지정 | ❌ 기존 DB 이름 유지 | ✅ --database-title로 지정 |
| 용도 | 기존 DB 완전 초기화 | 새 DB 생성 및 복제 |

## ⚠️ 주의사항

### 1. 필수 환경 변수

스크립트 실행 전 `.env` 파일에 다음 환경 변수가 설정되어 있어야 합니다:

```bash
# Notion API
NOTION_TOKEN=secret_xxxxxxxxxxxx
NOTION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  # 참조용 (실제로는 새 DB 생성)

# GitHub API
GH_TOKEN=ghp_xxxxxxxxxxxx
GH_ORG=ThakiCloud
GH_PROJECT_NUMBER=5

# Webhook (사용 안 하지만 필수)
GH_WEBHOOK_SECRET=your-webhook-secret
```

### 2. 권한 확인

- ✅ Notion Integration이 부모 페이지에 접근 권한이 있어야 합니다
- ✅ Integration이 새 데이터베이스를 생성할 수 있어야 합니다
- ✅ GitHub Token에 프로젝트 읽기 권한이 있어야 합니다

### 3. Rate Limit

- Notion API는 초당 3 requests 제한이 있습니다
- 대량의 아이템 동기화 시 시간이 오래 걸릴 수 있습니다
- `--batch-size`를 조정하여 처리 속도를 제어할 수 있습니다

### 4. 데이터베이스 중복

- 같은 부모 페이지에 여러 번 실행하면 데이터베이스가 중복 생성됩니다
- 실행 전 `--dry-run`으로 미리 확인하는 것을 권장합니다

## 🔍 트러블슈팅

### 문제 1: "Failed to create database" 에러

**원인**: Integration 권한 부족

**해결방법**:
1. Notion에서 부모 페이지 열기
2. 우측 상단 `...` → `Add connections`
3. 사용 중인 Integration 선택

### 문제 2: "No items found in GitHub project"

**원인**: GitHub 프로젝트가 비어있거나 권한 부족

**해결방법**:
1. GitHub 프로젝트에 아이템이 있는지 확인
2. `GH_TOKEN`에 프로젝트 읽기 권한이 있는지 확인
3. `GH_PROJECT_NUMBER`가 올바른지 확인

### 문제 3: Sprint 필터링이 작동하지 않음

**원인**: Sprint 필드 이름 불일치

**해결방법**:
1. GitHub 프로젝트에서 Sprint 필드 이름 확인 (예: "스프린트", "Sprint")
2. 정확한 스프린트 값 사용 (예: "25-10-Sprint4")
3. Dry-run으로 아이템 목록 확인

### 문제 4: 일부 페이지만 생성됨

**원인**: Rate limit 또는 일부 아이템 오류

**해결방법**:
1. 로그에서 실패한 아이템 확인
2. `--batch-size`를 줄여서 재시도 (예: 30 또는 20)
3. Rate limit 대기 후 다시 실행

## 📚 관련 문서

- [complete_resync.py](../scripts/complete_resync.py) - 기존 데이터베이스 재동기화
- [field_mappings.yml](../config/field_mappings.yml) - 필드 매핑 설정
- [Notion API Documentation](https://developers.notion.com/) - Notion API 공식 문서
- [GitHub Projects API](https://docs.github.com/en/graphql/reference/objects#projectv2) - GitHub Projects v2 API

## 🤝 기여

버그 리포트나 기능 제안은 GitHub Issues로 등록해주세요.

## 📄 라이센스

이 프로젝트의 라이센스를 따릅니다.

