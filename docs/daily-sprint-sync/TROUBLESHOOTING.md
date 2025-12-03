# Troubleshooting Guide

Daily Sprint Sync 시스템의 문제 해결 가이드입니다.

---

## 1. 일반적인 오류

### 1.1 "Sprint not found in iterations"

**증상:**
```
Sprint '25-12-Sprint1' not found in iterations
Available sprints: ['25-11-Sprint3', '25-11-Sprint4']
```

**원인:**
- `sprint_config.yml`의 스프린트 이름이 GitHub Project의 Iteration 이름과 불일치

**해결:**
1. GitHub Project에서 정확한 스프린트 이름 확인
2. 설정 파일 수정:
   - 레거시: `config/sprint_config.yml`
   - 멀티 팀: `config/teams/{team}/sprint_config.yml`
   ```yaml
   # 레거시
   current_sprint: 25-12-Sprint1

   # 멀티 팀
   sprint:
     current: 25-12-Sprint1
   ```
3. 또는 수동 실행 시 `sprint_filter` 입력에 정확한 이름 입력

---

### 1.2 "Could not find page" (Notion)

**증상:**
```
APIResponseError: Could not find page with ID: abc123...
```

**원인:**
1. 페이지 ID가 잘못됨
2. Notion Integration이 해당 페이지에 연결되지 않음
3. 페이지가 삭제됨

**해결:**
1. 페이지 ID 재확인:
   - Notion에서 페이지 열기
   - Share → Copy link
   - URL에서 ID 추출

2. Integration 연결 확인:
   - 페이지에서 ⋯ → Add connections
   - GitHub Sync Integration 연결

---

### 1.3 "401 Unauthorized" (GitHub)

**증상:**
```
401 Unauthorized - Bad credentials
```

**원인:**
1. GitHub Token이 만료됨
2. Token이 잘못됨
3. Token 권한 부족

**해결:**
1. 새 PAT 생성 (Settings → Developer settings → Personal access tokens)
2. 필요한 권한 확인: `repo`, `read:org`, `read:project`
3. GitHub Secrets에서 `GH_TOKEN` 업데이트

---

### 1.4 "401 Unauthorized" (Notion)

**증상:**
```
APIResponseError: Could not find integration
```

**원인:**
1. Notion Token이 잘못됨
2. Integration이 삭제됨

**해결:**
1. [Notion Integrations](https://www.notion.so/my-integrations) 페이지에서 Integration 확인
2. 새 Token 복사
3. GitHub Secrets에서 `NOTION_TOKEN` 업데이트

---

### 1.5 "Rate limit exceeded"

**증상:**
```
Rate limit exceeded. Please retry after X seconds.
```

**원인:**
- API 호출 횟수 초과

**해결:**
1. 자동 재시도 대기 (스크립트가 자동 처리)
2. 수동 실행 시: 잠시 후 재실행
3. 배치 크기 줄이기: `--batch-size 20`

---

### 1.6 "Anthropic API Error"

**증상:**
```
anthropic.APIError: Invalid API key
```

**원인:**
1. API 키가 잘못됨
2. 잔액 부족
3. 요금제 제한

**해결:**
1. [Anthropic Console](https://console.anthropic.com/)에서 API 키 확인
2. 잔액/사용량 확인
3. 필요시 새 키 생성

**우회:**
AI 요약 없이 실행:
```bash
--skip-summary
```

---

## 2. 멀티 팀 관련 오류 - NEW!

### 2.1 "Team 'xxx' not found"

**증상:**
```
FileNotFoundError: Team configuration not found: config/teams/xxx/sprint_config.yml
```

**원인:**
1. 팀 디렉토리가 없음
2. sprint_config.yml 파일이 없음
3. 팀 ID 오타

**해결:**
1. 디렉토리 확인:
   ```bash
   ls config/teams/
   ```

2. 파일 확인:
   ```bash
   ls config/teams/xxx/
   ```

3. 팀 생성 (없는 경우):
   ```bash
   cp -r config/teams/_template config/teams/xxx
   vim config/teams/xxx/sprint_config.yml
   ```

---

### 2.2 "'NoneType' object has no attribute 'get'"

**증상:**
```
AttributeError: 'NoneType' object has no attribute 'get'
```

**원인:**
- YAML 파일에서 필수 섹션이 누락되었거나 비어있음

**해결:**
1. sprint_config.yml 구조 확인:
   ```yaml
   # 모든 섹션이 있어야 함
   team:
     id: "xxx"
     name: "팀이름"
     enabled: true

   github:
     org: "Organization"
     project_number: 5

   notion:
     # 비어있어도 섹션은 있어야 함

   sprint:
     current: "25-12-Sprint1"
     notion_parent_id: "xxx"
     sprint_checker_parent_id: "xxx"
     daily_scrum_parent_id: "xxx"
   ```

2. YAML 구문 검사:
   ```bash
   python -c "import yaml; print(yaml.safe_load(open('config/teams/xxx/sprint_config.yml')))"
   ```

---

### 2.3 "Skipping unmapped user: xxx"

**증상:**
```
WARNING: Skipping unmapped user: new-username (not in field_mappings.yml)
```

**원인:**
- 해당 사용자가 field_mappings.yml에 매핑되지 않음

**해결:**
1. 공통 매핑 추가 (모든 팀에서 사용):
   ```bash
   vim config/field_mappings.yml
   ```
   ```yaml
   github_to_display_name:
     "new-username": "새 사용자"
   ```

2. 또는 팀별 매핑 추가:
   ```bash
   vim config/teams/synos/field_mappings.yml
   ```
   ```yaml
   github_to_display_name:
     "new-username": "새 사용자"
   ```

3. Notion 사용자 ID가 필요한 경우:
   ```bash
   python get_notion_users.py
   ```

---

### 2.4 "Using legacy mode (no team config)"

**증상:**
```
INFO: Using legacy mode (no team config)
```

**원인:**
- `--team` 옵션이 제공되지 않음
- DEFAULT_TEAM 환경변수가 설정되지 않음
- config/teams/ 디렉토리가 없음

**해결 (의도하지 않은 경우):**
1. --team 옵션 추가:
   ```bash
   PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos
   ```

2. 또는 DEFAULT_TEAM 환경변수 설정:
   ```bash
   export DEFAULT_TEAM=synos
   ```

---

### 2.5 팀 설정과 CLI 옵션 충돌

**증상:**
- 예상과 다른 스프린트/페이지 ID가 사용됨

**원인:**
- CLI 옵션이 팀 설정을 오버라이드함

**해결:**
CLI 옵션 우선순위 이해:
```
1. CLI 옵션 (--sprint, --notion-parent-id 등) - 최우선
   ↓
2. 팀 설정 (config/teams/{team}/sprint_config.yml)
   ↓
3. 레거시 설정 (config/sprint_config.yml)
```

의도한 동작 확인:
```bash
# 팀 설정만 사용
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos

# CLI 옵션으로 오버라이드
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --sprint "25-12-Sprint2"
```

---

## 3. 워크플로우 실패

### 3.1 타임아웃

**증상:**
```
The job running on runner ... has exceeded the maximum execution time of 30 minutes.
```

**원인:**
- 데이터가 너무 많음
- API 응답이 느림
- 네트워크 문제

**해결:**
1. 스프린트 필터 적용하여 데이터 범위 축소
2. 배치 크기 조정
3. 필요한 기능만 선택 실행

---

### 3.2 부분 실패

**증상:**
- 일부 Step만 실패
- 90% 미만 성공률

**원인:**
- 특정 데이터에서 오류
- 일시적인 API 오류

**해결:**
1. 실패한 Step 로그 확인
2. 해당 기능만 수동 재실행
3. `--dry-run`으로 문제 데이터 확인

---

### 3.3 설정 파일 오류

**증상:**
```
yaml.scanner.ScannerError: while scanning...
```

**원인:**
- YAML 구문 오류

**해결:**
1. YAML 구문 검사:
   ```bash
   # 레거시
   python -c "import yaml; yaml.safe_load(open('config/sprint_config.yml'))"
   
   # 멀티 팀
   python -c "import yaml; yaml.safe_load(open('config/teams/synos/sprint_config.yml'))"
   ```
2. 들여쓰기 확인 (공백 사용, 탭 X)
3. 특수문자 이스케이프 확인

---

### 3.4 팀 설정 로드 실패 (워크플로우) - NEW!

**증상:**
```
Loading config for team: synos
grep: config/teams/synos/sprint_config.yml: No such file or directory
```

**원인:**
- 팀 설정 파일이 커밋되지 않음
- 파일 경로 오류

**해결:**
1. 파일이 Git에 커밋되었는지 확인:
   ```bash
   git status config/teams/
   git ls-files config/teams/
   ```

2. 커밋되지 않은 경우:
   ```bash
   git add config/teams/
   git commit -m "chore: add team configuration"
   git push
   ```

---

## 4. 데이터 문제

### 4.1 데이터 누락

**증상:**
- 일부 이슈/PR이 동기화되지 않음

**원인:**
1. 스프린트 필터에 해당하지 않음
2. GitHub Project에 추가되지 않음
3. 권한 문제

**확인 방법:**
```bash
# dry-run으로 수집되는 데이터 확인
# 레거시 모드
PYTHONPATH=. python scripts/complete_resync.py \
  --sprint-filter "25-12-Sprint1" \
  --dry-run

# 멀티 팀 모드
PYTHONPATH=. python scripts/complete_resync.py \
  --team synos \
  --dry-run
```

---

### 4.2 담당자 미표시

**증상:**
- Notion에서 담당자가 빈 값으로 표시

**원인:**
1. `field_mappings.yml`에 사용자 매핑 누락
2. Notion 사용자 ID가 잘못됨

**해결:**
1. 사용자 매핑 추가:
   ```yaml
   # config/field_mappings.yml 또는
   # config/teams/{team}/field_mappings.yml
   
   github_to_notion:
     assignees:
       value_mappings:
         "new-user": "notion-user-id"
   
   github_to_display_name:
     "new-user": "표시 이름"
   ```

2. Notion 사용자 ID 확인:
   ```bash
   python get_notion_users.py
   ```

---

### 4.3 상태/우선순위 미매핑

**증상:**
- Notion에서 상태/우선순위가 기본값으로 표시

**원인:**
- GitHub의 새 상태/우선순위 값이 매핑에 없음

**해결:**
`config/field_mappings.yml`에 새 매핑 추가:
```yaml
status:
  value_mappings:
    "New Status": "Notion 상태값"
```

---

## 5. 로컬 실행 문제

### 5.1 ImportError

**증상:**
```
ImportError: cannot import name 'xxx' from 'src.xxx'
```

**해결:**
```bash
# PYTHONPATH 설정 필수
PYTHONPATH=. python scripts/xxx.py
```

---

### 5.2 환경 변수 누락

**증상:**
```
KeyError: 'GH_TOKEN'
```

**해결:**
1. `.env` 파일 확인
2. 환경 변수 직접 설정:
   ```bash
   export GH_TOKEN="your-token"
   ```

---

### 5.3 의존성 오류

**증상:**
```
ModuleNotFoundError: No module named 'xxx'
```

**해결:**
```bash
pip install -r requirements.txt
```

---

### 5.4 팀 설정 모듈 없음 - NEW!

**증상:**
```
ModuleNotFoundError: No module named 'src.utils.team_config'
```

**원인:**
- 코드가 최신 버전이 아님

**해결:**
```bash
git pull origin main
pip install -r requirements.txt
```

---

## 6. 디버깅 팁

### 6.1 상세 로그 활성화

```bash
# LOG_LEVEL 설정
export LOG_LEVEL=DEBUG

# 또는 --quiet 제거
PYTHONPATH=. python scripts/xxx.py  # --quiet 없이
```

### 6.2 dry-run 사용

변경 없이 동작 확인:
```bash
# 레거시
PYTHONPATH=. python scripts/complete_resync.py --dry-run

# 멀티 팀
PYTHONPATH=. python scripts/complete_resync.py --team synos --dry-run
```

### 6.3 팀 설정 확인 - NEW!

```bash
PYTHONPATH=. python -c "
from src.utils.team_config import load_team_config, list_available_teams

# 사용 가능한 팀 목록
print('Available teams:', list_available_teams())

# 특정 팀 설정 확인
config = load_team_config('synos')
print(f'Team: {config.team_id}')
print(f'Sprint: {config.current_sprint}')
print(f'GitHub: {config.github_org}/{config.github_project_number}')
print(f'Daily Scrum Parent: {config.daily_scrum_parent_id}')
"
```

### 6.4 JSON 출력 저장

상세 데이터 분석:
```bash
PYTHONPATH=. python scripts/sprint_stats.py \
  --team synos \
  --output debug_stats.json \
  --dry-run
```

### 6.5 GitHub API 직접 테스트

```bash
# GraphQL 테스트
gh api graphql -f query='
query {
  organization(login: "ThakiCloud") {
    projectV2(number: 5) {
      title
      items(first: 10) {
        totalCount
      }
    }
  }
}'
```

### 6.6 Notion API 직접 테스트

```python
from notion_client import Client
notion = Client(auth="your-token")

# 데이터베이스 쿼리
result = notion.databases.query(database_id="your-db-id")
print(result)
```

---

## 7. 자주 묻는 질문 (FAQ)

### Q1: 특정 기능만 실행하고 싶어요

**A:** 수동 트리거에서 원하는 기능만 `true`로 설정:
```
team: synos
run_complete_resync: false
run_pr_review_check: true
run_sprint_stats: false
run_sprint_summary: false
run_daily_scrum: false
```

### Q2: AI 요약 없이 실행하고 싶어요

**A:** `--skip-summary` 옵션 사용 또는 `ANTHROPIC_API_KEY` 미설정

### Q3: 이전 스프린트 데이터를 동기화하고 싶어요

**A:** `--sprint` 옵션으로 이전 스프린트 이름 지정:
```bash
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --sprint "25-11-Sprint4"
```

### Q4: 새 팀원을 추가했는데 반영이 안 돼요

**A:** `config/field_mappings.yml` 또는 팀별 `field_mappings.yml`에 사용자 매핑 추가 후 커밋

### Q5: 워크플로우가 예약 시간에 실행되지 않아요

**A:** 
1. GitHub Actions가 비활성화되지 않았는지 확인
2. Repository가 60일 이상 비활성 상태인지 확인
3. `.github/workflows/` 디렉토리 권한 확인

### Q6: 새 팀을 추가하려면 어떻게 해요? - NEW!

**A:**
```bash
# 1. 템플릿 복사
cp -r config/teams/_template config/teams/newteam

# 2. 설정 수정
vim config/teams/newteam/sprint_config.yml

# 3. 커밋 & 푸시
git add config/teams/newteam/
git commit -m "chore: add newteam configuration"
git push

# 4. 테스트
PYTHONPATH=. python scripts/daily_scrum_sync.py --team newteam --dry-run
```

### Q7: 팀 간 설정을 공유하고 싶어요 - NEW!

**A:** `config/field_mappings.yml`에 공통 설정을 두고, 팀별로 필요한 경우만 `config/teams/{team}/field_mappings.yml`에서 오버라이드합니다.

---

## 8. 지원 요청

문제가 해결되지 않을 경우:

1. **로그 수집**
   - Actions 탭에서 실패한 워크플로우 로그
   - Artifacts의 로그 파일

2. **환경 정보**
   - Python 버전
   - 실행 환경 (GitHub Actions / 로컬)
   - 스프린트 이름
   - 팀 ID (멀티 팀 모드의 경우)

3. **이슈 생성**
   - GitHub Issues에 상세 정보와 함께 등록
   - 민감 정보(토큰 등) 제외

---

## 9. 복구 절차

### 9.1 Notion 데이터 복구

Complete Resync는 기존 데이터를 삭제합니다. 복구가 필요한 경우:

1. Notion의 휴지통 확인 (30일 이내)
2. 페이지 복원

### 9.2 워크플로우 롤백

이전 버전으로 롤백:
```bash
git revert HEAD  # 마지막 커밋 되돌리기
git push
```

### 9.3 설정 복구

설정 파일 이전 버전 확인:
```bash
# 레거시
git log --oneline config/sprint_config.yml
git show <commit-hash>:config/sprint_config.yml

# 멀티 팀
git log --oneline config/teams/synos/sprint_config.yml
git show <commit-hash>:config/teams/synos/sprint_config.yml
```

