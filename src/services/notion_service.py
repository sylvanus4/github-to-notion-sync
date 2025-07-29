"""
Notion service for interacting with Notion API.
Handles page creation, updates, queries, and rate limiting.
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError

from ..config import get_config
from ..utils.logger import get_logger
from ..models.notion_models import (
    NotionPage, NotionDatabase, NotionQueryResponse, NotionPropertyBuilder,
    NotionApiError, NotionRateLimitError, NotionPropertyValueUnion
)
from ..models.github_models import GitHubProjectItem, GitHubUser, GitHubLabel
from ..utils.mapping import FieldMapper
from ..utils.rate_limiter import NotionRateLimiter

logger = get_logger(__name__)


class NotionService:
    """Service for interacting with Notion API."""
    
    def __init__(self):
        """Initialize Notion service."""
        self.config = get_config()
        self.settings = self.config.settings
        
        # Initialize Notion client
        self.client = Client(auth=self.settings.notion_token)
        
        # Initialize rate limiter
        self.rate_limiter = NotionRateLimiter(
            requests_per_second=self.config.get_rate_limit("notion")
        )
        
        # Initialize field mapper
        self.field_mapper = FieldMapper(self.config)
    
    def _handle_rate_limit(self, func, *args, **kwargs):
        """Handle rate limiting for Notion API calls.
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        return self.rate_limiter.execute(func, *args, **kwargs)
    
    def _handle_api_error(self, error: APIResponseError) -> None:
        """Handle Notion API errors.
        
        Args:
            error: Notion API error
            
        Raises:
            NotionRateLimitError: If rate limited
            NotionApiError: For other API errors
        """
        if error.code == "rate_limited":
            retry_after = None
            if hasattr(error, 'headers') and error.headers:
                retry_after = int(error.headers.get("Retry-After", 1))
            
            raise NotionRateLimitError(
                f"Notion API rate limit exceeded: {error.code}",
                retry_after
            )
        
        raise NotionApiError(
            f"Notion API error: {error.code} - {str(error)}",
            getattr(error, 'status', 400),
            {"code": error.code, "error_message": str(error)}
        )
    
    def get_database(self) -> Optional[NotionDatabase]:
        """Get database information.
        
        Returns:
            NotionDatabase or None if not found
        """
        try:
            def _get_database():
                return self.client.databases.retrieve(
                    database_id=self.settings.notion_db_id
                )
            
            response = self._handle_rate_limit(_get_database)
            
            logger.debug("Retrieved database information", extra={
                "database_id": self.settings.notion_db_id,
                "title": response.get("title", [{}])[0].get("plain_text", "Unknown")
            })
            
            return NotionDatabase(**response)
            
        except APIResponseError as e:
            self._handle_api_error(e)
        except Exception as e:
            logger.error(f"Failed to retrieve database: {e}")
            return None
    
    def query_pages(self, filter_dict: Optional[Dict[str, Any]] = None, 
                   cursor: Optional[str] = None, page_size: int = 100) -> NotionQueryResponse:
        """Query pages from database.
        
        Args:
            filter_dict: Filter criteria
            cursor: Pagination cursor
            page_size: Number of results per page
            
        Returns:
            NotionQueryResponse
        """
        try:
            def _query_pages():
                query_params = {
                    "database_id": self.settings.notion_db_id,
                    "page_size": page_size
                }
                
                # Only include filter if it's not None
                if filter_dict is not None:
                    query_params["filter"] = filter_dict
                
                # Only include cursor if it's not None
                if cursor is not None:
                    query_params["start_cursor"] = cursor
                
                return self.client.databases.query(**query_params)
            
            response = self._handle_rate_limit(_query_pages)
            
            logger.debug("Queried database pages", extra={
                "database_id": self.settings.notion_db_id,
                "results_count": len(response.get("results", [])),
                "has_more": response.get("has_more", False)
            })
            
            return NotionQueryResponse(**response)
            
        except APIResponseError as e:
            self._handle_api_error(e)
        except Exception as e:
            logger.error(f"Failed to query pages: {e}")
            return NotionQueryResponse(results=[], has_more=False)
    
    def find_page_by_github_id(self, github_node_id: str) -> Optional[NotionPage]:
        """Find a Notion page by GitHub node ID.
        
        Args:
            github_node_id: GitHub project item node ID
            
        Returns:
            NotionPage or None if not found
        """
        github_id_property = self.field_mapper.get_notion_property_name("id")
        if not github_id_property:
            logger.warning("GitHub Node ID property not found in field mappings - skipping duplicate check")
            return None
        
        filter_dict = {
            "property": github_id_property,
            "rich_text": {
                "equals": github_node_id
            }
        }
        
        query_response = self.query_pages(filter_dict=filter_dict, page_size=1)
        
        if query_response.results:
            return query_response.results[0]
        
        return None
    
    def create_page(self, properties: Dict[str, Any], 
                   content: Optional[List[Dict[str, Any]]] = None) -> Optional[NotionPage]:
        """Create a new page in the database.
        
        Args:
            properties: Page properties
            content: Page content blocks
            
        Returns:
            NotionPage or None if creation failed
        """
        try:
            def _create_page():
                page_data = {
                    "parent": {"database_id": self.settings.notion_db_id},
                    "properties": properties
                }
                
                if content:
                    page_data["children"] = content
                
                # Debug: Log the properties being sent
                logger.info(f"Properties being sent to Notion: {properties}")
                
                return self.client.pages.create(**page_data)
            
            response = self._handle_rate_limit(_create_page)
            
            logger.info("Created Notion page", extra={
                "page_id": response["id"],
                "database_id": self.settings.notion_db_id
            })
            
            return NotionPage(**response)
            
        except APIResponseError as e:
            self._handle_api_error(e)
        except Exception as e:
            logger.error(f"Failed to create page: {e}")
            return None
    
    def update_page(self, page_id: str, properties: Dict[str, Any]) -> Optional[NotionPage]:
        """Update an existing page.
        
        Args:
            page_id: Notion page ID
            properties: Updated properties
            
        Returns:
            NotionPage or None if update failed
        """
        try:
            def _update_page():
                return self.client.pages.update(
                    page_id=page_id,
                    properties=properties
                )
            
            response = self._handle_rate_limit(_update_page)
            
            logger.info("Updated Notion page", extra={
                "page_id": page_id
            })
            
            return NotionPage(**response)
            
        except APIResponseError as e:
            self._handle_api_error(e)
        except Exception as e:
            logger.error(f"Failed to update page {page_id}: {e}")
            return None
    
    def build_properties_from_github_item(self, github_item: GitHubProjectItem) -> Dict[str, Any]:
        """Build Notion properties from GitHub project item.
        
        Args:
            github_item: GitHub project item
            
        Returns:
            Dictionary of Notion properties
        """
        properties = {}
        
        # Map each field from configuration
        for field_name, field_config in self.config.field_mappings.items():
            notion_property = field_config.get("notion_property")
            github_field = field_config.get("github_field")
            property_type = field_config.get("type")
            
            if not notion_property or not github_field:
                continue
            
            # Get value from GitHub item
            value = self._get_github_field_value(github_item, github_field)
            
            if value is None:
                continue
            
            # Apply field mapping transformation (GitHub value -> Notion value)
            from ..utils.mapping import FieldMapper
            field_mapper = FieldMapper(self.config)
            
            # Debug logging
            logger.debug(f"Transforming field '{github_field}' with value '{value}'")
            transformed_value = field_mapper.transform_value(github_field, value)
            logger.debug(f"Transformed '{value}' -> '{transformed_value}'")
            
            # Build Notion property based on type
            notion_property_value = self._build_notion_property(
                property_type, transformed_value, field_config
            )
            
            if notion_property_value:
                properties[notion_property] = notion_property_value
        
        return properties
    
    def _get_github_field_value(self, github_item: GitHubProjectItem, field_name: str) -> Any:
        """Get value from GitHub item for a specific field.
        
        Args:
            github_item: GitHub project item
            field_name: Field name to get value for
            
        Returns:
            Field value or None if not found
        """
        # Handle special fields
        if field_name == "id":
            return github_item.id
        elif field_name == "title":
            return github_item.get_title()
        elif field_name == "url":
            return github_item.get_url()
        elif field_name == "number":
            return github_item.get_number()
        elif field_name == "state":
            state = github_item.get_state()
            return state.value if state else None
        elif field_name == "__typename":
            return github_item.type.value
        elif field_name == "assignees":
            return github_item.get_assignees()
        elif field_name == "labels":
            return github_item.get_labels()
        elif field_name == "createdAt":
            return github_item.created_at
        elif field_name == "updatedAt":
            return github_item.updated_at
        elif field_name == "repository":
            repo = github_item.get_repository()
            return repo.full_name if repo else None
        else:
            # Try to get from custom field values
            return github_item.get_field_value(field_name)
    
    def _build_notion_property(self, property_type: str, value: Any, 
                              field_config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Build Notion property based on type and value.
        
        Args:
            property_type: Type of Notion property
            value: Value to set
            field_config: Field configuration
            
        Returns:
            Notion property dictionary or None
        """
        try:
            if property_type == "title":
                return {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(value)
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": str(value)
                        }
                    ]
                }
            
            elif property_type == "rich_text":
                return {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(value)
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": str(value)
                        }
                    ]
                }
            
            elif property_type == "number":
                return {
                    "number": float(value)
                }
            
            elif property_type == "select":
                return {
                    "select": {
                        "name": str(value)
                    }
                }
            
            elif property_type == "status":
                # Notion status fields require special handling
                # Try to use the exact value first, then fallback to ID if needed
                return {
                    "status": {
                        "name": str(value)
                    }
                }
            
            elif property_type == "multi_select":
                if isinstance(value, list):
                    if value and isinstance(value[0], GitHubLabel):
                        # Handle labels
                        names = [label.name for label in value]
                    else:
                        names = [str(v) for v in value]
                    return {
                        "multi_select": [
                            {"name": name} for name in names
                        ]
                    }
                else:
                    return {
                        "multi_select": [
                            {"name": str(value)}
                        ]
                    }
            
            elif property_type == "date":
                if isinstance(value, datetime):
                    return {
                        "date": {
                            "start": value.isoformat()
                        }
                    }
                else:
                    return {
                        "date": {
                            "start": str(value)
                        }
                    }
            
            elif property_type == "people":
                if isinstance(value, list) and value and isinstance(value[0], GitHubUser):
                    # Map GitHub users to Notion users
                    people_list = []
                    for user in value:
                        notion_user = self.config.map_github_user_to_notion(user.login)
                        if notion_user:
                            # Check if it's a user ID or email
                            if "@" in notion_user:
                                people_list.append({"email": notion_user})
                            else:
                                people_list.append({"id": notion_user})
                    
                    if people_list:
                        return {
                            "people": people_list
                        }
                
                return None
            
            elif property_type == "url":
                return {
                    "url": str(value)
                }
            
            elif property_type == "checkbox":
                return {
                    "checkbox": bool(value)
                }
            
            elif property_type == "email":
                return {
                    "email": str(value)
                }
            
            elif property_type == "phone_number":
                return {
                    "phone_number": str(value)
                }
            
        except Exception as e:
            logger.warning(f"Failed to build property {property_type}: {e}", extra={
                "property_type": property_type,
                "value": value
            })
        
        return None
    
    def upsert_github_item(self, github_item: GitHubProjectItem) -> Optional[NotionPage]:
        """Upsert a GitHub item to Notion (create or update).
        
        Args:
            github_item: GitHub project item
            
        Returns:
            NotionPage or None if operation failed
        """
        try:
            # Build properties from GitHub item
            properties = self.build_properties_from_github_item(github_item)
            
            if not properties:
                logger.warning(f"No properties built for GitHub item {github_item.id}")
                return None
            
            # Check if page already exists
            existing_page = self.find_page_by_github_id(github_item.id)
            
            if existing_page:
                # Update existing page
                logger.info(f"Updating existing page for GitHub item {github_item.id}")
                return self.update_page(existing_page.id, properties)
            else:
                # Create new page
                logger.info(f"Creating new page for GitHub item {github_item.id}")
                return self.create_page(properties)
            
        except Exception as e:
            logger.error(f"Failed to upsert GitHub item {github_item.id}: {e}")
            return None
    
    def sync_github_items(self, github_items: List[GitHubProjectItem]) -> Dict[str, int]:
        """Sync multiple GitHub items to Notion.
        
        Args:
            github_items: List of GitHub project items
            
        Returns:
            Dictionary with sync statistics
        """
        stats = {
            "total": len(github_items),
            "created": 0,
            "updated": 0,
            "failed": 0
        }
        
        for github_item in github_items:
            try:
                existing_page = self.find_page_by_github_id(github_item.id)
                result = self.upsert_github_item(github_item)
                
                if result:
                    if existing_page:
                        stats["updated"] += 1
                    else:
                        stats["created"] += 1
                else:
                    stats["failed"] += 1
                    
            except Exception as e:
                logger.error(f"Failed to sync GitHub item {github_item.id}: {e}")
                stats["failed"] += 1
        
        logger.info("Completed GitHub items sync", extra=stats)
        return stats
    
    def delete_page(self, page_id: str) -> bool:
        """Delete a page (archive it).
        
        Args:
            page_id: Notion page ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            def _delete_page():
                return self.client.pages.update(
                    page_id=page_id,
                    archived=True
                )
            
            self._handle_rate_limit(_delete_page)
            
            logger.info("Archived Notion page", extra={
                "page_id": page_id
            })
            
            return True
            
        except APIResponseError as e:
            self._handle_api_error(e)
        except Exception as e:
            logger.error(f"Failed to archive page {page_id}: {e}")
            return False
    
    def get_all_pages(self) -> List[NotionPage]:
        """Get all pages from the database.
        
        Returns:
            List of NotionPage
        """
        all_pages = []
        cursor = None
        
        while True:
            response = self.query_pages(cursor=cursor, page_size=100)
            all_pages.extend(response.results)
            
            if not response.has_more:
                break
            
            cursor = response.next_cursor
        
        logger.info(f"Retrieved {len(all_pages)} pages from Notion database")
        return all_pages
    
    def get_status_field_options(self) -> Dict[str, str]:
        """Get status field options mapping from the database.
        
        Returns:
            Dict mapping option names to their IDs
        """
        try:
            database = self.get_database()
            if not database:
                return {}
            
            status_options = {}
            for prop_name, prop in database.properties.items():
                if prop_name == "진행 상태" and hasattr(prop, 'status') and prop.status:
                    if hasattr(prop.status, 'options') and prop.status.options:
                        for option in prop.status.options:
                            if hasattr(option, 'name') and hasattr(option, 'id'):
                                status_options[option.name] = option.id
                            elif isinstance(option, dict):
                                status_options[option.get('name', '')] = option.get('id', '')
                    break
            
            logger.debug(f"Found status options: {status_options}")
            return status_options
            
        except Exception as e:
            logger.error(f"Failed to get status field options: {e}")
            return {}
    
    def _get_property_value_for_notion(self, property_type: str, value: Any) -> Optional[Dict[str, Any]]:
        """Helper to get the correct Notion property value format.
        
        Args:
            property_type: Type of Notion property
            value: Value to set
            
        Returns:
            Notion property dictionary or None
        """
        try:
            if property_type == "title":
                return {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(value)
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": str(value)
                        }
                    ]
                }
            
            elif property_type == "rich_text":
                return {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": str(value)
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": str(value)
                        }
                    ]
                }
            
            elif property_type == "number":
                return {
                    "number": float(value)
                }
            
            elif property_type == "select":
                return {
                    "select": {
                        "name": str(value)
                    }
                }
            
            elif property_type == "status":
                # Notion status fields require special handling
                # Try to use the exact value first, then fallback to ID if needed
                return {
                    "status": {
                        "name": str(value)
                    }
                }
            
            elif property_type == "multi_select":
                if isinstance(value, list):
                    if value and isinstance(value[0], GitHubLabel):
                        # Handle labels
                        names = [label.name for label in value]
                    else:
                        names = [str(v) for v in value]
                    return {
                        "multi_select": [
                            {"name": name} for name in names
                        ]
                    }
                else:
                    return {
                        "multi_select": [
                            {"name": str(value)}
                        ]
                    }
            
            elif property_type == "date":
                if isinstance(value, datetime):
                    return {
                        "date": {
                            "start": value.isoformat()
                        }
                    }
                else:
                    return {
                        "date": {
                            "start": str(value)
                        }
                    }
            
            elif property_type == "people":
                if isinstance(value, list) and value and isinstance(value[0], GitHubUser):
                    # Map GitHub users to Notion users
                    people_list = []
                    for user in value:
                        notion_user = self.config.map_github_user_to_notion(user.login)
                        if notion_user:
                            # Check if it's a user ID or email
                            if "@" in notion_user:
                                people_list.append({"email": notion_user})
                            else:
                                people_list.append({"id": notion_user})
                    
                    if people_list:
                        return {
                            "people": people_list
                        }
                
                return None
            
            elif property_type == "url":
                return {
                    "url": str(value)
                }
            
            elif property_type == "checkbox":
                return {
                    "checkbox": bool(value)
                }
            
            elif property_type == "email":
                return {
                    "email": str(value)
                }
            
            elif property_type == "phone_number":
                return {
                    "phone_number": str(value)
                }
            
        except Exception as e:
            logger.warning(f"Failed to build property {property_type}: {e}", extra={
                "property_type": property_type,
                "value": value
            })
        
        return None
    
    def update_page_content(self, page_id: str, github_item, comments: List = None) -> bool:
        """Update a Notion page with GitHub content (body + comments).
        
        Args:
            page_id: Notion page ID
            github_item: GitHub issue/PR object with body content
            comments: List of GitHub comments
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build content blocks
            content_blocks = []
            
            # Add GitHub body content if available
            if hasattr(github_item, 'body') and github_item.body:
                content_blocks.extend(self._markdown_to_notion_blocks(github_item.body, "📝 GitHub Description"))
            
            # Add comments if available
            if comments:
                content_blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "💬 Comments"}}]
                    }
                })
                
                for comment in comments:
                    if comment.body:
                        author_name = comment.author.login if comment.author else "Unknown"
                        comment_header = f"💬 {author_name} - {comment.created_at.strftime('%Y-%m-%d %H:%M')}"
                        
                        content_blocks.append({
                            "object": "block",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [{"type": "text", "text": {"content": comment_header}}]
                            }
                        })
                        
                        content_blocks.extend(self._markdown_to_notion_blocks(comment.body))
            
            # Update page with content
            if content_blocks:
                def _update_blocks():
                    return self.client.blocks.children.append(
                        block_id=page_id,
                        children=content_blocks
                    )
                
                response = self._handle_rate_limit(_update_blocks)
                
                logger.info(f"Successfully updated page content for {page_id}")
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update page content: {e}")
            return False
    
    def _markdown_to_notion_blocks(self, markdown_text: str, title: str = None) -> List[Dict]:
        """Convert markdown text to Notion blocks.
        
        Args:
            markdown_text: Markdown content
            title: Optional title for the section
            
        Returns:
            List of Notion block objects
        """
        blocks = []
        
        # Add title if provided
        if title:
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
            })
        
        if not markdown_text or not markdown_text.strip():
            return blocks
        
        # Simple markdown parsing - split by paragraphs
        paragraphs = markdown_text.split('\n\n')
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # Handle code blocks
            if paragraph.startswith('```'):
                language = ""
                code_content = paragraph
                
                # Extract language if specified
                first_line = paragraph.split('\n')[0]
                if len(first_line) > 3:
                    language = first_line[3:].strip()
                    code_content = '\n'.join(paragraph.split('\n')[1:])
                
                # Remove closing ```
                if code_content.endswith('```'):
                    code_content = code_content[:-3].strip()
                
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "language": language or "plain text",
                        "rich_text": [{"type": "text", "text": {"content": code_content}}]
                    }
                })
            
            # Handle headings
            elif paragraph.startswith('#'):
                heading_level = len(paragraph) - len(paragraph.lstrip('#'))
                heading_text = paragraph.lstrip('# ').strip()
                
                if heading_level == 1:
                    block_type = "heading_1"
                elif heading_level == 2:
                    block_type = "heading_2"
                else:
                    block_type = "heading_3"
                
                blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [{"type": "text", "text": {"content": heading_text}}]
                    }
                })
            
            # Handle bullet lists
            elif paragraph.startswith('- ') or paragraph.startswith('* '):
                list_items = paragraph.split('\n')
                for item in list_items:
                    item = item.strip()
                    if item.startswith('- ') or item.startswith('* '):
                        item_text = item[2:].strip()
                        blocks.append({
                            "object": "block",
                            "type": "bulleted_list_item",
                            "bulleted_list_item": {
                                "rich_text": [{"type": "text", "text": {"content": item_text}}]
                            }
                        })
            
            # Handle numbered lists
            elif any(paragraph.startswith(f'{i}. ') for i in range(1, 10)):
                list_items = paragraph.split('\n')
                for item in list_items:
                    item = item.strip()
                    if any(item.startswith(f'{i}. ') for i in range(1, 10)):
                        item_text = item.split('. ', 1)[1] if '. ' in item else item
                        blocks.append({
                            "object": "block",
                            "type": "numbered_list_item",
                            "numbered_list_item": {
                                "rich_text": [{"type": "text", "text": {"content": item_text}}]
                            }
                        })
            
            # Regular paragraph
            else:
                # Truncate very long paragraphs for Notion API limits
                if len(paragraph) > 2000:
                    paragraph = paragraph[:1997] + "..."
                    
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": paragraph}}]
                    }
                })
        
        return blocks
