#!/usr/bin/env python3
"""
Create new database and sync script for GitHub to Notion.
Creates a new Notion database under a specified page and syncs GitHub project data to it.
"""

import sys
import os
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.github_service import GitHubService
from src.services.notion_service import NotionService
from src.utils.logger import init_logging, get_logger
from src.config import get_config

# Initialize logging
init_logging()
logger = get_logger(__name__)


class CreateNewDatabaseSyncService:
    """Service for creating a new Notion database and syncing GitHub project data to it."""

    def __init__(self, parent_page_id: str):
        """Initialize sync service.

        Args:
            parent_page_id: ID of the parent page where the database will be created
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.parent_page_id = parent_page_id
        self.new_database_id = None

        # Track sync statistics
        self.stats = {
            "total_github_items": 0,
            "database_created": False,
            "notion_pages_created": 0,
            "failures": 0,
            "start_time": None,
            "end_time": None
        }

    def _build_database_properties_schema(self) -> Dict[str, Any]:
        """Build database properties schema based on field mappings configuration.

        Returns:
            Dictionary of Notion database properties schema
        """
        properties = {}

        # Map each field from configuration to Notion property schema
        for field_name, field_config in self.config.field_mappings.items():
            notion_property = field_config.get("notion_property")
            property_type = field_config.get("type")

            if not notion_property or not property_type:
                continue

            # Build property schema based on type
            if property_type == "title":
                properties[notion_property] = {"title": {}}

            elif property_type == "multi_select":
                # For multi_select, we need to define options
                value_mappings = field_config.get("value_mappings", {})
                options = [{"name": value, "color": "default"}
                          for value in value_mappings.values()]
                properties[notion_property] = {
                    "multi_select": {"options": options}
                }

            elif property_type == "status":
                # For status in database creation, Notion API doesn't allow specifying options/groups
                # We use select instead, which provides similar functionality
                value_mappings = field_config.get("value_mappings", {})
                options = [{"name": value, "color": self._get_status_color(value)}
                          for value in set(value_mappings.values())]
                properties[notion_property] = {
                    "select": {"options": options}
                }

            elif property_type == "select":
                # For select, define options
                value_mappings = field_config.get("value_mappings", {})
                options = [{"name": value, "color": "default"}
                          for value in value_mappings.values() if value]
                properties[notion_property] = {
                    "select": {"options": options}
                }

            elif property_type == "date":
                properties[notion_property] = {"date": {}}

            elif property_type == "number":
                properties[notion_property] = {"number": {}}

            elif property_type == "people":
                properties[notion_property] = {"people": {}}

        return properties

    def _get_status_color(self, status_name: str) -> str:
        """Get color for status option.

        Args:
            status_name: Status name

        Returns:
            Color name for the status
        """
        color_mapping = {
            "시작 전": "gray",
            "진행 중": "blue",
            "완료": "green",
            "보관": "red"
        }
        return color_mapping.get(status_name, "gray")

    async def create_new_database(self, database_title: str, dry_run: bool = False) -> bool:
        """Create a new Notion database under the specified parent page.

        Args:
            database_title: Title for the new database
            dry_run: If True, only show what would be created

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Creating new database: {database_title}")
        logger.info(f"Parent page ID: {self.parent_page_id}")

        try:
            # Build properties schema from configuration
            properties_schema = self._build_database_properties_schema()

            if dry_run:
                logger.info(f"[DRY RUN] Would create database with properties:")
                for prop_name, prop_config in properties_schema.items():
                    prop_type = list(prop_config.keys())[0]
                    logger.info(f"  - {prop_name} ({prop_type})")
                self.stats["database_created"] = True
                return True

            # Create the database
            database_id = self.notion_service.create_database(
                parent_page_id=self.parent_page_id,
                title=database_title,
                properties_schema=properties_schema
            )

            if not database_id:
                logger.error("Failed to create database")
                return False

            self.new_database_id = database_id
            self.stats["database_created"] = True

            logger.info(f"Successfully created database: {database_id}")
            logger.info(f"Database properties: {len(properties_schema)} properties")

            return True

        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return False

    async def sync_all_github_items(self, dry_run: bool = False, batch_size: int = 50, sprint_filter: Optional[str] = None) -> bool:
        """Sync all GitHub project items to the new Notion database.

        Args:
            dry_run: If True, only analyze items without creating
            batch_size: Number of items to process in each batch
            sprint_filter: Optional sprint name to filter items

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Retrieving items from GitHub project{f' for sprint: {sprint_filter}' if sprint_filter else ''}...")

        try:
            # Get all GitHub project items (with optional sprint filter)
            github_items = self.github_service.get_all_project_items(sprint_filter=sprint_filter)

            if not github_items:
                logger.info("No items found in GitHub project")
                return True

            self.stats["total_github_items"] = len(github_items)
            logger.info(f"Found {len(github_items)} items in GitHub project")

            if dry_run:
                logger.info(f"[DRY RUN] Would create {len(github_items)} pages in new database")
                self.stats["notion_pages_created"] = len(github_items)

                # Analyze item types and statuses
                item_types = {}
                item_statuses = {}
                item_priorities = {}
                sample_items = []

                for item in github_items[:5]:  # Show first 5 items as samples
                    # Get title safely
                    title = item.get_title() if hasattr(item, 'get_title') else 'Unknown'

                    # Count types
                    item_type = item.type.value if hasattr(item.type, 'value') else str(item.type)
                    item_types[item_type] = item_types.get(item_type, 0) + 1

                    # Count statuses and priorities from field values
                    status = None
                    priority = None

                    for field_value in getattr(item, 'field_values', []):
                        field_name = getattr(field_value.field, 'name', '')
                        if field_name == 'Status' and hasattr(field_value, 'name'):
                            status = field_value.name
                        elif field_name == 'Priority' and hasattr(field_value, 'name'):
                            priority = field_value.name

                    status = status or 'No Status'
                    priority = priority or 'No Priority'

                    item_statuses[status] = item_statuses.get(status, 0) + 1
                    item_priorities[priority] = item_priorities.get(priority, 0) + 1

                    sample_items.append({
                        'title': title,
                        'type': item_type,
                        'status': status,
                        'priority': priority
                    })

                logger.info("Item analysis:")
                logger.info(f"  Types: {dict(item_types)}")
                logger.info(f"  Statuses: {dict(item_statuses)}")
                logger.info(f"  Priorities: {dict(item_priorities)}")

                logger.info("\nSample items to be created:")
                for i, sample in enumerate(sample_items, 1):
                    logger.info(f"  {i}. {sample['title']} ({sample['type']}) - {sample['status']} - {sample['priority']}")

                return True

            # Temporarily override the database ID in settings to use the new database
            original_db_id = self.notion_service.settings.notion_db_id
            self.notion_service.settings.notion_db_id = self.new_database_id

            # Also temporarily change 'status' type to 'select' in field mappings
            # because we created the database with select type instead of status
            original_field_mappings = {}
            for field_name, field_config in self.config.field_mappings.items():
                if field_config.get("type") == "status":
                    original_field_mappings[field_name] = field_config.copy()
                    field_config["type"] = "select"
                    logger.debug(f"Temporarily changed {field_name} type from 'status' to 'select'")

            try:
                # Create pages in batches
                created_count = 0
                failed_count = 0

                logger.info("Starting GitHub item sync to new database...")
                for i in range(0, len(github_items), batch_size):
                    batch = github_items[i:i + batch_size]
                    batch_num = i//batch_size + 1
                    total_batches = (len(github_items) + batch_size - 1)//batch_size

                    logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} items)")

                    for j, item in enumerate(batch):
                        try:
                            # Get item title safely
                            title = item.get_title() if hasattr(item, 'get_title') else f"Item {i+j+1}"

                            logger.debug(f"Creating page for: {title}")

                            # Create or update the Notion page
                            notion_page = self.notion_service.upsert_github_item(item)

                            if notion_page:
                                # Add GitHub content (body + comments) to the page
                                await self._add_github_content_to_page(notion_page.id, item)

                                created_count += 1
                                if created_count % 10 == 0:  # Log progress every 10 creations
                                    logger.info(f"Created {created_count}/{len(github_items)} pages...")
                            else:
                                failed_count += 1
                                logger.warning(f"Failed to create page for item: {title}")

                        except Exception as e:
                            failed_count += 1
                            title = "Unknown"
                            try:
                                title = item.get_title() if hasattr(item, 'get_title') else "Unknown"
                            except:
                                pass
                            logger.error(f"Error creating page for item '{title}': {e}")

                    # Small delay between batches to avoid rate limits
                    if i + batch_size < len(github_items):
                        logger.debug(f"Waiting 1 second before next batch...")
                        await asyncio.sleep(1)

                self.stats["notion_pages_created"] = created_count
                self.stats["failures"] = failed_count

                if failed_count > 0:
                    logger.warning(f"Failed to create {failed_count} pages")

                logger.info(f"Successfully created {created_count} pages in new Notion database")
                return failed_count == 0

            finally:
                # Restore original database ID and field mappings
                self.notion_service.settings.notion_db_id = original_db_id

                # Restore original field type mappings
                for field_name, original_config in original_field_mappings.items():
                    self.config.field_mappings[field_name] = original_config
                    logger.debug(f"Restored {field_name} type to 'status'")

        except Exception as e:
            logger.error(f"Error syncing GitHub items: {e}")
            return False

    async def run_sync(self, database_title: Optional[str] = None, dry_run: bool = False, batch_size: int = 50, sprint_filter: Optional[str] = None) -> bool:
        """Run complete sync process with new database creation.

        Args:
            database_title: Optional title for the new database. If not provided, auto-generates based on sprint filter
            dry_run: If True, only analyze without making changes
            batch_size: Number of items to process in each batch
            sprint_filter: Optional sprint name to filter items

        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.utcnow()

        # Auto-generate database title if not provided (similar to sprint_stats.py)
        if not database_title:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            if sprint_filter:
                database_title = f"GitHub Sync - {sprint_filter} - {timestamp}"
            else:
                database_title = f"GitHub Sync - All Items - {timestamp}"
            logger.info(f"Auto-generated database title: {database_title}")

        logger.info("Starting new database creation and sync...")

        try:
            # Step 1: Create new Notion database
            logger.info("Step 1: Creating new Notion database...")
            create_success = await self.create_new_database(database_title, dry_run)

            if not create_success:
                logger.error("Failed to create new Notion database")
                return False

            # Step 2: Sync all GitHub items to new database
            logger.info("Step 2: Syncing GitHub items to new Notion database...")
            sync_success = await self.sync_all_github_items(dry_run, batch_size, sprint_filter)

            if not sync_success:
                logger.error("Failed to sync GitHub items")
                return False

            self.stats["end_time"] = datetime.utcnow()
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

            # Final summary
            logger.info("New database sync completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Database created: {self.stats['database_created']}")
            if self.new_database_id:
                logger.info(f"New database ID: {self.new_database_id}")
            logger.info(f"GitHub items processed: {self.stats['total_github_items']}")
            logger.info(f"Notion pages created: {self.stats['notion_pages_created']}")

            if self.stats["failures"] > 0:
                logger.warning(f"Failures: {self.stats['failures']}")

            return True

        except Exception as e:
            logger.error(f"Sync with new database failed: {e}")
            return False

    async def _add_github_content_to_page(self, page_id: str, github_item) -> bool:
        """Add GitHub content (body + comments) to a Notion page.

        Args:
            page_id: Notion page ID
            github_item: GitHub project item

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the underlying GitHub issue/PR
            github_content = github_item.content
            if not github_content:
                return True

            # Get repository info for comments
            repo_info = self._extract_repo_info(github_content)
            if not repo_info:
                # Still add body content even if we can't get comments
                return self.notion_service.update_page_content(page_id, github_content, [])

            repo_owner, repo_name, item_number = repo_info

            # Get comments based on item type
            comments = []
            try:
                if hasattr(github_content, 'merged_at'):  # It's a Pull Request
                    comments = self.github_service.get_pull_request_comments(repo_owner, repo_name, item_number)
                else:  # It's an Issue
                    comments = self.github_service.get_issue_comments(repo_owner, repo_name, item_number)

                logger.debug(f"Retrieved {len(comments)} comments for {github_content.title}")

            except Exception as e:
                logger.warning(f"Failed to get comments for {github_content.title}: {e}")
                comments = []

            # Update the Notion page with content
            return self.notion_service.update_page_content(page_id, github_content, comments)

        except Exception as e:
            logger.error(f"Failed to add GitHub content to page {page_id}: {e}")
            return False

    def _extract_repo_info(self, github_content):
        """Extract repository information from GitHub content.

        Args:
            github_content: GitHub issue/PR object

        Returns:
            Tuple of (owner, repo_name, number) or None
        """
        try:
            if hasattr(github_content, 'url') and github_content.url:
                # Parse URL like: https://github.com/owner/repo/issues/123
                # or: https://github.com/owner/repo/pull/123
                url_parts = github_content.url.split('/')
                if len(url_parts) >= 7 and 'github.com' in github_content.url:
                    owner = url_parts[3]
                    repo = url_parts[4]
                    number = github_content.number if hasattr(github_content, 'number') else None

                    if owner and repo and number:
                        return (owner, repo, number)

            return None

        except Exception as e:
            logger.debug(f"Failed to extract repo info: {e}")
            return None


async def main():
    """Main function for create new database sync script."""
    parser = argparse.ArgumentParser(description="Create new Notion database and sync GitHub project data")
    parser.add_argument(
        "--parent-page-id",
        type=str,
        required=True,
        help="ID of the parent page where the database will be created"
    )
    parser.add_argument(
        "--database-title",
        type=str,
        default=None,
        help="Title for the new database (default: auto-generated based on sprint filter)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for processing items (default: 50)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output"
    )
    parser.add_argument(
        "--sprint-filter",
        type=str,
        help="Filter items by sprint name (e.g., '25-07-Sprint4')"
    )

    args = parser.parse_args()

    # Configure logging based on quiet flag
    if args.quiet:
        logger.setLevel("WARNING")

    # Clean up page ID (remove hyphens if present)
    parent_page_id = args.parent_page_id.replace("-", "")

    logger.info("Starting new database creation and sync script")
    logger.info(f"Parent page ID: {parent_page_id}")
    if args.database_title:
        logger.info(f"Database title: {args.database_title}")
    else:
        logger.info("Database title: auto-generated")
    if args.sprint_filter:
        logger.info(f"Sprint filter: {args.sprint_filter}")

    try:
        # Initialize sync service
        sync_service = CreateNewDatabaseSyncService(parent_page_id)

        # Run sync
        success = await sync_service.run_sync(
            database_title=args.database_title,
            dry_run=args.dry_run,
            batch_size=args.batch_size,
            sprint_filter=args.sprint_filter
        )

        if success:
            logger.info("New database sync completed successfully")
            if sync_service.new_database_id:
                print(f"\n✅ New database created with ID: {sync_service.new_database_id}")
                print(f"   View at: https://notion.so/{sync_service.new_database_id.replace('-', '')}")
            sys.exit(0)
        else:
            logger.error("New database sync failed")
            sys.exit(1)

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
