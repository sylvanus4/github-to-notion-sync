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

### 3.3 연결해야 할 페이지

| 페이지 | 용도 |
|--------|------|
| Main Notion Database | Complete Resync 대상 |
| PR-Checker 페이지 | PR Review, Stats DB 생성 위치 |
| SprintChecker 페이지 | Sprint Summary 페이지 생성 위치 |
| DailyScrum 페이지 | Daily Scrum 페이지 생성 위치 |

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

### 5.2 Variables 설정

**Settings → Secrets and variables → Actions → Variables → New repository variable**

| Name | Value | 설명 |
|------|-------|------|
| `GH_ORG` | `ThakiCloud` | GitHub Organization |
| `GH_PROJECT_NUMBER` | `5` | GitHub Project 번호 |
| `NOTION_DB_ID` | `abc123...` | Notion Database ID |

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

## 7. 환경 변수 요약

### 7.1 필수 환경 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `GH_TOKEN` | GitHub Personal Access Token | `ghp_xxx...` |
| `NOTION_TOKEN` | Notion Integration Token | `secret_xxx...` |
| `GH_ORG` | GitHub Organization | `ThakiCloud` |
| `GH_PROJECT_NUMBER` | GitHub Project 번호 | `5` |
| `NOTION_DB_ID` | Notion Database ID | `abc123...` |
| `GH_WEBHOOK_SECRET` | Webhook Secret (로컬: dummy) | `dummy` |

### 7.2 선택 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API Key | - |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |
| `NOTION_STATS_PARENT_ID` | Stats DB 부모 페이지 | - |

---

## 8. 권한 체크리스트

### 8.1 GitHub

- [ ] PAT에 `repo` 권한 있음
- [ ] PAT에 `read:org` 권한 있음
- [ ] PAT에 `read:project` 권한 있음
- [ ] Organization의 멤버임
- [ ] Project에 접근 권한 있음

### 8.2 Notion

- [ ] Integration 생성됨
- [ ] Integration Token 복사됨
- [ ] Main Database에 Integration 연결됨
- [ ] PR-Checker 페이지에 Integration 연결됨
- [ ] SprintChecker 페이지에 Integration 연결됨
- [ ] DailyScrum 페이지에 Integration 연결됨

### 8.3 GitHub Repository

- [ ] `GH_TOKEN` Secret 설정됨
- [ ] `NOTION_TOKEN` Secret 설정됨
- [ ] `ANTHROPIC_API_KEY` Secret 설정됨 (선택)
- [ ] `GH_ORG` Variable 설정됨
- [ ] `GH_PROJECT_NUMBER` Variable 설정됨
- [ ] `NOTION_DB_ID` Variable 설정됨

---

## 9. 보안 주의사항

### 9.1 토큰 관리

- ⚠️ 토큰을 코드에 하드코딩하지 마세요
- ⚠️ 토큰을 Git에 커밋하지 마세요
- ⚠️ `.env` 파일은 `.gitignore`에 포함되어야 합니다

### 9.2 토큰 갱신

- GitHub PAT: 만료 전 갱신 필요 (기본 90일)
- Notion Token: 만료 없음 (단, Integration 삭제 시 무효화)
- Anthropic API Key: 만료 없음

### 9.3 권한 최소화

- 필요한 최소 권한만 부여
- 읽기 전용으로 충분한 경우 쓰기 권한 제외

---

## 10. 문제 해결

### 10.1 GitHub 401 Unauthorized

```
원인: GH_TOKEN이 유효하지 않거나 만료됨
해결: 새 PAT 생성 후 교체
```

### 10.2 Notion 404 Not Found

```
원인: 
1. NOTION_DB_ID/Page ID가 잘못됨
2. Integration이 페이지에 연결되지 않음

해결:
1. ID 다시 확인
2. 해당 페이지에서 Integration 연결 확인
```

### 10.3 Anthropic API Error

```
원인: ANTHROPIC_API_KEY가 유효하지 않거나 잔액 부족
해결: Console에서 키 확인 및 잔액 확인
```

자세한 문제 해결은 [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)를 참조하세요.

