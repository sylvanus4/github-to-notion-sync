---
name: github-workflow-automation
description: >-
  ai-platform-strategy 레포지토리의 GitHub 워크플로우를 자동화합니다. 변경사항 확인, 이슈 생성, 브랜치 생성,
  커밋, 푸시, PR 생성/업데이트, 이슈 코멘트까지 전체 흐름 처리. 이슈 만들어줘, 커밋해줘, PR 생성해줘, 변경사항 정리해줘, 깃
  워크플로우 요청 시 사용합니다. Do NOT use for 코드 생성(fsd-development), 화면
  구현(implement-screen), Notion 문서 동기화(notion-docs-sync), 또는 디자인
  리뷰(design-review).
---

# GitHub 워크플로우 자동화

## 워크플로우 개요

```
변경사항 확인 → 적합한 브랜치인가?
    ├── YES (issue/XXX 브랜치) → Step C → Step D
    └── NO → Step A → Step B → Step D
```

상세 명령어: [references/workflow-commands.md](references/workflow-commands.md)

---

## Step 0: 현재 상태 확인

```bash
git branch --show-current  # 브랜치
git status                 # 변경사항
git log --oneline -5       # 히스토리
```

**분기**:
- `issue/{NUMBER}-{SUMMARY}` → 기존 이슈 브랜치 → **Step C**
- `dev`, `main`, 기타 → **Step A**

## Step A: 이슈 생성

1. `gh issue create --title "..." --body "..." --assignee @me`
2. `gh project item-add 5 --owner ThakiCloud --url [이슈URL]`
3. 프로젝트 필드 설정 (Priority/Size/Estimate/Sprint)

**필드 규칙**:
- **Priority**: P0 (기본), Epic 하위면 상속
- **Size**: XS/S/M/L/XL (변경 규모 기반)
- **Estimate**: 피보나치 (0.5~8), 1일 = 1 기준
- **Sprint**: 오늘 날짜 기준 현재 활성 스프린트

상세 GraphQL: [references/workflow-commands.md](references/workflow-commands.md) Step A 참조

## Step B: 브랜치 생성

```bash
git checkout dev && git pull origin dev
git checkout -b issue/{ISSUE_NUMBER}-{summary}
```

## Step C: 이슈 업데이트 (기존 브랜치)

브랜치명에서 이슈 번호 추출 → `gh issue view` → 변경사항 반영 → `gh issue edit`

## Step D: Pre-commit → 커밋 → 푸시 → PR

### D-0. Pre-commit (필수)

```bash
pre-commit run --all-files
# 실패 → git add . → 재실행 반복. 통과까지 커밋 금지.
```

### D-1. 커밋

**형식**: `<type>: <summary>` (50자 이내, 영어 소문자 명령문, 마침표 없음)

| 타입 | 설명 |
|------|------|
| `feat` | 새 기능 | `fix` | 버그 수정 | `docs` | 문서 | `refactor` | 리팩토링 |
| `style` | 포맷팅 | `perf` | 성능 | `test` | 테스트 | `chore` | 기타 |

scope 선택: `auth`, `api`, `ui`, `kfp`, `storage`, `inference`, `ml-studio`, `pipeline`

### D-2. 푸시

`git push -u origin $(git branch --show-current)`

### D-3. PR 생성/업데이트

1. `gh pr list --head {branch}` 로 기존 PR 확인
2. **있으면** → `gh pr edit` 본문 업데이트 + `[NEW]` 표시
3. **없으면** → `gh pr create` (타겟: issue/* → `dev`, release-* → `main`)

**PR 제목**: `#<ISSUE> <type>: <summary>`

### D-4. 이슈 코멘트

커밋/PR 완료 후 이슈에 진행 상황 코멘트 자동 추가.

### D-5. 상태 업데이트 (선택)

PR 생성 시 프로젝트 보드 Status → In Review.

---

## 주의사항

1. Pre-commit 필수 통과 후 커밋
2. 프로젝트 ID: ThakiCloud **#5**
3. PR 타겟: issue/* → dev, release-* → main
4. 기존 PR 있으면 새로 생성하지 않고 업데이트
5. 커밋 후 이슈에 진행 상황 코멘트

## 세부 가이드 (필요시 참조)

- [references/workflow-commands.md](references/workflow-commands.md) — 상세 bash/GraphQL 명령어
- [references/graphql-reference.md](references/graphql-reference.md) — GraphQL 쿼리 레퍼런스
- [references/examples.md](references/examples.md) — 추가 사용 예시
- PR 자동화: `curl -L -s "https://r.jina.ai/https://thakicloud.notion.site/GitHub-PR-2549eddc34e6801d9804da9c590acabf"`
- 이슈 자동화: `curl -L -s "https://r.jina.ai/https://thakicloud.notion.site/GitHub-2549eddc34e6808ebbede86dc44e968f"`

## Examples

### Example 1: 새 이슈 + 브랜치 + 커밋 + PR 전체 흐름
User says: "이 변경사항 커밋하고 PR 만들어줘"
Actions:
1. Step 0: git status로 변경사항 확인, 현재 브랜치 dev → Step A로 분기
2. Step A: 이슈 생성 + 프로젝트 추가 + 필드 설정
3. Step B: `issue/{N}-{summary}` 브랜치 생성
4. Step D: pre-commit → 커밋 → 푸시 → PR 생성 → 이슈 코멘트
Result: 이슈 + 브랜치 + 커밋 + PR + 프로젝트 설정 완료

### Example 2: 기존 이슈 브랜치에서 추가 커밋 + PR 업데이트
User says: "추가 수정사항 커밋해줘"
Actions:
1. Step 0: `issue/42-add-auth` 브랜치 확인 → Step C로 분기
2. Step C: 이슈 본문 변경사항 반영
3. Step D: pre-commit → 커밋 → 푸시 → 기존 PR 본문 업데이트 + `[NEW]` 표시
Result: 기존 PR에 새 커밋이 추가되고 본문이 업데이트됨

## Troubleshooting

### pre-commit이 반복 실패
Cause: 자동 수정 불가능한 lint 에러 (타입 에러, import 순서 등)
Solution: 에러 메시지 확인 후 수동 수정. `git add .` → `pre-commit run --all-files` 재실행

### gh 명령어 인증 실패
Cause: GitHub CLI 인증이 만료되었거나 설정되지 않음
Solution: `gh auth login` 실행 후 재시도. Organization 접근 필요 시 `gh auth refresh -s project`
