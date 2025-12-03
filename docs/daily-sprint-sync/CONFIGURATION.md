# Configuration Guide

Daily Sprint Sync 시스템의 설정 파일 가이드입니다.

---

## 1. 설정 파일 구조

### 1.1 레거시 구조 (단일 팀)

```
config/
├── sprint_config.yml      # 스프린트 설정
└── field_mappings.yml     # 필드 매핑 설정
```

### 1.2 멀티 팀 구조 (NEW!)

```
config/
├── sprint_config.yml      # 레거시 스프린트 설정 (하위 호환)
├── field_mappings.yml     # 공통 필드 매핑 설정
└── teams/                 # 팀별 설정 디렉토리
    ├── synos/
    │   ├── sprint_config.yml    # Synos 팀 설정
    │   └── field_mappings.yml   # Synos 팀 필드 매핑 (선택)
    ├── ragos/
    │   └── sprint_config.yml    # RagOS 팀 설정
    └── _template/
        └── sprint_config.yml    # 새 팀 추가용 템플릿
```

---

## 2. Sprint Config (sprint_config.yml)

### 2.1 레거시 설정 (단일 팀)

**파일 위치:** `config/sprint_config.yml`

```yaml
# Sprint Configuration (레거시 - 하위 호환용)
current_sprint: 25-12-Sprint1

# PR-Checker 노션 페이지 ID
notion_parent_id: 2939eddc34e680f58c7ad076e5ba3e88

# SprintChecker 노션 페이지 ID
sprint_checker_parent_id: 2ba9eddc34e680ff82dad5032418ab58

# DailyScrum 노션 페이지 ID
daily_scrum_parent_id: 2ba9eddc34e6800cbb43c744a495df3f
```

### 2.2 팀별 설정 (멀티 팀) - NEW!

**파일 위치:** `config/teams/{team_id}/sprint_config.yml`

```yaml
# Team Configuration
# 팀별로 독립적인 GitHub-Notion 동기화 설정

# 팀 기본 정보
team:
  id: "synos"
  name: "Synos"
  description: "Synos 팀 GitHub-Notion 동기화"
  enabled: true

# GitHub 연결 설정
# 토큰은 환경변수 GH_TOKEN 사용 (secrets에서 관리)
github:
  org: "ThakiCloud"
  project_number: 5

# Notion 연결 설정
# 토큰은 환경변수 NOTION_TOKEN 사용 (secrets에서 관리)
notion:
  # 메인 동기화 데이터베이스 ID (선택, 환경변수로 오버라이드 가능)
  # database_id: "your-database-id"

# 스프린트 설정
sprint:
  # 현재 스프린트 (매주 업데이트)
  current: "25-12-Sprint1"
  
  # PR-Checker 노션 페이지 ID (PR 리뷰 체크, 스프린트 통계 등)
  notion_parent_id: "2939eddc34e680f58c7ad076e5ba3e88"
  
  # SprintChecker 노션 페이지 ID (스프린트 요약 페이지의 부모)
  sprint_checker_parent_id: "2ba9eddc34e680ff82dad5032418ab58"
  
  # DailyScrum 노션 페이지 ID (데일리 스크럼 페이지의 부모)
  daily_scrum_parent_id: "2ba9eddc34e6800cbb43c744a495df3f"
  
  # QA 이슈 노션 데이터베이스 ID (선택)
  qa_database_id: ""
```

### 2.3 설정 항목 (팀별)

| 섹션 | 항목 | 설명 | 필수 |
|------|------|------|------|
| `team` | `id` | 팀 식별자 (디렉토리명과 일치) | ✅ |
| | `name` | 팀 표시 이름 | ✅ |
| | `description` | 팀 설명 | - |
| | `enabled` | 활성화 여부 | ✅ |
| `github` | `org` | GitHub Organization | ✅ |
| | `project_number` | GitHub Project 번호 | ✅ |
| `notion` | `database_id` | 메인 Notion DB ID | - |
| `sprint` | `current` | 현재 스프린트 이름 | ✅ |
| | `notion_parent_id` | PR-Checker 페이지 ID | ✅ |
| | `sprint_checker_parent_id` | SprintChecker 페이지 ID | ✅ |
| | `daily_scrum_parent_id` | DailyScrum 페이지 ID | ✅ |

### 2.4 스프린트 전환 절차

#### 레거시 모드
```bash
# config/sprint_config.yml 수정
current_sprint: 25-12-Sprint2

git add config/sprint_config.yml
git commit -m "chore: update sprint to 25-12-Sprint2"
git push
```

#### 멀티 팀 모드
```bash
# 각 팀별 설정 수정
# config/teams/synos/sprint_config.yml
# config/teams/ragos/sprint_config.yml

git add config/teams/
git commit -m "chore: update sprint to 25-12-Sprint2 for all teams"
git push
```

---

## 3. Field Mappings (field_mappings.yml)

### 3.1 공통 설정

**파일 위치:** `config/field_mappings.yml`

이 파일은 모든 팀에서 공유하는 기본 필드 매핑을 정의합니다.

```yaml
github_to_notion:
  # 제목 필드
  title:
    github_field: "title"
    notion_property: "피드백 제목"
    type: "title"
    required: true

  # GitHub Node ID (중복 체크용)
  id:
    github_field: "id"
    notion_property: "GitHub ID"
    type: "rich_text"
    required: true

  # 타입 매핑
  type:
    github_field: "__typename"
    notion_property: "태그"
    type: "multi_select"
    value_mappings:
      "Issue": "ISSUE"
      "PullRequest": "PULL_REQUEST"
      "DraftIssue": "DRAFT_ISSUE"

  # 상태 매핑
  status:
    github_field: "Status"
    notion_property: "진행 상태"
    type: "status"
    value_mappings:
      "Epic": "시작 전"
      "Todo": "시작 전"
      "In Progress": "진행 중"
      "Done": "완료"
    default_value: "시작 전"

  # 우선순위 매핑
  priority:
    github_field: "Priority"
    notion_property: "우선순위"
    type: "select"
    value_mappings:
      "P0": "높음"
      "P1": "중간"
      "P2": "낮음"

  # 마감일
  due_date:
    github_field: "End date"
    notion_property: "마감일"
    type: "date"

  # 스토리포인트
  estimate:
    github_field: "Estimate"
    notion_property: "스토리포인트"
    type: "number"

  # 담당자 매핑
  assignees:
    github_field: "Assignees"
    notion_property: "담당자"
    type: "people"
    value_mappings:
      "github-username": "notion-user-id"
```

### 3.2 팀별 필드 매핑 (선택) - NEW!

**파일 위치:** `config/teams/{team_id}/field_mappings.yml`

팀별로 사용자 매핑을 오버라이드하거나 추가 설정을 정의할 수 있습니다.

```yaml
# Synos 팀 전용 사용자 매핑
# 공통 field_mappings.yml의 설정을 확장/오버라이드

# GitHub 사용자 → Notion 사용자 ID 매핑
user_mappings:
  "sylvanus4": "12345678-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  "duyeol-yu": "23456789-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  "thakicloud-jotaeyang": "34567890-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# GitHub 사용자 → 표시 이름 매핑
github_to_display_name:
  "sylvanus4": "한효정"
  "duyeol-yu": "유두열"
  "thakicloud-jotaeyang": "조태양"
```

### 3.3 설정 로드 우선순위

```
1. 팀별 field_mappings.yml (있는 경우)
   ↓ (병합)
2. 공통 config/field_mappings.yml
```

팀별 설정이 있으면 공통 설정과 병합되며, 같은 키가 있으면 팀별 설정이 우선합니다.

---

## 4. 새 팀 추가하기 - NEW!

### 4.1 템플릿 복사

```bash
# 템플릿 복사
cp -r config/teams/_template config/teams/newteam

# 설정 파일 수정
vim config/teams/newteam/sprint_config.yml
```

### 4.2 필수 설정 항목

1. **팀 정보 수정**
   ```yaml
   team:
     id: "newteam"
     name: "새팀"
     description: "새팀 GitHub-Notion 동기화"
     enabled: true
   ```

2. **GitHub 연결 설정**
   ```yaml
   github:
     org: "YourOrganization"
     project_number: 10
   ```

3. **Notion 페이지 ID 설정**
   ```yaml
   sprint:
     current: "25-12-Sprint1"
     notion_parent_id: "your-pr-checker-page-id"
     sprint_checker_parent_id: "your-sprint-checker-page-id"
     daily_scrum_parent_id: "your-daily-scrum-page-id"
   ```

4. **(선택) 사용자 매핑 추가**
   ```bash
   # 팀별 필드 매핑 생성
   vim config/teams/newteam/field_mappings.yml
   ```

### 4.3 검증 및 테스트

```bash
# 팀 설정 로드 테스트
PYTHONPATH=. python -c "
from src.utils.team_config import load_team_config
config = load_team_config('newteam')
print(f'Team: {config.team_name}')
print(f'GitHub: {config.github_org}/{config.github_project_number}')
print(f'Sprint: {config.current_sprint}')
"

# dry-run 테스트
PYTHONPATH=. python scripts/daily_scrum_sync.py --team newteam --dry-run
```

---

## 5. GitHub Repository Settings

### 5.1 Secrets 설정

**Settings → Secrets and variables → Actions → Secrets**

| Secret Name | 설명 | 필수 |
|-------------|------|------|
| `GH_TOKEN` | GitHub Personal Access Token | ✅ |
| `NOTION_TOKEN` | Notion Integration Token | ✅ |
| `ANTHROPIC_API_KEY` | Claude API Key | ✅ (AI 요약용) |

### 5.2 Variables 설정 (레거시 모드)

**Settings → Secrets and variables → Actions → Variables**

| Variable Name | 설명 | 예시 |
|---------------|------|------|
| `GH_ORG` | GitHub Organization | `ThakiCloud` |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 | `5` |
| `NOTION_DB_ID` | Notion Database ID | `abc123...` |

> **Note:** 멀티 팀 모드에서는 이 Variables 대신 팀별 `sprint_config.yml`의 설정이 사용됩니다.

---

## 6. 설정 우선순위

### 6.1 레거시 모드

```
1. workflow_dispatch 입력값 (최우선)
   ↓
2. config/sprint_config.yml 파일 값
   ↓
3. 환경 변수 (GH_ORG, GH_PROJECT_NUMBER 등)
```

### 6.2 멀티 팀 모드 - NEW!

```
1. workflow_dispatch 입력값 (최우선)
   ↓
2. config/teams/{team}/sprint_config.yml 파일 값
   ↓
3. config/sprint_config.yml (폴백)
   ↓
4. 환경 변수 (최종 폴백)
```

### 6.3 팀 선택 우선순위

```
1. --team CLI 인자 (스크립트 직접 실행)
   ↓
2. workflow_dispatch의 team 입력
   ↓
3. DEFAULT_TEAM 환경변수
   ↓
4. 레거시 모드 (팀 없음)
```

---

## 7. 설정 검증

### 7.1 YAML 구문 검사

```bash
# 레거시 설정
python -c "import yaml; yaml.safe_load(open('config/sprint_config.yml'))"

# 팀별 설정
python -c "import yaml; yaml.safe_load(open('config/teams/synos/sprint_config.yml'))"
```

### 7.2 팀 설정 로드 테스트

```bash
# 사용 가능한 팀 목록 확인
PYTHONPATH=. python -c "
from src.utils.team_config import list_available_teams
teams = list_available_teams()
print(f'Available teams: {teams}')
"

# 특정 팀 설정 확인
PYTHONPATH=. python -c "
from src.utils.team_config import load_team_config
config = load_team_config('synos')
print(f'Team: {config.team_id} ({config.team_name})')
print(f'GitHub: {config.github_org}/{config.github_project_number}')
print(f'Sprint: {config.current_sprint}')
print(f'Daily Scrum Parent: {config.daily_scrum_parent_id}')
"
```

### 7.3 스크립트 dry-run 테스트

```bash
# 레거시 모드
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-12-Sprint1" --dry-run

# 멀티 팀 모드
PYTHONPATH=. python scripts/complete_resync.py --team synos --dry-run
```

---

## 8. 일반적인 설정 오류

### 8.1 팀 설정 파일 없음 - NEW!

**증상:** "Team 'xxx' not found" 에러

**해결:**
1. `config/teams/xxx/` 디렉토리 존재 확인
2. `config/teams/xxx/sprint_config.yml` 파일 존재 확인
3. 파일명 오타 확인

### 8.2 YAML 섹션 누락

**증상:** "'NoneType' object has no attribute 'get'" 에러

**해결:**
- `sprint_config.yml`에서 `team`, `github`, `sprint` 섹션이 모두 있는지 확인
- 빈 섹션이라도 키는 존재해야 함

### 8.3 스프린트 이름 불일치

**증상:** "Sprint not found in iterations" 에러

**해결:**
1. GitHub Project의 스프린트 이름 확인
2. 팀별 `sprint.current` 값과 정확히 일치하는지 확인

### 8.4 사용자 매핑 누락

**증상:** "Skipping unmapped user: xxx" 경고

**해결:**
1. `config/field_mappings.yml` 또는 팀별 `field_mappings.yml`에 사용자 추가
2. `get_notion_users.py`로 Notion 사용자 ID 확인

---

## 9. 체크리스트

### 9.1 새 팀 설정 체크리스트

- [ ] `config/teams/{team_id}/sprint_config.yml` 생성
- [ ] `team.id` 설정 (디렉토리명과 일치)
- [ ] `github.org` 및 `github.project_number` 설정
- [ ] `sprint.current` 현재 스프린트 설정
- [ ] `sprint.notion_parent_id` 설정 (PR-Checker)
- [ ] `sprint.sprint_checker_parent_id` 설정
- [ ] `sprint.daily_scrum_parent_id` 설정
- [ ] Notion Integration이 필요한 페이지에 연결됨
- [ ] (선택) 팀별 `field_mappings.yml` 생성
- [ ] dry-run 테스트 성공

### 9.2 스프린트 전환 체크리스트 (멀티 팀)

- [ ] 각 팀의 `sprint_config.yml`에서 `sprint.current` 업데이트
- [ ] GitHub Project에 새 스프린트 Iteration 존재 확인
- [ ] 커밋 & 푸시
- [ ] (선택) 수동 실행으로 동기화 확인

