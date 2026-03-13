# Epic and Sub-Issue Management

## Priority Inheritance

Sub-issues **always inherit** the parent Epic's priority. If an Epic is P0, all sub-issues under it must also be P0.

## Sub-Issue Guidelines

### Scope

- Limit to **4-5 actionable tasks** per sub-issue
- Each task must have a clear deliverable
- Target **1-2 week** completion window per sub-issue
- Keep dependencies minimal — prefer independent work units

### Content

- Measurable success criteria (3-4 max)
- No unnecessary detail — each line should map to a concrete action
- Fibonacci estimate (0.5, 1, 2, 3, 5, 8) where 1 = one day with AI assistance

### Example

```markdown
## 주요 작업 내용

- [ ] PriorityClass 4단계 리소스 생성
- [ ] GPU 메모리 예산표 ConfigMap 구성
- [ ] Admission Webhook 검증 로직 추가
- [ ] 리소스 가용성 체크 API 구현

## 성공 기준

- PriorityClass 4단계가 정상 배포됨
- 예산표 기반 검증이 동작함
- API 호출이 정상 응답함
```

## addSubIssue Mutation

### Same-repo linking

```bash
EPIC_NODE_ID=$(gh api repos/ThakiCloud/REPO/issues/EPIC_NUMBER --jq '.node_id')
SUB_ISSUE_NODE_ID=$(gh api repos/ThakiCloud/REPO/issues/SUB_ISSUE_NUMBER --jq '.node_id')

gh api graphql -f query='
mutation($issueId: ID!, $subIssueId: ID!) {
  addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
    issue { id number title }
    subIssue { id number title }
  }
}' -F issueId="$EPIC_NODE_ID" -F subIssueId="$SUB_ISSUE_NODE_ID"
```

### Cross-repo linking

```bash
EPIC_NODE_ID=$(gh api repos/ThakiCloud/EPIC_REPO/issues/EPIC_NUMBER --jq '.node_id')
SUB_ISSUE_NODE_ID=$(gh api repos/ThakiCloud/SUB_REPO/issues/SUB_NUMBER --jq '.node_id')

gh api graphql -f query='
mutation($issueId: ID!, $subIssueId: ID!) {
  addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
    issue { id number title repository { name owner { login } } }
    subIssue { id number title repository { name owner { login } } }
  }
}' -F issueId="$EPIC_NODE_ID" -F subIssueId="$SUB_ISSUE_NODE_ID"
```

### Cross-repo prerequisites

Verify both repos are accessible before linking:

```bash
gh api repos/ThakiCloud/EPIC_REPO/issues/EPIC_NUMBER --jq '.number' > /dev/null 2>&1
gh api repos/ThakiCloud/SUB_REPO/issues/SUB_NUMBER --jq '.number' > /dev/null 2>&1
```

## Task List for Visual Tracking

After creating the parent-child relationship via `addSubIssue`, optionally add a task list to the Epic body for visual progress tracking.

### Same-repo task list

```bash
gh issue edit EPIC_NUMBER --body "$(cat <<'EOF'
## 📋 서브 이슈들

- [ ] #SUB_ISSUE1 제목1
- [ ] #SUB_ISSUE2 제목2

[기존 Epic 본문]
EOF
)"
```

### Cross-repo task list

```bash
gh issue edit EPIC_NUMBER --body "$(cat <<'EOF'
## 📋 서브 이슈들

- [ ] #SUB_ISSUE1 제목1 (같은 레포)
- [ ] ThakiCloud/OTHER_REPO#SUB_ISSUE2 제목2 (다른 레포)

[기존 Epic 본문]
EOF
)"
```

**IMPORTANT**: When editing an Epic body, always preserve the original content. Append the task list — never overwrite existing text.

## Project Association

Both Epic and sub-issues must be added to the same project (**ThakiCloud Project #5**):

```bash
gh project item-add 5 --owner ThakiCloud --url $ISSUE_URL
```
