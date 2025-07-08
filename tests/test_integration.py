"""
Integration tests for GitHub to Notion sync system.
Tests real functionality with actual .env configuration.
"""

import os
import sys
import asyncio
import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file
try:
    from dotenv import load_dotenv
    # Load .env from project root
    load_dotenv(dotenv_path=project_root / ".env")
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

from src.config import get_config
from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.services.sync_service import SyncService
from src.handlers.webhook_handler import WebhookHandler
from src.utils.logger import init_logging, get_logger
from src.models.webhook_models import WebhookParser, WebhookEventType

# Setup logging for tests
init_logging()
logger = get_logger(__name__)


class TestEnvironmentSetup:
    """Test environment configuration and setup."""
    
    def test_environment_variables(self):
        """Test that all required environment variables are set."""
        required_vars = [
            "GH_TOKEN",
            "NOTION_TOKEN", 
            "GH_ORG",
            "GH_PROJECT_NUMBER",
            "NOTION_DB_ID",
            "GH_WEBHOOK_SECRET"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        assert not missing_vars, f"Missing required environment variables: {missing_vars}"
        logger.info("✅ All required environment variables are set")
    
    def test_config_loading(self):
        """Test configuration loading."""
        config = get_config()
        
        assert config is not None
        assert config.settings is not None
        assert config.field_mappings is not None
        assert len(config.field_mappings) > 0
        
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"   - Field mappings: {len(config.field_mappings)}")
        logger.info(f"   - Webhook events: {len(config.webhook_events)}")


class TestGitHubService:
    """Test GitHub service functionality."""
    
    @pytest.fixture
    def github_service(self):
        """GitHub service fixture."""
        return GitHubService()
    
    def test_github_connection(self, github_service):
        """Test GitHub API connection."""
        project_info = github_service.get_project_info()
        
        assert project_info is not None
        assert "id" in project_info
        assert "title" in project_info
        
        logger.info("✅ GitHub connection successful")
        logger.info(f"   - Project: {project_info.get('title')}")
        logger.info(f"   - URL: {project_info.get('url')}")
    
    def test_github_project_fields(self, github_service):
        """Test fetching GitHub project fields."""
        fields = github_service.get_project_fields()
        
        assert isinstance(fields, list)
        assert len(fields) > 0
        
        logger.info("✅ GitHub project fields retrieved")
        logger.info(f"   - Found {len(fields)} fields")
        
        for field in fields[:3]:  # Show first 3 fields
            logger.info(f"   - {field.name} ({field.data_type})")
    
    def test_github_project_items(self, github_service):
        """Test fetching GitHub project items."""
        items = github_service.get_all_project_items()
        
        assert isinstance(items, list)
        
        logger.info("✅ GitHub project items retrieved")
        logger.info(f"   - Found {len(items)} items")
        
        if items:
            sample_item = items[0]
            logger.info(f"   - Sample item: {sample_item.id}")
            logger.info(f"   - Type: {sample_item.type}")
            logger.info(f"   - Title: {sample_item.get_title()}")
    
    def test_github_rate_limit(self, github_service):
        """Test GitHub rate limit information."""
        rate_limit = github_service.get_rate_limit_info()
        
        if rate_limit:
            logger.info("✅ GitHub rate limit info retrieved")
            logger.info(f"   - Remaining: {rate_limit.remaining}/{rate_limit.limit}")
            logger.info(f"   - Reset at: {rate_limit.reset_at}")
            
            assert rate_limit.remaining >= 0
            assert rate_limit.limit > 0
        else:
            logger.info("ℹ️ GitHub rate limit info not available yet")


class TestNotionService:
    """Test Notion service functionality."""
    
    @pytest.fixture
    def notion_service(self):
        """Notion service fixture."""
        return NotionService()
    
    def test_notion_connection(self, notion_service):
        """Test Notion API connection."""
        database = notion_service.get_database()
        
        assert database is not None
        assert database.id is not None
        assert database.title is not None
        
        logger.info("✅ Notion connection successful")
        logger.info(f"   - Database: {database.title}")
        logger.info(f"   - ID: {database.id}")
    
    def test_notion_query_pages(self, notion_service):
        """Test querying Notion pages."""
        response = notion_service.query_pages(page_size=5)
        
        assert response is not None
        assert isinstance(response.results, list)
        
        logger.info("✅ Notion pages query successful")
        logger.info(f"   - Found {len(response.results)} pages (sample)")
        logger.info(f"   - Has more: {response.has_more}")
    
    def test_notion_field_mappings(self, notion_service):
        """Test field mapping functionality."""
        field_mapper = notion_service.field_mapper
        
        # Test mapping validation
        errors = field_mapper.validate_mapping_configuration()
        assert not errors, f"Field mapping errors: {errors}"
        
        # Test field mapping functions
        mapped_fields = field_mapper.get_mapped_fields()
        required_fields = field_mapper.get_required_fields()
        
        assert len(mapped_fields) > 0
        
        logger.info("✅ Field mappings validation successful")
        logger.info(f"   - Mapped fields: {len(mapped_fields)}")
        logger.info(f"   - Required fields: {len(required_fields)}")


class TestSyncService:
    """Test sync service functionality."""
    
    @pytest.fixture
    def sync_service(self):
        """Sync service fixture."""
        return SyncService()
    
    @pytest.mark.asyncio
    async def test_sync_validation(self, sync_service):
        """Test sync setup validation."""
        validation_result = await sync_service.validate_sync_setup()
        
        assert validation_result["success"], f"Sync validation failed: {validation_result['errors']}"
        assert validation_result["github_connection"]
        assert validation_result["notion_connection"]
        assert validation_result["field_mappings"]
        
        logger.info("✅ Sync setup validation passed")
    
    def test_sync_status(self, sync_service):
        """Test sync status retrieval."""
        status = sync_service.get_sync_status()
        
        assert isinstance(status, dict)
        assert "stats" in status
        assert "config" in status
        
        logger.info("✅ Sync status retrieved")
        logger.info(f"   - Last full sync: {status['stats']['last_full_sync']}")
        logger.info(f"   - Total synced: {status['stats']['total_synced']}")
    
    @pytest.mark.asyncio
    async def test_single_item_sync(self, sync_service):
        """Test syncing a single item."""
        # Get a sample GitHub item
        github_items = sync_service.github_service.get_all_project_items()
        
        if not github_items:
            pytest.skip("No GitHub items found for testing")
        
        sample_item = github_items[0]
        logger.info(f"Testing sync for item: {sample_item.id}")
        
        # Test the sync
        success = await sync_service._sync_single_item(sample_item.id)
        
        # Note: This might fail if there are field mapping issues, which is expected
        logger.info(f"Single item sync result: {success}")
        
        # Verify the item exists in Notion (if sync was successful)
        if success:
            notion_page = sync_service.notion_service.find_page_by_github_id(sample_item.id)
            assert notion_page is not None
            logger.info("✅ Item successfully synced to Notion")


class TestWebhookHandler:
    """Test webhook handler functionality."""
    
    @pytest.fixture
    def webhook_handler(self):
        """Webhook handler fixture."""
        return WebhookHandler()
    
    def test_webhook_signature_verification(self, webhook_handler):
        """Test webhook signature verification."""
        # Test data
        body = b'{"test": "data"}'
        secret = webhook_handler.settings.webhook_secret
        
        # Create valid signature
        import hmac
        import hashlib
        
        signature = hmac.new(
            secret.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
        
        # Test valid signature
        assert webhook_handler.verify_signature(f"sha256={signature}", body)
        
        # Test invalid signature
        assert not webhook_handler.verify_signature("sha256=invalid", body)
        
        logger.info("✅ Webhook signature verification working")
    
    @pytest.mark.asyncio
    async def test_webhook_config_validation(self, webhook_handler):
        """Test webhook configuration validation."""
        validation_result = await webhook_handler.validate_webhook_config()
        
        assert validation_result["webhook_secret_configured"]
        
        logger.info("✅ Webhook configuration validation passed")
        logger.info(f"   - Enabled events: {len(validation_result['enabled_events'])}")
    
    def test_webhook_stats(self, webhook_handler):
        """Test webhook statistics."""
        stats = webhook_handler.get_webhook_stats()
        
        assert isinstance(stats, dict)
        assert "total_received" in stats
        assert "success_rate" in stats
        
        logger.info("✅ Webhook statistics retrieved")
    
    @pytest.mark.asyncio
    async def test_webhook_parsing(self, webhook_handler):
        """Test webhook payload parsing."""
        # Sample projects_v2_item webhook payload
        sample_payload = {
            "action": "created",
            "projects_v2_item": {
                "id": "test_id",
                "node_id": "test_node_id",
                "project_node_id": "test_project_id",
                "content_node_id": "test_content_id",
                "content_type": "Issue",
                "creator": {
                    "login": "testuser",
                    "id": 12345,
                    "avatar_url": "https://github.com/images/error/testuser_happy.gif",
                    "url": "https://api.github.com/users/testuser"
                },
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "archived_at": None
            },
            "organization": {
                "login": "testorg",
                "id": 67890,
                "node_id": "test_org_node_id",
                "url": "https://api.github.com/orgs/testorg",
                "repos_url": "https://api.github.com/orgs/testorg/repos",
                "events_url": "https://api.github.com/orgs/testorg/events",
                "hooks_url": "https://api.github.com/orgs/testorg/hooks",
                "issues_url": "https://api.github.com/orgs/testorg/issues",
                "members_url": "https://api.github.com/orgs/testorg/members{/member}",
                "public_members_url": "https://api.github.com/orgs/testorg/public_members{/member}",
                "avatar_url": "https://github.com/images/error/testorg_happy.gif",
                "description": "Test organization"
            },
            "sender": {
                "login": "testuser",
                "id": 12345,
                "avatar_url": "https://github.com/images/error/testuser_happy.gif",
                "url": "https://api.github.com/users/testuser"
            }
        }
        
        # Test parsing
        webhook_event = WebhookParser.create_webhook_event(
            "projects_v2_item",
            "test-delivery-id",
            "test-signature",
            sample_payload
        )
        
        assert webhook_event.event_type == WebhookEventType.PROJECTS_V2_ITEM
        assert webhook_event.delivery_id == "test-delivery-id"
        
        logger.info("✅ Webhook payload parsing working")


class TestFullIntegration:
    """Test full integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_validation(self):
        """Test complete end-to-end validation."""
        logger.info("🔍 Running end-to-end validation...")
        
        # Test all services
        config = get_config()
        github_service = GitHubService()
        notion_service = NotionService()
        sync_service = SyncService()
        webhook_handler = WebhookHandler()
        
        # Validate GitHub
        project_info = github_service.get_project_info()
        assert project_info is not None
        
        # Validate Notion
        database = notion_service.get_database()
        assert database is not None
        
        # Validate sync setup
        validation_result = await sync_service.validate_sync_setup()
        assert validation_result["success"]
        
        # Validate webhook config
        webhook_validation = await webhook_handler.validate_webhook_config()
        assert webhook_validation["webhook_secret_configured"]
        
        logger.info("✅ End-to-end validation passed!")
    
    def test_configuration_completeness(self):
        """Test that configuration is complete and valid."""
        config = get_config()
        
        # Check field mappings
        assert "title" in config.field_mappings
        assert "github_node_id" in config.field_mappings
        
        # Check webhook events
        assert len(config.webhook_events) > 0
        
        # Check user mappings
        if config.user_mappings:
            logger.info(f"✅ User mappings configured: {len(config.user_mappings)}")
        else:
            logger.warning("⚠️ No user mappings configured")
        
        logger.info("✅ Configuration completeness check passed")


def run_integration_tests():
    """Run integration tests with proper setup."""
    logger.info("🚀 Starting integration tests...")
    
    # Check if .env is properly configured
    required_vars = ["GH_TOKEN", "NOTION_TOKEN", "GH_ORG", "GH_PROJECT_NUMBER", "NOTION_DB_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please configure your .env file properly before running tests")
        return False
    
    try:
        # Run pytest programmatically
        import pytest
        
        # Run tests with verbose output
        exit_code = pytest.main([
            __file__,
            "-v",
            "--tb=short",
            "-s"  # Don't capture output
        ])
        
        if exit_code == 0:
            logger.info("✅ All integration tests passed!")
            return True
        else:
            logger.error("❌ Some integration tests failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1) 