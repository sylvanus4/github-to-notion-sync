"""
Data models for GitHub webhook payloads.
These models represent the structure of webhook events from GitHub.
"""

from datetime import datetime
from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel, Field
from enum import Enum

from .github_models import GitHubUser, GitHubLabel, GitHubRepository, GitHubIssue, GitHubPullRequest


class WebhookEventType(str, Enum):
    """GitHub webhook event types."""
    PROJECTS_V2_ITEM = "projects_v2_item"
    ISSUES = "issues"
    PULL_REQUEST = "pull_request"
    ISSUE_COMMENT = "issue_comment"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"


class WebhookAction(str, Enum):
    """GitHub webhook actions."""
    # Projects v2 item actions
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    RESTORED = "restored"
    ARCHIVED = "archived"
    CONVERTED = "converted"
    
    # Issues actions
    OPENED = "opened"
    CLOSED = "closed"
    REOPENED = "reopened"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    
    # Pull request actions
    REVIEW_REQUESTED = "review_requested"
    READY_FOR_REVIEW = "ready_for_review"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    SYNCHRONIZE = "synchronize"


class WebhookProjectV2Item(BaseModel):
    """Webhook project v2 item model."""
    id: str
    node_id: str
    project_node_id: str
    content_node_id: Optional[str] = None
    content_type: Optional[str] = None
    creator: Optional[GitHubUser] = None
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime] = None


class WebhookProjectV2(BaseModel):
    """Webhook project v2 model."""
    id: int
    node_id: str
    owner: GitHubUser
    creator: GitHubUser
    title: str
    description: Optional[str] = None
    public: bool
    closed: bool
    created_at: datetime
    updated_at: datetime
    number: int


class WebhookOrganization(BaseModel):
    """Webhook organization model."""
    login: str
    id: int
    node_id: str
    url: str
    repos_url: str
    events_url: str
    hooks_url: str
    issues_url: str
    members_url: str
    public_members_url: str
    avatar_url: str
    description: Optional[str] = None


class WebhookChanges(BaseModel):
    """Webhook changes model."""
    field_value: Optional[Dict[str, Any]] = None
    title: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None
    assignees: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, Any]] = None


class ProjectsV2ItemWebhookPayload(BaseModel):
    """Projects v2 item webhook payload."""
    action: WebhookAction
    projects_v2_item: WebhookProjectV2Item
    changes: Optional[WebhookChanges] = None
    organization: WebhookOrganization
    sender: GitHubUser
    
    class Config:
        populate_by_name = True


class IssuesWebhookPayload(BaseModel):
    """Issues webhook payload."""
    action: WebhookAction
    issue: GitHubIssue
    changes: Optional[WebhookChanges] = None
    assignee: Optional[GitHubUser] = None
    assigner: Optional[GitHubUser] = None
    label: Optional[GitHubLabel] = None
    organization: Optional[WebhookOrganization] = None
    repository: GitHubRepository
    sender: GitHubUser
    
    class Config:
        populate_by_name = True


class PullRequestWebhookPayload(BaseModel):
    """Pull request webhook payload."""
    action: WebhookAction
    pull_request: GitHubPullRequest
    changes: Optional[WebhookChanges] = None
    assignee: Optional[GitHubUser] = None
    assigner: Optional[GitHubUser] = None
    label: Optional[GitHubLabel] = None
    organization: Optional[WebhookOrganization] = None
    repository: GitHubRepository
    sender: GitHubUser
    number: Optional[int] = None
    
    class Config:
        populate_by_name = True


class WebhookPayload(BaseModel):
    """Generic webhook payload."""
    zen: Optional[str] = None
    hook_id: Optional[int] = None
    hook: Optional[Dict[str, Any]] = None
    organization: Optional[WebhookOrganization] = None
    repository: Optional[GitHubRepository] = None
    sender: Optional[GitHubUser] = None
    
    class Config:
        populate_by_name = True


class WebhookEvent(BaseModel):
    """Webhook event wrapper."""
    event_type: WebhookEventType
    delivery_id: str
    signature: str
    payload: Union[ProjectsV2ItemWebhookPayload, IssuesWebhookPayload, PullRequestWebhookPayload, WebhookPayload]
    timestamp: datetime
    
    def get_item_id(self) -> Optional[str]:
        """Get the relevant item ID from the payload.
        
        Returns:
            Item ID or None if not available
        """
        if isinstance(self.payload, ProjectsV2ItemWebhookPayload):
            return self.payload.projects_v2_item.node_id
        elif isinstance(self.payload, IssuesWebhookPayload):
            return self.payload.issue.id
        elif isinstance(self.payload, PullRequestWebhookPayload):
            return self.payload.pull_request.id
        return None
    
    def get_repository(self) -> Optional[GitHubRepository]:
        """Get the repository from the payload.
        
        Returns:
            GitHubRepository or None if not available
        """
        if hasattr(self.payload, 'repository'):
            return self.payload.repository
        return None
    
    def get_sender(self) -> Optional[GitHubUser]:
        """Get the sender from the payload.
        
        Returns:
            GitHubUser or None if not available
        """
        if hasattr(self.payload, 'sender'):
            return self.payload.sender
        return None
    
    def should_process(self, enabled_events: Dict[str, List[str]]) -> bool:
        """Check if this event should be processed.
        
        Args:
            enabled_events: Dictionary of enabled event types and actions
            
        Returns:
            True if event should be processed
        """
        event_config = enabled_events.get(self.event_type.value)
        if not event_config:
            return False
        
        if hasattr(self.payload, 'action'):
            return self.payload.action.value in event_config
        
        return True


class WebhookValidationError(Exception):
    """Webhook validation error."""
    pass


class WebhookSignatureError(Exception):
    """Webhook signature validation error."""
    pass


class WebhookParser:
    """Parser for GitHub webhook payloads."""
    
    @staticmethod
    def parse_payload(event_type: str, payload: Dict[str, Any]) -> Union[
        ProjectsV2ItemWebhookPayload, 
        IssuesWebhookPayload, 
        PullRequestWebhookPayload, 
        WebhookPayload
    ]:
        """Parse webhook payload based on event type.
        
        Args:
            event_type: GitHub event type
            payload: Raw payload dictionary
            
        Returns:
            Parsed webhook payload
            
        Raises:
            WebhookValidationError: If payload cannot be parsed
        """
        try:
            if event_type == WebhookEventType.PROJECTS_V2_ITEM:
                return ProjectsV2ItemWebhookPayload(**payload)
            elif event_type == WebhookEventType.ISSUES:
                return IssuesWebhookPayload(**payload)
            elif event_type == WebhookEventType.PULL_REQUEST:
                return PullRequestWebhookPayload(**payload)
            else:
                return WebhookPayload(**payload)
                
        except Exception as e:
            raise WebhookValidationError(f"Failed to parse {event_type} payload: {e}")
    
    @staticmethod
    def create_webhook_event(
        event_type: str,
        delivery_id: str,
        signature: str,
        payload: Dict[str, Any]
    ) -> WebhookEvent:
        """Create a webhook event from raw data.
        
        Args:
            event_type: GitHub event type
            delivery_id: Webhook delivery ID
            signature: Webhook signature
            payload: Raw payload dictionary
            
        Returns:
            WebhookEvent instance
            
        Raises:
            WebhookValidationError: If event cannot be created
        """
        try:
            parsed_payload = WebhookParser.parse_payload(event_type, payload)
            
            return WebhookEvent(
                event_type=WebhookEventType(event_type),
                delivery_id=delivery_id,
                signature=signature,
                payload=parsed_payload,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            raise WebhookValidationError(f"Failed to create webhook event: {e}")


def extract_project_item_from_webhook(event: WebhookEvent) -> Optional[str]:
    """Extract project item node ID from webhook event.
    
    Args:
        event: Webhook event
        
    Returns:
        Project item node ID or None if not available
    """
    if event.event_type == WebhookEventType.PROJECTS_V2_ITEM:
        if isinstance(event.payload, ProjectsV2ItemWebhookPayload):
            return event.payload.projects_v2_item.node_id
    
    return None


def extract_content_info_from_webhook(event: WebhookEvent) -> Optional[Dict[str, Any]]:
    """Extract content information from webhook event.
    
    Args:
        event: Webhook event
        
    Returns:
        Content information dictionary or None if not available
    """
    if event.event_type == WebhookEventType.ISSUES:
        if isinstance(event.payload, IssuesWebhookPayload):
            return {
                "type": "Issue",
                "id": event.payload.issue.id,
                "number": event.payload.issue.number,
                "title": event.payload.issue.title,
                "url": event.payload.issue.url,
                "state": event.payload.issue.state.value
            }
    
    elif event.event_type == WebhookEventType.PULL_REQUEST:
        if isinstance(event.payload, PullRequestWebhookPayload):
            return {
                "type": "PullRequest",
                "id": event.payload.pull_request.id,
                "number": event.payload.pull_request.number,
                "title": event.payload.pull_request.title,
                "url": event.payload.pull_request.url,
                "state": event.payload.pull_request.state.value
            }
    
    return None
