#!/usr/bin/env python3
"""
Full synchronization script for GitHub to Notion sync.
Can be run manually or scheduled via cron/task scheduler.
"""

import sys
import os
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.services.sync_service import SyncService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


async def main():
    """Main function for full sync script."""
    parser = argparse.ArgumentParser(description="Full GitHub to Notion synchronization")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Batch size for processing items (default: from config)"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Also run cleanup of orphaned pages after sync"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration before running sync"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )

    args = parser.parse_args()

    # Configure logging based on quiet flag
    if args.quiet:
        logger.setLevel("WARNING")

    logger.info("Starting full sync script")

    try:
        # Initialize sync service
        sync_service = SyncService()

        # Validate configuration if requested
        if args.validate:
            logger.info("Validating configuration...")
            validation_result = await sync_service.validate_sync_setup()

            if not validation_result["success"]:
                logger.error("Configuration validation failed:")
                for error in validation_result["errors"]:
                    logger.error(f"  - {error}")
                sys.exit(1)

            logger.info("Configuration validation passed")

        # Run dry run if requested
        if args.dry_run:
            logger.info("Running dry run...")
            github_items = sync_service.github_service.get_all_project_items()

            logger.info(f"Found {len(github_items)} items in GitHub project")

            # Check which items would be created vs updated
            created_count = 0
            updated_count = 0

            for item in github_items:
                existing_page = sync_service.notion_service.find_page_by_github_id(item.id)
                if existing_page:
                    updated_count += 1
                else:
                    created_count += 1

            logger.info(f"Would create {created_count} new pages")
            logger.info(f"Would update {updated_count} existing pages")

            return

        # Run full sync
        logger.info("Starting full synchronization...")
        start_time = datetime.utcnow()

        sync_result = await sync_service.full_sync(batch_size=args.batch_size)

        if sync_result["success"]:
            logger.info("Full sync completed successfully")
            logger.info(f"Total items: {sync_result['total_items']}")
            logger.info(f"Created: {sync_result['created']}")
            logger.info(f"Updated: {sync_result['updated']}")
            logger.info(f"Failed: {sync_result['failed']}")
            logger.info(f"Duration: {sync_result['duration_seconds']:.2f} seconds")
        else:
            logger.error(f"Full sync failed: {sync_result.get('error', 'Unknown error')}")
            sys.exit(1)

        # Run cleanup if requested
        if args.cleanup:
            logger.info("Running cleanup of orphaned pages...")
            cleanup_result = await sync_service.cleanup_orphaned_pages()

            if cleanup_result["success"]:
                logger.info("Cleanup completed successfully")
                logger.info(f"Total Notion pages: {cleanup_result['total_notion_pages']}")
                logger.info(f"Orphaned pages: {cleanup_result['orphaned_pages']}")
                logger.info(f"Archived: {cleanup_result['archived']}")
                logger.info(f"Failed to archive: {cleanup_result['failed']}")
            else:
                logger.error(f"Cleanup failed: {cleanup_result.get('error', 'Unknown error')}")
                sys.exit(1)

        # Final summary
        end_time = datetime.utcnow()
        total_duration = (end_time - start_time).total_seconds()

        logger.info(f"Script completed in {total_duration:.2f} seconds")

    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        sys.exit(1)


def run_sync_with_config():
    """Run sync with configuration validation."""
    try:
        config = get_config()
        logger.info("Configuration loaded successfully")

        # Run the async main function
        asyncio.run(main())

    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_sync_with_config()
