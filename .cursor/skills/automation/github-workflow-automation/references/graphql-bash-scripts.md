# GitHub Workflow GraphQL and Bash Scripts

## Project Item ID Query

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
}' -f owner='ThakiCloud' -f repo='ai-platform-strategy' -F issueNumber=$ISSUE_NUMBER
```

## Project Field ID Query (one-time)

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

## Field Value Setting

```bash
gh project item-edit --id $ITEM_ID --field-id $FIELD_ID --single-select-option-id $OPTION_ID --project-id $PROJECT_ID
```

## PR Check and Update

```bash
EXISTING_PR=$(gh pr list --head tmp --json number,url --jq '.[0]')
PR_NUMBER=$(gh pr list --head tmp --json number --jq '.[0].number')

gh pr edit $PR_NUMBER --body "$(cat <<EOF
## Issue?
Resolves #${ISSUE_NUMBER}
## Changes?
- 기존 변경사항 1
- **[NEW]** 새로 추가된 변경사항
...
EOF
)"
```

## Issue Comment Template

```bash
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
- [ ] 리뷰 대기 중
---
_자동 생성된 코멘트입니다._
EOF
)"
```

## Status Update (Project Item)

```bash
ITEM_ID=$(gh api graphql -f query='...' | jq -r '.data.repository.issue.projectItems.nodes[] | select(.project.number == 5) | .id')
gh project item-edit --id $ITEM_ID --field-id $STATUS_FIELD_ID --single-select-option-id $IN_REVIEW_OPTION_ID --project-id $PROJECT_ID
```
