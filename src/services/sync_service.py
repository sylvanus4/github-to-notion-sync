"""
Sync service for coordinating GitHub to Notion synchronization.
Handles both real-time webhook sync and periodic full sync operations.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..config import get_config
from ..utils.logger import get_logger
from ..services.github_service import GitHubService
from ..services.notion_service import NotionService
from ..models.github_models import GitHubProjectItem
from ..models.notion_models import NotionPage
from ..models.webhook_models import WebhookEvent, extract_project_item_from_webhook

logger = get_logger(__name__)


class SyncService:
    """Service for coordinating GitHub to Notion synchronization."""
    
    def __init__(self):
        """Initialize sync service."""
        self.config = get_config()
        self.settings = self.config.settings
        
        # Initialize dependent services
        self.github_service = GitHubService()
        self.notion_service = NotionService()
        
        # Track sync statistics
        self.sync_stats = {
            "last_full_sync": None,
            "total_synced": 0,
            "webhook_syncs": 0,
            "full_syncs": 0,
            "errors": 0
        }
    
    async def sync_webhook_event(self, webhook_event: WebhookEvent) -> Dict[str, Any]:
        """Sync a single webhook event.
        
        Args:
            webhook_event: Webhook event to process
            
        Returns:
            Dictionary with sync results
        """
        from ..utils.logger import get_logger_manager
        logger_manager = get_logger_manager()
        
        # Log webhook event
        logger_manager.log_webhook_event(
            logger,
            webhook_event.event_type.value,
            webhook_event.payload.action.value if hasattr(webhook_event.payload, 'action') else 'unknown',
            webhook_event.get_item_id(),
            webhook_event.get_repository().full_name if webhook_event.get_repository() else None
        )
        
        result = {
            "success": False,
            "action": "none",
            "item_id": None,
            "error": None
        }
        
        try:
            # Check if this event should be processed
            if not webhook_event.should_process(self.config.webhook_events):
                logger.info(f"Skipping webhook event {webhook_event.event_type.value}:{webhook_event.payload.action.value}")
                result["action"] = "skipped"
                result["success"] = True
                return result
            
            # Extract project item ID from webhook
            project_item_id = extract_project_item_from_webhook(webhook_event)
            if not project_item_id:
                # For non-project events, we need to find the related project item
                # This would require additional GitHub API calls
                logger.warning(f"No project item ID found in webhook event {webhook_event.event_type.value}")
                result["error"] = "No project item ID found"
                return result
            
            result["item_id"] = project_item_id
            
            # Handle different webhook actions
            action = webhook_event.payload.action.value
            
            if action in ["created", "edited", "opened", "closed", "reopened", "assigned", "unassigned"]:
                # Sync the item from GitHub to Notion
                success = await self._sync_single_item(project_item_id)
                if success:
                    result["action"] = "upserted"
                    result["success"] = True
                    self.sync_stats["webhook_syncs"] += 1
                else:
                    result["error"] = "Failed to sync item"
            
            elif action in ["deleted", "archived"]:
                # Archive the item in Notion
                success = await self._archive_notion_item(project_item_id)
                if success:
                    result["action"] = "archived"
                    result["success"] = True
                    self.sync_stats["webhook_syncs"] += 1
                else:
                    result["error"] = "Failed to archive item"
            
            else:
                logger.info(f"Unhandled webhook action: {action}")
                result["action"] = "ignored"
                result["success"] = True
            
            # Log sync event
            logger_manager.log_sync_event(
                logger,
                "webhook",
                project_item_id,
                result["action"],
                result["success"],
                result.get("error")
            )
            
        except Exception as e:
            logger.error(f"Error processing webhook event: {e}")
            result["error"] = str(e)
            self.sync_stats["errors"] += 1
        
        return result
    
    async def _sync_single_item(self, item_id: str) -> bool:
        """Sync a single GitHub item to Notion.
        
        Args:
            item_id: GitHub project item node ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the item from GitHub
            github_item = self.github_service.get_single_item(item_id)
            if not github_item:
                # Fallback: get all items and find the one we need
                all_items = self.github_service.get_all_project_items()
                github_item = next((item for item in all_items if item.id == item_id), None)
            
            if not github_item:
                logger.warning(f"GitHub item {item_id} not found")
                return False
            
            # Sync to Notion
            notion_page = self.notion_service.upsert_github_item(github_item)
            return notion_page is not None
            
        except Exception as e:
            logger.error(f"Error syncing single item {item_id}: {e}")
            return False
    
    async def _archive_notion_item(self, item_id: str) -> bool:
        """Archive a Notion item.
        
        Args:
            item_id: GitHub project item node ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Find the Notion page by GitHub ID
            notion_page = self.notion_service.find_page_by_github_id(item_id)
            if not notion_page:
                logger.warning(f"Notion page for GitHub item {item_id} not found")
                return True  # Already deleted/not exists
            
            # Archive the page
            return self.notion_service.delete_page(notion_page.id)
            
        except Exception as e:
            logger.error(f"Error archiving Notion item for GitHub ID {item_id}: {e}")
            return False
    
    async def full_sync(self, batch_size: Optional[int] = None) -> Dict[str, Any]:
        """Perform a full synchronization of all GitHub items to Notion.
        
        Args:
            batch_size: Number of items to process in each batch
            
        Returns:
            Dictionary with sync results
        """
        batch_size = batch_size or self.settings.batch_size
        start_time = datetime.utcnow()
        
        logger.info("Starting full sync from GitHub to Notion")
        
        result = {
            "success": False,
            "total_items": 0,
            "created": 0,
            "updated": 0,
            "failed": 0,
            "duration_seconds": 0,
            "error": None
        }
        
        try:
            # Get all GitHub project items
            logger.info("Fetching all GitHub project items")
            github_items = self.github_service.get_all_project_items()
            result["total_items"] = len(github_items)
            
            if not github_items:
                logger.warning("No GitHub items found")
                result["success"] = True
                return result
            
            # Process items in batches with parallel processing
            total_processed = 0
            
            for i in range(0, len(github_items), batch_size):
                batch = github_items[i:i + batch_size]
                logger.info(f"Processing batch {i // batch_size + 1} ({len(batch)} items)")
                
                batch_stats = await self._process_batch(batch)
                
                result["created"] += batch_stats["created"]
                result["updated"] += batch_stats["updated"]
                result["failed"] += batch_stats["failed"]
                total_processed += len(batch)
                
                logger.info(f"Batch completed: {total_processed}/{len(github_items)} items processed")
            
            result["success"] = True
            self.sync_stats["full_syncs"] += 1
            self.sync_stats["last_full_sync"] = start_time
            
        except Exception as e:
            logger.error(f"Error during full sync: {e}")
            result["error"] = str(e)
            self.sync_stats["errors"] += 1
        
        finally:
            end_time = datetime.utcnow()
            result["duration_seconds"] = (end_time - start_time).total_seconds()
            
            logger.info("Full sync completed", extra={
                "duration_seconds": result["duration_seconds"],
                "total_items": result["total_items"],
                "created": result["created"],
                "updated": result["updated"],
                "failed": result["failed"],
                "success": result["success"]
            })
        
        return result
    
    async def _process_batch(self, github_items: List[GitHubProjectItem]) -> Dict[str, int]:
        """Process a batch of GitHub items with parallel execution.
        
        Args:
            github_items: List of GitHub items to process
            
        Returns:
            Dictionary with batch statistics
        """
        stats = {"created": 0, "updated": 0, "failed": 0}
        
        # Use ThreadPoolExecutor for I/O-bound operations
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self._sync_item_to_notion, item): item 
                for item in github_items
            }
            
            # Process completed tasks
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    sync_result = future.result()
                    if sync_result == "created":
                        stats["created"] += 1
                    elif sync_result == "updated":
                        stats["updated"] += 1
                    else:
                        stats["failed"] += 1
                        
                except Exception as e:
                    logger.error(f"Error processing item {item.id}: {e}")
                    stats["failed"] += 1
        
        return stats
    
    def _sync_item_to_notion(self, github_item: GitHubProjectItem) -> str:
        """Sync a single GitHub item to Notion (blocking).
        
        Args:
            github_item: GitHub project item
            
        Returns:
            Sync result: "created", "updated", or "failed"
        """
        try:
            # Check if page already exists
            existing_page = self.notion_service.find_page_by_github_id(github_item.id)
            
            # Upsert the item
            result_page = self.notion_service.upsert_github_item(github_item)
            
            if result_page:
                return "updated" if existing_page else "created"
            else:
                return "failed"
                
        except Exception as e:
            logger.error(f"Error syncing item {github_item.id}: {e}")
            return "failed"
    
    async def cleanup_orphaned_pages(self) -> Dict[str, Any]:
        """Clean up Notion pages that no longer exist in GitHub.
        
        Returns:
            Dictionary with cleanup results
        """
        logger.info("Starting cleanup of orphaned Notion pages")
        
        result = {
            "success": False,
            "total_notion_pages": 0,
            "orphaned_pages": 0,
            "archived": 0,
            "failed": 0,
            "error": None
        }
        
        try:
            # Get all Notion pages
            notion_pages = self.notion_service.get_all_pages()
            result["total_notion_pages"] = len(notion_pages)
            
            # Get all GitHub item IDs
            github_items = self.github_service.get_all_project_items()
            github_item_ids = {item.id for item in github_items}
            
            orphaned_pages = []
            
            # Find orphaned pages
            for page in notion_pages:
                github_id_property = self.config.get_notion_property_name("id")
                if github_id_property:
                    github_id = page.get_property_value(github_id_property)
                    if github_id and github_id not in github_item_ids:
                        orphaned_pages.append(page)
            
            result["orphaned_pages"] = len(orphaned_pages)
            
            # Archive orphaned pages
            for page in orphaned_pages:
                try:
                    if self.notion_service.delete_page(page.id):
                        result["archived"] += 1
                    else:
                        result["failed"] += 1
                except Exception as e:
                    logger.error(f"Error archiving orphaned page {page.id}: {e}")
                    result["failed"] += 1
            
            result["success"] = True
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            result["error"] = str(e)
        
        logger.info("Cleanup completed", extra=result)
        return result
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status and statistics.
        
        Returns:
            Dictionary with sync status
        """
        return {
            "stats": self.sync_stats.copy(),
            "github_rate_limit": self.github_service.get_rate_limit_info().__dict__ if self.github_service.get_rate_limit_info() else None,
            "last_sync_time": self.sync_stats.get("last_full_sync"),
            "config": {
                "github_org": self.settings.github_org,
                "github_project": self.settings.github_project_number,
                "notion_db_id": self.settings.notion_db_id,
                "batch_size": self.settings.batch_size
            }
        }
    
    async def validate_sync_setup(self) -> Dict[str, Any]:
        """Validate the sync setup and configuration.
        
        Returns:
            Dictionary with validation results
        """
        logger.info("Validating sync setup")
        
        validation_result = {
            "success": False,
            "github_connection": False,
            "notion_connection": False,
            "field_mappings": False,
            "errors": []
        }
        
        try:
            # Test GitHub connection
            try:
                project_info = self.github_service.get_project_info()
                if project_info:
                    validation_result["github_connection"] = True
                    logger.info(f"GitHub connection successful: {project_info.get('title')}")
                else:
                    validation_result["errors"].append("Failed to retrieve GitHub project info")
            except Exception as e:
                validation_result["errors"].append(f"GitHub connection failed: {e}")
            
            # Test Notion connection
            try:
                database_info = self.notion_service.get_database()
                if database_info:
                    validation_result["notion_connection"] = True
                    logger.info("Notion connection successful")
                else:
                    validation_result["errors"].append("Failed to retrieve Notion database info")
            except Exception as e:
                validation_result["errors"].append(f"Notion connection failed: {e}")
            
            # Validate field mappings
            try:
                mapping_errors = self.notion_service.field_mapper.validate_mapping_configuration()
                if not mapping_errors:
                    validation_result["field_mappings"] = True
                    logger.info("Field mappings validation successful")
                else:
                    validation_result["errors"].extend(mapping_errors)
            except Exception as e:
                validation_result["errors"].append(f"Field mappings validation failed: {e}")
            
            # Overall success
            validation_result["success"] = (
                validation_result["github_connection"] and
                validation_result["notion_connection"] and
                validation_result["field_mappings"]
            )
            
        except Exception as e:
            validation_result["errors"].append(f"Validation error: {e}")
        
        if validation_result["success"]:
            logger.info("Sync setup validation passed")
        else:
            logger.error("Sync setup validation failed", extra={
                "errors": validation_result["errors"]
            })
        
        return validation_result
