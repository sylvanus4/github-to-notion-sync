"""
GitHub service for interacting with GitHub GraphQL API v4.
Handles project data fetching, rate limiting, and error handling.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Iterator
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import get_config
from ..utils.logger import get_logger
from ..models.github_models import (
    GitHubProject, GitHubProjectItem, GitHubGraphQLResponse,
    GitHubRateLimitInfo, GitHubApiError, GitHubRateLimitError,
    GitHubIssue, GitHubPullRequest, GitHubDraftIssue, GitHubComment,
    GitHubProjectField, GitHubProjectFieldValueUnion,
    GitHubProjectTextFieldValue, GitHubProjectNumberFieldValue,
    GitHubProjectDateFieldValue, GitHubProjectSingleSelectFieldValue,
    GitHubProjectIterationFieldValue, GitHubProjectTitleFieldValue,
    GitHubItemType, GitHubProjectFieldType
)

logger = get_logger(__name__)


class GitHubService:
    """Service for interacting with GitHub GraphQL API."""
    
    def __init__(self):
        """Initialize GitHub service."""
        self.config = get_config()
        self.settings = self.config.settings
        self.base_url = "https://api.github.com/graphql"
        
        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        
        # Set headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.settings.github_token}",
            "Content-Type": "application/json",
            "User-Agent": "github-notion-sync/1.0"
        })
        
        # Rate limiting
        self.rate_limit_info: Optional[GitHubRateLimitInfo] = None
        self.last_request_time: Optional[datetime] = None
    
    def _make_request(self, query: str, variables: Optional[Dict[str, Any]] = None) -> GitHubGraphQLResponse:
        """Make a GraphQL request to GitHub API.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            GitHubGraphQLResponse
            
        Raises:
            GitHubApiError: If request fails
            GitHubRateLimitError: If rate limited
        """
        # Rate limiting check
        self._check_rate_limit()
        
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        start_time = time.time()
        
        try:
            logger.debug(f"Making GraphQL request", extra={
                "query_length": len(query),
                "variables": variables
            })
            
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=30
            )
            
            duration = time.time() - start_time
            
            # Log API call
            from ..utils.logger import get_logger_manager
            logger_manager = get_logger_manager()
            logger_manager.log_api_call(
                logger, "github", "POST", self.base_url,
                response.status_code, duration,
                query_length=len(query)
            )
            
            # Update rate limit info
            self._update_rate_limit_info(response.headers)
            
            if response.status_code == 429:
                reset_time = self._get_rate_limit_reset_time(response.headers)
                raise GitHubRateLimitError(
                    "GitHub API rate limit exceeded",
                    reset_time
                )
            
            if response.status_code != 200:
                raise GitHubApiError(
                    f"GitHub API request failed with status {response.status_code}",
                    response.status_code,
                    response.json() if response.content else None
                )
            
            response_data = response.json()
            github_response = GitHubGraphQLResponse(**response_data)
            
            if github_response.has_errors():
                error_messages = github_response.get_error_messages()
                raise GitHubApiError(
                    f"GraphQL errors: {'; '.join(error_messages)}",
                    response.status_code,
                    response_data
                )
            
            return github_response
            
        except requests.exceptions.RequestException as e:
            raise GitHubApiError(f"Request failed: {str(e)}")
    
    def _check_rate_limit(self):
        """Check if we're within rate limits."""
        if self.rate_limit_info and self.rate_limit_info.remaining <= 5:
            reset_time = self.rate_limit_info.reset_at
            wait_time = (reset_time - datetime.utcnow()).total_seconds()
            
            if wait_time > 0:
                logger.warning(f"Rate limit low, waiting {wait_time:.2f} seconds", extra={
                    "remaining_requests": self.rate_limit_info.remaining,
                    "reset_time": reset_time.isoformat()
                })
                time.sleep(wait_time + 1)
    
    def _update_rate_limit_info(self, headers: Dict[str, str]):
        """Update rate limit information from response headers."""
        try:
            if "x-ratelimit-limit" in headers:
                self.rate_limit_info = GitHubRateLimitInfo(
                    limit=int(headers["x-ratelimit-limit"]),
                    remaining=int(headers["x-ratelimit-remaining"]),
                    reset_at=datetime.fromtimestamp(int(headers["x-ratelimit-reset"])),
                    used=int(headers["x-ratelimit-used"])
                )
                
                # Log rate limit info
                from ..utils.logger import get_logger_manager
                logger_manager = get_logger_manager()
                logger_manager.log_rate_limit(
                    logger, "github", 
                    self.rate_limit_info.remaining,
                    self.rate_limit_info.reset_at
                )
        except (KeyError, ValueError) as e:
            logger.warning(f"Failed to parse rate limit headers: {e}")
    
    def _get_rate_limit_reset_time(self, headers: Dict[str, str]) -> Optional[datetime]:
        """Get rate limit reset time from headers."""
        try:
            if "x-ratelimit-reset" in headers:
                return datetime.fromtimestamp(int(headers["x-ratelimit-reset"]))
        except (KeyError, ValueError):
            pass
        return None
    
    def get_project_fields(self) -> List[GitHubProjectField]:
        """Get project fields configuration.
        
        Returns:
            List of GitHubProjectField
        """
        query = self.config.load_graphql_query("get_project_fields")
        if not query:
            raise GitHubApiError("Could not load get_project_fields query")
        
        variables = {
            "org": self.settings.github_org,
            "num": self.settings.github_project_number
        }
        
        response = self._make_request(query, variables)
        
        if not response.data:
            return []
        
        project_data = response.data.get("organization", {}).get("projectV2", {})
        fields_data = project_data.get("fields", {}).get("nodes", [])
        
        fields = []
        for field_data in fields_data:
            try:
                field = GitHubProjectField(**field_data)
                fields.append(field)
            except Exception as e:
                logger.warning(f"Failed to parse field: {e}", extra={"field_data": field_data})
        
        return fields
    
    def get_project_items(self, cursor: Optional[str] = None) -> Iterator[GitHubProjectItem]:
        """Get project items with pagination.
        
        Args:
            cursor: Pagination cursor
            
        Yields:
            GitHubProjectItem instances
        """
        query = self.config.load_graphql_query("get_project_items")
        if not query:
            raise GitHubApiError("Could not load get_project_items query")
        
        variables = {
            "org": self.settings.github_org,
            "num": self.settings.github_project_number,
            "after": cursor
        }
        
        response = self._make_request(query, variables)
        
        if not response.data:
            return
        
        project_data = response.data.get("organization", {}).get("projectV2", {})
        items_data = project_data.get("items", {})
        
        # Process items
        for item_data in items_data.get("nodes", []):
            try:
                item = self._parse_project_item(item_data)
                if item:
                    yield item
            except Exception as e:
                logger.error(f"Failed to parse project item: {e}", extra={"item_data": item_data})
        
        # Handle pagination
        page_info = items_data.get("pageInfo", {})
        if page_info.get("hasNextPage"):
            next_cursor = page_info.get("endCursor")
            if next_cursor:
                yield from self.get_project_items(next_cursor)
    
    def _parse_project_item(self, item_data: Dict[str, Any]) -> Optional[GitHubProjectItem]:
        """Parse project item data from GraphQL response.
        
        Args:
            item_data: Raw item data from GraphQL
            
        Returns:
            GitHubProjectItem or None if parsing fails
        """
        try:
            # Parse content based on type
            content = None
            content_data = item_data.get("content")
            
            if content_data:
                typename = content_data.get("__typename")
                if typename == "Issue":
                    content = GitHubIssue(**content_data)
                elif typename == "PullRequest":
                    content = GitHubPullRequest(**content_data)
                elif typename == "DraftIssue":
                    content = GitHubDraftIssue(**content_data)
            
            # Parse field values
            field_values = []
            field_values_data = item_data.get("fieldValues", {}).get("nodes", [])
            
            for field_value_data in field_values_data:
                # Skip empty field objects or objects without proper structure
                if not field_value_data or not isinstance(field_value_data, dict):
                    continue
                if not field_value_data.get("field") or not field_value_data["field"].get("name"):
                    continue
                    
                field_value = self._parse_field_value(field_value_data)
                if field_value:
                    field_values.append(field_value)
            
            # Create project item
            created_at = None
            if item_data.get("createdAt"):
                created_at = datetime.fromisoformat(item_data["createdAt"].replace("Z", "+00:00"))
                
            updated_at = None
            if item_data.get("updatedAt"):
                updated_at = datetime.fromisoformat(item_data["updatedAt"].replace("Z", "+00:00"))
            
            item = GitHubProjectItem(
                id=item_data["id"],
                type=GitHubItemType(item_data["type"]),
                content=content,
                fieldValues=field_values,  # Use alias name
                createdAt=created_at,     # Use alias name
                updatedAt=updated_at      # Use alias name
            )
            
            return item
            
        except Exception as e:
            logger.error(f"Failed to parse project item: {e}", extra={"item_data": item_data})
            return None
    
    def _parse_field_value(self, field_value_data: Dict[str, Any]) -> Optional[GitHubProjectFieldValueUnion]:
        """Parse field value data.
        
        Args:
            field_value_data: Raw field value data
            
        Returns:
            GitHubProjectFieldValueUnion or None if parsing fails
        """
        try:
            field_data = field_value_data.get("field", {})

            
            field = GitHubProjectField(**field_data)
            
            # Determine field value type and parse accordingly
            if field.dataType == GitHubProjectFieldType.TITLE and "text" in field_value_data:
                return GitHubProjectTitleFieldValue(
                    field=field,
                    text=field_value_data["text"]
                )
            elif field.dataType == GitHubProjectFieldType.TEXT and "text" in field_value_data:
                return GitHubProjectTextFieldValue(
                    field=field,
                    text=field_value_data["text"]
                )
            elif field.dataType == GitHubProjectFieldType.NUMBER and "number" in field_value_data:
                return GitHubProjectNumberFieldValue(
                    field=field,
                    number=field_value_data["number"]
                )
            elif field.dataType == GitHubProjectFieldType.DATE and "date" in field_value_data:
                return GitHubProjectDateFieldValue(
                    field=field,
                    date=datetime.fromisoformat(field_value_data["date"].replace("Z", "+00:00"))
                )
            elif field.dataType == GitHubProjectFieldType.SINGLE_SELECT and "name" in field_value_data:
                return GitHubProjectSingleSelectFieldValue(
                    field=field,
                    name=field_value_data["name"],
                    option_id=field_value_data.get("optionId")
                )
            elif field.dataType == GitHubProjectFieldType.ITERATION and "title" in field_value_data:
                return GitHubProjectIterationFieldValue(
                    field=field,
                    title=field_value_data["title"],
                    duration=field_value_data.get("duration"),
                    start_date=datetime.fromisoformat(field_value_data["startDate"].replace("Z", "+00:00")) if field_value_data.get("startDate") else None
                )
            
        except Exception as e:
            logger.warning(f"Failed to parse field value: {e}", extra={"field_value_data": field_value_data})
        
        return None
    
    def get_single_item(self, item_id: str) -> Optional[GitHubProjectItem]:
        """Get a single project item by ID.
        
        Args:
            item_id: GitHub project item node ID
            
        Returns:
            GitHubProjectItem or None if not found
        """
        query = self.config.load_graphql_query("get_single_item")
        if not query:
            # Fallback to getting all items and filtering
            for item in self.get_project_items():
                if item.id == item_id:
                    return item
            return None
        
        variables = {
            "org": self.settings.github_org,
            "num": self.settings.github_project_number,
            "itemId": item_id
        }
        
        response = self._make_request(query, variables)
        
        if not response.data:
            return None
        
        # Parse the single item response
        # This would need to be implemented based on the specific query structure
        # For now, fall back to the full list approach
        return None
    
    def get_all_project_items(self, sprint_filter: Optional[str] = None) -> List[GitHubProjectItem]:
        """Get all project items.
        
        Args:
            sprint_filter: Optional sprint name to filter items (e.g., "25-07-Sprint4")
        
        Returns:
            List of GitHubProjectItem
        """
        items = []
        for item in self.get_project_items():
            # Apply sprint filter if specified
            if sprint_filter:
                if self._item_matches_sprint(item, sprint_filter):
                    items.append(item)
            else:
                items.append(item)
        
        logger.info(f"Retrieved {len(items)} project items{f' matching sprint {sprint_filter}' if sprint_filter else ''}", extra={
            "project_org": self.settings.github_org,
            "project_number": self.settings.github_project_number
        })
        
        return items
    
    def _item_matches_sprint(self, item: GitHubProjectItem, sprint_filter: str) -> bool:
        """Check if an item matches the given sprint filter.
        
        Args:
            item: GitHub project item
            sprint_filter: Sprint name to match
            
        Returns:
            True if item matches the sprint filter
        """
        for field_value in item.field_values:
            if field_value.field.name == "스프린트":
                # For iteration fields, we need to check the title
                if hasattr(field_value, 'title') and field_value.title:
                    return field_value.title == sprint_filter
                # Alternative check for iteration field value text
                elif hasattr(field_value, 'text') and field_value.text:
                    return field_value.text == sprint_filter
                # Check for iteration object with title
                elif hasattr(field_value, 'iteration') and field_value.iteration:
                    iteration_title = getattr(field_value.iteration, 'title', None)
                    if iteration_title:
                        return iteration_title == sprint_filter
        return False
    
    def get_issue_comments(self, repo_owner: str, repo_name: str, issue_number: int) -> List[GitHubComment]:
        """Get comments for a specific issue.
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name  
            issue_number: Issue number
            
        Returns:
            List of GitHubComment objects
        """
        query = """
        query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            issue(number: $number) {
              comments(first: 100, after: $cursor) {
                nodes {
                  id
                  body
                  author {
                    login
                    avatarUrl
                    url
                  }
                  createdAt
                  updatedAt
                  url
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
          }
        }
        """
        
        all_comments = []
        cursor = None
        
        while True:
            variables = {
                "owner": repo_owner,
                "name": repo_name,
                "number": issue_number,
                "cursor": cursor
            }
            
            response = self._make_request(query, variables)
            
            issue_data = response.get("data", {}).get("repository", {}).get("issue", {})
            if not issue_data:
                break
                
            comments_connection = issue_data.get("comments", {})
            comments = comments_connection.get("nodes", [])
            
            for comment_data in comments:
                try:
                    comment = GitHubComment(**comment_data)
                    all_comments.append(comment)
                except Exception as e:
                    logger.warning(f"Failed to parse comment: {e}")
                    continue
            
            # Check for pagination
            page_info = comments_connection.get("pageInfo", {})
            if not page_info.get("hasNextPage", False):
                break
                
            cursor = page_info.get("endCursor")
        
        return all_comments
    
    def get_pull_request_comments(self, repo_owner: str, repo_name: str, pr_number: int) -> List[GitHubComment]:
        """Get comments for a specific pull request.
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name  
            pr_number: Pull request number
            
        Returns:
            List of GitHubComment objects
        """
        query = """
        query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
          repository(owner: $owner, name: $name) {
            pullRequest(number: $number) {
              comments(first: 100, after: $cursor) {
                nodes {
                  id
                  body
                  author {
                    login
                    avatarUrl
                    url
                  }
                  createdAt
                  updatedAt
                  url
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
          }
        }
        """
        
        all_comments = []
        cursor = None
        
        while True:
            variables = {
                "owner": repo_owner,
                "name": repo_name,
                "number": pr_number,
                "cursor": cursor
            }
            
            response = self._make_request(query, variables)
            
            pr_data = response.get("data", {}).get("repository", {}).get("pullRequest", {})
            if not pr_data:
                break
                
            comments_connection = pr_data.get("comments", {})
            comments = comments_connection.get("nodes", [])
            
            for comment_data in comments:
                try:
                    comment = GitHubComment(**comment_data)
                    all_comments.append(comment)
                except Exception as e:
                    logger.warning(f"Failed to parse comment: {e}")
                    continue
            
            # Check for pagination
            page_info = comments_connection.get("pageInfo", {})
            if not page_info.get("hasNextPage", False):
                break
                
            cursor = page_info.get("endCursor")
        
        return all_comments
    
    def get_project_info(self) -> Optional[Dict[str, Any]]:
        """Get basic project information.
        
        Returns:
            Project information dictionary
        """
        query = self.config.load_graphql_query("get_project_fields")
        if not query:
            return None
        
        variables = {
            "org": self.settings.github_org,
            "num": self.settings.github_project_number
        }
        
        response = self._make_request(query, variables)
        
        if not response.data:
            return None
        
        project_data = response.data.get("organization", {}).get("projectV2", {})
        
        return {
            "id": project_data.get("id"),
            "title": project_data.get("title"),
            "description": project_data.get("description"),
            "url": project_data.get("url"),
            "created_at": project_data.get("createdAt"),
            "updated_at": project_data.get("updatedAt"),
            "closed": project_data.get("closed", False)
        }
    
    def get_rate_limit_info(self) -> Optional[GitHubRateLimitInfo]:
        """Get current rate limit information.
        
        Returns:
            GitHubRateLimitInfo or None if not available
        """
        return self.rate_limit_info
