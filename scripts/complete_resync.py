#!/usr/bin/env python3
"""
Complete resynchronization script for GitHub to Notion sync.
Clears all existing Notion pages and rebuilds from GitHub project data.
"""

import sys
import os
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional
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


class CompleteResyncService:
    """Service for performing complete GitHub to Notion resynchronization."""
    
    def __init__(self):
        """Initialize resync service."""
        self.config = get_config()
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        
        # Track sync statistics
        self.stats = {
            "total_github_items": 0,
            "notion_pages_deleted": 0,
            "notion_pages_created": 0,
            "failures": 0,
            "start_time": None,
            "end_time": None
        }
    
    async def clear_notion_database(self, dry_run: bool = False) -> bool:
        """Clear all pages from the Notion database.
        
        Args:
            dry_run: If True, only count pages without deleting
            
        Returns:
            True if successful, False otherwise
        """
        logger.info("Retrieving all pages from Notion database...")
        
        try:
            # Get all pages from the database
            all_pages = self.notion_service.get_all_pages()
            
            if not all_pages:
                logger.info("No pages found in Notion database")
                return True
            
            logger.info(f"Found {len(all_pages)} pages in Notion database")
            
            if dry_run:
                logger.info(f"[DRY RUN] Would delete {len(all_pages)} pages")
                self.stats["notion_pages_deleted"] = len(all_pages)
                
                # Show sample of pages that would be deleted
                for i, page in enumerate(all_pages[:5]):
                    title = getattr(page, 'title', 'Unknown')
                    if hasattr(title, '__iter__') and not isinstance(title, str):
                        title = str(title[0].plain_text if title else 'Unknown')
                    logger.info(f"  Would delete: {title}")
                    
                if len(all_pages) > 5:
                    logger.info(f"  ... and {len(all_pages) - 5} more pages")
                    
                return True
            
            # Delete all pages with improved error handling
            deleted_count = 0
            failed_count = 0
            
            logger.info("Starting page deletion...")
            for i, page in enumerate(all_pages, 1):
                try:
                    title = getattr(page, 'title', 'Unknown')
                    if hasattr(title, '__iter__') and not isinstance(title, str):
                        title = str(title[0].plain_text if title else 'Unknown')
                    
                    logger.debug(f"Deleting page {i}/{len(all_pages)}: {title}")
                    success = self.notion_service.delete_page(page.id)
                    
                    if success:
                        deleted_count += 1
                        if i % 10 == 0:  # Log progress every 10 deletions
                            logger.info(f"Deleted {deleted_count}/{len(all_pages)} pages...")
                    else:
                        failed_count += 1
                        logger.warning(f"Failed to delete page: {title}")
                        
                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Error deleting page {i}: {e}")
            
            self.stats["notion_pages_deleted"] = deleted_count
            
            # Calculate success rate
            total_pages = len(all_pages)
            success_rate = (deleted_count / total_pages * 100) if total_pages > 0 else 0
            
            if failed_count > 0:
                logger.warning(f"Failed to delete {failed_count} pages out of {total_pages} (Success rate: {success_rate:.1f}%)")
            
            logger.info(f"Successfully deleted {deleted_count} pages from Notion database")
            
            # Consider deletion successful if success rate is above 95%
            # This allows for occasional failures due to permissions, references, network issues, etc.
            return success_rate >= 95.0
            
        except Exception as e:
            logger.error(f"Error clearing Notion database: {e}")
            return False
    
    async def sync_all_github_items(self, dry_run: bool = False, batch_size: int = 50, sprint_filter: Optional[str] = None) -> bool:
        """Sync all GitHub project items to Notion.
        
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
                logger.info(f"[DRY RUN] Would create {len(github_items)} pages in Notion")
                self.stats["notion_pages_created"] = len(github_items)
                
                # Analyze item types and statuses with improved field access
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
            
            # Create pages in batches with improved error handling
            created_count = 0
            failed_count = 0
            
            logger.info("Starting GitHub item sync...")
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
                        item_id = "Unknown"
                        try:
                            title = item.get_title() if hasattr(item, 'get_title') else "Unknown"
                            item_id = item.id if hasattr(item, 'id') else "Unknown"
                        except:
                            pass
                        logger.error(f"Error creating page for item '{title}' (ID: {item_id}): {e}", exc_info=True)
                
                # Small delay between batches to avoid rate limits
                if i + batch_size < len(github_items):
                    logger.debug(f"Waiting 1 second before next batch...")
                    await asyncio.sleep(1)
            
            self.stats["notion_pages_created"] = created_count
            self.stats["failures"] = failed_count
            
            # Calculate success rate
            total_items = len(github_items)
            success_rate = (created_count / total_items * 100) if total_items > 0 else 0
            
            if failed_count > 0:
                logger.warning(f"Failed to create {failed_count} pages out of {total_items} (Success rate: {success_rate:.1f}%)")
            
            logger.info(f"Successfully created {created_count} pages in Notion database")
            
            # Consider sync successful if success rate is above 95%
            # This allows for occasional failures due to network issues, rate limits, etc.
            return success_rate >= 95.0
            
        except Exception as e:
            logger.error(f"Error syncing GitHub items: {e}")
            return False
    
    async def update_database_title(self, database_title: str, dry_run: bool = False) -> bool:
        """Update the database title.
        
        Args:
            database_title: New title for the database
            dry_run: If True, only show what would be done
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Updating database title to: {database_title}")
        
        try:
            if dry_run:
                logger.info(f"[DRY RUN] Would update database title to: {database_title}")
                return True
            
            # Update the database title
            success = self.notion_service.update_database_title(title=database_title)
            
            if not success:
                logger.error("Failed to update database title")
                return False
            
            logger.info(f"Successfully updated database title to: {database_title}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating database title: {e}")
            return False
    
    async def run_complete_resync(self, dry_run: bool = False, batch_size: int = 50, 
                                 sprint_filter: Optional[str] = None, database_title: Optional[str] = None) -> bool:
        """Run complete resynchronization.
        
        Args:
            dry_run: If True, only analyze without making changes
            batch_size: Number of items to process in each batch
            sprint_filter: Optional sprint name to filter items
            database_title: Optional new title for the database. If not provided, auto-generates based on sprint filter
            
        Returns:
            True if successful, False otherwise
        """
        self.stats["start_time"] = datetime.utcnow()
        
        # Auto-generate database title if not provided (similar to create_new_database_sync.py)
        if not database_title:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            if sprint_filter:
                database_title = f"GitHub Sync - {sprint_filter} - {timestamp}"
            else:
                database_title = f"GitHub Sync - All Items - {timestamp}"
            logger.info(f"Auto-generated database title: {database_title}")
        
        logger.info("Starting complete resynchronization...")
        
        try:
            # Step 0: Update database title
            logger.info("Step 0: Updating database title...")
            title_update_success = await self.update_database_title(database_title, dry_run)
            
            if not title_update_success:
                logger.error("Failed to update database title")
                return False
            
            # Step 1: Clear existing Notion database
            logger.info("Step 1: Clearing Notion database...")
            clear_success = await self.clear_notion_database(dry_run)
            
            if not clear_success:
                logger.error("Failed to clear Notion database")
                return False
            
            # Step 2: Sync all GitHub items
            logger.info("Step 2: Syncing GitHub items to Notion...")
            sync_success = await self.sync_all_github_items(dry_run, batch_size, sprint_filter)
            
            if not sync_success:
                logger.error("Failed to sync GitHub items")
                return False
            
            self.stats["end_time"] = datetime.utcnow()
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            
            # Final summary
            logger.info("Complete resynchronization finished!")
            logger.info(f"Duration: {duration:.2f} seconds")
            if database_title:
                logger.info(f"Database title updated to: {database_title}")
            logger.info(f"GitHub items processed: {self.stats['total_github_items']}")
            logger.info(f"Notion pages deleted: {self.stats['notion_pages_deleted']}")
            logger.info(f"Notion pages created: {self.stats['notion_pages_created']}")
            
            if self.stats["failures"] > 0:
                logger.warning(f"Failures: {self.stats['failures']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Complete resync failed: {e}")
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
    """Main function for complete resync script."""
    parser = argparse.ArgumentParser(description="Complete GitHub to Notion resynchronization")
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
        "--force",
        action="store_true",
        help="Skip confirmation prompt (dangerous!)"
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
    parser.add_argument(
        "--database-title",
        type=str,
        default=None,
        help="New title for the database (default: auto-generated based on sprint filter and timestamp)"
    )
    
    args = parser.parse_args()
    
    # Configure logging based on quiet flag
    if args.quiet:
        logger.setLevel("WARNING")
    
    # Safety check - require confirmation unless forced or dry run
    if not args.dry_run and not args.force:
        print("\n⚠️  WARNING: This will DELETE ALL existing pages in your Notion database!")
        print("This action cannot be undone.")
        if args.database_title:
            print(f"Database title will be updated to: {args.database_title}")
        else:
            print("Database title will be auto-generated (GitHub Sync - [Sprint/All Items] - [Timestamp])")
        print("\nAre you sure you want to continue? (type 'yes' to confirm)")
        
        confirmation = input().strip().lower()
        if confirmation != 'yes':
            print("Operation cancelled.")
            sys.exit(0)
    
    logger.info("Starting complete resync script")
    if args.database_title:
        logger.info(f"Database title: {args.database_title}")
    else:
        logger.info("Database title: auto-generated (based on sprint filter and timestamp)")
    if args.sprint_filter:
        logger.info(f"Sprint filter: {args.sprint_filter}")
    
    try:
        # Initialize resync service
        resync_service = CompleteResyncService()
        
        # Run complete resync
        success = await resync_service.run_complete_resync(
            dry_run=args.dry_run,
            batch_size=args.batch_size,
            sprint_filter=args.sprint_filter,
            database_title=args.database_title
        )
        
        if success:
            logger.info("Complete resync completed successfully")
            sys.exit(0)
        else:
            logger.error("Complete resync failed")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        sys.exit(1)


def run_resync_with_config():
    """Run resync with configuration validation."""
    try:
        config = get_config()
        logger.info("Configuration loaded successfully")
        
        # Run the async main function
        asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_resync_with_config() 