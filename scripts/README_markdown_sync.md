# GitHub Markdown to Notion Sync Script

이 스크립트는 GitHub 저장소의 특정 markdown 파일을 Notion 페이지에 동기화하는 도구입니다.

## 🚀 사용법

### 📚 사용 예시 보기

```bash
# 모든 사용 예시를 한번에 보기
python3 scripts/sync_markdown_to_notion.py --examples
```

### 기본 사용법

```bash
# README.md를 Notion 페이지에 싱크
python3 scripts/sync_markdown_to_notion.py \
  --owner ThakiCloud \
  --repo my-repo \
  --file README.md \
  --page-id your-notion-page-id

EX) 
python3 scripts/sync_markdown_to_notion.py \
    --owner ThakiCloud \
    --repo ai-platform-webui \
    --file docs/onboarding/development-guide.md \
    --page-id 2629eddc-34e6-8030-9921-e30907ac0031 \
    --branch dev \
    --title "Development Guide"
```

### 고급 사용법

```bash
# 특정 브랜치에서 파일 싱크
python3 scripts/sync_markdown_to_notion.py \
  --owner ThakiCloud \
  --repo my-repo \
  --file docs/guide.md \
  --page-id your-notion-page-id \
  --branch develop \
  --title "Development Guide"

# 기존 내용에 추가 (교체하지 않음)
python3 scripts/sync_markdown_to_notion.py \
  --owner ThakiCloud \
  --repo my-repo \
  --file CHANGELOG.md \
  --page-id your-notion-page-id \
  --no-replace

# Dry-run 모드 (실제 변경 없이 확인만)
python3 scripts/sync_markdown_to_notion.py \
  --owner ThakiCloud \
  --repo my-repo \
  --file README.md \
  --page-id your-notion-page-id \
  --dry-run
```

## 📋 필수 환경 변수

스크립트를 실행하기 전에 다음 환경 변수들을 설정해야 합니다:

```bash
# 필수 환경 변수
export NOTION_TOKEN="your-notion-integration-token"
export GITHUB_TOKEN="your-github-personal-access-token"
```

### 환경 변수 설명

- **NOTION_TOKEN**: Notion Integration Token (필수)
  - Notion에서 Integration을 생성하고 페이지에 연결해야 합니다
- **GITHUB_TOKEN**: GitHub Personal Access Token (필수)
  - `repo` 권한이 있는 토큰이 필요합니다

### 선택적 환경 변수

다음 환경 변수들은 전체 동기화 시스템에서만 필요하며, markdown 싱크 스크립트에는 필요하지 않습니다:

```bash
# 선택적 환경 변수 (전체 시스템용)
export NOTION_DB_ID="your-notion-database-id"
export GH_ORG="your-github-organization"
export GH_PROJECT_NUMBER="your-project-number"
export GH_WEBHOOK_SECRET="your-webhook-secret"
```

## 🔧 매개변수 설명

| 매개변수 | 설명 | 필수 | 기본값 |
|---------|------|------|--------|
| `--owner`, `-o` | GitHub 저장소 소유자 | ✅ | - |
| `--repo`, `-r` | 저장소 이름 | ✅ | - |
| `--file`, `-f` | Markdown 파일 경로 | ✅ | - |
| `--page-id`, `-p` | Notion 페이지 ID | ✅ | - |
| `--branch`, `-b` | GitHub 브랜치 이름 | ❌ | `main` |
| `--title`, `-t` | 콘텐츠 섹션 제목 | ❌ | 없음 |
| `--no-replace` | 기존 내용에 추가 | ❌ | `false` (교체) |
| `--dry-run` | 실제 변경 없이 확인만 | ❌ | `false` |

## 📝 지원하는 Markdown 기능

- **제목** (H1, H2, H3)
- **코드 블록** (언어 지정 가능)
- **불릿 리스트**
- **번호 리스트**
- **일반 텍스트**

## ⚠️ 주의사항

1. **Notion 페이지 ID**: Notion 페이지의 URL에서 32자리 ID를 추출해야 합니다.
   - 예: `https://notion.so/your-page-id-32chars` → `your-page-id-32chars`

2. **GitHub 토큰**: `repo` 권한이 있는 Personal Access Token이 필요합니다.

3. **Notion 토큰**: 해당 페이지에 대한 쓰기 권한이 있는 Integration Token이 필요합니다.

4. **파일 경로**: GitHub 저장소의 루트부터의 상대 경로를 사용합니다.
   - 예: `README.md`, `docs/guide.md`, `src/README.md`

## 🔍 문제 해결

### 환경 변수 오류
```
❌ Error: Required modules not available.
```
→ 모든 필수 환경 변수가 설정되었는지 확인하세요.

### GitHub API 오류
```
Failed to fetch markdown from GitHub: 404 Not Found
```
→ 저장소 이름, 파일 경로, 브랜치 이름이 올바른지 확인하세요.

### Notion API 오류
```
Failed to sync markdown to Notion page: 401 Unauthorized
```
→ Notion 토큰이 유효하고 해당 페이지에 대한 권한이 있는지 확인하세요.

## 📊 실행 결과

스크립트 실행 후 다음과 같은 통계가 표시됩니다:

```
==================================================
MARKDOWN SYNC STATISTICS
==================================================
Markdown fetched: ✅
Notion page updated: ✅
Duration: 2.34 seconds
==================================================
```

## 🎯 사용 사례

1. **문서 동기화**: GitHub README를 Notion 위키에 자동 동기화
2. **릴리즈 노트**: CHANGELOG.md를 Notion 페이지에 업데이트
3. **API 문서**: GitHub의 API 문서를 Notion에 동기화
4. **가이드 문서**: 개발 가이드를 Notion에 실시간 반영
