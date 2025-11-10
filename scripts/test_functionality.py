#!/usr/bin/env python3
"""
Functionality test script for GitHub to Notion sync.
Simple script to verify all components work with .env configuration.
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

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

# Setup logging
init_logging()
logger = get_logger(__name__)


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")


def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️  {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"ℹ️  {message}")


def test_environment_variables():
    """Test environment variables."""
    print_header("Environment Variables Check")

    required_vars = [
        "GH_TOKEN",
        "NOTION_TOKEN",
        "GH_ORG",
        "GH_PROJECT_NUMBER",
        "NOTION_DB_ID",
        "GH_WEBHOOK_SECRET"
    ]

    optional_vars = [
        "LOG_LEVEL",
        "ENVIRONMENT",
        "BATCH_SIZE"
    ]

    all_good = True

    # Check required variables
    for var in required_vars:
        if os.getenv(var):
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is missing")
            all_good = False

    # Check optional variables
    for var in optional_vars:
        if os.getenv(var):
            print_info(f"{var} is set: {os.getenv(var)}")
        else:
            print_warning(f"{var} is not set (optional)")

    return all_good


def test_configuration():
    """Test configuration loading."""
    print_header("Configuration Loading")

    try:
        config = get_config()
        print_success("Configuration loaded successfully")

        # Check settings
        settings = config.settings
        print_info(f"GitHub Org: {settings.github_org}")
        print_info(f"GitHub Project: {settings.github_project_number}")
        print_info(f"Notion DB ID: {settings.notion_db_id[:8]}...")
        print_info(f"Environment: {settings.environment}")
        print_info(f"Log Level: {settings.log_level}")
        print_info(f"Batch Size: {settings.batch_size}")

        # Check field mappings
        if config.field_mappings:
            print_success(f"Field mappings loaded: {len(config.field_mappings)} fields")

            # Check required mappings
            required_fields = ["title", "github_node_id"]
            for field in required_fields:
                if field in config.field_mappings:
                    print_success(f"Required field '{field}' is mapped")
                else:
                    print_error(f"Required field '{field}' is missing")
                    return False
        else:
            print_error("No field mappings found")
            return False

        # Check webhook events
        if config.webhook_events:
            print_success(f"Webhook events configured: {len(config.webhook_events)} types")
        else:
            print_warning("No webhook events configured")

        # Check user mappings
        if config.user_mappings:
            print_success(f"User mappings configured: {len(config.user_mappings)} users")
        else:
            print_warning("No user mappings configured")

        return True

    except Exception as e:
        print_error(f"Configuration loading failed: {e}")
        return False


def test_github_service():
    """Test GitHub service."""
    print_header("GitHub Service Test")

    try:
        github_service = GitHubService()

        # Test connection
        project_info = github_service.get_project_info()
        if project_info:
            print_success("GitHub connection successful")
            print_info(f"Project: {project_info.get('title', 'Unknown')}")
            print_info(f"URL: {project_info.get('url', 'Unknown')}")
        else:
            print_error("Failed to get GitHub project info")
            return False

        # Test project fields
        fields = github_service.get_project_fields()
        if fields:
            print_success(f"GitHub project fields retrieved: {len(fields)} fields")
            for field in fields[:3]:  # Show first 3
                print_info(f"  - {field.name} ({field.data_type})")
        else:
            print_warning("No project fields found")

        # Test project items
        items = github_service.get_all_project_items()
        if items:
            print_success(f"GitHub project items retrieved: {len(items)} items")
            sample_item = items[0]
            print_info(f"Sample item: {sample_item.get_title()}")
            print_info(f"Type: {sample_item.type.value}")
        else:
            print_warning("No project items found")

        # Test rate limit
        rate_limit = github_service.get_rate_limit_info()
        if rate_limit:
            print_info(f"Rate limit: {rate_limit.remaining}/{rate_limit.limit} remaining")

        return True

    except Exception as e:
        print_error(f"GitHub service test failed: {e}")
        return False


def test_notion_service():
    """Test Notion service."""
    print_header("Notion Service Test")

    try:
        notion_service = NotionService()

        # Test connection
        database = notion_service.get_database()
        if database:
            print_success("Notion connection successful")
            print_info(f"Database: {database.title}")
            print_info(f"ID: {database.id}")
        else:
            print_error("Failed to get Notion database info")
            return False

        # Test query
        response = notion_service.query_pages(page_size=3)
        if response:
            print_success(f"Notion query successful: {len(response.results)} pages found")
            print_info(f"Has more pages: {response.has_more}")
        else:
            print_error("Failed to query Notion database")
            return False

        # Test field mappings
        field_mapper = notion_service.field_mapper
        errors = field_mapper.validate_mapping_configuration()
        if not errors:
            print_success("Field mappings validation passed")
            mapped_fields = field_mapper.get_mapped_fields()
            print_info(f"Mapped fields: {len(mapped_fields)}")
        else:
            print_error("Field mappings validation failed:")
            for error in errors:
                print_error(f"  - {error}")
            return False

        return True

    except Exception as e:
        print_error(f"Notion service test failed: {e}")
        return False


async def test_sync_service():
    """Test sync service."""
    print_header("Sync Service Test")

    try:
        sync_service = SyncService()

        # Test validation
        validation_result = await sync_service.validate_sync_setup()
        if validation_result["success"]:
            print_success("Sync setup validation passed")
            print_success(f"GitHub connection: {validation_result['github_connection']}")
            print_success(f"Notion connection: {validation_result['notion_connection']}")
            print_success(f"Field mappings: {validation_result['field_mappings']}")
        else:
            print_error("Sync setup validation failed:")
            for error in validation_result["errors"]:
                print_error(f"  - {error}")
            return False

        # Test status
        status = sync_service.get_sync_status()
        print_info(f"Last full sync: {status['stats']['last_full_sync'] or 'Never'}")
        print_info(f"Total synced: {status['stats']['total_synced']}")
        print_info(f"Webhook syncs: {status['stats']['webhook_syncs']}")
        print_info(f"Errors: {status['stats']['errors']}")

        return True

    except Exception as e:
        print_error(f"Sync service test failed: {e}")
        return False


async def test_webhook_handler():
    """Test webhook handler."""
    print_header("Webhook Handler Test")

    try:
        webhook_handler = WebhookHandler()

        # Test signature verification
        import hmac
        import hashlib

        body = b'{"test": "data"}'
        secret = webhook_handler.settings.webhook_secret
        signature = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()

        if webhook_handler.verify_signature(f"sha256={signature}", body):
            print_success("Webhook signature verification working")
        else:
            print_error("Webhook signature verification failed")
            return False

        # Test configuration validation
        validation_result = await webhook_handler.validate_webhook_config()
        if validation_result["success"]:
            print_success("Webhook configuration validation passed")
            print_info(f"Webhook secret configured: {validation_result['webhook_secret_configured']}")
            print_info(f"Enabled events: {len(validation_result['enabled_events'])}")
        else:
            print_error("Webhook configuration validation failed:")
            for error in validation_result["errors"]:
                print_error(f"  - {error}")
            return False

        # Test stats
        stats = webhook_handler.get_webhook_stats()
        print_info(f"Total received: {stats['total_received']}")
        print_info(f"Success rate: {stats['success_rate']:.1f}%")

        return True

    except Exception as e:
        print_error(f"Webhook handler test failed: {e}")
        return False


async def test_sample_sync():
    """Test a sample sync operation."""
    print_header("Sample Sync Test")

    try:
        sync_service = SyncService()

        # Get GitHub items
        github_items = sync_service.github_service.get_all_project_items()
        if not github_items:
            print_warning("No GitHub items found to test sync")
            return True

        # Test syncing one item
        sample_item = github_items[0]
        print_info(f"Testing sync for item: {sample_item.get_title()}")
        print_info(f"Item ID: {sample_item.id}")

        # Build properties (test without actually syncing)
        properties = sync_service.notion_service.build_properties_from_github_item(sample_item)
        if properties:
            print_success("Properties built successfully")
            print_info(f"Built {len(properties)} properties")

            # Show some properties
            for key, value in list(properties.items())[:3]:
                print_info(f"  - {key}: {type(value).__name__}")
        else:
            print_warning("No properties could be built")

        # Check if item already exists in Notion
        existing_page = sync_service.notion_service.find_page_by_github_id(sample_item.id)
        if existing_page:
            print_info("Item already exists in Notion")
        else:
            print_info("Item does not exist in Notion (would be created)")

        return True

    except Exception as e:
        print_error(f"Sample sync test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 GitHub to Notion Sync - Functionality Test")
    print("=" * 60)

    start_time = datetime.now()
    tests_passed = 0
    total_tests = 7

    # Run tests
    test_results = []

    # Test 1: Environment Variables
    result = test_environment_variables()
    test_results.append(("Environment Variables", result))
    if result:
        tests_passed += 1

    # Test 2: Configuration
    result = test_configuration()
    test_results.append(("Configuration", result))
    if result:
        tests_passed += 1

    # Test 3: GitHub Service
    result = test_github_service()
    test_results.append(("GitHub Service", result))
    if result:
        tests_passed += 1

    # Test 4: Notion Service
    result = test_notion_service()
    test_results.append(("Notion Service", result))
    if result:
        tests_passed += 1

    # Test 5: Sync Service
    result = await test_sync_service()
    test_results.append(("Sync Service", result))
    if result:
        tests_passed += 1

    # Test 6: Webhook Handler
    result = await test_webhook_handler()
    test_results.append(("Webhook Handler", result))
    if result:
        tests_passed += 1

    # Test 7: Sample Sync
    result = await test_sample_sync()
    test_results.append(("Sample Sync", result))
    if result:
        tests_passed += 1

    # Print summary
    print_header("Test Summary")

    for test_name, passed in test_results:
        if passed:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{'='*60}")
    print(f"Tests completed in {duration:.2f} seconds")
    print(f"Passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print_success("🎉 All tests passed! Your setup is working correctly.")
        return True
    else:
        print_error(f"❌ {total_tests - tests_passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test script failed: {e}")
        exit(1)
