# Pre-commit 가이드

## 🎯 개요

이 프로젝트는 **pre-commit**을 사용하여 코드 품질을 자동으로 관리합니다.
커밋 전에 자동으로 코드 검사, 포맷팅, 보안 검사 등이 실행됩니다.

## 🚀 빠른 시작

### 1. 설치

```bash
make install-dev
```

이 명령어는 자동으로:

- ✅ 개발 의존성 설치
- ✅ Pre-commit 훅 설치
- ✅ Commit 메시지 검증 훅 설치

### 2. 사용

평소처럼 커밋하면 자동으로 검사가 실행됩니다:

```bash
git add .
git commit -m "feat: add new feature"
```

Pre-commit이 자동으로:

1. 코드 포맷팅 (Black, isort)
2. 린팅 (Ruff, flake8)
3. 타입 체킹 (mypy)
4. 보안 검사 (Bandit)
5. YAML/JSON 검증
6. 파일 검사 등을 실행합니다.

### 3. 수동 실행

모든 파일에 대해 pre-commit을 수동으로 실행:

```bash
make pre-commit
# 또는
pre-commit run --all-files
```

## 📋 포함된 검사 항목

### 🐍 Python 검사

| 도구           | 설명                    | 자동 수정 |
| -------------- | ----------------------- | --------- |
| **Black**      | 코드 포맷팅 (120자)     | ✅        |
| **isort**      | Import 정렬             | ✅        |
| **Ruff**       | 빠른 린팅 (flake8 대체) | ✅ (일부) |
| **mypy**       | 타입 체킹               | ❌        |
| **Bandit**     | 보안 취약점 검사        | ❌        |
| **Pydocstyle** | Docstring 검사          | ❌        |

### 📄 파일 검사

| 도구              | 설명              | 자동 수정 |
| ----------------- | ----------------- | --------- |
| **YAML lint**     | YAML 문법 검사    | ✅        |
| **JSON lint**     | JSON 문법 검사    | ✅        |
| **Markdown lint** | 마크다운 린팅     | ✅        |
| **Hadolint**      | Dockerfile 린팅   | ❌        |
| **ShellCheck**    | Shell script 검사 | ❌        |

### 🔒 보안 & 기타

- Private key 감지
- Debug 구문 검사
- Merge conflict 마커 검사
- 큰 파일 방지 (5MB)
- 파일 끝 개행 추가
- Trailing whitespace 제거

## 🛠️ 주요 명령어

```bash
# 개발 환경 설정
make install-dev

# Pre-commit 수동 실행 (모든 파일)
make pre-commit

# 코드 포맷팅
make format

# 린팅
make lint

# 타입 체킹
make type-check

# 보안 검사
make security

# 전체 검사 (포맷팅 + 린팅 + 타입체킹 + 보안 + 테스트)
make check

# 테스트
make test

# 커버리지와 함께 테스트
make test-cov

# 캐시 삭제
make clean
```

## 💡 실전 팁

### 1. 커밋 전 체크리스트

```bash
# ✅ 1. 코드 포맷팅
make format

# ✅ 2. 모든 검사 실행
make check

# ✅ 3. 커밋
git commit -m "feat: add feature"
```

### 2. 빠른 피드백 루프

개발 중에는 자주 실행:

```bash
# 변경한 파일만 빠르게 체크
make lint
make test
```

### 3. 에러 해결

Pre-commit이 실패하면:

```bash
# 1. 자동 수정 가능한 항목들 (Black, isort, Ruff 등)은 자동 수정됨
# 2. 파일이 수정되면 다시 add
git add .

# 3. 다시 커밋
git commit -m "your message"
```

### 4. 특정 훅만 실행

```bash
# Black만 실행
pre-commit run black --all-files

# Ruff만 실행
pre-commit run ruff --all-files

# mypy만 실행
pre-commit run mypy --all-files
```

### 5. 특정 훅 건너뛰기 (비권장)

긴급한 경우에만:

```bash
# 모든 훅 건너뛰기
git commit -m "message" --no-verify

# 특정 훅만 건너뛰기
SKIP=mypy git commit -m "message"
```

## 🔧 문제 해결

### Pre-commit이 느린 경우

```bash
# 캐시 사용으로 속도 향상 (자동)
# 처음 실행은 느리지만 이후에는 빠름
```

### Pre-commit 재설치

```bash
pre-commit clean
pre-commit uninstall
pre-commit install
pre-commit install --hook-type commit-msg
```

### 특정 훅이 실패하는 경우

```bash
# 1. 해당 도구 직접 실행
ruff check src/
black src/
mypy src/

# 2. 상세 에러 확인
pre-commit run ruff --all-files --verbose

# 3. 수정 후 다시 시도
```

## 📊 코드 품질 기준

프로젝트의 품질 기준:

- ✅ **Line length**: 최대 120자
- ✅ **Test coverage**: 최소 70%
- ✅ **복잡도**: 최대 10 (McCabe)
- ✅ **Type hints**: 가능한 모든 곳에 추가
- ✅ **Docstring**: Google 스타일

## 🎓 커밋 메시지 규칙

Pre-commit은 **Conventional Commits** 규칙을 강제합니다:

### 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 변경
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/설정 변경
- `perf`: 성능 개선
- `ci`: CI 설정 변경

### 예시

```bash
# ✅ 좋은 예
feat: add GitHub webhook handler for issue events
fix: resolve race condition in sync service
docs: update API documentation
refactor: simplify error handling logic
test: add integration tests for sync service

# ❌ 나쁜 예
update code
fix
WIP
temp commit
```

## 🔄 GitHub Actions 통합

Pre-commit은 CI/CD에서도 자동 실행됩니다:

- 📝 **Push/PR 시**: 모든 검사 자동 실행
- 🔍 **Code Quality 워크플로우**: `.github/workflows/code-quality.yml`
- 📊 **결과 리포트**: PR 코멘트로 자동 생성

## 📚 추가 자료

- [Pre-commit 공식 문서](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [기여 가이드](docs/CONTRIBUTING.md)

## ❓ FAQ

### Q: Pre-commit이 너무 많은 것을 검사하지 않나요?

A: 초기에는 시간이 걸리지만, 장기적으로 코드 품질과 버그 감소에 도움이 됩니다.

### Q: 특정 파일을 제외하고 싶어요

A: `.pre-commit-config.yaml`에서 `exclude` 패턴을 수정하세요.

### Q: 새로운 훅을 추가하고 싶어요

A: `.pre-commit-config.yaml`에 새로운 repo와 hook을 추가하세요.

---

Happy Coding! 🚀
