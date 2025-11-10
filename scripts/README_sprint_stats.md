# Sprint Statistics Script

스프린트별 팀원들의 기여도(이슈, PR, 리뷰 개수)를 수집하고 노션 데이터베이스에 자동으로 동기화하는 스크립트입니다.

## 기능

- **GitHub 통계 수집**

  - 스프린트에 할당된 이슈 개수 (assignee별)
  - 스프린트에 생성된 PR 개수 (author별)
  - Organization 전체의 PR 리뷰 개수 (reviewer별, 스프린트 기간 기준)

- **노션 연동**

  - 새로운 노션 데이터베이스 자동 생성
  - 유저별 통계를 노션 페이지로 동기화
  - Upsert 방식으로 중복 방지

- **유연한 실행 모드**
  - Dry-run: 실제 동기화 없이 미리보기
  - JSON 출력: 통계를 파일로 저장

## 사용법

### 기본 실행

```bash
# 스프린트 통계 수집 및 노션 동기화
python scripts/sprint_stats.py \
  --sprint "25-10-Sprint4" \
  --notion-parent-id "abc123def456"
```

### Dry Run (미리보기)

```bash
# 실제 동기화 없이 통계만 확인 (권장: 먼저 테스트)
python scripts/sprint_stats.py \
  --sprint "25-10-Sprint4" \
  --dry-run
```

### JSON 파일로 저장

```bash
# 통계를 JSON 파일로 저장
python scripts/sprint_stats.py \
  --sprint "25-10-Sprint4" \
  --output stats_output.json \
  --dry-run
```

### 디버그 모드

```bash
# 상세한 로그와 함께 실행 (문제 해결 시 유용)
LOG_LEVEL=DEBUG python scripts/sprint_stats.py \
  --sprint "25-10-Sprint4" \
  --dry-run
```

## 명령줄 옵션

| 옵션                 | 필수 | 설명                                                | 예시              |
| -------------------- | ---- | --------------------------------------------------- | ----------------- |
| `--sprint`           | ✅   | 스프린트 이름 (GitHub Iteration 필드와 정확히 일치) | `"25-10-Sprint4"` |
| `--notion-parent-id` | ❌   | 노션 페이지 ID (데이터베이스 생성 위치)             | `"abc123def456"`  |
| `--dry-run`          | ❌   | 실제 동기화 없이 미리보기 (권장)                    | -                 |
| `--output`           | ❌   | JSON 파일로 통계 저장                               | `stats.json`      |
| `--quiet`            | ❌   | 오류만 출력                                         | -                 |

> **팁:** 처음 실행할 때는 반드시 `--dry-run` 옵션으로 테스트한 후 실제 동기화를 진행하세요.

## 환경 변수

노션 페이지 ID를 매번 입력하기 번거롭다면 환경 변수로 설정할 수 있습니다:

```bash
# .env 파일에 추가
NOTION_STATS_PARENT_ID=abc123def456
```

이렇게 설정하면 `--notion-parent-id` 옵션을 생략할 수 있습니다.

## 노션 데이터베이스 스키마

스크립트가 자동으로 생성하는 노션 데이터베이스의 구조:

| 필드명       | 타입      | 설명                      |
| ------------ | --------- | ------------------------- |
| Sprint       | Title     | 스프린트 이름 + 유저 이름 |
| User         | Rich Text | GitHub 유저명             |
| Issues       | Number    | 할당된 이슈 개수          |
| PRs          | Number    | 생성한 PR 개수            |
| Reviews      | Number    | 작성한 리뷰 개수          |
| Last Updated | Date      | 마지막 업데이트 시간      |

## 출력 예시

```
============================================================
Sprint: 25-10-Sprint4
Period: 2025-10-20 to 2025-10-25
Total Users: 13
Total Issues: 63
Total PRs: 0
Total Reviews: 24
============================================================

User Statistics:
  chohongcheol-thakicloud - Issues:   5, PRs:   0, Reviews:   2
  duyeol-yu            - Issues:  10, PRs:   0, Reviews:   0
  hwyncho-thakicloud   - Issues:   4, PRs:   0, Reviews:   3
  jaehoonkim           - Issues:   4, PRs:   0, Reviews:   0
  jongmin-kim-thakicloud - Issues:   5, PRs:   0, Reviews:   0
  mjhan-tk             - Issues:   3, PRs:   0, Reviews:   0
  ryangkyung-thaki     - Issues:   4, PRs:   0, Reviews:   1
  sylvanus4            - Issues:   1, PRs:   0, Reviews:   0
  thaki-yakhyo         - Issues:  10, PRs:   0, Reviews:   1
  thakicloud-chanwoo   - Issues:   5, PRs:   0, Reviews:   1
  thakicloud-jotaeyang - Issues:   6, PRs:   0, Reviews:   0
  yunjae-park1111      - Issues:   6, PRs:   0, Reviews:   2

[DRY RUN] Would sync statistics to Notion

============================================================
Sprint statistics collection completed!
Duration: 10.05 seconds
Notion Database ID: (dry-run mode)
Pages Created: 0 (would create 13)
Pages Updated: 0
============================================================
```

> **참고:** 위 예시는 dry-run 모드의 출력입니다. 실제 동기화 시에는 노션 데이터베이스 ID와 생성된 페이지 수가 표시됩니다.

## JSON 출력 형식

`--output` 옵션을 사용하면 다음과 같은 JSON 형식으로 저장됩니다:

```json
{
  "sprint": "25-10-Sprint4",
  "date_range": {
    "start": "2025-10-20T00:00:00+00:00",
    "end": "2025-10-25T23:59:59+00:00"
  },
  "summary": {
    "total_users": 13,
    "total_issues": 63,
    "total_prs": 0,
    "total_reviews": 24
  },
  "user_stats": {
    "duyeol-yu": {
      "issues": 10,
      "prs": 0,
      "reviews": 0
    },
    "thaki-yakhyo": {
      "issues": 10,
      "prs": 0,
      "reviews": 1
    },
    "hwyncho-thakicloud": {
      "issues": 4,
      "prs": 0,
      "reviews": 3
    }
  }
}
```

이 JSON 파일은 추가 분석이나 리포팅에 활용할 수 있습니다.

## 작동 원리

### 1. 스프린트 기간 계산

- GitHub 프로젝트의 스프린트(Iteration) 필드에서 시작일과 기간 정보를 추출
- 자동으로 종료일 계산

### 2. 통계 수집

- **이슈 개수**: 프로젝트 아이템 중 스프린트에 할당된 이슈를 assignee별로 집계
- **PR 개수**: 프로젝트 아이템 중 스프린트에 할당된 PR을 author별로 집계
- **리뷰 개수**: Organization 전체에서 스프린트 기간 동안 작성된 PR 리뷰를 reviewer별로 집계

### 3. 노션 동기화

- 부모 페이지 아래에 새 데이터베이스 생성
- 각 유저별 통계를 개별 페이지로 생성
- 이미 존재하는 페이지는 업데이트 (upsert 방식)

## 필요 권한

### GitHub

- Organization read 권한
- Projects read 권한
- Repository read 권한 (PR 리뷰 조회)

### Notion

- 데이터베이스 생성 권한
- 페이지 생성/수정 권한

## 문제 해결

### "Could not determine sprint date range" 오류

스프린트 이름이 GitHub 프로젝트의 Iteration 필드와 정확히 일치하는지 확인하세요.

```bash
# 잘못된 예
--sprint "Sprint 4"

# 올바른 예
--sprint "25-10-Sprint4"
```

**원인:**

- 스프린트 필드 이름이 "스프린트", "Sprint", "Iteration" 중 하나여야 합니다
- 필드 타입이 ITERATION이어야 합니다
- 스프린트 이름이 정확히 일치해야 합니다 (대소문자 구분)

**해결 방법:**

1. GitHub 프로젝트에서 스프린트 필드 이름 확인
2. 스프린트 이름을 정확히 복사해서 사용
3. 디버그 로그를 활성화하여 사용 가능한 스프린트 목록 확인:

   ```bash
   LOG_LEVEL=DEBUG python scripts/sprint_stats.py --sprint "25-10-Sprint4" --dry-run
   ```

### "No parent page ID provided" 오류

노션 페이지 ID를 제공해야 합니다:

```bash
# 방법 1: 명령줄 옵션
--notion-parent-id "abc123"

# 방법 2: 환경 변수
export NOTION_STATS_PARENT_ID="abc123"
```

**노션 페이지 ID 찾는 방법:**

1. 노션에서 데이터베이스를 생성할 페이지 열기
2. URL에서 페이지 ID 복사 (32자리 영숫자)
3. 예: `https://notion.so/Your-Page-abc123def456` → `abc123def456`

### Rate Limit 오류

많은 PR과 리뷰가 있는 경우 GitHub API rate limit에 도달할 수 있습니다. 스크립트는 자동으로 rate limit을 처리하지만, 필요시 간격을 두고 다시 실행하세요.

### "GraphQL errors" 관련 오류

과거 버전에서 발생했던 GraphQL 쿼리 오류는 수정되었습니다. 최신 버전을 사용하고 있는지 확인하세요.

## 개발 정보

### 의존성

- `src/services/github_service.py`: GitHub API 통신
- `src/services/notion_service.py`: Notion API 통신
- `src/models/github_models.py`: GitHub 데이터 모델
- `src/config.py`: 설정 관리

### 추가/수정된 컴포넌트

**GitHubService (`src/services/github_service.py`):**

- `get_organization_pr_reviews()`: Organization PR 리뷰 조회 (페이지네이션)
- `get_all_organization_pr_reviews()`: 모든 PR 리뷰 수집

**NotionService (`src/services/notion_service.py`):**

- `create_database()`: 노션 데이터베이스 자동 생성
- `find_page_by_composite_key()`: 복합 키로 페이지 검색
- `create_page_in_database()`: 특정 데이터베이스에 페이지 생성
- `update_page_properties()`: 페이지 속성 업데이트

**GitHub Models (`src/models/github_models.py`):**

- `GitHubIteration`: Iteration 정보 모델 (id, title, start_date, duration)
- `GitHubIterationConfiguration`: Iteration 설정 모델 (iterations 리스트)
- `GitHubProjectField`: configuration 필드 추가 (Iteration 필드 지원)

### 주요 개선사항

**v1.1.0 (2025-10-21)**

- ✅ 스프린트 Iteration 필드 자동 인식 및 날짜 범위 계산
- ✅ Organization 전체 PR 리뷰 수집 기능
- ✅ datetime deprecation 경고 수정 (utcnow → now(timezone.utc))
- ✅ 다국어 스프린트 필드 이름 지원 (스프린트, Sprint, Iteration)
- ✅ 상세한 디버그 로깅 및 에러 메시지 개선
- ✅ GraphQL 쿼리 최적화 (미사용 변수 제거)

### 테스트 결과

**테스트 환경:**

- Sprint: 25-10-Sprint4
- Period: 2025-10-20 to 2025-10-25
- Items: 53개 프로젝트 아이템

**수집 성능:**

- 프로젝트 아이템 수집: ~9초
- PR 리뷰 수집: ~0.5초
- 총 실행 시간: ~10초

**통계:**

- 13명의 유저
- 63개의 이슈 (assignee별 집계)
- 24개의 PR 리뷰 (reviewer별 집계)

## 라이선스

이 스크립트는 프로젝트의 메인 라이선스를 따릅니다.
