#!/usr/bin/env python3
"""
Validation script for GitHub to Notion sync setup.
Checks configuration, connections, and field mappings.
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.sync_service import SyncService
from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Setup logging
init_logging()
logger = get_logger(__name__)


class ValidationResult:
    """Container for validation results."""

    def __init__(self):
        self.success = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.success = False

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)

    def add_info(self, message: str):
        """Add an info message."""
        self.info.append(message)

    def print_results(self):
        """Print validation results."""
        if self.info:
            print("\n=== INFORMATION ===")
            for msg in self.info:
                print(f"ℹ️  {msg}")

        if self.warnings:
            print("\n=== WARNINGS ===")
            for msg in self.warnings:
                print(f"⚠️  {msg}")

        if self.errors:
            print("\n=== ERRORS ===")
            for msg in self.errors:
                print(f"❌ {msg}")

        print(f"\n=== SUMMARY ===")
        if self.success:
            print("✅ Validation passed - setup is ready!")
        else:
            print("❌ Validation failed - please fix the errors above")
            print(f"   {len(self.errors)} error(s), {len(self.warnings)} warning(s)")


async def validate_environment_variables() -> ValidationResult:
    """Validate environment variables."""
    result = ValidationResult()

    required_vars = [
        "GITHUB_TOKEN",
        "NOTION_TOKEN",
        "GITHUB_ORG",
        "GITHUB_PROJECT_NUMBER",
        "NOTION_DB_ID",
        "WEBHOOK_SECRET"
    ]

    optional_vars = [
        "LOG_LEVEL",
        "ENVIRONMENT",
        "BATCH_SIZE"
    ]

    # Check required variables
    for var in required_vars:
        if not os.getenv(var):
            result.add_error(f"Required environment variable {var} is not set")
        else:
            result.add_info(f"✅ {var} is set")

    # Check optional variables
    for var in optional_vars:
        if os.getenv(var):
            result.add_info(f"✅ {var} is set ({os.getenv(var)})")
        else:
            result.add_warning(f"Optional environment variable {var} is not set")

    return result


async def validate_configuration() -> ValidationResult:
    """Validate configuration loading and parsing."""
    result = ValidationResult()

    try:
        config = get_config()
        result.add_info("✅ Configuration loaded successfully")

        # Validate settings
        settings = config.settings

        # Check Notion DB ID format
        if not settings.notion_db_id.replace("-", "").isalnum():
            result.add_error("Invalid Notion DB ID format")
        else:
            result.add_info("✅ Notion DB ID format is valid")

        # Check GitHub project number
        if settings.github_project_number <= 0:
            result.add_error("Invalid GitHub project number")
        else:
            result.add_info(f"✅ GitHub project number: {settings.github_project_number}")

        # Check batch size
        if settings.batch_size <= 0:
            result.add_error("Invalid batch size")
        else:
            result.add_info(f"✅ Batch size: {settings.batch_size}")

        # Validate field mappings
        if not config.field_mappings:
            result.add_error("No field mappings configured")
        else:
            result.add_info(f"✅ Field mappings: {len(config.field_mappings)} configured")

            # Check for required mappings
            required_mappings = ["title", "github_node_id"]
            for required_field in required_mappings:
                if required_field not in config.field_mappings:
                    result.add_error(f"Required field mapping '{required_field}' is missing")
                else:
                    result.add_info(f"✅ Required field mapping '{required_field}' is present")

        # Validate webhook events
        if not config.webhook_events:
            result.add_warning("No webhook events configured")
        else:
            result.add_info(f"✅ Webhook events: {len(config.webhook_events)} configured")

    except Exception as e:
        result.add_error(f"Configuration validation failed: {e}")

    return result


async def validate_github_connection() -> ValidationResult:
    """Validate GitHub API connection."""
    result = ValidationResult()

    try:
        github_service = GitHubService()

        # Test basic connection
        project_info = github_service.get_project_info()
        if project_info:
            result.add_info(f"✅ GitHub connection successful")
            result.add_info(f"   Project: {project_info.get('title', 'Unknown')}")
            result.add_info(f"   URL: {project_info.get('url', 'Unknown')}")
        else:
            result.add_error("Failed to retrieve GitHub project information")

        # Test project fields
        fields = github_service.get_project_fields()
        if fields:
            result.add_info(f"✅ GitHub project fields: {len(fields)} found")
            for field in fields[:5]:  # Show first 5 fields
                result.add_info(f"   - {field.name} ({field.data_type})")
        else:
            result.add_warning("No project fields found")

        # Test project items (sample)
        items = list(github_service.get_project_items())
        if items:
            result.add_info(f"✅ GitHub project items: {len(items)} found")
        else:
            result.add_warning("No project items found")

        # Check rate limit
        rate_limit = github_service.get_rate_limit_info()
        if rate_limit:
            result.add_info(f"✅ GitHub rate limit: {rate_limit.remaining}/{rate_limit.limit} remaining")
            if rate_limit.remaining < 100:
                result.add_warning("GitHub rate limit is low")

    except Exception as e:
        result.add_error(f"GitHub connection failed: {e}")

    return result


async def validate_notion_connection() -> ValidationResult:
    """Validate Notion API connection."""
    result = ValidationResult()

    try:
        notion_service = NotionService()

        # Test basic connection
        database_info = notion_service.get_database()
        if database_info:
            result.add_info(f"✅ Notion connection successful")
            result.add_info(f"   Database: {database_info.title}")
            result.add_info(f"   ID: {database_info.id}")
        else:
            result.add_error("Failed to retrieve Notion database information")

        # Test database query
        query_response = notion_service.query_pages(page_size=1)
        if query_response:
            result.add_info(f"✅ Notion database query successful")
            result.add_info(f"   Total pages: {len(query_response.results)}")
        else:
            result.add_error("Failed to query Notion database")

    except Exception as e:
        result.add_error(f"Notion connection failed: {e}")

    return result


async def validate_field_mappings() -> ValidationResult:
    """Validate field mappings configuration."""
    result = ValidationResult()

    try:
        config = get_config()
        notion_service = NotionService()

        # Validate mapping configuration
        mapping_errors = notion_service.field_mapper.validate_mapping_configuration()
        if mapping_errors:
            for error in mapping_errors:
                result.add_error(f"Field mapping error: {error}")
        else:
            result.add_info("✅ Field mappings configuration is valid")

        # Test field mapping functionality
        mapped_fields = notion_service.field_mapper.get_mapped_fields()
        result.add_info(f"✅ Mapped fields: {len(mapped_fields)}")

        required_fields = notion_service.field_mapper.get_required_fields()
        if required_fields:
            result.add_info(f"✅ Required fields: {len(required_fields)}")
            for field in required_fields:
                result.add_info(f"   - {field}")

        # Test user mappings
        user_mappings = config.user_mappings
        if user_mappings:
            result.add_info(f"✅ User mappings: {len(user_mappings)} configured")
        else:
            result.add_warning("No user mappings configured - assignees won't be synced")

    except Exception as e:
        result.add_error(f"Field mappings validation failed: {e}")

    return result


async def validate_sync_functionality() -> ValidationResult:
    """Validate sync functionality."""
    result = ValidationResult()

    try:
        sync_service = SyncService()

        # Test sync service initialization
        result.add_info("✅ Sync service initialized successfully")

        # Test sync validation
        validation_result = await sync_service.validate_sync_setup()
        if validation_result["success"]:
            result.add_info("✅ Sync setup validation passed")
        else:
            for error in validation_result["errors"]:
                result.add_error(f"Sync validation error: {error}")

        # Get sync status
        sync_status = sync_service.get_sync_status()
        result.add_info(f"✅ Sync status retrieved successfully")
        result.add_info(f"   Last full sync: {sync_status['stats']['last_full_sync'] or 'Never'}")
        result.add_info(f"   Total synced: {sync_status['stats']['total_synced']}")
        result.add_info(f"   Errors: {sync_status['stats']['errors']}")

    except Exception as e:
        result.add_error(f"Sync functionality validation failed: {e}")

    return result


async def main():
    """Main function for validation script."""
    parser = argparse.ArgumentParser(description="Validate GitHub to Notion sync setup")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick validation (skip detailed checks)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to fix common issues (if possible)"
    )

    args = parser.parse_args()

    print("🔍 GitHub to Notion Sync Validation")
    print("=" * 50)

    overall_result = ValidationResult()

    # Run validation steps
    validation_steps = [
        ("Environment Variables", validate_environment_variables),
        ("Configuration", validate_configuration),
        ("GitHub Connection", validate_github_connection),
        ("Notion Connection", validate_notion_connection),
        ("Field Mappings", validate_field_mappings),
    ]

    if not args.quick:
        validation_steps.append(("Sync Functionality", validate_sync_functionality))

    for step_name, step_func in validation_steps:
        print(f"\n🔍 Validating {step_name}...")

        try:
            step_result = await step_func()

            # Merge results
            overall_result.errors.extend(step_result.errors)
            overall_result.warnings.extend(step_result.warnings)
            overall_result.info.extend(step_result.info)

            if step_result.errors:
                overall_result.success = False
                print(f"❌ {step_name} validation failed")
            else:
                print(f"✅ {step_name} validation passed")

        except Exception as e:
            overall_result.add_error(f"{step_name} validation crashed: {e}")
            print(f"💥 {step_name} validation crashed")

    # Print final results
    overall_result.print_results()

    # Exit with appropriate code
    sys.exit(0 if overall_result.success else 1)


if __name__ == "__main__":
    asyncio.run(main())
