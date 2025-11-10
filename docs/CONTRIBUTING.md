# 기여 가이드 (Contributing Guide)

GitHub to Notion Sync 프로젝트에 기여해주셔서 감사합니다! 🎉

## 🚀 개발 환경 설정

### 1. 저장소 클론

```bash
git clone https://github.com/ThakiCloud/github-to-notion-sync.git
cd github-to-notion-sync
```

### 2. 개발 의존성 설치

```bash
# Python 3.11 이상 필요
python --version

# 개발 의존성 설치 및 pre-commit 설정
make install-dev
```

이 명령어는 다음을 수행합니다:
- 프로덕션 의존성 설치 (`requirements.txt`)
- 개발 의존성 설치 (`requirements-dev.txt`)
- Pre-commit 훅 자동 설치
- Commit 메시지 검증 훅 설치

### 3. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 편집하여 필요한 값 입력
```

## 📝 개발 워크플로우

### 1. 브랜치 생성

```bash
# 기능 개발
git checkout -b feature/your-feature-name

# 버그 수정
git checkout -b fix/your-bug-fix

# 문서 업데이트
git checkout -b docs/your-documentation
```

### 2. 코드 작성

#### 코드 스타일 가이드

- **Line length**: 최대 120자
- **Import 순서**: 표준 라이브러리 → 써드파티 → 로컬
- **Docstring**: Google 스타일
- **Type hints**: 가능한 모든 곳에 추가

#### 예시

```python
from typing import Optional, List
from datetime import datetime

import requests
from fastapi import FastAPI

from src.models.github_models import GitHubIssue
from src.services.github_service import GitHubService


def process_issues(
    issues: List[GitHubIssue],
    filter_date: Optional[datetime] = None
) -> List[dict]:
    """Process GitHub issues and return formatted data.
    
    Args:
        issues: List of GitHub issues to process
        filter_date: Optional date to filter issues
        
    Returns:
        List of processed issue dictionaries
        
    Raises:
        ValueError: If issues list is empty
    """
    if not issues:
        raise ValueError("Issues list cannot be empty")
    
    # Your code here
    return processed_issues
```

### 3. 코드 품질 검사

개발 중에 주기적으로 실행:

```bash
# 코드 포맷팅
make format

# 린팅
make lint

# 타입 체킹
make type-check

# 보안 검사
make security

# 모든 검사 한번에
make check
```

### 4. 테스트 작성 및 실행

모든 새로운 기능에는 테스트를 작성해야 합니다:

```bash
# 테스트 실행
make test

# 커버리지와 함께 테스트
make test-cov
```

테스트 작성 예시:

```python
import pytest
from src.services.github_service import GitHubService


class TestGitHubService:
    """GitHub 서비스 테스트"""
    
    @pytest.fixture
    def github_service(self):
        """GitHub 서비스 픽스처"""
        return GitHubService()
    
    def test_get_issues(self, github_service):
        """이슈 가져오기 테스트"""
        issues = github_service.get_issues()
        assert len(issues) > 0
        assert all(hasattr(issue, 'title') for issue in issues)
```

### 5. 커밋

Pre-commit 훅이 자동으로 실행되어 코드를 검사합니다:

```bash
git add .
git commit -m "feat: add new feature"
```

#### 커밋 메시지 규칙 (Conventional Commits)

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 스타일 변경 (포맷팅)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/설정 변경
- `perf`: 성능 개선
- `ci`: CI 설정 변경

**예시**:

```bash
# 좋은 커밋 메시지
git commit -m "feat: add GitHub webhook handler for issue events"
git commit -m "fix: resolve race condition in sync service"
git commit -m "docs: update API documentation"

# 나쁜 커밋 메시지
git commit -m "update"
git commit -m "fix bug"
git commit -m "WIP"
```

### 6. Pull Request 생성

```bash
git push origin feature/your-feature-name
```

그리고 GitHub에서 PR을 생성하세요.

## 🔍 Pre-commit 훅 상세

Pre-commit은 커밋 전에 자동으로 다음을 실행합니다:

### 1. 기본 파일 검사
- ✅ 파일 끝 개행 추가
- ✅ 공백 제거
- ✅ 큰 파일 방지 (5MB)
- ✅ YAML/JSON 문법 검사
- ✅ Merge conflict 마커 검사
- ✅ Private key 방지

### 2. Python 코드 검사
- 🎨 **Black**: 코드 포맷팅
- 📦 **isort**: Import 정렬
- 🔍 **Ruff**: 빠른 린팅 (flake8 대체)
- 📝 **Pydocstyle**: Docstring 검사
- 🔎 **mypy**: 타입 체킹
- 🔒 **Bandit**: 보안 검사

### 3. 기타 파일 검사
- 📄 **Markdown**: 마크다운 린팅
- 🐳 **Dockerfile**: Dockerfile 린팅
- 🐚 **ShellCheck**: Shell script 검사

### Pre-commit 훅 건너뛰기 (비권장)

긴급한 경우에만:

```bash
git commit -m "message" --no-verify
```

## 🐛 문제 해결

### Pre-commit 훅이 실패하는 경우

```bash
# Pre-commit 캐시 삭제
pre-commit clean

# Pre-commit 재설치
pre-commit uninstall
pre-commit install

# 모든 파일에 대해 수동 실행
make pre-commit
```

### 테스트가 실패하는 경우

```bash
# 캐시 삭제
make clean

# 의존성 재설치
pip install -r requirements.txt -r requirements-dev.txt

# 테스트 재실행
make test-cov
```

### Type checking 에러

```bash
# mypy 캐시 삭제
rm -rf .mypy_cache

# 타입 체킹 재실행
make type-check
```

## 📚 유용한 명령어

```bash
# 도움말 보기
make help

# 개발 서버 실행
make run

# 모든 캐시 삭제
make clean

# 전체 검사 (포맷팅 + 린팅 + 타입체킹 + 보안 + 테스트)
make check

# Pre-commit 훅 수동 실행
make pre-commit
```

## 💡 코딩 팁

### 1. 작은 커밋을 자주

큰 PR보다 작은 PR이 리뷰하기 쉽습니다.

### 2. 테스트 우선 작성 (TDD)

```bash
# 1. 테스트 작성
# 2. 테스트 실패 확인
# 3. 코드 작성
# 4. 테스트 통과 확인
# 5. 리팩토링
```

### 3. 로깅 활용

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Processing started")
logger.debug(f"Processing item: {item}")
logger.error(f"Failed to process: {error}", exc_info=True)
```

### 4. 에러 핸들링

```python
# ❌ 나쁜 예
try:
    result = process()
except Exception:
    pass

# ✅ 좋은 예
try:
    result = process()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

## 📖 추가 문서

- [아키텍처 문서](ARCHITECTURE.md)
- [API 문서](API.md)
- [배포 가이드](DEPLOYMENT.md)
- [트러블슈팅](TROUBLESHOOTING.md)

## ❓ 질문이나 도움이 필요하신가요?

- 💬 [GitHub Discussions](https://github.com/ThakiCloud/github-to-notion-sync/discussions)
- 🐛 [이슈 생성](https://github.com/ThakiCloud/github-to-notion-sync/issues/new)

---

다시 한번 기여해주셔서 감사합니다! 🙏

