# Configuration Guide

Daily Sprint Sync 시스템의 설정 파일 가이드입니다.

---

## 1. 설정 파일 구조

```
config/
├── sprint_config.yml      # 스프린트 설정
└── field_mappings.yml     # 필드 매핑 설정
```

---

## 2. Sprint Config (sprint_config.yml)

### 2.1 파일 위치

```
config/sprint_config.yml
```

### 2.2 전체 구조

```yaml
# Sprint Configuration
# 일주일마다 이 파일만 업데이트하면 자동으로 GitHub Actions에서 사용됩니다.

current_sprint: 25-12-Sprint1

# PR-Checker 노션 페이지 ID (PR 리뷰 체크, 스프린트 통계 등)
notion_parent_id: 2939eddc34e680f58c7ad076e5ba3e88

# SprintChecker 노션 페이지 ID (스프린트 요약 페이지의 부모)
sprint_checker_parent_id: 2ba9eddc34e680ff82dad5032418ab58

# DailyScrum 노션 페이지 ID (데일리 스크럼 페이지의 부모)
daily_scrum_parent_id: 2ba9eddc34e6800cbb43c744a495df3f
```

### 2.3 설정 항목

| 항목 | 설명 | 형식 | 예시 |
|------|------|------|------|
| `current_sprint` | 현재 스프린트 이름 | `{YY}-{MM}-Sprint{N}` | `25-12-Sprint1` |
| `notion_parent_id` | PR-Checker 페이지 ID | Notion 페이지 ID | `2939eddc...` |
| `sprint_checker_parent_id` | SprintChecker 페이지 ID | Notion 페이지 ID | `2ba9eddc...` |
| `daily_scrum_parent_id` | DailyScrum 페이지 ID | Notion 페이지 ID | `2ba9eddc...` |

### 2.4 스프린트 전환 절차

새 스프린트 시작 시:

1. **스프린트 이름 형식 확인**
   ```
   {YY}-{MM}-Sprint{N}
   예: 25-12-Sprint1, 25-12-Sprint2
   ```

2. **파일 수정**
   ```yaml
   current_sprint: 25-12-Sprint2  # 새 스프린트로 변경
   ```

3. **커밋 & 푸시**
   ```bash
   git add config/sprint_config.yml
   git commit -m "chore: update sprint to 25-12-Sprint2"
   git push
   ```

4. **확인**
   - 다음 자동 실행 시 새 스프린트 적용
   - 또는 수동 실행으로 즉시 확인

### 2.5 Notion 페이지 ID 찾기

1. Notion에서 해당 페이지 열기
2. 우측 상단 **Share** 클릭
3. **Copy link** 클릭
4. URL에서 페이지 ID 추출:
   ```
   https://www.notion.so/workspace/Page-Title-{페이지ID}
   ```
   또는
   ```
   https://www.notion.so/{페이지ID}
   ```

---

## 3. Field Mappings (field_mappings.yml)

### 3.1 파일 위치

```
config/field_mappings.yml
```

### 3.2 주요 섹션

#### 3.2.1 GitHub to Notion 필드 매핑

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
      "25-07-Archive": "보관"
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
    default_value: null

  # 마감일
  due_date:
    github_field: "End date"
    notion_property: "마감일"
    type: "date"
    required: false

  # 스토리포인트
  estimate:
    github_field: "Estimate"
    notion_property: "스토리포인트"
    type: "number"
    required: false

  # 담당자 매핑 (GitHub 사용자 → Notion 사용자)
  assignees:
    github_field: "Assignees"
    notion_property: "담당자"
    type: "people"
    value_mappings:
      "github-username": "notion-user-id"
```

#### 3.2.2 사용자 표시 이름 매핑

```yaml
github_to_display_name:
  "github-username": "한글 이름"
  "duyeol-yu": "유두열"
  "sylvanus4": "한효정"
  "thaki-yakhyo": "yakhyo"
  # ...
```

#### 3.2.3 동기화 설정

```yaml
sync_config:
  rate_limits:
    notion_api: 3     # requests per second
    github_api: 5000  # requests per hour

  batch_size: 50
  retry_attempts: 3
  retry_delay: 1      # seconds

  full_sync_interval: "0 */6 * * *"  # every 6 hours

  backup_enabled: true
  backup_schedule: "0 2 * * 0"  # weekly at 2 AM
```

### 3.3 필드 타입별 설정

| Type | 설명 | value_mappings |
|------|------|----------------|
| `title` | 제목 필드 | 불필요 |
| `rich_text` | 텍스트 필드 | 불필요 |
| `select` | 단일 선택 | 필요 |
| `multi_select` | 다중 선택 | 필요 |
| `status` | 상태 필드 | 필요 |
| `date` | 날짜 필드 | 불필요 |
| `number` | 숫자 필드 | 불필요 |
| `people` | 사용자 필드 | 필요 (사용자 ID) |

### 3.4 새 사용자 추가

새 팀원 추가 시:

1. **Notion 사용자 ID 확인**
   - `get_notion_users.py` 스크립트 실행:
     ```bash
     python get_notion_users.py
     ```

2. **field_mappings.yml 수정**
   ```yaml
   github_to_notion:
     assignees:
       value_mappings:
         "new-github-username": "new-notion-user-id"

   github_to_display_name:
     "new-github-username": "새 사용자 이름"
   ```

3. **커밋 & 푸시**

---

## 4. GitHub Repository Settings

### 4.1 Secrets 설정

**Settings → Secrets and variables → Actions → Secrets**

| Secret Name | 설명 | 필수 |
|-------------|------|------|
| `GH_TOKEN` | GitHub Personal Access Token | ✅ |
| `NOTION_TOKEN` | Notion Integration Token | ✅ |
| `ANTHROPIC_API_KEY` | Claude API Key | ✅ (AI 요약용) |

### 4.2 Variables 설정

**Settings → Secrets and variables → Actions → Variables**

| Variable Name | 설명 | 예시 |
|---------------|------|------|
| `GH_ORG` | GitHub Organization | `ThakiCloud` |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 | `5` |
| `NOTION_DB_ID` | Notion Database ID | `abc123...` |

---

## 5. 설정 우선순위

워크플로우 실행 시 설정 우선순위:

```
1. workflow_dispatch 입력값 (최우선)
   ↓
2. config/sprint_config.yml 파일 값
   ↓
3. 환경 변수 기본값 (해당되는 경우)
```

### 5.1 예시

**수동 실행 시 `sprint_filter`를 입력한 경우:**
- 입력된 `sprint_filter` 값 사용

**수동 실행 시 `sprint_filter`를 비워둔 경우:**
- `config/sprint_config.yml`의 `current_sprint` 값 사용

---

## 6. 설정 검증

### 6.1 로컬에서 설정 검증

```bash
# 설정 파일 구문 검사
python -c "import yaml; yaml.safe_load(open('config/sprint_config.yml'))"
python -c "import yaml; yaml.safe_load(open('config/field_mappings.yml'))"
```

### 6.2 스크립트 dry-run 테스트

```bash
# 환경 변수 설정
export GH_TOKEN="your-token"
export NOTION_TOKEN="your-token"
export GH_ORG="ThakiCloud"
export GH_PROJECT_NUMBER="5"
export NOTION_DB_ID="your-db-id"
export GH_WEBHOOK_SECRET="dummy"

# dry-run 실행
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-12-Sprint1" --dry-run
```

---

## 7. 일반적인 설정 오류

### 7.1 스프린트 이름 불일치

**증상:** "Sprint not found in iterations" 에러

**해결:**
1. GitHub Project의 스프린트 이름 확인
2. `sprint_config.yml`의 `current_sprint` 값과 정확히 일치하는지 확인

### 7.2 Notion 페이지 ID 오류

**증상:** "Could not find page" 또는 권한 에러

**해결:**
1. 페이지 ID가 올바른지 확인
2. Notion Integration이 해당 페이지에 접근 권한이 있는지 확인
3. 페이지가 삭제되지 않았는지 확인

### 7.3 사용자 매핑 누락

**증상:** 담당자가 Notion에 표시되지 않음

**해결:**
1. `field_mappings.yml`에 해당 사용자 매핑 추가
2. Notion 사용자 ID가 올바른지 확인

---

## 8. 체크리스트

### 8.1 초기 설정 체크리스트

- [ ] `config/sprint_config.yml` 생성 및 설정
- [ ] `config/field_mappings.yml` 사용자 매핑 설정
- [ ] GitHub Secrets 설정 (`GH_TOKEN`, `NOTION_TOKEN`, `ANTHROPIC_API_KEY`)
- [ ] GitHub Variables 설정 (`GH_ORG`, `GH_PROJECT_NUMBER`, `NOTION_DB_ID`)
- [ ] Notion Integration이 필요한 페이지에 연결됨
- [ ] 로컬 dry-run 테스트 성공

### 8.2 스프린트 전환 체크리스트

- [ ] `sprint_config.yml`의 `current_sprint` 업데이트
- [ ] GitHub Project에 새 스프린트 Iteration 존재 확인
- [ ] 커밋 & 푸시
- [ ] (선택) 수동 실행으로 동기화 확인

