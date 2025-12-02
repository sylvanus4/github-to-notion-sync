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

자동 실행 시 `config/sprint_config.yml` 파일의 설정을 사용합니다:

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
| `sprint_filter` | 스프린트 필터 (예: 25-12-Sprint1) | config 파일 값 |
| `notion_parent_id` | Notion 부모 페이지 ID | config 파일 값 |
| `run_complete_resync` | 전체 동기화 실행 | true |
| `run_pr_review_check` | PR 리뷰 체크 실행 | true |
| `run_sprint_stats` | 스프린트 통계 실행 | true |
| `run_sprint_summary` | 스프린트 요약 실행 | true |
| `run_daily_scrum` | 데일리 스크럼 실행 | true |

### 3.3 선택적 실행 예시

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

### 4.2 Step 2: Load sprint config

```yaml
- name: Load sprint config
  id: config
  run: |
    SPRINT=$(grep '^current_sprint:' config/sprint_config.yml | awk '{print $2}' | tr -d '"')
    # ...
```

`config/sprint_config.yml`에서 설정을 읽어옵니다:
- `current_sprint`: 현재 스프린트
- `notion_parent_id`: PR-Checker 페이지 ID
- `sprint_checker_parent_id`: SprintChecker 페이지 ID
- `daily_scrum_parent_id`: DailyScrum 페이지 ID

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
      SPRINT="${{ steps.config.outputs.default_sprint }}"
    fi
    echo "SPRINT_FILTER=${SPRINT}" >> $GITHUB_ENV
```

환경 변수를 설정합니다. **수동 입력값이 config 파일 값보다 우선**합니다.

### 4.6 Step 6-10: 기능 실행

각 기능은 조건부로 실행됩니다:

```yaml
- name: Run complete resync
  if: github.event_name == 'schedule' || github.event.inputs.run_complete_resync == 'true'
  timeout-minutes: 30
  env:
    GH_TOKEN: ${{ secrets.GH_TOKEN }}
    NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
    # ...
  run: |
    PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "${{ env.SPRINT_FILTER }}" --force
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

### 6.2 Variables (설정)

| 변수 | 설명 |
|------|------|
| `GH_ORG` | GitHub Organization 이름 |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 |
| `NOTION_DB_ID` | Notion Database ID |

### 6.3 런타임 환경 변수

| 변수 | 소스 | 설명 |
|------|------|------|
| `SPRINT_FILTER` | 입력 또는 config | 스프린트 필터 |
| `NOTION_PARENT_ID` | 입력 또는 config | PR-Checker 페이지 ID |
| `SPRINT_CHECKER_PARENT_ID` | config | SprintChecker 페이지 ID |
| `DAILY_SCRUM_PARENT_ID` | config | DailyScrum 페이지 ID |

---

## 7. 실행 결과 확인

### 7.1 Actions 탭에서 확인

1. **Actions** 탭으로 이동
2. 실행된 워크플로우 선택
3. 각 Step의 로그 확인

### 7.2 Artifacts 다운로드

1. 워크플로우 실행 결과 페이지 하단의 **Artifacts** 섹션
2. `sprint-sync-logs` 다운로드
3. 로그 및 JSON 파일 확인

---

## 8. 문제 해결

### 8.1 실행 실패 시

1. Actions 로그에서 에러 메시지 확인
2. 해당 Step의 상세 로그 검토
3. [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) 참조

### 8.2 부분 실패 시

일부 기능만 실패한 경우:
1. 실패한 기능만 수동으로 재실행
2. 해당 옵션만 `true`로 설정하여 실행

### 8.3 재실행

1. 실패한 워크플로우의 **Re-run jobs** 버튼 클릭
2. 또는 수동으로 새로운 워크플로우 트리거

---

## 9. 모범 사례

### 9.1 스프린트 전환 시

1. `config/sprint_config.yml` 업데이트
2. 커밋 및 푸시
3. 자동 실행 대기 또는 수동 실행

### 9.2 긴급 동기화 시

수동 트리거로 필요한 기능만 선택 실행:

```
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
# 로컬 테스트
PYTHONPATH=. python scripts/complete_resync.py --sprint-filter "25-12-Sprint1" --dry-run
```

