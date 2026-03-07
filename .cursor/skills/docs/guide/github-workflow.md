## 개요

GitHub 이슈 생성부터 커밋, PR까지 전체 워크플로우를 자동화하는 스킬이다. 코드 변경 후 "커밋해줘"라고 요청하면 에이전트가 이슈 확인 → pre-commit → 커밋 → 푸시 → PR 생성/업데이트까지 한 번에 처리한다.

> 트리거 키워드: 이슈 만들어줘, 커밋해줘, PR 생성해줘, 변경사항 정리해줘, 깃 워크플로우

## 사전 조건

- `gh` CLI 인증 완료 (`gh auth login`)
- `pre-commit` 설치 (`pip install pre-commit && pre-commit install`)

## 절차

### 1. 이슈 생성

작업을 시작할 때 이슈를 먼저 만든다.

```
"로그인 버그 이슈 만들어줘"
"사용자 인증 기능 추가 이슈 만들어줘"
```

에이전트가 수행하는 작업:
- `gh issue create`로 이슈 생성
- ThakiCloud 프로젝트(#22)에 자동 연결
- Priority, Size, Estimate, Sprint 필드 설정
- `issue/{NUMBER}-{summary}` 브랜치 생성

### 2. 커밋

코드 변경 후 커밋을 요청한다.

```
"커밋해줘"
"변경사항 커밋하고 푸시해줘"
```

에이전트가 수행하는 작업:
- `git status`로 변경사항 확인
- `pre-commit run --all-files` 실행 (실패 시 자동 수정 후 재시도)
- Conventional Commits 형식으로 커밋 메시지 생성
- 원격에 푸시

### 3. PR 생성

커밋 후 PR을 요청한다. 커밋과 함께 요청할 수도 있다.

```
"PR 만들어줘"
"커밋하고 PR까지 만들어줘"
```

에이전트가 수행하는 작업:
- 기존 PR이 있으면 본문을 업데이트 (새로 생성하지 않음)
- 없으면 `.github/PULL_REQUEST_TEMPLATE.md` 형식에 맞춰 PR 생성
- 타겟 브랜치 자동 결정 (`issue/*` → `dev`, `release-*` → `main`)
- 이슈에 진행 상황 코멘트 추가

### 4. 전체 흐름 한 번에

이슈부터 PR까지 한 번에 요청할 수도 있다.

```
"이 변경사항으로 이슈 만들고 커밋하고 PR까지 해줘"
```

에이전트가 현재 브랜치 상태를 확인해서 필요한 단계부터 자동으로 시작한다:
- `issue/*` 브랜치에 있으면 → 커밋부터 시작
- `dev`, `main` 등에 있으면 → 이슈 생성부터 시작

## 검증

- `gh issue view {NUMBER}`로 이슈 확인
- `gh pr view`로 PR 확인
- 이슈에 진행 상황 코멘트가 달렸는지 확인

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `gh: command not found` | gh CLI 미설치 | `brew install gh && gh auth login` |
| pre-commit 계속 실패 | 코드 품질 문제 | 에러 메시지 확인 후 수동 수정, 재요청 |
| PR 타겟이 잘못됨 | 브랜치 네이밍 규칙 불일치 | `issue/{NUMBER}-{summary}` 형식으로 브랜치명 확인 |
| 프로젝트 필드 설정 실패 | 권한 부족 | `gh auth refresh -s project` 실행 |
