"""
Data models for GitHub entities.
These models represent the structure of data returned from GitHub's GraphQL API v4.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class GitHubItemType(str, Enum):
    """GitHub item types."""
    ISSUE = "ISSUE"
    PULL_REQUEST = "PULL_REQUEST"
    DRAFT_ISSUE = "DRAFT_ISSUE"


class GitHubState(str, Enum):
    """GitHub item states."""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    MERGED = "MERGED"
    DRAFT = "DRAFT"


class GitHubUser(BaseModel):
    """GitHub user model."""
    login: str
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")
    
    class Config:
        allow_population_by_field_name = True


class GitHubLabel(BaseModel):
    """GitHub label model."""
    id: str
    name: str
    color: str
    description: Optional[str] = None


class GitHubComment(BaseModel):
    """GitHub comment model."""
    id: str
    body: str
    author: Optional[GitHubUser] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    url: str
    
    class Config:
        allow_population_by_field_name = True


class GitHubRepository(BaseModel):
    """GitHub repository model."""
    id: str
    name: str
    full_name: str = Field(alias="nameWithOwner")
    url: str
    description: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class GitHubIssue(BaseModel):
    """GitHub issue model."""
    id: str
    number: int
    title: str
    body: Optional[str] = None
    url: str
    state: GitHubState
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")
    assignees: List[GitHubUser] = []
    labels: List[GitHubLabel] = []
    repository: Optional[GitHubRepository] = None
    
    @field_validator('assignees', mode='before')
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and 'nodes' in v:
            return v['nodes']
        return v if isinstance(v, list) else []
    
    @field_validator('labels', mode='before')
    @classmethod
    def parse_labels(cls, v):
        """Parse labels from nodes structure."""
        if isinstance(v, dict) and 'nodes' in v:
            return v['nodes']
        return v if isinstance(v, list) else []
    
    class Config:
        allow_population_by_field_name = True


class GitHubPullRequest(BaseModel):
    """GitHub pull request model."""
    id: str
    number: int
    title: str
    body: Optional[str] = None
    url: str
    state: GitHubState
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")
    merged_at: Optional[datetime] = Field(None, alias="mergedAt")
    assignees: List[GitHubUser] = []
    labels: List[GitHubLabel] = []
    repository: Optional[GitHubRepository] = None
    draft: bool = False
    
    @field_validator('assignees', mode='before')
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and 'nodes' in v:
            return v['nodes']
        return v if isinstance(v, list) else []
    
    @field_validator('labels', mode='before')
    @classmethod
    def parse_labels(cls, v):
        """Parse labels from nodes structure."""
        if isinstance(v, dict) and 'nodes' in v:
            return v['nodes']
        return v if isinstance(v, list) else []
    
    class Config:
        allow_population_by_field_name = True


class GitHubDraftIssue(BaseModel):
    """GitHub draft issue model."""
    id: str
    title: str
    body: Optional[str] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    assignees: List[GitHubUser] = []
    
    @field_validator('assignees', mode='before')
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and 'nodes' in v:
            return v['nodes']
        return v if isinstance(v, list) else []
    
    class Config:
        allow_population_by_field_name = True


class GitHubProjectFieldType(str, Enum):
    """GitHub project field types."""
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    SINGLE_SELECT = "SINGLE_SELECT"
    ITERATION = "ITERATION"
    TITLE = "TITLE"
    ASSIGNEES = "ASSIGNEES"
    LABELS = "LABELS"
    LINKED_PULL_REQUESTS = "LINKED_PULL_REQUESTS"
    MILESTONE = "MILESTONE"
    REPOSITORY = "REPOSITORY"
    REVIEWERS = "REVIEWERS"
    PARENT_ISSUE = "PARENT_ISSUE"
    SUB_ISSUES_PROGRESS = "SUB_ISSUES_PROGRESS"


class GitHubProjectField(BaseModel):
    """GitHub project field model."""
    id: str
    name: str
    dataType: GitHubProjectFieldType
    options: Optional[List[Dict[str, Any]]] = None


class GitHubProjectFieldValue(BaseModel):
    """Base class for project field values."""
    field: GitHubProjectField


class GitHubProjectTextFieldValue(GitHubProjectFieldValue):
    """Text field value."""
    text: str


class GitHubProjectNumberFieldValue(GitHubProjectFieldValue):
    """Number field value."""
    number: float


class GitHubProjectDateFieldValue(GitHubProjectFieldValue):
    """Date field value."""
    date: datetime


class GitHubProjectSingleSelectFieldValue(GitHubProjectFieldValue):
    """Single select field value."""
    name: str
    option_id: Optional[str] = Field(None, alias="optionId")
    
    class Config:
        allow_population_by_field_name = True


class GitHubProjectIterationFieldValue(GitHubProjectFieldValue):
    """Iteration field value."""
    title: str
    duration: Optional[int] = None


class GitHubProjectTitleFieldValue(GitHubProjectFieldValue):
    """Title field value."""
    text: str
    start_date: Optional[datetime] = Field(None, alias="startDate")
    
    class Config:
        allow_population_by_field_name = True


# Union type for all field values
GitHubProjectFieldValueUnion = Union[
    GitHubProjectTextFieldValue,
    GitHubProjectNumberFieldValue,
    GitHubProjectDateFieldValue,
    GitHubProjectSingleSelectFieldValue,
    GitHubProjectIterationFieldValue,
    GitHubProjectTitleFieldValue
]


class GitHubProjectItem(BaseModel):
    """GitHub project item model."""
    id: str  # This is the project item node ID (unique key for Notion)
    type: GitHubItemType
    content: Optional[Union[GitHubIssue, GitHubPullRequest, GitHubDraftIssue]] = None
    field_values: List[GitHubProjectFieldValueUnion] = Field(default_factory=list, alias="fieldValues")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        allow_population_by_field_name = True
    
    def get_field_value(self, field_name: str) -> Optional[Any]:
        """Get the value of a specific field by name.
        
        Args:
            field_name: Name of the field to get value for
            
        Returns:
            Field value or None if not found
        """
        for field_value in self.field_values:
            if field_value.field.name == field_name:
                if isinstance(field_value, GitHubProjectTextFieldValue):
                    return field_value.text
                elif isinstance(field_value, GitHubProjectNumberFieldValue):
                    return field_value.number
                elif isinstance(field_value, GitHubProjectDateFieldValue):
                    return field_value.date
                elif isinstance(field_value, GitHubProjectSingleSelectFieldValue):
                    return field_value.name
                elif isinstance(field_value, GitHubProjectIterationFieldValue):
                    return field_value.title
        return None
    
    def get_title(self) -> str:
        """Get the title of the item."""
        if self.content:
            return self.content.title
        return "Untitled"
    
    def get_url(self) -> Optional[str]:
        """Get the URL of the item."""
        if self.content and hasattr(self.content, 'url'):
            return self.content.url
        return None
    
    def get_number(self) -> Optional[int]:
        """Get the number of the item."""
        if self.content and hasattr(self.content, 'number'):
            return self.content.number
        return None
    
    def get_state(self) -> Optional[GitHubState]:
        """Get the state of the item."""
        if self.content and hasattr(self.content, 'state'):
            return self.content.state
        return None
    
    def get_assignees(self) -> List[GitHubUser]:
        """Get the assignees of the item."""
        if self.content and hasattr(self.content, 'assignees'):
            return self.content.assignees
        return []
    
    def get_labels(self) -> List[GitHubLabel]:
        """Get the labels of the item."""
        if self.content and hasattr(self.content, 'labels'):
            return self.content.labels
        return []
    
    def get_repository(self) -> Optional[GitHubRepository]:
        """Get the repository of the item."""
        if self.content and hasattr(self.content, 'repository'):
            return self.content.repository
        return None


class GitHubProject(BaseModel):
    """GitHub project model."""
    id: str
    number: int
    title: str
    description: Optional[str] = None
    url: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed: bool = False
    fields: List[GitHubProjectField] = Field(default_factory=list)
    items: List[GitHubProjectItem] = Field(default_factory=list)
    
    class Config:
        allow_population_by_field_name = True
    
    def get_field_by_name(self, field_name: str) -> Optional[GitHubProjectField]:
        """Get a field by name.
        
        Args:
            field_name: Name of the field
            
        Returns:
            GitHubProjectField or None if not found
        """
        for field in self.fields:
            if field.name == field_name:
                return field
        return None


class GitHubGraphQLResponse(BaseModel):
    """GitHub GraphQL response model."""
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict[str, Any]]] = None
    
    def has_errors(self) -> bool:
        """Check if response has errors."""
        return self.errors is not None and len(self.errors) > 0
    
    def get_error_messages(self) -> List[str]:
        """Get error messages from response."""
        if not self.has_errors():
            return []
        return [error.get("message", "Unknown error") for error in self.errors]


class GitHubRateLimitInfo(BaseModel):
    """GitHub rate limit information."""
    limit: int
    remaining: int
    reset_at: Optional[datetime] = Field(None, alias="resetAt")
    used: int
    
    class Config:
        allow_population_by_field_name = True


class GitHubApiError(Exception):
    """GitHub API error."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class GitHubRateLimitError(GitHubApiError):
    """GitHub rate limit error."""
    
    def __init__(self, message: str, reset_at: Optional[datetime] = None):
        super().__init__(message, status_code=429)
        self.reset_at = reset_at
