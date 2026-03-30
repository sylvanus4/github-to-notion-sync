# 사용 예시

## 예시 1: 새로운 기능 개발 (처음부터)

### 상황

- 현재 브랜치: `dev`
- 변경 파일: `frontend/src/components/NewFeature.tsx`

### 실행 흐름

```bash
# Step 0: 상태 확인
$ git branch --show-current
dev

$ git status
Changes not staged for commit:
  modified: frontend/src/components/NewFeature.tsx

# → dev 브랜치이므로 Step A로 이동

# Step A: 이슈 생성
$ gh issue create --title "새로운 기능 컴포넌트 추가" --body "..." --assignee @me
https://github.com/ThakiCloud/ai-platform-webui/issues/123

$ gh project item-add 5 --owner ThakiCloud --url https://github.com/ThakiCloud/ai-platform-webui/issues/123

# (프로젝트 필드 설정 - Priority: P0, Size: S, Estimate: 2, Sprint: 현재)

# Step B: 브랜치 생성
$ git checkout -b issue/123-add-new-feature

# Step D: Pre-commit → 커밋 → 푸시 → PR
$ pre-commit run --all-files
$ git add .
$ git commit -m "$(cat <<'EOF'
feat: add NewFeature component

- 새로운 기능 컴포넌트 구현
- Props 타입 정의
- 기본 스타일링 적용
EOF
)"

$ git push origin HEAD:tmp

$ gh pr create --title "#123 feat: add NewFeature component" --body "..." --base dev
```

### 완료 보고

```
✅ GitHub 워크플로우 완료

## 📋 이슈
- #123 새로운 기능 컴포넌트 추가
- URL: https://github.com/ThakiCloud/ai-platform-webui/issues/123

## ⚙️ 프로젝트 설정
- Priority: P0
- Size: S
- Estimate: 2
- Sprint: 25-01-Sprint2

## 🔀 브랜치
- issue/123-add-new-feature

## 📝 커밋
- feat: add NewFeature component

## 🔗 PR
- #124 feat: add NewFeature component
- URL: https://github.com/ThakiCloud/ai-platform-webui/pull/124
- Base: dev ← Head: issue/123-add-new-feature
- 머지 전략: Squash
```

---

## 예시 2: 기존 이슈 브랜치에서 작업 완료

### 상황

- 현재 브랜치: `issue/100-fix-login-bug`
- 추가 변경 파일 있음

### 실행 흐름

```bash
# Step 0: 상태 확인
$ git branch --show-current
issue/100-fix-login-bug

# → 이슈 브랜치이므로 Step C로 바로 이동

# Step C: 이슈 내용 업데이트 (필요시)
$ gh issue view 100
$ gh issue edit 100 --body "업데이트된 내용..."

# Step D: Pre-commit → 커밋 → 푸시 → PR
$ pre-commit run --all-files
$ git add .
$ git commit -m "$(cat <<'EOF'
fix: resolve login validation error

- 이메일 형식 검증 로직 수정
- 에러 메시지 개선
- 테스트 케이스 추가
EOF
)"

$ git push origin HEAD:tmp

$ gh pr create --title "#100 fix: resolve login validation error" --body "..." --base dev
```

---

## 예시 3: 버그 수정 (긴급)

### 상황

- 프로덕션 버그 발생
- 빠른 수정 필요

### 실행 흐름

```bash
# Step 0: 상태 확인 (dev에서 시작)
$ git checkout dev
$ git pull origin tmp

# Step A: 긴급 이슈 생성
$ gh issue create \
  --title "[긴급] 로그인 실패 오류 수정" \
  --body "## 문제
- 로그인 시 500 에러 발생

## 원인
- DB 연결 타임아웃

## 해결
- 커넥션 풀 설정 조정" \
  --assignee @me

# 프로젝트 추가 및 필드 설정 (Priority: P0)

# Step B: 브랜치 생성
$ git checkout -b issue/125-fix-login-error

# Step D: Pre-commit → 수정 → 커밋
$ pre-commit run --all-files
$ git add .
$ git commit -m "$(cat <<'EOF'
fix: resolve database connection timeout

- 커넥션 풀 최대 크기 증가
- 타임아웃 설정 조정
- 재연결 로직 추가
EOF
)"

$ git push origin HEAD:tmp

$ gh pr create --title "#125 fix: resolve database connection timeout" --body "..."
```

---

## 예시 4: 테스트 코드 추가

### 커밋 메시지 예시

```bash
git commit -m "$(cat <<'EOF'
test: add E2E tests for settings page

- 설정 페이지 기본 동작 테스트 추가
- 사용자 권한별 접근 테스트
- 폼 유효성 검증 테스트
EOF
)"
```

---

## 예시 5: 문서 업데이트

### 커밋 메시지 예시

```bash
git commit -m "$(cat <<'EOF'
docs: update API documentation

- 새로운 엔드포인트 문서 추가
- 인증 플로우 다이어그램 업데이트
- 에러 코드 목록 정리
EOF
)"
```

---

## 예시 6: 리팩토링

### 커밋 메시지 예시

```bash
git commit -m "$(cat <<'EOF'
refactor: reorganize component structure

- 컴포넌트 폴더 구조 개선
- 공통 유틸 함수 추출
- 타입 정의 분리
EOF
)"
```

---

## 예시 7: 성능 개선

### 커밋 메시지 예시

```bash
git commit -m "$(cat <<'EOF'
perf: optimize vLLM batch size

- 배치 크기 동적 조정 로직 추가
- 메모리 사용량 최적화
- 추론 속도 20% 개선
EOF
)"
```

---

## 예시 8: scope 포함 커밋

### 커밋 메시지 예시

```bash
# 인증 관련
git commit -m "$(cat <<'EOF'
feat(auth): add OAuth 2.0 PKCE flow

- GitHub OAuth 연동 추가
- 토큰 갱신 로직 구현
EOF
)"

# 스토리지 관련
git commit -m "$(cat <<'EOF'
fix(storage): resolve PVC mount issue

- 볼륨 마운트 경로 수정
- 권한 설정 업데이트
EOF
)"

# 추론 관련
git commit -m "$(cat <<'EOF'
perf(inference): optimize model loading

- 모델 캐싱 로직 개선
- 로딩 시간 50% 단축
EOF
)"
```

---

## PR 본문 예시

```markdown
## Issue?

Resolves #123

## Changes?

- 새로운 인증 컴포넌트 추가
- JWT 토큰 갱신 로직 구현
- 로그아웃 기능 구현

## Why we need?

사용자 인증 시스템이 필요하여 OAuth 2.0 기반 인증 플로우를 구현했습니다.
기존 세션 기반 인증의 보안 취약점을 해결합니다.

## Test?

- [x] 로컬 환경에서 로그인/로그아웃 테스트
- [x] 토큰 만료 시 자동 갱신 확인
- [x] E2E 테스트 통과

## CC (Optional)

## Anything else? (Optional)

- 환경 변수 `JWT_SECRET` 설정 필요
- 배포 전 DB 마이그레이션 필요
```

---

## 이슈 본문 예시

```markdown
## 📋 개요

설정 페이지의 E2E 테스트를 추가합니다.

## 🎯 목표

- 설정 페이지 기본 기능 테스트
- 권한별 접근 제어 테스트
- 폼 검증 테스트

## ✅ 주요 작업

- [ ] 기본 설정 조회 테스트
- [ ] 설정 변경 테스트
- [ ] 에러 케이스 테스트

## 📎 참고

- 관련 PR: #120
- Figma: (링크)
```
