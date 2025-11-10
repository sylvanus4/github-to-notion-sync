"""
Pytest configuration and fixtures.

테스트 환경 설정 및 공통 fixture 정의
"""

import os
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """테스트 환경 변수 설정 (모든 테스트에 자동 적용)."""
    # 32자 더미 Notion DB ID (Pydantic validation 통과)
    os.environ["NOTION_DB_ID"] = "12345678901234567890123456789012"
    os.environ["NOTION_TOKEN"] = "secret_test_token_12345678901234567890"
    os.environ["GH_TOKEN"] = "ghp_test_token_1234567890123456789012"
    os.environ["GH_ORG"] = "test-org"
    os.environ["GH_PROJECT_NUMBER"] = "1"
    os.environ["GH_WEBHOOK_SECRET"] = "test-webhook-secret"

    # 테스트 실행

    # Cleanup (필요시)


@pytest.fixture
def mock_config():
    """Mock configuration for tests."""
    config = MagicMock()
    config.settings.notion_token = "secret_test_token"
    config.settings.notion_db_id = "12345678901234567890123456789012"
    config.settings.gh_token = "ghp_test_token"
    config.settings.gh_org = "test-org"
    config.settings.gh_project_number = 1
    config.settings.gh_webhook_secret = "test-webhook-secret"
    return config


@pytest.fixture
def mock_github_service():
    """Mock GitHub service for tests."""
    service = MagicMock()
    service.get_project_items.return_value = []
    service.get_project_fields.return_value = {}
    return service


@pytest.fixture
def mock_notion_service():
    """Mock Notion service for tests."""
    service = MagicMock()
    service.get_all_pages.return_value = []
    service.upsert_github_item.return_value = MagicMock(id="test-page-id")
    return service
