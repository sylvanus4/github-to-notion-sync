"""
Data models for GitHub entities.
These models represent the structure of data returned from GitHub's GraphQL API v4.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


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
    email: str | None = None
    name: str | None = None
    avatar_url: str | None = Field(None, alias="avatarUrl")

    class Config:
        populate_by_name = True


class GitHubLabel(BaseModel):
    """GitHub label model."""

    id: str
    name: str
    color: str
    description: str | None = None


class GitHubComment(BaseModel):
    """GitHub comment model."""

    id: str
    body: str
    author: GitHubUser | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    url: str

    class Config:
        populate_by_name = True


class GitHubRepository(BaseModel):
    """GitHub repository model."""

    id: str
    name: str
    full_name: str = Field(alias="nameWithOwner")
    url: str
    description: str | None = None

    class Config:
        populate_by_name = True


class GitHubIssue(BaseModel):
    """GitHub issue model."""

    id: str
    number: int
    title: str
    body: str | None = None
    url: str
    state: GitHubState
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed_at: datetime | None = Field(None, alias="closedAt")
    assignees: list[GitHubUser] = []
    labels: list[GitHubLabel] = []
    repository: GitHubRepository | None = None

    @field_validator("assignees", mode="before")
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and "nodes" in v:
            return v["nodes"]
        return v if isinstance(v, list) else []

    @field_validator("labels", mode="before")
    @classmethod
    def parse_labels(cls, v):
        """Parse labels from nodes structure."""
        if isinstance(v, dict) and "nodes" in v:
            return v["nodes"]
        return v if isinstance(v, list) else []

    class Config:
        populate_by_name = True


class GitHubPullRequest(BaseModel):
    """GitHub pull request model."""

    id: str
    number: int
    title: str
    body: str | None = None
    url: str
    state: GitHubState
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed_at: datetime | None = Field(None, alias="closedAt")
    merged_at: datetime | None = Field(None, alias="mergedAt")
    assignees: list[GitHubUser] = []
    labels: list[GitHubLabel] = []
    repository: GitHubRepository | None = None
    draft: bool = False

    @field_validator("assignees", mode="before")
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and "nodes" in v:
            return v["nodes"]
        return v if isinstance(v, list) else []

    @field_validator("labels", mode="before")
    @classmethod
    def parse_labels(cls, v):
        """Parse labels from nodes structure."""
        if isinstance(v, dict) and "nodes" in v:
            return v["nodes"]
        return v if isinstance(v, list) else []

    class Config:
        populate_by_name = True


class GitHubDraftIssue(BaseModel):
    """GitHub draft issue model."""

    id: str
    title: str
    body: str | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    assignees: list[GitHubUser] = []

    @field_validator("assignees", mode="before")
    @classmethod
    def parse_assignees(cls, v):
        """Parse assignees from nodes structure."""
        if isinstance(v, dict) and "nodes" in v:
            return v["nodes"]
        return v if isinstance(v, list) else []

    class Config:
        populate_by_name = True


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


class GitHubIteration(BaseModel):
    """GitHub iteration model."""

    id: str
    title: str
    start_date: datetime = Field(alias="startDate")
    duration: int

    @field_validator("start_date", mode="before")
    @classmethod
    def parse_start_date(cls, v):
        """Parse start date from date string or datetime.

        GitHub API returns dates in 'YYYY-MM-DD' format which needs to be
        converted to datetime with time component.
        """
        if isinstance(v, str):
            # If it's a date string without time, add time component
            if "T" not in v:
                v = f"{v}T00:00:00Z"
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    class Config:
        populate_by_name = True


class GitHubIterationConfiguration(BaseModel):
    """GitHub iteration configuration model."""

    iterations: list[GitHubIteration] = Field(default_factory=list)

    @field_validator("iterations", mode="before")
    @classmethod
    def parse_iterations(cls, v):
        """Parse iterations list."""
        if v is None:
            return []
        return v if isinstance(v, list) else []


class GitHubProjectField(BaseModel):
    """GitHub project field model."""

    id: str
    name: str
    dataType: GitHubProjectFieldType
    options: list[dict[str, Any]] | None = None
    configuration: GitHubIterationConfiguration | None = None


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
    option_id: str | None = Field(None, alias="optionId")

    class Config:
        populate_by_name = True


class GitHubProjectIterationFieldValue(GitHubProjectFieldValue):
    """Iteration field value."""

    title: str
    duration: int | None = None


class GitHubProjectTitleFieldValue(GitHubProjectFieldValue):
    """Title field value."""

    text: str
    start_date: datetime | None = Field(None, alias="startDate")

    class Config:
        populate_by_name = True


# Union type for all field values
GitHubProjectFieldValueUnion = (
    GitHubProjectTextFieldValue
    | GitHubProjectNumberFieldValue
    | GitHubProjectDateFieldValue
    | GitHubProjectSingleSelectFieldValue
    | GitHubProjectIterationFieldValue
    | GitHubProjectTitleFieldValue
)


class GitHubProjectItem(BaseModel):
    """GitHub project item model."""

    id: str  # This is the project item node ID (unique key for Notion)
    type: GitHubItemType
    content: GitHubIssue | GitHubPullRequest | GitHubDraftIssue | None = None
    field_values: list[GitHubProjectFieldValueUnion] = Field(default_factory=list, alias="fieldValues")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True

    def get_field_value(self, field_name: str) -> Any | None:
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
                if isinstance(field_value, GitHubProjectNumberFieldValue):
                    return field_value.number
                if isinstance(field_value, GitHubProjectDateFieldValue):
                    return field_value.date
                if isinstance(field_value, GitHubProjectSingleSelectFieldValue):
                    return field_value.name
                if isinstance(field_value, GitHubProjectIterationFieldValue):
                    return field_value.title
        return None

    def get_title(self) -> str:
        """Get the title of the item."""
        if self.content:
            return self.content.title
        return "Untitled"

    def get_url(self) -> str | None:
        """Get the URL of the item."""
        if self.content and hasattr(self.content, "url"):
            return self.content.url
        return None

    def get_number(self) -> int | None:
        """Get the number of the item."""
        if self.content and hasattr(self.content, "number"):
            return self.content.number
        return None

    def get_state(self) -> GitHubState | None:
        """Get the state of the item."""
        if self.content and hasattr(self.content, "state"):
            return self.content.state
        return None

    def get_assignees(self) -> list[GitHubUser]:
        """Get the assignees of the item."""
        if self.content and hasattr(self.content, "assignees"):
            return self.content.assignees
        return []

    def get_labels(self) -> list[GitHubLabel]:
        """Get the labels of the item."""
        if self.content and hasattr(self.content, "labels"):
            return self.content.labels
        return []

    def get_repository(self) -> GitHubRepository | None:
        """Get the repository of the item."""
        if self.content and hasattr(self.content, "repository"):
            return self.content.repository
        return None


class GitHubProject(BaseModel):
    """GitHub project model."""

    id: str
    number: int
    title: str
    description: str | None = None
    url: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    closed: bool = False
    fields: list[GitHubProjectField] = Field(default_factory=list)
    items: list[GitHubProjectItem] = Field(default_factory=list)

    class Config:
        populate_by_name = True

    def get_field_by_name(self, field_name: str) -> GitHubProjectField | None:
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

    data: dict[str, Any] | None = None
    errors: list[dict[str, Any]] | None = None

    def has_errors(self) -> bool:
        """Check if response has errors."""
        return self.errors is not None and len(self.errors) > 0

    def get_error_messages(self) -> list[str]:
        """Get error messages from response."""
        if not self.has_errors():
            return []
        return [error.get("message", "Unknown error") for error in self.errors]


class GitHubRateLimitInfo(BaseModel):
    """GitHub rate limit information."""

    limit: int
    remaining: int
    reset_at: datetime | None = Field(None, alias="resetAt")
    used: int

    class Config:
        populate_by_name = True


class GitHubApiError(Exception):
    """GitHub API error."""

    def __init__(self, message: str, status_code: int | None = None, response_data: dict[str, Any] | None = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class GitHubRateLimitError(GitHubApiError):
    """GitHub rate limit error."""

    def __init__(self, message: str, reset_at: datetime | None = None):
        super().__init__(message, status_code=429)
        self.reset_at = reset_at
