# Notion 데이터베이스 템플릿 복사 및 동기화

GitHub 프로젝트 데이터를 기존 Notion 데이터베이스 템플릿을 복사하여 새로운 데이터베이스에 동기화하는 스크립트입니다.

## 목적

기존 `create_new_database_sync.py`는 처음부터 새로운 데이터베이스를 생성하는데, 이 방식은 다음과 같은 문제가 있습니다:
- 기존 데이터베이스의 뷰(View) 설정이 사라짐
- 탭 구성이 초기화됨
- 커스텀 필터와 정렬 설정을 다시 만들어야 함

이 스크립트는 기존 데이터베이스의 구조(properties)를 복사하여 새 데이터베이스를 생성합니다.

## 주요 기능

- ✅ 템플릿 데이터베이스의 properties 구조 복사
- ✅ Select/Multi-select 옵션 자동 복사
- ✅ Status 필드를 Select로 변환 (Notion API 제약)
- ✅ GitHub 프로젝트 아이템 동기화
- ✅ Sprint 필터링 지원
- ✅ Dry-run 모드로 미리보기

## 설치 및 설정

### 1. 환경 변수 설정

`.env` 파일에 다음 변수를 추가하세요:

```bash
# 필수
NOTION_TOKEN=your_notion_integration_token
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_ORG=ThakiCloud
GITHUB_PROJECT_NUMBER=5

# 선택 (템플릿 데이터베이스 ID)
NOTION_TEMPLATE_DB_ID=2329eddc34e68057a86ed3de6bae90da
```

### 2. 템플릿 데이터베이스 준비

템플릿으로 사용할 Notion 데이터베이스를 준비합니다. 이 데이터베이스의 properties 구조가 새 데이터베이스에 복사됩니다.

기본 템플릿 ID: `2329eddc34e68057a86ed3de6bae90da`

### 3. 부모 페이지 ID 확인

새 데이터베이스를 생성할 Notion 페이지의 ID를 확인합니다:

1. Notion에서 페이지를 열고 URL을 확인
2. URL 형식: `https://www.notion.so/{PAGE_ID}`
3. PAGE_ID를 복사 (하이픈 포함 또는 제외 가능)

## 사용 방법

### 기본 사용법

```bash
python scripts/copy_database_and_sync.py \
  --parent-page-id <PARENT_PAGE_ID> \
  --database-title "내 새로운 데이터베이스"
```

### Sprint 필터링

특정 Sprint의 아이템만 동기화:

```bash
python scripts/copy_database_and_sync.py \
  --parent-page-id <PARENT_PAGE_ID> \
  --sprint-filter "25-10-Sprint4" \
  --database-title "25-10-Sprint4 Snapshot"
```

### Dry-run 모드

실제 생성 없이 미리보기:

```bash
python scripts/copy_database_and_sync.py \
  --parent-page-id <PARENT_PAGE_ID> \
  --dry-run
```

### 커스텀 템플릿 사용

다른 데이터베이스를 템플릿으로 사용:

```bash
python scripts/copy_database_and_sync.py \
  --template-database-id <TEMPLATE_DB_ID> \
  --parent-page-id <PARENT_PAGE_ID>
```

## 명령줄 옵션

| 옵션 | 설명 | 필수 | 기본값 |
|------|------|------|--------|
| `--template-database-id` | 템플릿 데이터베이스 ID | 아니오 | NOTION_TEMPLATE_DB_ID 환경 변수 또는 `2329eddc34e68057a86ed3de6bae90da` |
| `--parent-page-id` | 새 데이터베이스를 생성할 부모 페이지 ID | **예** | - |
| `--database-title` | 새 데이터베이스 제목 | 아니오 | 자동 생성 (timestamp 포함) |
| `--sprint-filter` | Sprint 이름으로 필터링 | 아니오 | 모든 아이템 |
| `--batch-size` | 배치 처리 크기 | 아니오 | 50 |
| `--dry-run` | 실제 생성 없이 미리보기 | 아니오 | False |
| `--quiet` | 에러 메시지만 출력 | 아니오 | False |

## 테스트

테스트 스크립트를 실행하여 설정을 확인할 수 있습니다:

```bash
python scripts/test_copy_database.py
```

테스트 항목:
1. ✅ 템플릿 데이터베이스 properties 읽기
2. ✅ Dry-run 모드로 데이터베이스 복사
3. ✅ Dry-run 모드로 전체 동기화

## 작동 방식

### 1. 템플릿 데이터베이스 구조 읽기

```python
# 템플릿 데이터베이스의 properties 읽기
template_properties = service._get_template_database_properties()

# Properties 종류:
# - title, rich_text, number
# - select, multi_select, status
# - date, people, url
# - checkbox, email, phone_number
```

### 2. 새 데이터베이스 생성

```python
# 템플릿 구조로 새 데이터베이스 생성
new_db_id = notion_service.create_database(
    parent_page_id=parent_page_id,
    title=database_title,
    properties_schema=template_properties
)
```

### 3. GitHub 데이터 동기화

```python
# GitHub 프로젝트 아이템 가져오기
github_items = github_service.get_all_project_items(sprint_filter=sprint_filter)

# 배치 처리로 Notion 페이지 생성
for item in github_items:
    notion_page = notion_service.upsert_github_item(item)
    # GitHub 이슈/PR 본문과 댓글 추가
    await service._add_github_content_to_page(notion_page.id, item)
```

## 제약 사항

### 1. Status 필드 변환

Notion API는 Status 필드 생성을 지원하지 않으므로, Status는 Select 필드로 변환됩니다:
- ✅ 옵션 값은 동일하게 복사됨
- ✅ 색상도 유지됨
- ⚠️  그룹화 기능은 없음 (수동 설정 필요)

### 2. Views 미지원

Notion API는 views(탭, 필터, 정렬) 복사를 지원하지 않습니다:
- ❌ 탭 구성 자동 복사 불가
- ❌ 필터와 정렬 설정 자동 복사 불가
- 💡 **해결 방법**: 데이터베이스 생성 후 Notion UI에서 수동으로 views 설정

### 3. 권한 제한

- Notion Integration이 템플릿 데이터베이스에 접근 권한이 있어야 함
- 부모 페이지에 쓰기 권한이 필요

## 문제 해결

### "Failed to retrieve template database"

**원인**: Notion Integration이 템플릿 데이터베이스에 접근할 수 없음

**해결**:
1. Notion에서 템플릿 데이터베이스 페이지 열기
2. 우측 상단 "..." → "Add connections"
3. 사용 중인 Integration 선택

### "Failed to create database"

**원인**: 부모 페이지에 쓰기 권한이 없음

**해결**:
1. 부모 페이지에서 Integration 연결 확인
2. 페이지 권한 설정 확인

### "Some properties failed to copy"

**원인**: 일부 property 타입이 지원되지 않음

**해결**:
- 로그를 확인하여 어떤 property가 실패했는지 확인
- 필요시 field_mappings.yml 조정

## 출력 예시

### 성공 케이스

```
[INFO] Starting database copy and sync script
[INFO] Template database ID: 2329eddc34e68057a86ed3de6bae90da
[INFO] Parent page ID: abc123def456
[INFO] Database title: GitHub Sync - 25-10-Sprint4 - 20251022120000

[INFO] Step 1: Copying template Notion database...
[INFO] Retrieved template database: 2329eddc34e68057a86ed3de6bae90da
[INFO] Template database properties: 15 properties
[INFO] Successfully copied database: xyz789abc012
[INFO] Copied 15 properties from template

[INFO] Step 2: Syncing GitHub items to new Notion database...
[INFO] Found 23 items in GitHub project
[INFO] Starting GitHub item sync to new database...
[INFO] Processing batch 1/3 (10 items)
[INFO] Created 10/23 pages...
[INFO] Processing batch 2/3 (10 items)
[INFO] Created 20/23 pages...
[INFO] Processing batch 3/3 (3 items)
[INFO] Successfully created 23 pages in new Notion database

[INFO] Database copy and sync completed!
[INFO] Duration: 45.23 seconds
[INFO] Database copied: True
[INFO] New database ID: xyz789abc012
[INFO] GitHub items processed: 23
[INFO] Notion pages created: 23

✅ New database created with ID: xyz789abc012
   View at: https://notion.so/xyz789abc012
```

## 기존 스크립트와 비교

| 기능 | create_new_database_sync.py | copy_database_and_sync.py |
|------|----------------------------|---------------------------|
| 데이터베이스 생성 | ✅ 처음부터 생성 | ✅ 템플릿 복사 |
| Properties 구조 | field_mappings.yml 기반 | 템플릿 데이터베이스 기반 |
| Select 옵션 | 수동 설정 | 자동 복사 |
| Status 필드 | Select로 생성 | Select로 변환 (옵션 복사) |
| Views | ❌ 없음 | ❌ 없음 (수동 설정 필요) |
| 사용 시나리오 | 새로운 구조 테스트 | 기존 구조 재사용 |

## 추천 워크플로우

### Sprint 종료 시 스냅샷 생성

```bash
# 1. 현재 Sprint 데이터 스냅샷
python scripts/copy_database_and_sync.py \
  --parent-page-id <ARCHIVE_PAGE_ID> \
  --sprint-filter "25-10-Sprint4" \
  --database-title "✅ 25-10-Sprint4 - Complete"

# 2. Notion에서 views 수동 설정
# - "In Progress" 뷰
# - "Done" 뷰  
# - "By Priority" 뷰

# 3. 결과 확인 및 공유
```

### 테스트 환경 구축

```bash
# 1. Dry-run으로 미리보기
python scripts/copy_database_and_sync.py \
  --parent-page-id <TEST_PAGE_ID> \
  --dry-run

# 2. 실제 생성
python scripts/copy_database_and_sync.py \
  --parent-page-id <TEST_PAGE_ID> \
  --database-title "Test Environment - $(date +%Y%m%d)"

# 3. 테스트 후 불필요하면 삭제
```

## 참고 자료

- [Notion API - Databases](https://developers.notion.com/reference/database)
- [Notion API - Properties](https://developers.notion.com/reference/property-object)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)

## 라이선스

이 프로젝트의 라이선스를 따릅니다.

## 기여

문제를 발견하거나 개선 사항이 있으면 이슈를 생성해주세요.

