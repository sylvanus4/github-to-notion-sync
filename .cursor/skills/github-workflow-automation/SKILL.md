---
name: github-workflow-automation
description: ai-platform-webui 레포지토리의 GitHub 워크플로우를 자동화합니다. 변경사항 확인 → 이슈 생성 → 브랜치 생성 → 커밋 → 푸시 → PR 생성/업데이트 → 이슈 코멘트 추가까지 전체 흐름을 처리합니다. 기존 PR이 있으면 자동으로 업데이트하고, 이슈에 진행 상황 코멘트를 남깁니다. "이슈 만들어줘", "커밋해줘", "PR 생성해줘", "변경사항 정리해줘", "깃 워크플로우" 등 GitHub 관련 작업 요청 시 사용합니다.
---

# GitHub 워크플로우 자동화

ai-platform-webui 레포지토리의 GitHub 워크플로우를 자동화합니다.

## 워크플로우 개요

```
변경사항 확인 → 적합한 브랜치인가?
    │
    ├── YES (issue/XXX 브랜치) → C로 이동
    │       ↓
    │   이슈 업데이트 → pre-commit → 커밋 → 푸시
    │       ↓
    │   PR 존재? ─┬─ YES → PR 본문 업데이트 → 이슈 코멘트 추가
    │             └─ NO → PR 생성 → 이슈 코멘트 추가
    │
    └── NO → A로 이동
            ↓
        이슈 생성 → 브랜치 생성 → pre-commit → 커밋 → 푸시 → PR 생성 → 이슈 코멘트 추가
```

## 실행 순서

### Step 0: 현재 상태 확인

```bash
# 1. 현재 브랜치 확인
git branch --show-current

# 2. 변경사항 확인 (staged + unstaged)
git status

# 3. 커밋 히스토리 확인
git log --oneline -5
```

**브랜치 판단 기준**:

- `issue/{NUMBER}-{SUMMARY}` 형태 → 적합한 이슈 브랜치 → **Step C로 이동**
- `dev`, `main`, 기타 → 이슈 브랜치 필요 → **Step A로 이동**

---

### Step A: 이슈 생성 (브랜치가 없을 때)

#### A-1. 이슈 생성

```bash
gh issue create \
  --title "이슈 제목 (한글)" \
  --body "이슈 내용" \
  --assignee @me
```

#### A-2. 프로젝트에 추가 (Project ID: 5)

```bash
gh project item-add 5 --owner ThakiCloud --url [이슈URL]
```

#### A-3. 프로젝트 필드 설정

프로젝트 아이템 ID 조회:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      projectItems(first: 10) {
        nodes {
          id
          project { number }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -f repo='ai-platform-webui' -F issueNumber=$ISSUE_NUMBER
```

필드 설정 (Priority/Size/Estimate/Sprint):

```bash
# 프로젝트 필드 ID 조회 (최초 1회)
gh api graphql -f query='
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      fields(first: 50) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
          ... on ProjectV2IterationField {
            id
            name
            configuration {
              iterations { id title startDate }
            }
          }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -F number=5

# 필드 값 설정
gh project item-edit --id $ITEM_ID --field-id $FIELD_ID --single-select-option-id $OPTION_ID --project-id $PROJECT_ID
```

**필드 설정 규칙**:

- **Priority**: P0 (기본값)
- **Size**: XS/S/M/L/XL (변경사항 규모에 따라 AI가 결정)
- **Estimate**: 피보나치 스케일 (0.5, 1, 2, 3, 5, 8) - 1일 = 1 기준, AI를 활용한 개발 시 예상 소요일
- **Sprint/Iteration**: 오늘 날짜가 속한 현재 스프린트 선택

---

### Step B: 브랜치 생성

```bash
# dev 브랜치에서 새 브랜치 생성
git checkout dev
git pull origin tmp
git checkout -b issue/{ISSUE_NUMBER}-{summary}
```

**브랜치 네이밍**:

- 형식: `issue/{NUMBER}-{SUMMARY}`
- 예시: `issue/123-add-auth`, `issue/456-fix-login-bug`

---

### Step C: 이슈 내용 업데이트 (기존 브랜치일 때)

```bash
# 현재 브랜치에서 이슈 번호 추출
BRANCH=$(git branch --show-current)
ISSUE_NUMBER=$(echo $BRANCH | sed 's/issue\/\([0-9]*\).*/\1/')

# 이슈 내용 조회
gh issue view $ISSUE_NUMBER

# 변경사항 기반으로 이슈 본문 업데이트
gh issue edit $ISSUE_NUMBER --body "업데이트된 내용"
```

---

### Step D: Pre-commit → 커밋 → 푸시 → PR 생성

#### D-0. Pre-commit 체크 (필수)

커밋 전 코드 품질 검사를 수행합니다.

```bash
# pre-commit 전체 파일 검사
pre-commit run --all-files
```

**실패 시 처리**:

- 자동 수정된 파일이 있으면 → 다시 `git add .` 후 재검사
- 에러가 있으면 → 에러 수정 후 재검사
- 모든 검사 통과 시 → D-1로 진행

```bash
# 실패 시 반복 패턴
pre-commit run --all-files
# 실패하면...
git add .  # 자동 수정된 파일 스테이징
pre-commit run --all-files  # 재검사
# 통과할 때까지 반복
```

**주의**: pre-commit이 통과하지 않으면 커밋하지 않습니다.

---

#### D-1. 커밋 생성

**커밋 메시지 형식** (Conventional Commits):

```
<type>: <summary>

- <상세 내용 1>
- <상세 내용 2>
- <상세 내용 3>
```

**또는 scope 포함**:

```
<type>(<scope>): <summary>

- <상세 내용 1>
- <상세 내용 2>
```

**타입**:
| 타입 | 설명 |
|------|------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 코드 포맷팅 (로직 변경 없음) |
| `refactor` | 코드 리팩토링 |
| `perf` | 성능 개선 |
| `test` | 테스트 코드 |
| `build` | 빌드 시스템/외부 의존성 변경 |
| `ci` | CI 설정 변경 |
| `chore` | 기타 변경 (툴링, 설정 등) |
| `revert` | 이전 커밋 되돌리기 |

**scope 예시**: `auth`, `api`, `ui`, `kfp`, `storage`, `inference`, `ml-studio`, `pipeline`

**작성 규칙**:

- summary: **50자 이내, 영어 소문자 명령문, 마침표 없음**
- details: 72자마다 줄바꿈, 한글/영어 가능

```bash
git add .
git commit -m "$(cat <<'EOF'
feat: add user authentication

- GitHub OAuth 2.0 PKCE 플로우 구현
- JWT 토큰 기반 인증 미들웨어 추가
- 사용자 세션 관리 기능
EOF
)"

# scope 포함 예시
git commit -m "$(cat <<'EOF'
feat(auth): add user authentication

- GitHub OAuth 2.0 PKCE 플로우 구현
- JWT 토큰 기반 인증 미들웨어 추가
EOF
)"
```

#### D-2. 푸시

```bash
git push origin HEAD:tmp
```

#### D-3. PR 확인 및 생성/업데이트

**PR 존재 여부 확인**:

```bash
# tmp 브랜치의 PR 조회
EXISTING_PR=$(gh pr list --head tmp --json number,url --jq '.[0]')

if [ -n "$EXISTING_PR" ]; then
  echo "✅ 기존 PR 발견: $(echo $EXISTING_PR | jq -r '.url')"
  # → D-3a. PR 업데이트로 이동
else
  echo "📝 새 PR 생성 필요"
  # → D-3b. PR 생성으로 이동
fi
```

---

##### D-3a. 기존 PR 업데이트 (PR이 이미 있을 때)

```bash
# PR 번호 추출
PR_NUMBER=$(gh pr list --head tmp --json number --jq '.[0].number')

# PR 본문에 새 변경사항 추가
# 방법 1: 기존 본문 유지하면서 Changes 섹션만 업데이트
gh pr view $PR_NUMBER --json body --jq '.body' > /tmp/pr_body.md

# 방법 2: 전체 본문 교체 (권장)
gh pr edit $PR_NUMBER --body "$(cat <<EOF
## Issue?
Resolves #${ISSUE_NUMBER}

## Changes?
- 기존 변경사항 1
- 기존 변경사항 2
- **[NEW]** 새로 추가된 변경사항

## Why we need?
이 PR이 필요한 이유 설명

## Test?
- [x] 완료된 테스트
- [ ] 남은 테스트 항목

## CC (Optional)
<!-- 사용자가 직접 멘션 예정 -->

## Anything else? (Optional)
- 추가 커밋: {커밋 메시지}
EOF
)"

echo "✅ PR #$PR_NUMBER 본문 업데이트 완료"
```

---

##### D-3b. 새 PR 생성 (PR이 없을 때)

**PR 제목 형식**: `#<ISSUE_NUMBER> <type>: <summary>`

**타겟 브랜치 결정** (브랜치명에 따라 동적 결정):

- `issue/*` → `dev`
- `epic/*` → `dev`
- `release-*` → `main`

```bash
# 타겟 브랜치 동적 결정
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" == release-* ]]; then
  TARGET_BRANCH="main"
else
  TARGET_BRANCH="dev"
fi

gh pr create --title "#${ISSUE_NUMBER} <type>: <summary>" --body "$(cat <<EOF
## Issue?
Resolves #${ISSUE_NUMBER}

## Changes?
- 변경사항 1
- 변경사항 2

## Why we need?
이 PR이 필요한 이유 설명

## Test?
- [ ] 테스트 항목 1
- [ ] 테스트 항목 2

## CC (Optional)
<!-- 사용자가 직접 멘션 예정 -->

## Anything else? (Optional)
<!-- 추가 정보 -->
EOF
)" --base $TARGET_BRANCH --head tmp --assignee @me
```

---

#### D-4. 이슈 업데이트 (진행 상황 코멘트 추가)

커밋/PR 작업 후 관련 이슈에 진행 상황을 코멘트로 남깁니다.

```bash
# 이슈 번호 추출 (브랜치명에서)
BRANCH=$(git branch --show-current)
ISSUE_NUMBER=$(echo $BRANCH | sed 's/issue\/\([0-9]*\).*/\1/')

# 최근 커밋 정보
COMMIT_SHA=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=format:'%s')

# PR 정보 (있으면)
PR_INFO=$(gh pr list --head tmp --json number,url --jq '.[0]')
PR_NUMBER=$(echo $PR_INFO | jq -r '.number // empty')
PR_URL=$(echo $PR_INFO | jq -r '.url // empty')

# 이슈에 진행 상황 코멘트 추가
if [ -n "$PR_NUMBER" ]; then
  gh issue comment $ISSUE_NUMBER --body "$(cat <<EOF
## 📝 진행 상황 업데이트

### 커밋
- **SHA**: \`$COMMIT_SHA\`
- **메시지**: $COMMIT_MSG

### PR
- **PR**: #$PR_NUMBER
- **URL**: $PR_URL

### 상태
- [x] 코드 변경 완료
- [x] 커밋 & 푸시 완료
- [x] PR 생성/업데이트 완료
- [ ] 리뷰 대기 중

---
_자동 생성된 코멘트입니다._
EOF
)"
  echo "✅ 이슈 #$ISSUE_NUMBER에 진행 상황 코멘트 추가됨"
else
  gh issue comment $ISSUE_NUMBER --body "$(cat <<EOF
## 📝 진행 상황 업데이트

### 커밋
- **SHA**: \`$COMMIT_SHA\`
- **메시지**: $COMMIT_MSG

### 상태
- [x] 코드 변경 완료
- [x] 커밋 & 푸시 완료
- [ ] PR 생성 필요

---
_자동 생성된 코멘트입니다._
EOF
)"
  echo "✅ 이슈 #$ISSUE_NUMBER에 진행 상황 코멘트 추가됨 (PR 미생성)"
fi
```

**코멘트 추가 타이밍**:

- 커밋 & 푸시 완료 후
- PR 생성/업데이트 후
- 중요한 마일스톤 달성 시

---

#### D-5. 이슈 상태 업데이트 (선택적)

PR이 생성되면 프로젝트 보드의 Status를 업데이트합니다.

```bash
# 이슈의 프로젝트 아이템 ID 조회
ITEM_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      projectItems(first: 10) {
        nodes {
          id
          project { number }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -f repo='ai-platform-webui' -F issueNumber=$ISSUE_NUMBER \
  | jq -r '.data.repository.issue.projectItems.nodes[] | select(.project.number == 5) | .id')

if [ -n "$ITEM_ID" ] && [ "$ITEM_ID" != "null" ]; then
  # Status를 "In Review"로 변경 (필드 ID와 옵션 ID는 프로젝트 설정에서 조회)
  # gh project item-edit --id $ITEM_ID --field-id $STATUS_FIELD_ID --single-select-option-id $IN_REVIEW_OPTION_ID --project-id $PROJECT_ID
  echo "📊 프로젝트 상태 업데이트 필요: Status → In Review"
fi
```

---

## 완료 보고 템플릿

```
✅ GitHub 워크플로우 완료

## 📋 이슈
- #{NUMBER} {제목}
- URL: https://github.com/ThakiCloud/ai-platform-webui/issues/{NUMBER}

## ⚙️ 프로젝트 설정
- Priority: P0
- Size: {XS/S/M/L/XL}
- Estimate: {0.5/1/2/3/5/8}
- Sprint: {현재 스프린트}

## 🔀 브랜치
- {브랜치명}

## ✅ Pre-commit
- 상태: Passed
- 검사 항목: {통과한 검사 수}/{전체 검사 수}

## 📝 커밋
- {커밋 메시지 제목}
- SHA: {커밋 SHA}

## 🔗 PR
- #{PR_NUMBER} {PR 제목}
- URL: {PR URL}
- Base: dev ← Head: {브랜치명}
- 머지 전략: Squash
- 상태: {신규 생성 / 기존 PR 업데이트}

## 💬 이슈 업데이트
- 이슈 #${NUMBER}에 진행 상황 코멘트 추가됨
- 프로젝트 상태: {Todo → In Progress / In Progress → In Review}
```

---

## 주의사항

1. **Pre-commit 필수**: 커밋 전 반드시 `pre-commit run --all-files` 통과 확인
2. **이슈 번호 확인**: 브랜치에서 이슈 번호를 정확히 추출
3. **프로젝트 ID**: ThakiCloud 프로젝트 **#5** 사용
4. **Priority**: 기본값 P0, Epic 하위면 Epic의 Priority 상속
5. **Sprint**: 오늘 날짜 기준 현재 활성 스프린트 지정
6. **커밋 형식**: Conventional Commits - `<type>: <summary>` (소문자, 50자 이내)
7. **PR 타겟**: issue/\* 브랜치는 항상 dev로
8. **PR 제목**: `#<ISSUE_NUMBER> <type>: <summary>` 형식
9. **PR 업데이트**: 기존 PR이 있으면 새로 생성하지 않고 본문 업데이트
10. **이슈 코멘트**: 커밋/PR 후 이슈에 진행 상황 코멘트 추가
11. **상태 동기화**: PR 생성 시 프로젝트 보드 Status도 업데이트

---

## 세부 가이드 (필요시 참조)

더 상세한 내용은 아래 가이드 참조 (curl로 조회):

- GitHub PR 자동화: `curl -L -s "https://r.jina.ai/https://thakicloud.notion.site/GitHub-PR-2549eddc34e6801d9804da9c590acabf"`
- GitHub 이슈 자동화: `curl -L -s "https://r.jina.ai/https://thakicloud.notion.site/GitHub-2549eddc34e6808ebbede86dc44e968f"`
- GitHub 커밋 자동화: `curl -L -s "https://r.jina.ai/https://thakicloud.notion.site/Github-2639eddc34e6806a8b8bdfc0e4593c02"`
