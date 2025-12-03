# Scripts Reference

Daily Sprint Sync 스크립트 CLI 레퍼런스입니다.

---

## 1. 공통 사항

### 1.1 실행 전 환경 설정

```bash
# 프로젝트 루트에서 실행
cd /path/to/github-to-notion-sync

# 환경 변수 설정 (또는 .env 파일 사용)
export GH_TOKEN="your-github-token"
export NOTION_TOKEN="your-notion-token"
export GH_ORG="ThakiCloud"
export GH_PROJECT_NUMBER="5"
export NOTION_DB_ID="your-notion-db-id"
export GH_WEBHOOK_SECRET="dummy-for-local"

# (선택) AI 요약용
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### 1.2 실행 방법

```bash
# PYTHONPATH 설정 필수
PYTHONPATH=. python scripts/<script_name>.py [options]
```

### 1.3 공통 옵션

| 옵션 | 설명 |
|------|------|
| `--team` | 팀 ID (synos, ragos 등) - **NEW!** |
| `--dry-run` | 실제 변경 없이 미리보기 |
| `--quiet` | 에러 외 출력 억제 |
| `--output <file>` | 결과를 JSON 파일로 저장 |

### 1.4 팀 옵션 사용법 - NEW!

모든 스크립트는 `--team` 옵션을 지원합니다:

```bash
# 레거시 모드 (팀 미지정)
PYTHONPATH=. python scripts/daily_scrum_sync.py --sprint "25-12-Sprint1" --notion-parent-id "xxx"

# 멀티 팀 모드 (팀 지정)
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos

# 팀 설정 + 개별 옵션 오버라이드
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --sprint "25-12-Sprint2"
```

**팀 지정 시 자동 로드되는 설정:**
- `github.org`: GitHub Organization
- `github.project_number`: GitHub Project 번호
- `sprint.current`: 현재 스프린트
- `sprint.notion_parent_id`: PR-Checker 페이지 ID
- `sprint.sprint_checker_parent_id`: SprintChecker 페이지 ID
- `sprint.daily_scrum_parent_id`: DailyScrum 페이지 ID

---

## 2. complete_resync.py

GitHub Projects 데이터를 Notion Database로 전체 동기화합니다.

### 2.1 사용법

```bash
PYTHONPATH=. python scripts/complete_resync.py [OPTIONS]
```

### 2.2 옵션

| 옵션 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `--team` | string | - | 팀 ID (NEW!) |
| `--dry-run` | flag | - | 변경 없이 미리보기 |
| `--batch-size` | int | 50 | 배치 크기 |
| `--force` | flag | - | 확인 프롬프트 스킵 |
| `--quiet` | flag | - | 출력 최소화 |
| `--sprint-filter` | string | - | 스프린트 필터 |
| `--database-title` | string | auto | DB 타이틀 |

### 2.3 예시

```bash
# 레거시 모드 - 미리보기 (dry-run)
PYTHONPATH=. python scripts/complete_resync.py --dry-run

# 레거시 모드 - 특정 스프린트만 동기화
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-12-Sprint1" --force

# 멀티 팀 모드 - Synos 팀 (NEW!)
PYTHONPATH=. python scripts/complete_resync.py --team synos --force

# 멀티 팀 모드 - RagOS 팀 dry-run (NEW!)
PYTHONPATH=. python scripts/complete_resync.py --team ragos --dry-run

# 커스텀 DB 타이틀
PYTHONPATH=. python scripts/complete_resync.py --team synos --database-title "My Custom DB" --force

# 작은 배치로 실행
PYTHONPATH=. python scripts/complete_resync.py --team synos --batch-size 20 --force
```

### 2.4 출력 예시

```
Starting complete resync script
Using team configuration: synos
Sprint filter: 25-12-Sprint1
Configuration loaded successfully
Starting complete resynchronization...
Step 0: Updating database title...
Successfully updated database title to: GitHub Sync - 25-12-Sprint1 - 20251202070000
Step 1: Clearing Notion database...
Found 45 pages in Notion database
Successfully deleted 45 pages from Notion database
Step 2: Syncing GitHub items to Notion...
Found 32 items in GitHub project
Processing batch 1/1 (32 items)
Created 32/32 pages...
Complete resynchronization finished!
Duration: 125.43 seconds
GitHub items processed: 32
Notion pages deleted: 45
Notion pages created: 32
```

---

## 3. sprint_pr_review_check.py

스프린트 기간 PR들의 리뷰 상태를 체크합니다.

### 3.1 사용법

```bash
PYTHONPATH=. python scripts/sprint_pr_review_check.py --sprint <SPRINT_NAME> [OPTIONS]
```

### 3.2 옵션

| 옵션 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `--team` | string | - | 팀 ID (NEW!) |
| `--sprint` | string | ✅* | 스프린트 이름 |
| `--notion-parent-id` | string | - | Notion 부모 페이지 ID |
| `--dry-run` | flag | - | 변경 없이 미리보기 |
| `--output` | string | - | 결과 JSON 파일 경로 |
| `--quiet` | flag | - | 출력 최소화 |

> *`--team` 지정 시 `--sprint`는 선택 사항 (팀 설정에서 자동 로드)

### 3.3 예시

```bash
# 레거시 모드 - 미리보기
PYTHONPATH=. python scripts/sprint_pr_review_check.py --sprint "25-12-Sprint1" --dry-run

# 레거시 모드 - Notion에 동기화
PYTHONPATH=. python scripts/sprint_pr_review_check.py \
  --sprint "25-12-Sprint1" \
  --notion-parent-id "2939eddc34e680f58c7ad076e5ba3e88"

# 멀티 팀 모드 - Synos 팀 (NEW!)
PYTHONPATH=. python scripts/sprint_pr_review_check.py --team synos

# 멀티 팀 모드 - dry-run (NEW!)
PYTHONPATH=. python scripts/sprint_pr_review_check.py --team synos --dry-run

# JSON 파일로 저장
PYTHONPATH=. python scripts/sprint_pr_review_check.py \
  --team synos \
  --output pr_review_status.json \
  --dry-run
```

### 3.4 출력 예시

```
Using team configuration: synos
Starting sprint PR review check for: 25-12-Sprint1
Sprint date range: 2025-11-29 to 2025-12-06
Collecting PRs from 2025-11-29 to 2025-12-06
Found 15 PRs in sprint period

============================================================
Sprint: 25-12-Sprint1
Period: 2025-11-29 to 2025-12-06
Total PRs: 15
Reviewed PRs: 12
Not Reviewed PRs: 3
============================================================

PR Review Status (Not Reviewed First):
  ❌ Not Reviewed - ThakiCloud/repo1#123 - Fix bug in login (0 reviews)
  ❌ Not Reviewed - ThakiCloud/repo2#45 - Add new feature (0 reviews)
  ✅ Reviewed - ThakiCloud/repo1#120 - Refactor code (2 reviews)
  ...
```

---

## 4. sprint_stats.py

사용자별 이슈/PR/리뷰 통계를 수집합니다.

### 4.1 사용법

```bash
PYTHONPATH=. python scripts/sprint_stats.py --sprint <SPRINT_NAME> [OPTIONS]
```

### 4.2 옵션

| 옵션 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `--team` | string | - | 팀 ID (NEW!) |
| `--sprint` | string | ✅* | 스프린트 이름 |
| `--notion-parent-id` | string | - | Notion 부모 페이지 ID |
| `--dry-run` | flag | - | 변경 없이 미리보기 |
| `--output` | string | - | 결과 JSON 파일 경로 |
| `--quiet` | flag | - | 출력 최소화 |

> *`--team` 지정 시 `--sprint`는 선택 사항

### 4.3 예시

```bash
# 레거시 모드 - 미리보기
PYTHONPATH=. python scripts/sprint_stats.py --sprint "25-12-Sprint1" --dry-run

# 레거시 모드 - Notion에 동기화
PYTHONPATH=. python scripts/sprint_stats.py \
  --sprint "25-12-Sprint1" \
  --notion-parent-id "2939eddc34e680f58c7ad076e5ba3e88"

# 멀티 팀 모드 - Synos 팀 (NEW!)
PYTHONPATH=. python scripts/sprint_stats.py --team synos

# 멀티 팀 모드 - dry-run (NEW!)
PYTHONPATH=. python scripts/sprint_stats.py --team synos --dry-run

# JSON 파일로 저장
PYTHONPATH=. python scripts/sprint_stats.py \
  --team synos \
  --output sprint_stats.json \
  --dry-run
```

### 4.4 출력 예시

```
Using team configuration: synos
Starting sprint stats script
Collecting project items for sprint: 25-12-Sprint1
Found 32 items in sprint
Collecting PR reviews from 2025-11-29 to 2025-12-06
Found 45 reviews in sprint period
Calculating user statistics...
  Total Issues: 18
  Total PRs: 12
  Total Reviews: 45

============================================================
Sprint: 25-12-Sprint1
Period: 2025-11-29 to 2025-12-06
Total Users: 6
Total Issues: 18
Total PRs: 12
Total Reviews: 45
============================================================

User Statistics:
  유두열               (duyeol-yu               ) - Issues:   5, PRs:   3, Reviews:  12
  한효정               (sylvanus4               ) - Issues:   4, PRs:   2, Reviews:   8
  ...
```

---

## 5. sprint_summary_sync.py

AI 기반 스프린트 전체 요약을 생성합니다.

### 5.1 사용법

```bash
PYTHONPATH=. python scripts/sprint_summary_sync.py --sprint <SPRINT_NAME> --notion-parent-id <ID> [OPTIONS]
```

### 5.2 옵션

| 옵션 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `--team` | string | - | 팀 ID (NEW!) |
| `--sprint` | string | ✅* | 스프린트 이름 |
| `--notion-parent-id` | string | ✅* | SprintChecker 페이지 ID |
| `--dry-run` | flag | - | 변경 없이 미리보기 |
| `--output` | string | - | 결과 JSON 파일 경로 |
| `--skip-details` | flag | - | 상세 정보 수집 스킵 (빠름) |
| `--skip-summary` | flag | - | AI 요약 생성 스킵 |
| `--anthropic-api-key` | string | - | Claude API 키 |
| `--start-date` | string | - | 수동 시작일 (YYYY-MM-DD) |
| `--end-date` | string | - | 수동 종료일 (YYYY-MM-DD) |
| `--quiet` | flag | - | 출력 최소화 |

> *`--team` 지정 시 `--sprint`와 `--notion-parent-id`는 선택 사항

### 5.3 예시

```bash
# 레거시 모드 - 미리보기
PYTHONPATH=. python scripts/sprint_summary_sync.py \
  --sprint "25-12-Sprint1" \
  --notion-parent-id "2ba9eddc34e680ff82dad5032418ab58" \
  --dry-run

# 레거시 모드 - Notion에 페이지 생성
PYTHONPATH=. python scripts/sprint_summary_sync.py \
  --sprint "25-12-Sprint1" \
  --notion-parent-id "2ba9eddc34e680ff82dad5032418ab58"

# 멀티 팀 모드 - Synos 팀 (NEW!)
PYTHONPATH=. python scripts/sprint_summary_sync.py --team synos

# 멀티 팀 모드 - dry-run (NEW!)
PYTHONPATH=. python scripts/sprint_summary_sync.py --team synos --dry-run

# 빠른 실행 (상세/AI 스킵)
PYTHONPATH=. python scripts/sprint_summary_sync.py \
  --team synos \
  --skip-details \
  --skip-summary

# 수동 날짜 범위
PYTHONPATH=. python scripts/sprint_summary_sync.py \
  --team synos \
  --start-date "2025-11-29" \
  --end-date "2025-12-06"
```

### 5.4 출력 예시

```
Using team configuration: synos
Starting Sprint Summary sync for: 25-12-Sprint1
Sprint date range: 2025-11-29 to 2025-12-06
Collecting project items for sprint: 25-12-Sprint1
Found 32 project items
Collecting PR reviews from 2025-11-29 to 2025-12-06
Found 45 PR reviews
Collecting detailed information for items...
Collected details for 32 items
Organizing data by user...
Collected data for 6 users
Generating AI summaries...
Generated summary for duyeol-yu
Generated summary for sylvanus4
...
Generated 6 summaries

============================================================
Sprint Summary: 25-12-Sprint1
Period: 2025-11-29 to 2025-12-06
Total Issues: 18
Total PRs: 12
Total Reviews: 45
Active Users: 6
============================================================

Creating Notion page...
Created Notion page: abc123-def456-...
Sprint Summary sync completed!
Duration: 85.23 seconds
Notion Page ID: abc123-def456-...
```

---

## 6. daily_scrum_sync.py

AI 기반 일일 스크럼 요약을 생성합니다.

### 6.1 사용법

```bash
PYTHONPATH=. python scripts/daily_scrum_sync.py --notion-parent-id <ID> [OPTIONS]
```

### 6.2 옵션

| 옵션 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `--team` | string | - | 팀 ID (NEW!) |
| `--notion-parent-id` | string | ✅* | DailyScrum 페이지 ID |
| `--days` | int | - | 조회 일수 (기본: 2) |
| `--sprint` | string | - | 스프린트 필터 |
| `--dry-run` | flag | - | 변경 없이 미리보기 |
| `--output` | string | - | 결과 JSON 파일 경로 |
| `--skip-details` | flag | - | 상세 정보 수집 스킵 |
| `--skip-summary` | flag | - | AI 요약 생성 스킵 |
| `--anthropic-api-key` | string | - | Claude API 키 |
| `--quiet` | flag | - | 출력 최소화 |

> *`--team` 지정 시 `--notion-parent-id`와 `--sprint`는 선택 사항

### 6.3 예시

```bash
# 레거시 모드 - 미리보기
PYTHONPATH=. python scripts/daily_scrum_sync.py \
  --notion-parent-id "2ba9eddc34e6800cbb43c744a495df3f" \
  --dry-run

# 레거시 모드 - Notion에 페이지 생성
PYTHONPATH=. python scripts/daily_scrum_sync.py \
  --notion-parent-id "2ba9eddc34e6800cbb43c744a495df3f"

# 멀티 팀 모드 - Synos 팀 (NEW!)
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos

# 멀티 팀 모드 - dry-run (NEW!)
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --dry-run

# 최근 3일
PYTHONPATH=. python scripts/daily_scrum_sync.py \
  --team synos \
  --days 3

# 빠른 실행
PYTHONPATH=. python scripts/daily_scrum_sync.py \
  --team synos \
  --skip-details \
  --skip-summary
```

### 6.4 출력 예시

```
Using team configuration: synos
Starting Daily Scrum sync for 2025-12-01 to 2025-12-02
Sprint filter: 25-12-Sprint1
Collecting project items...
Found 32 project items
Filtered 8 items from 32 total (activity since 2025-12-01)
Collecting PR reviews from 2025-12-01 to 2025-12-02
Found 12 PR reviews
Organizing data by user...
Collected data for 4 users
Generating AI summaries...
Generated summary for duyeol-yu
Generated summary for sylvanus4
Generated 4 summaries

============================================================
Daily Scrum Summary
Period: 2025-12-01 to 2025-12-02
Total Issues: 5
Total PRs: 3
Total Reviews: 12
Active Users: 4
============================================================

Creating Notion page...
Created Notion page: xyz789-...
Daily Scrum sync completed!
Duration: 45.67 seconds
Notion Page ID: xyz789-...
```

---

## 7. 에러 코드

| 코드 | 의미 | 해결 방법 |
|------|------|----------|
| 0 | 성공 | - |
| 1 | 일반 오류 | 로그 확인 |
| 120 | 설정 오류 | 팀/설정 파일 확인 (NEW!) |
| 130 | 사용자 중단 (Ctrl+C) | - |

---

## 8. 로그 레벨

| 레벨 | 설명 |
|------|------|
| DEBUG | 상세 디버그 정보 |
| INFO | 일반 정보 (기본) |
| WARNING | 경고 (계속 실행) |
| ERROR | 오류 (실행 중단) |

`--quiet` 옵션 사용 시 WARNING 이상만 출력됩니다.

---

## 9. JSON 출력 형식

### 9.1 sprint_stats.py 출력

```json
{
  "sprint": "25-12-Sprint1",
  "team": "synos",
  "date_range": {
    "start": "2025-11-29T00:00:00+09:00",
    "end": "2025-12-06T00:00:00+09:00"
  },
  "summary": {
    "total_users": 6,
    "total_issues": 18,
    "total_prs": 12,
    "total_reviews": 45
  },
  "user_stats": {
    "duyeol-yu": {
      "issues": 5,
      "prs": 3,
      "reviews": 12
    }
  }
}
```

### 9.2 sprint_summary_sync.py 출력

```json
{
  "sprint": "25-12-Sprint1",
  "team": "synos",
  "date_range": {...},
  "summary": {...},
  "user_data": {
    "duyeol-yu": {
      "display_name": "유두열",
      "issues": [...],
      "prs": [...],
      "reviews": [...],
      "ai_summary": {
        "narrative": "...",
        "tree": "..."
      }
    }
  }
}
```

---

## 10. 팀별 실행 요약 - NEW!

### 10.1 빠른 시작

```bash
# Synos 팀 전체 동기화
PYTHONPATH=. python scripts/complete_resync.py --team synos --force

# Synos 팀 데일리 스크럼
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos

# RagOS 팀 dry-run 테스트
PYTHONPATH=. python scripts/daily_scrum_sync.py --team ragos --dry-run
```

### 10.2 사용 가능한 팀 확인

```bash
# 설정된 팀 목록 확인
ls config/teams/

# 팀 설정 상세 확인
PYTHONPATH=. python -c "
from src.utils.team_config import list_available_teams, load_team_config
teams = list_available_teams()
for team_id in teams:
    config = load_team_config(team_id)
    print(f'{team_id}: {config.team_name} - Sprint: {config.current_sprint}')
"
```

### 10.3 팀 설정 오버라이드

```bash
# 팀 설정의 스프린트를 오버라이드
PYTHONPATH=. python scripts/daily_scrum_sync.py \
  --team synos \
  --sprint "25-12-Sprint2"  # 팀 설정의 current_sprint 대신 사용
```

