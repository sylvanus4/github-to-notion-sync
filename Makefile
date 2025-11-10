.PHONY: help install install-dev test test-cov lint format type-check security check pre-commit run clean deploy-lambda

# 기본 타겟: help
help:
	@echo "사용 가능한 명령어:"
	@echo "  make install        - 프로덕션 의존성 설치"
	@echo "  make install-dev    - 개발 의존성 설치 + pre-commit 설정"
	@echo "  make test           - 테스트 실행"
	@echo "  make test-cov       - 커버리지와 함께 테스트 실행"
	@echo "  make lint           - 코드 린팅 (ruff)"
	@echo "  make format         - 코드 포맷팅 (black + isort)"
	@echo "  make type-check     - 타입 체킹 (mypy)"
	@echo "  make security       - 보안 검사 (bandit)"
	@echo "  make check          - 모든 검사 실행 (lint + type-check + security + test)"
	@echo "  make pre-commit     - pre-commit 훅 실행 (모든 파일)"
	@echo "  make run            - FastAPI 서버 실행 (개발 모드)"
	@echo "  make clean          - 캐시 및 빌드 파일 삭제"
	@echo "  make deploy-lambda  - Lambda 배포 패키지 생성"

# 프로덕션 의존성 설치
install:
	pip install -r requirements.txt

# 개발 의존성 설치 + pre-commit 설정
install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "✅ 개발 환경 설정 완료!"

# 테스트 실행
test:
	pytest tests/ -v

# 커버리지와 함께 테스트 실행
test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# 코드 린팅 (ruff - 빠른 린터)
lint:
	@echo "🔍 Ruff 린팅 실행..."
	ruff check src/ tests/ scripts/ --fix
	@echo "✅ 린팅 완료!"

# 코드 포맷팅
format:
	@echo "🎨 코드 포맷팅 실행..."
	black src/ tests/ scripts/
	isort src/ tests/ scripts/
	@echo "✅ 포맷팅 완료!"

# 타입 체킹
type-check:
	@echo "🔎 타입 체킹 실행..."
	mypy src/
	@echo "✅ 타입 체킹 완료!"

# 보안 검사
security:
	@echo "🔒 보안 검사 실행..."
	bandit -r src/ -c pyproject.toml
	@echo "✅ 보안 검사 완료!"

# 모든 검사 실행
check: format lint type-check security test
	@echo "✅ 모든 검사 완료!"

# Pre-commit 훅 실행 (모든 파일)
pre-commit:
	pre-commit run --all-files

# FastAPI 서버 실행 (개발 모드)
run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 캐시 및 빌드 파일 삭제
clean:
	@echo "🧹 캐시 및 빌드 파일 삭제..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 정리 완료!"

# Lambda 배포 패키지 생성
deploy-lambda:
	cd deployment/lambda && ./deployment_package.sh