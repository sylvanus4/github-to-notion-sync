# GitHub Workflow Commands Reference

SKILL.md의 각 Step에서 사용하는 상세 명령어 모음.

---

## Step A: 이슈 생성 + 프로젝트 설정

### A-1. 이슈 생성

```bash
gh issue create \
  --title "이슈 제목 (한글)" \
  --body "이슈 내용" \
  --assignee @me
```

### A-2. 프로젝트에 추가 (Project ID: 22)

```bash
gh project item-add 5 --owner ThakiCloud --url [이슈URL]
```

### A-3. 프로젝트 필드 설정

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

필드 ID 조회 (최초 1회):

```bash
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
```

필드 값 설정:

```bash
gh project item-edit --id $ITEM_ID --field-id $FIELD_ID --single-select-option-id $OPTION_ID --project-id $PROJECT_ID
```

---

## Step C: 이슈 내용 업데이트

```bash
BRANCH=$(git branch --show-current)
ISSUE_NUMBER=$(echo $BRANCH | sed 's/issue\/\([0-9]*\).*/\1/')

gh issue view $ISSUE_NUMBER
gh issue edit $ISSUE_NUMBER --body "업데이트된 내용"
```

---

## Step D: Pre-commit → 커밋 → 푸시 → PR

### D-0. Pre-commit

```bash
pre-commit run --all-files
# 실패 시: git add . → 재실행 반복
```

### D-1. 커밋 생성

```bash
git add .
git commit -m "$(cat <<'EOF'
feat: add user authentication

- GitHub OAuth 2.0 PKCE 플로우 구현
- JWT 토큰 기반 인증 미들웨어 추가
EOF
)"
```

scope 포함:

```bash
git commit -m "$(cat <<'EOF'
feat(auth): add user authentication

- GitHub OAuth 2.0 PKCE 플로우 구현
EOF
)"
```

### D-2. 푸시

```bash
git push -u origin $(git branch --show-current)
```

### D-3. PR 확인 및 생성/업데이트

PR 존재 여부 확인:

```bash
EXISTING_PR=$(gh pr list --head $(git branch --show-current) --json number,url --jq '.[0]')
```

**기존 PR 업데이트** (PR이 이미 있을 때):

```bash
PR_NUMBER=$(gh pr list --head $(git branch --show-current) --json number --jq '.[0].number')

gh pr edit $PR_NUMBER --body "$(cat <<EOF
## Issue?
Resolves #${ISSUE_NUMBER}

## Changes?
- 기존 변경사항 1
- **[NEW]** 새로 추가된 변경사항

## Why we need?
이 PR이 필요한 이유

## Test?
- [x] 완료된 테스트
- [ ] 남은 테스트

## CC (Optional)
<!-- 사용자가 직접 멘션 예정 -->

## Anything else? (Optional)
EOF
)"
```

**새 PR 생성** (PR이 없을 때):

```bash
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
- 변경사항

## Why we need?
이유

## Test?
- [ ] 테스트 항목

## CC (Optional)
## Anything else? (Optional)
EOF
)" --base $TARGET_BRANCH --head $CURRENT_BRANCH --assignee @me
```

### D-4. 이슈 진행 상황 코멘트

```bash
BRANCH=$(git branch --show-current)
ISSUE_NUMBER=$(echo $BRANCH | sed 's/issue\/\([0-9]*\).*/\1/')
COMMIT_SHA=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=format:'%s')
PR_INFO=$(gh pr list --head $BRANCH --json number,url --jq '.[0]')
PR_NUMBER=$(echo $PR_INFO | jq -r '.number // empty')
PR_URL=$(echo $PR_INFO | jq -r '.url // empty')

gh issue comment $ISSUE_NUMBER --body "$(cat <<EOF
## 📝 진행 상황 업데이트

### 커밋
- **SHA**: \`$COMMIT_SHA\`
- **메시지**: $COMMIT_MSG

### PR
- **PR**: #$PR_NUMBER ($PR_URL)

### 상태
- [x] 코드 변경 완료
- [x] 커밋 & 푸시 완료
- [x] PR 생성/업데이트 완료
- [ ] 리뷰 대기 중

---
_자동 생성된 코멘트입니다._
EOF
)"
```

### D-5. 이슈 상태 업데이트 (선택적)

```bash
ITEM_ID=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      projectItems(first: 10) {
        nodes { id project { number } }
      }
    }
  }
}' -f owner='ThakiCloud' -f repo='ai-platform-webui' -F issueNumber=$ISSUE_NUMBER \
  | jq -r '.data.repository.issue.projectItems.nodes[] | select(.project.number == 5) | .id')
```

---

## 완료 보고 템플릿

```
✅ GitHub 워크플로우 완료

## 📋 이슈
- #{NUMBER} {제목}
- URL: https://github.com/ThakiCloud/ai-platform-webui/issues/{NUMBER}

## ⚙️ 프로젝트 설정
- Priority: P0 | Size: {XS~XL} | Estimate: {0.5~8} | Sprint: {현재}

## 🔀 브랜치
- {브랜치명}

## ✅ Pre-commit: Passed ({N}/{N})

## 📝 커밋
- {커밋 메시지} (SHA: {short})

## 🔗 PR
- #{PR_NUMBER} | Base: dev ← Head: {브랜치명} | Squash merge

## 💬 이슈 #${NUMBER}에 진행 상황 코멘트 추가됨
```
