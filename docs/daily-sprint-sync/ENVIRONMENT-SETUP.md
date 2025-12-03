# Environment Setup Guide

Daily Sprint Sync 시스템의 환경 설정 가이드입니다.

---

## 1. 필수 요구사항

### 1.1 시스템 요구사항

| 항목 | 요구사항 |
|------|----------|
| Python | 3.11 이상 |
| pip | 최신 버전 |
| Git | 최신 버전 |

### 1.2 외부 서비스

| 서비스 | 용도 | 필수 |
|--------|------|------|
| GitHub | 소스 데이터 | ✅ |
| Notion | 출력 대상 | ✅ |
| Anthropic (Claude) | AI 요약 | 선택 |

---

## 2. GitHub 설정

### 2.1 Personal Access Token (PAT) 생성

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**

2. **Generate new token (classic)** 클릭

3. 필요한 권한 선택:

| 권한 | 설명 | 필수 |
|------|------|------|
| `repo` | 프라이빗 레포 접근 | ✅ |
| `read:org` | 조직 정보 읽기 | ✅ |
| `read:project` | 프로젝트 읽기 | ✅ |
| `write:project` | 프로젝트 쓰기 | 선택 |

4. **Generate token** 클릭 후 토큰 복사

### 2.2 토큰 권한 요약

```
✅ repo (Full control of private repositories)
  ✅ repo:status
  ✅ repo_deployment
  ✅ public_repo
  ✅ repo:invite
  ✅ security_events

✅ read:org (Read org and team membership)

✅ read:project (Read access to projects)
```

### 2.3 GitHub Project 확인

1. Organization의 Projects 탭 확인
2. 프로젝트 번호 확인 (URL에서):
   ```
   https://github.com/orgs/ThakiCloud/projects/5
                                              ↑
                                        프로젝트 번호
   ```

---

## 3. Notion 설정

### 3.1 Integration 생성

1. [Notion Integrations](https://www.notion.so/my-integrations) 페이지 접속

2. **New integration** 클릭

3. 설정:
   - **Name**: `GitHub Sync` (또는 원하는 이름)
   - **Associated workspace**: 사용할 워크스페이스 선택
   - **Capabilities**:
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content

4. **Submit** 클릭

5. **Internal Integration Token** 복사 (secret_xxx...)

### 3.2 페이지에 Integration 연결

**각 대상 페이지/데이터베이스에 Integration 연결 필수!**

1. Notion에서 대상 페이지 열기
2. 우측 상단 **⋯** (더보기) 클릭
3. **Add connections** 클릭
4. 생성한 Integration 선택

### 3.3 연결해야 할 페이지 (팀별) - NEW!

각 팀마다 다음 페이지들에 Integration을 연결해야 합니다:

| 페이지 | 용도 | 설정 키 |
|--------|------|---------|
| Main Notion Database | Complete Resync 대상 | `notion.database_id` |
| PR-Checker 페이지 | PR Review, Stats DB 생성 위치 | `sprint.notion_parent_id` |
| SprintChecker 페이지 | Sprint Summary 페이지 생성 위치 | `sprint.sprint_checker_parent_id` |
| DailyScrum 페이지 | Daily Scrum 페이지 생성 위치 | `sprint.daily_scrum_parent_id` |

### 3.4 Database ID 확인

1. Notion에서 데이터베이스 페이지 열기
2. URL에서 ID 추출:
   ```
   https://www.notion.so/workspace/{database-id}?v=xxx
                                   ↑
                              Database ID
   ```

### 3.5 Page ID 확인

1. Notion에서 페이지 열기
2. **Share** → **Copy link**
3. URL에서 ID 추출:
   ```
   https://www.notion.so/workspace/Page-Title-{page-id}
                                              ↑
                                           Page ID
   ```

---

## 4. Anthropic (Claude) 설정 (선택)

### 4.1 API Key 생성

1. [Anthropic Console](https://console.anthropic.com/) 접속

2. **API Keys** 메뉴

3. **Create Key** 클릭

4. API Key 복사 (sk-ant-xxx...)

### 4.2 사용 모델

현재 사용 모델: `claude-sonnet-4-20250514`

### 4.3 비용 고려

- 요약 생성 당 약 1,500 토큰 사용
- 사용자 수 × 실행 횟수에 비례

---

## 5. GitHub Repository Secrets/Variables 설정

### 5.1 Secrets 설정

**Settings → Secrets and variables → Actions → Secrets → New repository secret**

| Name | Value | 설명 |
|------|-------|------|
| `GH_TOKEN` | `ghp_xxx...` | GitHub PAT |
| `NOTION_TOKEN` | `secret_xxx...` | Notion Integration Token |
| `ANTHROPIC_API_KEY` | `sk-ant-xxx...` | Claude API Key |

### 5.2 Variables 설정 (레거시 모드)

**Settings → Secrets and variables → Actions → Variables → New repository variable**

| Name | Value | 설명 |
|------|-------|------|
| `GH_ORG` | `ThakiCloud` | GitHub Organization |
| `GH_PROJECT_NUMBER` | `5` | GitHub Project 번호 |
| `NOTION_DB_ID` | `abc123...` | Notion Database ID |

> **Note:** 멀티 팀 모드에서는 이 Variables 대신 팀별 `sprint_config.yml`의 설정이 사용됩니다.

---

## 6. 로컬 개발 환경 설정

### 6.1 프로젝트 클론

```bash
git clone https://github.com/ThakiCloud/github-to-notion-sync.git
cd github-to-notion-sync
```

### 6.2 Python 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 활성화
source venv/bin/activate  # macOS/Linux
# 또는
.\venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 6.3 환경 변수 설정

#### 방법 1: .env 파일 사용

```bash
# .env 파일 생성
cat > .env << 'EOF'
GH_TOKEN=ghp_your_github_token
NOTION_TOKEN=secret_your_notion_token
GH_ORG=ThakiCloud
GH_PROJECT_NUMBER=5
NOTION_DB_ID=your_notion_database_id
GH_WEBHOOK_SECRET=dummy-for-local
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key
EOF
```

#### 방법 2: 환경 변수 직접 설정

```bash
export GH_TOKEN="ghp_your_github_token"
export NOTION_TOKEN="secret_your_notion_token"
export GH_ORG="ThakiCloud"
export GH_PROJECT_NUMBER="5"
export NOTION_DB_ID="your_notion_database_id"
export GH_WEBHOOK_SECRET="dummy-for-local"
export ANTHROPIC_API_KEY="sk-ant-your_anthropic_key"
```

### 6.4 설정 검증

```bash
# 환경 변수 확인
echo $GH_TOKEN
echo $NOTION_TOKEN
echo $GH_ORG

# 스크립트 dry-run 테스트
PYTHONPATH=. python scripts/complete_resync.py --dry-run
```

---

## 7. 멀티 팀 설정 - NEW!

### 7.1 팀별 설정 디렉토리 구조

```
config/
├── sprint_config.yml          # 레거시 설정 (하위 호환)
├── field_mappings.yml         # 공통 필드 매핑
└── teams/                     # 팀별 설정 디렉토리
    ├── synos/
    │   ├── sprint_config.yml  # Synos 팀 설정
    │   └── field_mappings.yml # Synos 팀 필드 매핑 (선택)
    ├── ragos/
    │   └── sprint_config.yml  # RagOS 팀 설정
    └── _template/
        └── sprint_config.yml  # 새 팀 추가용 템플릿
```

### 7.2 새 팀 추가하기

```bash
# 1. 템플릿 복사
cp -r config/teams/_template config/teams/newteam

# 2. 설정 수정
vim config/teams/newteam/sprint_config.yml
```

**필수 수정 항목:**
```yaml
team:
  id: "newteam"           # 디렉토리명과 일치
  name: "새팀"
  enabled: true

github:
  org: "YourOrganization"
  project_number: 10

sprint:
  current: "25-12-Sprint1"
  notion_parent_id: "your-pr-checker-page-id"
  sprint_checker_parent_id: "your-sprint-checker-page-id"
  daily_scrum_parent_id: "your-daily-scrum-page-id"
```

### 7.3 팀 설정 검증

```bash
# 팀 목록 확인
ls config/teams/

# 팀 설정 로드 테스트
PYTHONPATH=. python -c "
from src.utils.team_config import load_team_config, list_available_teams

# 사용 가능한 팀 목록
teams = list_available_teams()
print(f'Available teams: {teams}')

# 특정 팀 설정 확인
config = load_team_config('synos')
print(f'Team: {config.team_id} ({config.team_name})')
print(f'GitHub: {config.github_org}/{config.github_project_number}')
print(f'Sprint: {config.current_sprint}')
"

# 팀별 dry-run 테스트
PYTHONPATH=. python scripts/daily_scrum_sync.py --team synos --dry-run
```

### 7.4 팀별 사용자 매핑 추가

각 팀에서 사용하는 사용자 매핑을 추가합니다:

```bash
# 팀별 field_mappings.yml 생성 (선택)
vim config/teams/synos/field_mappings.yml
```

```yaml
# Synos 팀 전용 사용자 매핑
user_mappings:
  "sylvanus4": "12345678-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  "duyeol-yu": "23456789-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

github_to_display_name:
  "sylvanus4": "한효정"
  "duyeol-yu": "유두열"
```

---

## 8. 환경 변수 요약

### 8.1 필수 환경 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `GH_TOKEN` | GitHub Personal Access Token | `ghp_xxx...` |
| `NOTION_TOKEN` | Notion Integration Token | `secret_xxx...` |
| `GH_ORG` | GitHub Organization | `ThakiCloud` |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 | `5` |
| `NOTION_DB_ID` | Notion Database ID | `abc123...` |
| `GH_WEBHOOK_SECRET` | Webhook Secret (로컬: dummy) | `dummy` |

### 8.2 선택 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API Key | - |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |
| `NOTION_STATS_PARENT_ID` | Stats DB 부모 페이지 | - |
| `DEFAULT_TEAM` | 기본 팀 ID (NEW!) | - |

### 8.3 멀티 팀 모드 환경 변수 - NEW!

| 변수 | 설명 | 예시 |
|------|------|------|
| `DEFAULT_TEAM` | 기본 팀 ID | `synos` |
| `CONFIG_DIR` | 설정 디렉토리 경로 (오버라이드) | `/path/to/config` |

---

## 9. 권한 체크리스트

### 9.1 GitHub

- [ ] PAT에 `repo` 권한 있음
- [ ] PAT에 `read:org` 권한 있음
- [ ] PAT에 `read:project` 권한 있음
- [ ] Organization의 멤버임
- [ ] Project에 접근 권한 있음

### 9.2 Notion (팀별)

각 팀의 Notion 페이지에 대해:

- [ ] Integration 생성됨
- [ ] Integration Token 복사됨
- [ ] Main Database에 Integration 연결됨
- [ ] PR-Checker 페이지에 Integration 연결됨
- [ ] SprintChecker 페이지에 Integration 연결됨
- [ ] DailyScrum 페이지에 Integration 연결됨

### 9.3 GitHub Repository

- [ ] `GH_TOKEN` Secret 설정됨
- [ ] `NOTION_TOKEN` Secret 설정됨
- [ ] `ANTHROPIC_API_KEY` Secret 설정됨 (선택)
- [ ] `GH_ORG` Variable 설정됨 (레거시)
- [ ] `GH_PROJECT_NUMBER` Variable 설정됨 (레거시)
- [ ] `NOTION_DB_ID` Variable 설정됨 (레거시)

### 9.4 팀 설정 파일 - NEW!

각 팀에 대해:

- [ ] `config/teams/{team}/sprint_config.yml` 존재
- [ ] `team.id` 설정됨
- [ ] `github.org` 및 `github.project_number` 설정됨
- [ ] `sprint.current` 설정됨
- [ ] `sprint.notion_parent_id` 설정됨
- [ ] `sprint.sprint_checker_parent_id` 설정됨
- [ ] `sprint.daily_scrum_parent_id` 설정됨

---

## 10. 보안 주의사항

### 10.1 토큰 관리

- ⚠️ 토큰을 코드에 하드코딩하지 마세요
- ⚠️ 토큰을 Git에 커밋하지 마세요
- ⚠️ `.env` 파일은 `.gitignore`에 포함되어야 합니다
- ⚠️ 팀별 설정 파일에 토큰을 저장하지 마세요

### 10.2 토큰 갱신

- GitHub PAT: 만료 전 갱신 필요 (기본 90일)
- Notion Token: 만료 없음 (단, Integration 삭제 시 무효화)
- Anthropic API Key: 만료 없음

### 10.3 권한 최소화

- 필요한 최소 권한만 부여
- 읽기 전용으로 충분한 경우 쓰기 권한 제외

---

## 11. 문제 해결

### 11.1 GitHub 401 Unauthorized

```
원인: GH_TOKEN이 유효하지 않거나 만료됨
해결: 새 PAT 생성 후 교체
```

### 11.2 Notion 404 Not Found

```
원인: 
1. NOTION_DB_ID/Page ID가 잘못됨
2. Integration이 페이지에 연결되지 않음

해결:
1. ID 다시 확인
2. 해당 페이지에서 Integration 연결 확인
```

### 11.3 팀 설정 로드 실패 - NEW!

```
원인: 
1. config/teams/{team}/ 디렉토리 없음
2. sprint_config.yml 파일 없음
3. YAML 구문 오류

해결:
1. 디렉토리 존재 확인
2. 파일 존재 확인
3. YAML 구문 검사:
   python -c "import yaml; yaml.safe_load(open('config/teams/synos/sprint_config.yml'))"
```

### 11.4 Anthropic API Error

```
원인: ANTHROPIC_API_KEY가 유효하지 않거나 잔액 부족
해결: Console에서 키 확인 및 잔액 확인
```

자세한 문제 해결은 [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)를 참조하세요.

