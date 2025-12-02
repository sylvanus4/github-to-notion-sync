#!/usr/bin/env python3
"""
QA Issues Sync Script.
Filters GitHub project issues by QA-related labels (qa, 품질, bug)
and syncs them to a dedicated Notion database.
Supports duplicate prevention via GitHub ID.
"""

import sys
import os
import asyncio
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Any

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import yaml

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.models.github_models import GitHubProjectItem, GitHubLabel
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)

# Korean Standard Time (UTC+9)
KST = timezone(timedelta(hours=9))

# QA-related label keywords (case-insensitive)
QA_LABEL_KEYWORDS = ['qa', '품질', 'bug']


def load_qa_config() -> dict:
    """Load QA sync configuration from sprint_config.yml.
    
    Returns:
        Dictionary with QA sync configuration
    """
    config_path = Path(__file__).parent.parent / "config" / "sprint_config.yml"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return {
            'qa_database_id': config.get('qa_database_id'),
            'current_sprint': config.get('current_sprint'),
        }
    except Exception as e:
        logger.warning(f"Failed to load QA config from sprint_config.yml: {e}")
        return {}


def is_qa_issue(item: GitHubProjectItem) -> bool:
    """Check if a GitHub project item has QA-related labels.
    
    Args:
        item: GitHub project item to check
        
    Returns:
        True if the item has QA-related labels, False otherwise
    """
    labels: List[GitHubLabel] = item.get_labels()
    
    if not labels:
        return False
    
    for label in labels:
        label_name = label.name.lower()
        if any(keyword in label_name for keyword in QA_LABEL_KEYWORDS):
            logger.debug(f"Item '{item.get_title()}' matched QA label: {label.name}")
            return True
    
    return False


class QAIssuesSyncService:
    """Service for syncing QA-related issues from GitHub to Notion."""
    
    def __init__(self, notion_database_id: str, sprint_filter: Optional[str] = None):
        """Initialize QA issues sync service.
        
        Args:
            notion_database_id: Target Notion database ID for QA issues
            sprint_filter: Optional sprint name to filter items
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.notion_database_id = notion_database_id
        self.sprint_filter = sprint_filter
        
        # Track sync statistics
        self.stats = {
            "start_time": None,
            "end_time": None,
            "total_github_items": 0,
            "qa_items_found": 0,
            "notion_pages_created": 0,
            "notion_pages_updated": 0,
            "failures": 0,
        }
    
    def _find_existing_page(self, github_node_id: str) -> Optional[Any]:
        """Find existing page by GitHub Node ID in the QA database.
        
        Args:
            github_node_id: GitHub project item node ID
            
        Returns:
            NotionPage or None if not found
        """
        try:
            # Query the QA database for existing page with this GitHub ID
            filter_dict = {
                "property": "GitHub ID",
                "rich_text": {"equals": github_node_id}
            }
            
            def _query_pages():
                return self.notion_service.client.databases.query(
                    database_id=self.notion_database_id,
                    filter=filter_dict,
                    page_size=1
                )
            
            response = self.notion_service._handle_rate_limit(_query_pages)
            results = response.get("results", [])
            
            if results:
                from src.models.notion_models import NotionPage
                return NotionPage(**results[0])
            
            return None
            
        except Exception as e:
            logger.warning(f"Error finding existing page for {github_node_id}: {e}")
            return None
    
    def _create_page_in_qa_database(self, properties: dict) -> Optional[Any]:
        """Create a page in the QA database.
        
        Args:
            properties: Page properties
            
        Returns:
            NotionPage or None if creation failed
        """
        try:
            def _create_page():
                return self.notion_service.client.pages.create(
                    parent={"database_id": self.notion_database_id},
                    properties=properties
                )
            
            response = self.notion_service._handle_rate_limit(_create_page)
            
            from src.models.notion_models import NotionPage
            return NotionPage(**response)
            
        except Exception as e:
            logger.error(f"Failed to create page in QA database: {e}")
            return None
    
    def _update_page(self, page_id: str, properties: dict) -> Optional[Any]:
        """Update an existing page.
        
        Args:
            page_id: Notion page ID
            properties: Updated properties
            
        Returns:
            NotionPage or None if update failed
        """
        try:
            def _update_page():
                return self.notion_service.client.pages.update(
                    page_id=page_id,
                    properties=properties
                )
            
            response = self.notion_service._handle_rate_limit(_update_page)
            
            from src.models.notion_models import NotionPage
            return NotionPage(**response)
            
        except Exception as e:
            logger.error(f"Failed to update page {page_id}: {e}")
            return None
    
    def upsert_qa_item(self, github_item: GitHubProjectItem) -> tuple[bool, str]:
        """Upsert a QA item to the Notion database.
        
        Args:
            github_item: GitHub project item
            
        Returns:
            Tuple of (success, action) where action is 'created', 'updated', or 'failed'
        """
        try:
            # Build properties from GitHub item
            properties = self.notion_service.build_properties_from_github_item(github_item)
            
            if not properties:
                logger.warning(f"No properties built for GitHub item {github_item.id}")
                return False, 'failed'
            
            # Check if page already exists in QA database
            existing_page = self._find_existing_page(github_item.id)
            
            if existing_page:
                # Update existing page
                result = self._update_page(existing_page.id, properties)
                if result:
                    logger.debug(f"Updated page for: {github_item.get_title()}")
                    return True, 'updated'
                return False, 'failed'
            else:
                # Create new page
                result = self._create_page_in_qa_database(properties)
                if result:
                    logger.debug(f"Created page for: {github_item.get_title()}")
                    return True, 'created'
                return False, 'failed'
                
        except Exception as e:
            logger.error(f"Failed to upsert QA item {github_item.id}: {e}")
            return False, 'failed'
    
    async def collect_qa_items(self) -> List[GitHubProjectItem]:
        """Collect QA-related items from GitHub project.
        
        Returns:
            List of QA-related GitHub project items
        """
        logger.info(f"Collecting GitHub project items{f' for sprint: {self.sprint_filter}' if self.sprint_filter else ''}...")
        
        try:
            # Get all project items (with optional sprint filter)
            all_items = self.github_service.get_all_project_items(sprint_filter=self.sprint_filter)
            self.stats["total_github_items"] = len(all_items)
            
            logger.info(f"Found {len(all_items)} total items in GitHub project")
            
            # Filter for QA-related items
            qa_items = [item for item in all_items if is_qa_issue(item)]
            self.stats["qa_items_found"] = len(qa_items)
            
            logger.info(f"Found {len(qa_items)} QA-related items (labels containing: {', '.join(QA_LABEL_KEYWORDS)})")
            
            return qa_items
            
        except Exception as e:
            logger.error(f"Error collecting QA items: {e}")
            return []
    
    async def run(self, dry_run: bool = False, batch_size: int = 50) -> bool:
        """Run QA issues sync.
        
        Args:
            dry_run: If True, only analyze without making changes
            batch_size: Number of items to process in each batch
            
        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.now(KST)
        
        logger.info("=" * 60)
        logger.info("Starting QA Issues Sync")
        logger.info(f"Target database: {self.notion_database_id}")
        if self.sprint_filter:
            logger.info(f"Sprint filter: {self.sprint_filter}")
        logger.info(f"QA label keywords: {QA_LABEL_KEYWORDS}")
        logger.info("=" * 60)
        
        try:
            # Step 1: Collect QA items
            qa_items = await self.collect_qa_items()
            
            if not qa_items:
                logger.info("No QA-related items found to sync")
                return True
            
            if dry_run:
                logger.info(f"\n[DRY RUN] Would sync {len(qa_items)} QA items to Notion")
                logger.info("\nSample QA items:")
                for i, item in enumerate(qa_items[:10], 1):
                    labels = [label.name for label in item.get_labels()]
                    logger.info(f"  {i}. {item.get_title()}")
                    logger.info(f"     Labels: {', '.join(labels)}")
                    logger.info(f"     URL: {item.get_url()}")
                    
                if len(qa_items) > 10:
                    logger.info(f"  ... and {len(qa_items) - 10} more items")
                    
                return True
            
            # Step 2: Sync items to Notion
            logger.info(f"\nSyncing {len(qa_items)} QA items to Notion...")
            
            for i, item in enumerate(qa_items, 1):
                try:
                    success, action = self.upsert_qa_item(item)
                    
                    if success:
                        if action == 'created':
                            self.stats["notion_pages_created"] += 1
                        elif action == 'updated':
                            self.stats["notion_pages_updated"] += 1
                    else:
                        self.stats["failures"] += 1
                    
                    # Progress logging
                    if i % 10 == 0 or i == len(qa_items):
                        logger.info(f"Progress: {i}/{len(qa_items)} items processed")
                    
                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    logger.error(f"Error processing item {i}: {e}")
                    self.stats["failures"] += 1
            
            self.stats["end_time"] = datetime.now(KST)
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            
            # Final summary
            logger.info("\n" + "=" * 60)
            logger.info("QA Issues Sync Completed!")
            logger.info("=" * 60)
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Total GitHub items scanned: {self.stats['total_github_items']}")
            logger.info(f"QA items found: {self.stats['qa_items_found']}")
            logger.info(f"Pages created: {self.stats['notion_pages_created']}")
            logger.info(f"Pages updated: {self.stats['notion_pages_updated']}")
            
            if self.stats["failures"] > 0:
                logger.warning(f"Failures: {self.stats['failures']}")
            
            # Success if at least 90% of items were synced
            total_synced = self.stats["notion_pages_created"] + self.stats["notion_pages_updated"]
            success_rate = (total_synced / len(qa_items) * 100) if qa_items else 100
            
            return success_rate >= 90.0
            
        except Exception as e:
            logger.error(f"QA Issues sync failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main function for QA issues sync script."""
    parser = argparse.ArgumentParser(
        description="Sync QA-related issues from GitHub to Notion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync QA issues for current sprint
  python scripts/qa_issues_sync.py --notion-database-id abc123

  # Sync with sprint filter
  python scripts/qa_issues_sync.py --notion-database-id abc123 --sprint "25-12-Sprint1"

  # Dry run (preview only)
  python scripts/qa_issues_sync.py --notion-database-id abc123 --dry-run

  # Use config file for database ID
  python scripts/qa_issues_sync.py
        """
    )
    
    parser.add_argument(
        "--notion-database-id",
        help="Target Notion database ID for QA issues (or set via config/sprint_config.yml)"
    )
    parser.add_argument(
        "--sprint",
        help="Sprint name to filter items (e.g., '25-12-Sprint1')"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be synced without making changes"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for processing (default: 50)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.quiet:
        logger.setLevel("WARNING")
    
    # Load configuration
    qa_config = load_qa_config()
    
    # Determine database ID
    database_id = args.notion_database_id or qa_config.get('qa_database_id')
    if not database_id:
        logger.error("Notion database ID is required. Provide via --notion-database-id or config/sprint_config.yml")
        sys.exit(1)
    
    # Determine sprint filter
    sprint_filter = args.sprint or qa_config.get('current_sprint')
    
    logger.info("Starting QA Issues Sync script")
    
    try:
        # Initialize service
        sync_service = QAIssuesSyncService(
            notion_database_id=database_id,
            sprint_filter=sprint_filter
        )
        
        # Run sync
        success = await sync_service.run(
            dry_run=args.dry_run,
            batch_size=args.batch_size
        )
        
        if success:
            logger.info("QA Issues sync script completed successfully")
            sys.exit(0)
        else:
            logger.error("QA Issues sync script failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_with_config():
    """Run script with configuration validation."""
    try:
        config = get_config()
        logger.info("Configuration loaded successfully")
        
        # Run the async main function
        asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_with_config()

