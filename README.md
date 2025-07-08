# GitHub-Notion 동기화 파이프라인 - 리포지토리 구조

```
github-notion-sync/
├── .github/
│   ├── workflows/
│   │   ├── notion_sync.yml              # 주기적 전체 동기화 워크플로우
│   │   ├── deploy_lambda.yml            # Lambda 배포 워크플로우
│   │   └── tests.yml                    # CI/CD 테스트 워크플로우
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md                # 버그 리포트 템플릿
│
├── src/
│   ├── __init__.py
│   ├── main.py                          # FastAPI 애플리케이션 엔트리포인트
│   ├── config.py                        # 환경 변수 및 설정 관리
│   ├── models/
│   │   ├── __init__.py
│   │   ├── github_models.py             # GitHub API 응답 모델
│   │   ├── notion_models.py             # Notion API 요청/응답 모델
│   │   └── webhook_models.py            # Webhook 페이로드 모델
│   ├── services/
│   │   ├── __init__.py
│   │   ├── github_service.py            # GitHub API 클라이언트 및 로직
│   │   ├── notion_service.py            # Notion API 클라이언트 및 Upsert 로직
│   │   ├── webhook_service.py           # Webhook 처리 로직
│   │   └── sync_service.py              # 동기화 조정 로직
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                    # 구조화된 로깅 유틸리티
│   │   ├── rate_limiter.py              # API Rate Limit 처리
│   │   ├── validators.py                # 데이터 검증 유틸리티
│   │   └── mapping.py                   # GitHub-Notion 데이터 매핑 유틸리티
│   └── handlers/
│       ├── __init__.py
│       ├── webhook_handler.py           # Webhook 이벤트 핸들러
│       └── sync_handler.py              # 동기화 핸들러
│
├── scripts/
│   ├── setup_github_webhook.py         # GitHub Webhook 설정 스크립트
│   ├── full_sync.py                     # 전체 동기화 스크립트
│   ├── validate_setup.py               # 설정 검증 스크립트
│   └── migrate_data.py                  # 데이터 마이그레이션 스크립트
│
├── queries/
│   ├── get_project_items.graphql        # 프로젝트 아이템 조회 쿼리
│   ├── get_single_item.graphql          # 단일 아이템 조회 쿼리
│   └── get_project_fields.graphql       # 프로젝트 필드 조회 쿼리
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                      # pytest 설정 및 fixtures
│   ├── test_github_service.py          # GitHub 서비스 테스트
│   ├── test_notion_service.py          # Notion 서비스 테스트
│   ├── test_webhook_handler.py         # Webhook 핸들러 테스트
│   ├── test_sync_service.py            # 동기화 서비스 테스트
│   └── fixtures/
│       ├── github_responses.json       # GitHub API 응답 샘플
│       ├── notion_responses.json       # Notion API 응답 샘플
│       └── webhook_payloads.json       # Webhook 페이로드 샘플
│
├── deployment/
│   ├── lambda/
│   │   ├── requirements.txt             # Lambda 의존성
│   │   ├── lambda_function.py           # Lambda 엔트리포인트
│   │   └── deployment_package.sh       # 배포 패키지 생성 스크립트
│   ├── docker/
│   │   ├── Dockerfile                   # Docker 컨테이너 정의
│   │   └── docker-compose.yml          # 로컬 개발환경 구성
│   └── terraform/
│       ├── main.tf                      # Terraform 메인 설정
│       ├── variables.tf                 # 변수 정의
│       └── outputs.tf                   # 출력 정의
│
├── docs/
│   ├── README.md                        # 프로젝트 개요 및 사용법
│   ├── SETUP.md                         # 설치 및 설정 가이드
│   ├── API.md                           # API 문서
│   ├── DEPLOYMENT.md                    # 배포 가이드
│   ├── TROUBLESHOOTING.md              # 문제 해결 가이드
│   └── ARCHITECTURE.md                  # 아키텍처 문서
│
├── monitoring/
│   ├── dashboards/
│   │   ├── cloudwatch_dashboard.json   # CloudWatch 대시보드 설정
│   │   └── grafana_dashboard.json      # Grafana 대시보드 설정
│   ├── alerts/
│   │   ├── cloudwatch_alarms.yml       # CloudWatch 알람 설정
│   │   └── slack_notifications.py      # Slack 알림 설정
│   └── health_check.py                  # 헬스 체크 스크립트
│
├── config/
│   ├── field_mappings.yml               # GitHub-Notion 필드 매핑 설정
│   ├── webhook_events.yml               # 처리할 Webhook 이벤트 설정
│   └── sync_config.yml                  # 동기화 설정
│
├── .env.example                         # 환경 변수 예시 파일
├── .gitignore                          # Git 무시 파일
├── requirements.txt                     # Python 의존성
├── requirements-dev.txt                 # 개발 의존성
├── pyproject.toml                       # Python 프로젝트 설정
├── Makefile                            # 빌드 및 개발 명령어
└── README.md                           # 프로젝트 루트 README
```

## 주요 파일 및 디렉토리 설명

### 📁 **src/** - 메인 애플리케이션 코드
- **main.py**: FastAPI 애플리케이션의 엔트리포인트, Webhook 라우팅
- **config.py**: 환경 변수 로딩, 설정 관리
- **models/**: Pydantic 모델 정의 (타입 안정성 보장)
- **services/**: 비즈니스 로직 및 외부 API 클라이언트
- **handlers/**: 이벤트 처리 및 동기화 로직
- **utils/**: 공통 유틸리티 함수

### 📁 **scripts/** - 유틸리티 스크립트
- **setup_github_webhook.py**: GitHub Webhook 자동 설정
- **full_sync.py**: GitHub Actions에서 실행되는 전체 동기화
- **validate_setup.py**: 설정 검증 및 연결 테스트

### 📁 **queries/** - GraphQL 쿼리
- 재사용 가능한 GraphQL 쿼리 파일들
- 버전 관리 및 유지보수 용이성

### 📁 **tests/** - 테스트 코드
- 단위 테스트 및 통합 테스트
- Mock 데이터 및 fixtures

### 📁 **deployment/** - 배포 관련 파일
- **lambda/**: AWS Lambda 배포 설정
- **docker/**: 컨테이너 배포 설정
- **terraform/**: 인프라 코드 (IaC)

### 📁 **monitoring/** - 모니터링 설정
- 대시보드 설정 파일
- 알림 및 헬스 체크 스크립트

### 📁 **config/** - 설정 파일
- YAML 형식의 설정 파일들
- 환경별 설정 분리

## 개발 워크플로우

### 1. 로컬 개발 환경 설정
```bash
# 의존성 설치
pip install -r requirements-dev.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 설정 검증
python scripts/validate_setup.py
```

### 2. 개발 및 테스트
```bash
# 테스트 실행
make test

# 코드 품질 검사
make lint

# 로컬 서버 실행
make run
```

### 3. 배포
```bash
# Lambda 배포
make deploy-lambda

# Docker 배포
make deploy-docker
```

## 설정 관리

### 환경 변수 (.env)
```bash
# API 토큰
NOTION_TOKEN=secret_...
GH_TOKEN=github_pat_...

# 프로젝트 설정
GH_ORG=your-org
GH_PROJECT_NUMBER=123
NOTION_DB_ID=...

# 보안
GH_WEBHOOK_SECRET=...

# 옵션
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
```

### 필드 매핑 (config/field_mappings.yml)
```yaml
github_to_notion:
  status:
    github_field: "Status"
    notion_property: "Status"
    type: "select"
  
  sprint:
    github_field: "Sprint"
    notion_property: "Sprint"
    type: "select"
  
  assignees:
    github_field: "assignees"
    notion_property: "Assignees"
    type: "people"
```

## 파일 역할 세부 설명

### 🔧 **Makefile** - 개발 명령어
```makefile
.PHONY: test lint run deploy-lambda

test:
	pytest tests/ -v

lint:
	black src/ tests/
	flake8 src/ tests/

run:
	uvicorn src.main:app --reload

deploy-lambda:
	cd deployment/lambda && ./deployment_package.sh
```

