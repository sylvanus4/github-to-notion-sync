# Workflow Guide

GitHub Actions 워크플로우 사용 가이드입니다.

---

## 1. 워크플로우 개요

### 1.1 파일 위치

```
.github/workflows/daily-sprint-sync.yml
```

### 1.2 트리거 방식

| 방식 | 설명 | 시간 |
|------|------|------|
| **Schedule** | 자동 스케줄 실행 | 매일 KST 07:30 (UTC 22:30) |
| **Manual** | 수동 실행 (workflow_dispatch) | 필요 시 |

---

## 2. 자동 실행 (Schedule)

### 2.1 스케줄 설정

```yaml
on:
  schedule:
    # 한국 시간 오전 7시 30분 = UTC 22시 30분 (전날)
    - cron: '30 22 * * *'
```

### 2.2 자동 실행 동작

자동 실행 시 **모든 기능이 순차적으로 실행**됩니다:

1. ✅ Complete Resync (전체 동기화)
2. ✅ PR Review Check (PR 리뷰 체크)
3. ✅ Sprint Stats (스프린트 통계)
4. ✅ Sprint Summary (스프린트 요약)
5. ✅ Daily Scrum (데일리 스크럼)

### 2.3 설정 소스

자동 실행 시 `config/sprint_config.yml` 파일의 설정을 사용합니다 (레거시 모드):

```yaml
current_sprint: 25-12-Sprint1
notion_parent_id: <PR-Checker 페이지 ID>
sprint_checker_parent_id: <SprintChecker 페이지 ID>
daily_scrum_parent_id: <DailyScrum 페이지 ID>
```

---

## 3. 수동 실행 (Manual Trigger)

### 3.1 실행 방법

1. GitHub 저장소의 **Actions** 탭으로 이동
2. 왼쪽 사이드바에서 **Daily Sprint Sync** 선택
3. **Run workflow** 버튼 클릭
4. 옵션 입력 후 **Run workflow** 클릭

### 3.2 입력 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| **`team`** | 팀 ID (synos, ragos 등) - NEW! | 빈 값 (레거시 모드) |
| `sprint_filter` | 스프린트 필터 (예: 25-12-Sprint1) | config 파일 값 |
| `notion_parent_id` | Notion 부모 페이지 ID | config 파일 값 |
| `run_complete_resync` | 전체 동기화 실행 | true |
| `run_pr_review_check` | PR 리뷰 체크 실행 | true |
| `run_sprint_stats` | 스프린트 통계 실행 | true |
| `run_sprint_summary` | 스프린트 요약 실행 | true |
| `run_daily_scrum` | 데일리 스크럼 실행 | true |

### 3.3 팀별 실행 (멀티 팀 모드) - NEW!

#### 팀 선택 시 동작

1. `team` 입력에 팀 ID를 입력하면 해당 팀의 설정을 자동 로드
2. `config/teams/{team}/sprint_config.yml`에서 설정 읽기
3. 팀별 GitHub 연결 정보와 Notion 페이지 ID 사용

#### 레거시 모드 vs 멀티 팀 모드

| 모드 | `team` 값 | 설정 소스 |
|------|-----------|-----------|
| **레거시** | 빈 값 | `config/sprint_config.yml` + GitHub Variables |
| **멀티 팀** | `synos` 등 | `config/teams/synos/sprint_config.yml` |

#### 팀별 실행 예시

**Synos 팀만 실행:**
```
team: synos
sprint_filter: (비워둠 - 팀 설정 사용)
run_complete_resync: true
run_pr_review_check: true
run_sprint_stats: true
run_sprint_summary: true
run_daily_scrum: true
```

**RagOS 팀 특정 기능만 실행:**
```
team: ragos
run_complete_resync: false
run_pr_review_check: false
run_sprint_stats: false
run_sprint_summary: false
run_daily_scrum: true  # 데일리 스크럼만 실행
```

### 3.4 선택적 실행 예시

**PR 리뷰 체크만 실행:**
- `run_complete_resync`: false
- `run_pr_review_check`: true
- `run_sprint_stats`: false
- `run_sprint_summary`: false
- `run_daily_scrum`: false

**데일리 스크럼만 실행:**
- `run_complete_resync`: false
- `run_pr_review_check`: false
- `run_sprint_stats`: false
- `run_sprint_summary`: false
- `run_daily_scrum`: true

---

## 4. 워크플로우 단계별 설명

### 4.1 Step 1: Checkout code

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

저장소 코드를 체크아웃합니다.

### 4.2 Step 2: Load team config or legacy config - NEW!

```yaml
- name: Load team config or legacy config
  id: config_loader
  run: |
    TEAM_ID="${{ github.event.inputs.team }}"
    if [ -n "$TEAM_ID" ]; then
      echo "Loading config for team: $TEAM_ID"
      # 팀별 sprint_config.yml에서 설정 로드
      SPRINT=$(grep '^  current:' config/teams/"$TEAM_ID"/sprint_config.yml | awk '{print $2}' | tr -d '"')
      # ...
    else
      echo "Loading legacy config"
      # 레거시 config/sprint_config.yml에서 설정 로드
      SPRINT=$(grep '^current_sprint:' config/sprint_config.yml | awk '{print $2}' | tr -d '"')
      # ...
    fi
```

**팀 지정 시:** `config/teams/{team}/sprint_config.yml`에서 설정 로드
**팀 미지정 시:** `config/sprint_config.yml` + GitHub Variables 사용

### 4.3 Step 3: Set up Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

Python 3.11 환경을 설정합니다.

### 4.4 Step 4: Install dependencies

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

필요한 Python 패키지를 설치합니다.

### 4.5 Step 5: Set environment variables

```yaml
- name: Set environment variables
  run: |
    # 수동 입력값이 있으면 우선, 없으면 config 파일 값 사용
    SPRINT="${{ github.event.inputs.sprint_filter }}"
    if [ -z "$SPRINT" ]; then
      SPRINT="${{ steps.config_loader.outputs.default_sprint }}"
    fi
    echo "SPRINT_FILTER=${SPRINT}" >> $GITHUB_ENV
    echo "DEFAULT_TEAM=${{ steps.config_loader.outputs.default_team }}" >> $GITHUB_ENV
```

환경 변수를 설정합니다. **수동 입력값이 config 파일 값보다 우선**합니다.

### 4.6 Step 6-10: 기능 실행

각 기능은 조건부로 실행되며, `--team` 인자가 전달됩니다:

```yaml
- name: Run daily scrum sync
  if: github.event_name == 'schedule' || github.event.inputs.run_daily_scrum == 'true'
  timeout-minutes: 15
  env:
    GH_TOKEN: ${{ secrets.GH_TOKEN }}
    NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
    # ...
  run: |
    PYTHONPATH=. python scripts/daily_scrum_sync.py \
      --sprint "${{ env.SPRINT_FILTER }}" \
      --notion-parent-id "${{ env.DAILY_SCRUM_PARENT_ID }}" \
      --team "${{ env.DEFAULT_TEAM }}"
```

**실행 조건:**
- 스케줄 실행: 항상 실행
- 수동 실행: 해당 옵션이 `true`인 경우만 실행

### 4.7 Step 11: Upload artifacts

```yaml
- name: Upload artifacts (if any)
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: sprint-sync-logs
    path: |
      *.log
      *.json
    retention-days: 7
```

실행 로그와 결과 파일을 7일간 보관합니다.

---

## 5. 타임아웃 설정

| 단계 | 타임아웃 |
|------|----------|
| 전체 Job | 60분 |
| Complete Resync | 30분 |
| PR Review Check | 15분 |
| Sprint Stats | 15분 |
| Sprint Summary | 15분 |
| Daily Scrum | 15분 |

---

## 6. 환경 변수

### 6.1 Secrets (민감 정보)

| 변수 | 설명 |
|------|------|
| `GH_TOKEN` | GitHub Personal Access Token |
| `NOTION_TOKEN` | Notion Integration Token |
| `ANTHROPIC_API_KEY` | Claude API Key |

### 6.2 Variables (설정) - 레거시 모드

| 변수 | 설명 |
|------|------|
| `GH_ORG` | GitHub Organization 이름 |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 |
| `NOTION_DB_ID` | Notion Database ID |

> **Note:** 멀티 팀 모드에서는 Variables 대신 팀별 `sprint_config.yml` 설정이 사용됩니다.

### 6.3 런타임 환경 변수

| 변수 | 소스 | 설명 |
|------|------|------|
| `SPRINT_FILTER` | 입력 또는 config | 스프린트 필터 |
| `NOTION_PARENT_ID` | 입력 또는 config | PR-Checker 페이지 ID |
| `SPRINT_CHECKER_PARENT_ID` | config | SprintChecker 페이지 ID |
| `DAILY_SCRUM_PARENT_ID` | config | DailyScrum 페이지 ID |
| `DEFAULT_TEAM` | 입력 | 팀 ID (NEW!) |
| `GH_ORG` | config 또는 Variables | GitHub Organization |
| `GH_PROJECT_NUMBER` | config 또는 Variables | GitHub Project 번호 |

---

## 7. 실행 결과 확인

### 7.1 Actions 탭에서 확인

1. **Actions** 탭으로 이동
2. 실행된 워크플로우 선택
3. 각 Step의 로그 확인

### 7.2 팀 설정 로드 확인 - NEW!

워크플로우 로그에서 다음 메시지 확인:

**멀티 팀 모드:**
```
📋 Config loaded - Team: synos
   Sprint: 25-12-Sprint1
   PR-Checker: 2939eddc34e680f58c7ad076e5ba3e88
   SprintChecker: 2ba9eddc34e680ff82dad5032418ab58
   DailyScrum: 2ba9eddc34e6800cbb43c744a495df3f
   GH Org: ThakiCloud
   GH Project: 5
```

**레거시 모드:**
```
📋 Config loaded - Team: Legacy
   Sprint: 25-12-Sprint1
   ...
```

### 7.3 Artifacts 다운로드

1. 워크플로우 실행 결과 페이지 하단의 **Artifacts** 섹션
2. `sprint-sync-logs` 다운로드
3. 로그 및 JSON 파일 확인

---

## 8. 문제 해결

### 8.1 실행 실패 시

1. Actions 로그에서 에러 메시지 확인
2. 해당 Step의 상세 로그 검토
3. [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) 참조

### 8.2 팀 설정 오류 - NEW!

**증상:** "Team 'xxx' not found" 에러

**확인:**
1. `config/teams/xxx/` 디렉토리 존재 확인
2. `sprint_config.yml` 파일 존재 및 구문 확인

### 8.3 부분 실패 시

일부 기능만 실패한 경우:
1. 실패한 기능만 수동으로 재실행
2. 해당 옵션만 `true`로 설정하여 실행

### 8.4 재실행

1. 실패한 워크플로우의 **Re-run jobs** 버튼 클릭
2. 또는 수동으로 새로운 워크플로우 트리거

---

## 9. 모범 사례

### 9.1 스프린트 전환 시 (멀티 팀)

1. 각 팀의 `config/teams/{team}/sprint_config.yml` 업데이트
2. 커밋 및 푸시
3. 자동 실행 대기 또는 수동 실행

```bash
# 모든 팀의 스프린트 업데이트
git add config/teams/
git commit -m "chore: update sprint to 25-12-Sprint2 for all teams"
git push
```

### 9.2 긴급 동기화 시

수동 트리거로 필요한 팀과 기능만 선택 실행:

```
team: synos
sprint_filter: 25-12-Sprint1
run_complete_resync: true
run_pr_review_check: false
run_sprint_stats: false
run_sprint_summary: false
run_daily_scrum: false
```

### 9.3 테스트 실행

로컬에서 개별 스크립트 테스트 후 워크플로우 실행 권장:

```bash
# 레거시 모드 테스트
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-12-Sprint1" --dry-run

# 멀티 팀 모드 테스트
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --dry-run
```

### 9.4 여러 팀 순차 실행

현재 워크플로우는 한 번에 하나의 팀만 실행합니다. 여러 팀을 실행하려면:

1. 각 팀별로 수동 트리거 실행
2. 또는 Matrix 전략을 사용한 워크플로우 확장 (고급)

---

## 10. 팀별 워크플로우 실행 요약 - NEW!

### 10.1 Synos 팀 실행

```
team: synos
(나머지 옵션은 팀 설정에서 자동 로드)
```

### 10.2 RagOS 팀 실행

```
team: ragos
(나머지 옵션은 팀 설정에서 자동 로드)
```

### 10.3 새 팀 추가 후 실행

1. `config/teams/newteam/sprint_config.yml` 생성
2. 커밋 및 푸시
3. 워크플로우에서 `team: newteam` 입력하여 실행

