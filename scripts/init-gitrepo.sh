#!/bin/bash
# 현재 디렉터리에 github-notion-sync 프로젝트의 전체 파일 구조를 생성하는 스크립트입니다.

# --- 디렉터리 생성 ---
# -p 옵션은 상위 디렉터리가 없을 경우 함께 생성해 줍니다.
echo "Creating directories in the current path..."
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p src/models
mkdir -p src/services
mkdir -p src/utils
mkdir -p src/handlers
mkdir -p scripts
mkdir -p queries
mkdir -p tests/fixtures
mkdir -p deployment/lambda
mkdir -p deployment/docker
mkdir -p deployment/terraform
mkdir -p docs
mkdir -p monitoring/dashboards
mkdir -p monitoring/alerts
mkdir -p config

# --- 빈 파일 생성 ---
# touch 명령어는 파일이 존재하지 않으면 빈 파일을 생성합니다.
echo "Creating empty files..."
touch \
  .github/workflows/notion_sync.yml \
  .github/workflows/deploy_lambda.yml \
  .github/workflows/tests.yml \
  .github/ISSUE_TEMPLATE/bug_report.md \
  src/__init__.py \
  src/main.py \
  src/config.py \
  src/models/__init__.py \
  src/models/github_models.py \
  src/models/notion_models.py \
  src/models/webhook_models.py \
  src/services/__init__.py \
  src/services/github_service.py \
  src/services/notion_service.py \
  src/services/webhook_service.py \
  src/services/sync_service.py \
  src/utils/__init__.py \
  src/utils/logger.py \
  src/utils/rate_limiter.py \
  src/utils/validators.py \
  src/utils/mapping.py \
  src/handlers/__init__.py \
  src/handlers/webhook_handler.py \
  src/handlers/sync_handler.py \
  scripts/setup_github_webhook.py \
  scripts/full_sync.py \
  scripts/validate_setup.py \
  scripts/migrate_data.py \
  queries/get_project_items.graphql \
  queries/get_single_item.graphql \
  queries/get_project_fields.graphql \
  tests/__init__.py \
  tests/conftest.py \
  tests/test_github_service.py \
  tests/test_notion_service.py \
  tests/test_webhook_handler.py \
  tests/test_sync_service.py \
  tests/fixtures/github_responses.json \
  tests/fixtures/notion_responses.json \
  tests/fixtures/webhook_payloads.json \
  deployment/lambda/requirements.txt \
  deployment/lambda/lambda_function.py \
  deployment/lambda/deployment_package.sh \
  deployment/docker/Dockerfile \
  deployment/docker/docker-compose.yml \
  deployment/terraform/main.tf \
  deployment/terraform/variables.tf \
  deployment/terraform/outputs.tf \
  docs/README.md \
  docs/SETUP.md \
  docs/API.md \
  docs/DEPLOYMENT.md \
  docs/TROUBLESHOOTING.md \
  docs/ARCHITECTURE.md \
  monitoring/dashboards/cloudwatch_dashboard.json \
  monitoring/dashboards/grafana_dashboard.json \
  monitoring/alerts/cloudwatch_alarms.yml \
  monitoring/alerts/slack_notifications.py \
  monitoring/health_check.py \
  config/field_mappings.yml \
  config/webhook_events.yml \
  config/sync_config.yml \
  .env.example \
  .gitignore \
  requirements.txt \
  requirements-dev.txt \
  pyproject.toml \
  Makefile

echo "Project structure created successfully in the current directory!"

#--- 생성된 구조 확인 (선택 사항) ---
tree 명령어가 설치되어 있다면 주석을 해제하여 구조를 확인할 수 있습니다.
if command -v tree &> /dev/null
then
    echo "Displaying created structure:"
    tree .
else
    echo "Tree command not found. Skipping structure display."
fi
