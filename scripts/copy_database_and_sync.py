#!/usr/bin/env python3
"""
Copy Notion database template and sync script for GitHub to Notion.
Copies an existing Notion database structure (properties) and syncs GitHub project data to it.
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


class CopyDatabaseSyncService:
    """Service for copying a Notion database template and syncing GitHub project data to it."""
    
    def __init__(self, template_database_id: str, parent_page_id: str):
        """Initialize sync service.
        
        Args:
            template_database_id: ID of the template database to copy
            parent_page_id: ID of the parent page where the new database will be created
        """
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        self.template_database_id = template_database_id
        self.parent_page_id = parent_page_id
        self.new_database_id = None
        
        # Track sync statistics
        self.stats = {
            "total_github_items": 0,
            "database_copied": False,
            "notion_pages_created": 0,
            "failures": 0,
            "start_time": None,
            "end_time": None
        }
    
    def _get_template_database_properties(self) -> Optional[Dict[str, Any]]:
        """Get properties schema from template database.
        
        Returns:
            Dictionary of database properties schema or None if failed
        """
        try:
            # Save original database ID
            original_db_id = self.notion_service.settings.notion_db_id
            
            # Temporarily set to template database ID to read its structure
            self.notion_service.settings.notion_db_id = self.template_database_id
            
            try:
                # Get template database
                template_db = self.notion_service.get_database()
                
                if not template_db:
                    logger.error("Failed to retrieve template database")
                    return None
                
                logger.info(f"Retrieved template database: {self.template_database_id}")
                logger.info(f"Template database properties: {len(template_db.properties)} properties")
                
                # Extract properties schema
                properties_schema = {}
                for prop_name, prop in template_db.properties.items():
                    prop_dict = prop if isinstance(prop, dict) else prop.__dict__
                    
                    # Get property type
                    prop_type = prop_dict.get('type')
                    
                    if not prop_type:
                        logger.warning(f"Property {prop_name} has no type, skipping")
                        continue
                    
                    # Build property schema based on type
                    if prop_type == "title":
                        properties_schema[prop_name] = {"title": {}}
                    
                    elif prop_type == "rich_text":
                        properties_schema[prop_name] = {"rich_text": {}}
                    
                    elif prop_type == "number":
                        number_config = prop_dict.get('number', {})
                        if isinstance(number_config, dict):
                            properties_schema[prop_name] = {"number": number_config}
                        else:
                            properties_schema[prop_name] = {"number": {}}
                    
                    elif prop_type == "select":
                        # Copy select options
                        select_config = prop_dict.get('select', {})
                        options = []
                        
                        if isinstance(select_config, dict) and 'options' in select_config:
                            for option in select_config['options']:
                                if isinstance(option, dict):
                                    options.append({
                                        "name": option.get('name', ''),
                                        "color": option.get('color', 'default')
                                    })
                        
                        properties_schema[prop_name] = {
                            "select": {"options": options} if options else {}
                        }
                    
                    elif prop_type == "multi_select":
                        # Copy multi_select options
                        multi_select_config = prop_dict.get('multi_select', {})
                        options = []
                        
                        if isinstance(multi_select_config, dict) and 'options' in multi_select_config:
                            for option in multi_select_config['options']:
                                if isinstance(option, dict):
                                    options.append({
                                        "name": option.get('name', ''),
                                        "color": option.get('color', 'default')
                                    })
                        
                        properties_schema[prop_name] = {
                            "multi_select": {"options": options} if options else {}
                        }
                    
                    elif prop_type == "status":
                        # For status, use select type as Notion API doesn't allow creating status fields
                        # Copy status options to select
                        status_config = prop_dict.get('status', {})
                        options = []
                        
                        if isinstance(status_config, dict) and 'options' in status_config:
                            for option in status_config['options']:
                                if isinstance(option, dict):
                                    options.append({
                                        "name": option.get('name', ''),
                                        "color": option.get('color', 'default')
                                    })
                        
                        # Use select instead of status for API compatibility
                        properties_schema[prop_name] = {
                            "select": {"options": options} if options else {}
                        }
                    
                    elif prop_type == "date":
                        properties_schema[prop_name] = {"date": {}}
                    
                    elif prop_type == "people":
                        properties_schema[prop_name] = {"people": {}}
                    
                    elif prop_type == "url":
                        properties_schema[prop_name] = {"url": {}}
                    
                    elif prop_type == "email":
                        properties_schema[prop_name] = {"email": {}}
                    
                    elif prop_type == "phone_number":
                        properties_schema[prop_name] = {"phone_number": {}}
                    
                    elif prop_type == "checkbox":
                        properties_schema[prop_name] = {"checkbox": {}}
                    
                    elif prop_type == "files":
                        properties_schema[prop_name] = {"files": {}}
                    
                    elif prop_type in ["created_time", "created_by", "last_edited_time", "last_edited_by"]:
                        # Skip auto-generated properties
                        logger.debug(f"Skipping auto-generated property: {prop_name} ({prop_type})")
                        continue
                    
                    else:
                        logger.warning(f"Unknown property type for {prop_name}: {prop_type}, skipping")
                        continue
                    
                    logger.debug(f"Copied property: {prop_name} ({prop_type})")
                
                return properties_schema
                
            finally:
                # Restore original database ID
                self.notion_service.settings.notion_db_id = original_db_id
        
        except Exception as e:
            logger.error(f"Error getting template database properties: {e}")
            return None
    
    async def copy_database(self, database_title: str, dry_run: bool = False) -> bool:
        """Copy template database to create a new database.
        
        Args:
            database_title: Title for the new database
            dry_run: If True, only show what would be created
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Copying template database: {self.template_database_id}")
        logger.info(f"New database title: {database_title}")
        logger.info(f"Parent page ID: {self.parent_page_id}")
        
        try:
            # Get template database properties
            properties_schema = self._get_template_database_properties()
            
            if not properties_schema:
                logger.error("Failed to get template database properties")
                return False
            
            if dry_run:
                logger.info(f"[DRY RUN] Would copy database with {len(properties_schema)} properties:")
                for prop_name, prop_config in properties_schema.items():
                    prop_type = list(prop_config.keys())[0]
                    logger.info(f"  - {prop_name} ({prop_type})")
                self.stats["database_copied"] = True
                return True
            
            # Create the new database
            database_id = self.notion_service.create_database(
                parent_page_id=self.parent_page_id,
                title=database_title,
                properties_schema=properties_schema
            )
            
            if not database_id:
                logger.error("Failed to create new database")
                return False
            
            self.new_database_id = database_id
            self.stats["database_copied"] = True
            
            logger.info(f"Successfully copied database: {database_id}")
            logger.info(f"Copied {len(properties_schema)} properties from template")
            
            return True
            
        except Exception as e:
            logger.error(f"Error copying database: {e}")
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
        """Run complete sync process with database copy.
        
        Args:
            database_title: Optional title for the new database. If not provided, auto-generates based on sprint filter
            dry_run: If True, only analyze without making changes
            batch_size: Number of items to process in each batch
            sprint_filter: Optional sprint name to filter items
            
        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.utcnow()
        
        # Auto-generate database title if not provided
        if not database_title:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            if sprint_filter:
                database_title = f"GitHub Sync - {sprint_filter} - {timestamp}"
            else:
                database_title = f"GitHub Sync - All Items - {timestamp}"
            logger.info(f"Auto-generated database title: {database_title}")
        
        logger.info("Starting database copy and sync...")
        
        try:
            # Step 1: Copy template database
            logger.info("Step 1: Copying template Notion database...")
            copy_success = await self.copy_database(database_title, dry_run)
            
            if not copy_success:
                logger.error("Failed to copy template Notion database")
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
            logger.info("Database copy and sync completed!")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Database copied: {self.stats['database_copied']}")
            if self.new_database_id:
                logger.info(f"New database ID: {self.new_database_id}")
            logger.info(f"GitHub items processed: {self.stats['total_github_items']}")
            logger.info(f"Notion pages created: {self.stats['notion_pages_created']}")
            
            if self.stats["failures"] > 0:
                logger.warning(f"Failures: {self.stats['failures']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Sync with database copy failed: {e}")
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
    """Main function for copy database and sync script."""
    parser = argparse.ArgumentParser(description="Copy Notion database template and sync GitHub project data")
    parser.add_argument(
        "--template-database-id",
        type=str,
        default=os.getenv("NOTION_TEMPLATE_DB_ID", "2329eddc34e68057a86ed3de6bae90da"),
        help="ID of the template database to copy (default: from NOTION_TEMPLATE_DB_ID env or 2329eddc34e68057a86ed3de6bae90da)"
    )
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
    
    # Clean up IDs (remove hyphens if present)
    template_database_id = args.template_database_id.replace("-", "")
    parent_page_id = args.parent_page_id.replace("-", "")
    
    logger.info("Starting database copy and sync script")
    logger.info(f"Template database ID: {template_database_id}")
    logger.info(f"Parent page ID: {parent_page_id}")
    if args.database_title:
        logger.info(f"Database title: {args.database_title}")
    else:
        logger.info("Database title: auto-generated")
    if args.sprint_filter:
        logger.info(f"Sprint filter: {args.sprint_filter}")
    
    try:
        # Initialize sync service
        sync_service = CopyDatabaseSyncService(template_database_id, parent_page_id)
        
        # Run sync
        success = await sync_service.run_sync(
            database_title=args.database_title,
            dry_run=args.dry_run,
            batch_size=args.batch_size,
            sprint_filter=args.sprint_filter
        )
        
        if success:
            logger.info("Database copy and sync completed successfully")
            if sync_service.new_database_id:
                print(f"\n✅ New database created with ID: {sync_service.new_database_id}")
                print(f"   View at: https://notion.so/{sync_service.new_database_id.replace('-', '')}")
            sys.exit(0)
        else:
            logger.error("Database copy and sync failed")
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

