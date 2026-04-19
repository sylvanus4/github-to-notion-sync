# GitHub GraphQL API 레퍼런스

## 프로젝트 필드 조회

### 전체 필드 및 옵션 조회

```bash
gh api graphql -f query='
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      title
      fields(first: 50) {
        nodes {
          ... on ProjectV2Field {
            id
            name
            dataType
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            dataType
            options {
              id
              name
              color
            }
          }
          ... on ProjectV2IterationField {
            id
            name
            dataType
            configuration {
              iterations {
                id
                title
                startDate
                duration
              }
            }
          }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -F number=5
```

### 이슈의 프로젝트 아이템 ID 조회

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      number
      title
      projectItems(first: 10) {
        nodes {
          id
          project {
            number
            title
          }
        }
      }
    }
  }
}' -f owner='ThakiCloud' -f repo='ai-platform-strategy' -F issueNumber=$ISSUE_NUMBER
```

---

## 프로젝트 필드 설정

### Single Select 필드 설정 (Priority, Status, Size)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $FIELD_ID \
  --single-select-option-id $OPTION_ID \
  --project-id $PROJECT_ID
```

### Number 필드 설정 (Estimate)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $FIELD_ID \
  --number $VALUE \
  --project-id $PROJECT_ID
```

### Iteration 필드 설정 (Sprint)

```bash
gh project item-edit \
  --id $ITEM_ID \
  --field-id $FIELD_ID \
  --iteration-id $ITERATION_ID \
  --project-id $PROJECT_ID
```

---

## Epic 관계 설정

### 이슈 Node ID 조회

```bash
# Epic 이슈의 node_id
EPIC_NODE_ID=$(gh api repos/ThakiCloud/ai-platform-strategy/issues/$EPIC_NUMBER --jq '.node_id')

# 서브 이슈의 node_id
SUB_ISSUE_NODE_ID=$(gh api repos/ThakiCloud/ai-platform-strategy/issues/$SUB_ISSUE_NUMBER --jq '.node_id')
```

### addSubIssue Mutation

```bash
gh api graphql -f query='
mutation($issueId:ID!, $subIssueId:ID!) {
  addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
    issue {
      id
      number
      title
    }
    subIssue {
      id
      number
      title
    }
  }
}' -F issueId="$EPIC_NODE_ID" -F subIssueId="$SUB_ISSUE_NODE_ID"
```

### 크로스 레포 연결

```bash
# 다른 레포지토리의 Epic과 연결
EPIC_NODE_ID=$(gh api repos/ThakiCloud/$EPIC_REPO/issues/$EPIC_NUMBER --jq '.node_id')
SUB_ISSUE_NODE_ID=$(gh api repos/ThakiCloud/$SUB_REPO/issues/$SUB_ISSUE_NUMBER --jq '.node_id')

gh api graphql -f query='
mutation($issueId:ID!, $subIssueId:ID!) {
  addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
    issue {
      id
      number
      title
      repository { name owner { login } }
    }
    subIssue {
      id
      number
      title
      repository { name owner { login } }
    }
  }
}' -F issueId="$EPIC_NODE_ID" -F subIssueId="$SUB_ISSUE_NODE_ID"
```

---

## PR 관련 명령어

### PR 생성

```bash
gh pr create \
  --title "#<ISSUE_NUMBER> <type>: <summary>" \
  --body "PR 본문" \
  --base dev \
  --head tmp \
  --assignee @me
```

### PR 상태 확인

```bash
gh pr status
gh pr view
gh pr checks
```

### PR 머지

```bash
# Squash 머지 (issue 브랜치 → dev)
gh pr merge --squash

# 일반 머지 (epic 브랜치 → dev)
gh pr merge --merge
```

---

## 이슈 관련 명령어

### 이슈 생성

```bash
gh issue create \
  --title "제목" \
  --body "내용" \
  --assignee @me \
  --label "label1,label2"
```

### 이슈 조회 및 수정

```bash
# 이슈 조회
gh issue view $ISSUE_NUMBER

# 이슈 본문 수정
gh issue edit $ISSUE_NUMBER --body "새로운 본문"

# 이슈 제목 수정
gh issue edit $ISSUE_NUMBER --title "새로운 제목"
```

### 이슈 닫기

```bash
gh issue close $ISSUE_NUMBER
```

---

## 유용한 JQ 필터

### 이슈 번호만 추출

```bash
gh issue list --json number --jq '.[].number'
```

### 프로젝트 아이템 ID 추출

```bash
# 프로젝트 아이템 존재 여부 확인 후 ID 추출
ITEM_ID=$(gh api graphql -f query='...' | jq -r '.data.repository.issue.projectItems.nodes[0].id // empty')
if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
  echo "❌ 프로젝트 아이템이 없습니다. 먼저 프로젝트에 추가하세요."
  exit 1
fi
echo "✅ 프로젝트 아이템 ID: $ITEM_ID"
```

### 현재 스프린트 ID 찾기

```bash
# 오늘 날짜와 비교하여 현재 스프린트 찾기
# Note: .duration is in days, not weeks
TODAY=$(date -u +%Y-%m-%d)
gh api graphql -f query='...' | jq -r --arg today "$TODAY" '
  .data.organization.projectV2.fields.nodes[]
  | select(.name == "Sprint")
  | .configuration.iterations[]
  | select(.startDate <= $today and (.startDate | strptime("%Y-%m-%d") | mktime + (.duration * 86400)) > ($today | strptime("%Y-%m-%d") | mktime))
  | .id
'
```

---

## 에러 처리

### 이슈 존재 여부 확인

```bash
gh api repos/ThakiCloud/ai-platform-strategy/issues/$ISSUE_NUMBER --jq '.number' > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ 이슈가 존재하지 않습니다: #$ISSUE_NUMBER"
  exit 1
fi
```

### 프로젝트 권한 확인

```bash
gh api repos/ThakiCloud/ai-platform-strategy --jq '.permissions.push' > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ 레포지토리 접근 권한이 없습니다"
  exit 1
fi
```
