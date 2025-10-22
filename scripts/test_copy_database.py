#!/usr/bin/env python3
"""
Test script for copy_database_and_sync.py
Tests the database template copying and syncing functionality.
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.logger import init_logging, get_logger
from src.config import get_config
from copy_database_and_sync import CopyDatabaseSyncService

# Initialize logging
init_logging()
logger = get_logger(__name__)


async def test_get_template_properties():
    """Test getting template database properties."""
    logger.info("=" * 70)
    logger.info("Test 1: Get Template Database Properties")
    logger.info("=" * 70)
    
    try:
        # Get template database ID from environment or default
        template_db_id = os.getenv("NOTION_TEMPLATE_DB_ID", "2329eddc34e68057a86ed3de6bae90da")
        template_db_id = template_db_id.replace("-", "")
        
        # Use a dummy parent page ID for testing
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID", "")
        
        if not parent_page_id:
            logger.warning("NOTION_PARENT_PAGE_ID not set, using template DB ID as parent")
            parent_page_id = template_db_id
        
        service = CopyDatabaseSyncService(template_db_id, parent_page_id)
        
        logger.info(f"Template Database ID: {template_db_id}")
        
        # Get properties
        properties = service._get_template_database_properties()
        
        if properties:
            logger.info(f"✅ Successfully retrieved {len(properties)} properties")
            logger.info("\nProperties Schema:")
            for prop_name, prop_config in properties.items():
                prop_type = list(prop_config.keys())[0]
                logger.info(f"  - {prop_name}: {prop_type}")
                
                # Show options for select/multi_select
                if prop_type in ["select", "multi_select"]:
                    options = prop_config[prop_type].get("options", [])
                    if options:
                        logger.info(f"    Options: {[opt['name'] for opt in options]}")
            
            return True
        else:
            logger.error("❌ Failed to retrieve template properties")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False


async def test_dry_run_copy():
    """Test database copy in dry-run mode."""
    logger.info("\n" + "=" * 70)
    logger.info("Test 2: Dry Run Database Copy")
    logger.info("=" * 70)
    
    try:
        # Get configuration
        template_db_id = os.getenv("NOTION_TEMPLATE_DB_ID", "2329eddc34e68057a86ed3de6bae90da")
        template_db_id = template_db_id.replace("-", "")
        
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID", "")
        
        if not parent_page_id:
            logger.warning("NOTION_PARENT_PAGE_ID not set, using template DB ID as parent")
            parent_page_id = template_db_id
        
        service = CopyDatabaseSyncService(template_db_id, parent_page_id)
        
        # Run dry-run copy
        database_title = "Test Copy Database - Dry Run"
        logger.info(f"Database Title: {database_title}")
        
        success = await service.copy_database(database_title, dry_run=True)
        
        if success:
            logger.info("✅ Dry run copy successful")
            return True
        else:
            logger.error("❌ Dry run copy failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False


async def test_dry_run_sync():
    """Test complete sync in dry-run mode."""
    logger.info("\n" + "=" * 70)
    logger.info("Test 3: Dry Run Complete Sync")
    logger.info("=" * 70)
    
    try:
        # Get configuration
        template_db_id = os.getenv("NOTION_TEMPLATE_DB_ID", "2329eddc34e68057a86ed3de6bae90da")
        template_db_id = template_db_id.replace("-", "")
        
        parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID", "")
        
        if not parent_page_id:
            logger.warning("NOTION_PARENT_PAGE_ID not set, using template DB ID as parent")
            parent_page_id = template_db_id
        
        service = CopyDatabaseSyncService(template_db_id, parent_page_id)
        
        # Run dry-run sync
        database_title = "Test Complete Sync - Dry Run"
        logger.info(f"Database Title: {database_title}")
        
        success = await service.run_sync(
            database_title=database_title,
            dry_run=True,
            batch_size=10
        )
        
        if success:
            logger.info("✅ Dry run sync successful")
            logger.info(f"Stats: {service.stats}")
            return True
        else:
            logger.error("❌ Dry run sync failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False


async def run_all_tests():
    """Run all tests."""
    logger.info("Starting copy_database_and_sync tests...\n")
    
    results = []
    
    # Test 1: Get template properties
    result1 = await test_get_template_properties()
    results.append(("Get Template Properties", result1))
    
    # Test 2: Dry run copy
    result2 = await test_dry_run_copy()
    results.append(("Dry Run Copy", result2))
    
    # Test 3: Dry run sync
    result3 = await test_dry_run_sync()
    results.append(("Dry Run Sync", result3))
    
    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info("TEST SUMMARY")
    logger.info("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info(f"\nTotal: {len(results)} tests")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    
    return failed == 0


def main():
    """Main test function."""
    try:
        # Check required environment variables
        if not os.getenv("NOTION_TOKEN"):
            logger.error("NOTION_TOKEN environment variable not set")
            sys.exit(1)
        
        if not os.getenv("GITHUB_TOKEN"):
            logger.error("GITHUB_TOKEN environment variable not set")
            sys.exit(1)
        
        # Run tests
        success = asyncio.run(run_all_tests())
        
        if success:
            logger.info("\n🎉 All tests passed!")
            sys.exit(0)
        else:
            logger.error("\n❌ Some tests failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nTests failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

