"""
Data models for Notion entities.
These models represent the structure of data used with Notion's API.
"""

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class NotionPropertyType(str, Enum):
    """Notion property types."""

    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    STATUS = "status"
    DATE = "date"
    PEOPLE = "people"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    FORMULA = "formula"
    RELATION = "relation"
    ROLLUP = "rollup"
    CREATED_TIME = "created_time"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    LAST_EDITED_BY = "last_edited_by"


class NotionColor(str, Enum):
    """Notion colors for select options."""

    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"


class NotionUser(BaseModel):
    """Notion user model."""

    id: str
    name: str | None = None
    avatar_url: str | None = None
    type: str = "person"
    person: dict[str, Any] | None = None


class NotionRichText(BaseModel):
    """Notion rich text model."""

    type: str = "text"
    text: dict[str, Any]
    annotations: dict[str, Any] = Field(
        default_factory=lambda: {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        }
    )
    plain_text: str | None = None
    href: str | None = None


class NotionSelectOption(BaseModel):
    """Notion select option model."""

    id: str | None = None
    name: str
    color: NotionColor = NotionColor.DEFAULT


class NotionSelect(BaseModel):
    """Notion select property model."""

    id: str | None = None
    name: str
    color: NotionColor | None = None


class NotionMultiSelect(BaseModel):
    """Notion multi-select property model."""

    id: str | None = None
    name: str
    color: NotionColor | None = None


class NotionStatus(BaseModel):
    """Notion status property model."""

    id: str | None = None
    name: str
    color: NotionColor | None = None


class NotionDate(BaseModel):
    """Notion date property model."""

    start: str  # ISO 8601 date string
    end: str | None = None
    time_zone: str | None = None


class NotionTitle(BaseModel):
    """Notion title property model."""

    type: str = "text"
    text: dict[str, str]
    annotations: dict[str, Any] = Field(
        default_factory=lambda: {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        }
    )
    plain_text: str | None = None

    class Config:
        exclude_none = True

    href: str | None = None


class NotionPropertyValue(BaseModel):
    """Base class for Notion property values."""

    id: str | None = None
    type: NotionPropertyType


class NotionTitlePropertyValue(NotionPropertyValue):
    """Title property value."""

    type: NotionPropertyType = NotionPropertyType.TITLE
    title: list[NotionTitle]


class NotionRichTextPropertyValue(NotionPropertyValue):
    """Rich text property value."""

    type: NotionPropertyType = NotionPropertyType.RICH_TEXT
    rich_text: list[NotionRichText]


class NotionNumberPropertyValue(NotionPropertyValue):
    """Number property value."""

    type: NotionPropertyType = NotionPropertyType.NUMBER
    number: float | None = None


class NotionSelectPropertyValue(NotionPropertyValue):
    """Select property value."""

    type: NotionPropertyType = NotionPropertyType.SELECT
    select: NotionSelect | None = None


class NotionMultiSelectPropertyValue(NotionPropertyValue):
    """Multi-select property value."""

    type: NotionPropertyType = NotionPropertyType.MULTI_SELECT
    multi_select: list[NotionMultiSelect]


class NotionStatusPropertyValue(NotionPropertyValue):
    """Status property value."""

    type: NotionPropertyType = NotionPropertyType.STATUS
    status: NotionStatus | None = None


class NotionDatePropertyValue(NotionPropertyValue):
    """Date property value."""

    type: NotionPropertyType = NotionPropertyType.DATE
    date: NotionDate | None = None


class NotionPeoplePropertyValue(NotionPropertyValue):
    """People property value."""

    type: NotionPropertyType = NotionPropertyType.PEOPLE
    people: list[NotionUser]


class NotionCheckboxPropertyValue(NotionPropertyValue):
    """Checkbox property value."""

    type: NotionPropertyType = NotionPropertyType.CHECKBOX
    checkbox: bool


class NotionUrlPropertyValue(NotionPropertyValue):
    """URL property value."""

    type: NotionPropertyType = NotionPropertyType.URL
    url: str | None = None


class NotionEmailPropertyValue(NotionPropertyValue):
    """Email property value."""

    type: NotionPropertyType = NotionPropertyType.EMAIL
    email: str | None = None


class NotionPhoneNumberPropertyValue(NotionPropertyValue):
    """Phone number property value."""

    type: NotionPropertyType = NotionPropertyType.PHONE_NUMBER
    phone_number: str | None = None


# Union type for all property values
NotionPropertyValueUnion = (
    NotionTitlePropertyValue
    | NotionRichTextPropertyValue
    | NotionNumberPropertyValue
    | NotionSelectPropertyValue
    | NotionMultiSelectPropertyValue
    | NotionStatusPropertyValue
    | NotionDatePropertyValue
    | NotionPeoplePropertyValue
    | NotionCheckboxPropertyValue
    | NotionUrlPropertyValue
    | NotionEmailPropertyValue
    | NotionPhoneNumberPropertyValue
)


class NotionPage(BaseModel):
    """Notion page model."""

    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: NotionUser
    last_edited_by: NotionUser
    cover: dict[str, Any] | None = None
    icon: dict[str, Any] | None = None
    parent: dict[str, Any]
    archived: bool = False
    properties: dict[str, NotionPropertyValueUnion]
    url: str

    def get_property_value(self, property_name: str) -> Any | None:
        """Get the value of a specific property.

        Args:
            property_name: Name of the property

        Returns:
            Property value or None if not found
        """
        prop = self.properties.get(property_name)
        if not prop:
            return None

        if isinstance(prop, NotionTitlePropertyValue):
            if prop.title:
                return prop.title[0].plain_text
        elif isinstance(prop, NotionRichTextPropertyValue):
            if prop.rich_text:
                return prop.rich_text[0].plain_text
        elif isinstance(prop, NotionNumberPropertyValue):
            return prop.number
        elif isinstance(prop, NotionSelectPropertyValue):
            return prop.select.name if prop.select else None
        elif isinstance(prop, NotionMultiSelectPropertyValue):
            return [option.name for option in prop.multi_select]
        elif isinstance(prop, NotionStatusPropertyValue):
            return prop.status.name if prop.status else None
        elif isinstance(prop, NotionDatePropertyValue):
            return prop.date.start if prop.date else None
        elif isinstance(prop, NotionPeoplePropertyValue):
            return [user.name for user in prop.people]
        elif isinstance(prop, NotionCheckboxPropertyValue):
            return prop.checkbox
        elif isinstance(prop, NotionUrlPropertyValue):
            return prop.url
        elif isinstance(prop, NotionEmailPropertyValue):
            return prop.email
        elif isinstance(prop, NotionPhoneNumberPropertyValue):
            return prop.phone_number

        return None


class NotionDatabase(BaseModel):
    """Notion database model."""

    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: NotionUser
    last_edited_by: NotionUser
    title: list[NotionRichText]
    description: list[NotionRichText]
    icon: dict[str, Any] | None = None
    cover: dict[str, Any] | None = None
    properties: dict[str, dict[str, Any]]
    parent: dict[str, Any]
    url: str
    archived: bool = False

    def get_property_config(self, property_name: str) -> dict[str, Any] | None:
        """Get the configuration of a specific property.

        Args:
            property_name: Name of the property

        Returns:
            Property configuration or None if not found
        """
        return self.properties.get(property_name)


class NotionQueryResponse(BaseModel):
    """Notion database query response model."""

    results: list[NotionPage]
    next_cursor: str | None = None
    has_more: bool = False
    type: str = "page_or_database"
    page_or_database: dict[str, Any] | None = None

    def get_all_results(self) -> list[NotionPage]:
        """Get all results from the query."""
        return self.results


class NotionPropertyBuilder:
    """Helper class to build Notion properties."""

    @staticmethod
    def title(text: str) -> NotionTitlePropertyValue:
        """Build a title property.

        Args:
            text: Title text

        Returns:
            NotionTitlePropertyValue
        """
        return NotionTitlePropertyValue(title=[NotionTitle(text={"content": text}, plain_text=text)])

    @staticmethod
    def rich_text(text: str) -> NotionRichTextPropertyValue:
        """Build a rich text property.

        Args:
            text: Rich text content

        Returns:
            NotionRichTextPropertyValue
        """
        return NotionRichTextPropertyValue(rich_text=[NotionRichText(text={"content": text}, plain_text=text)])

    @staticmethod
    def number(value: float) -> NotionNumberPropertyValue:
        """Build a number property.

        Args:
            value: Number value

        Returns:
            NotionNumberPropertyValue
        """
        return NotionNumberPropertyValue(number=value)

    @staticmethod
    def select(name: str, color: NotionColor | None = None) -> NotionSelectPropertyValue:
        """Build a select property.

        Args:
            name: Select option name
            color: Select option color

        Returns:
            NotionSelectPropertyValue
        """
        return NotionSelectPropertyValue(select=NotionSelect(name=name, color=color))

    @staticmethod
    def multi_select(names: list[str]) -> NotionMultiSelectPropertyValue:
        """Build a multi-select property.

        Args:
            names: List of select option names

        Returns:
            NotionMultiSelectPropertyValue
        """
        return NotionMultiSelectPropertyValue(multi_select=[NotionMultiSelect(name=name) for name in names])

    @staticmethod
    def date(
        start: str | datetime | date, end: str | datetime | date | None = None
    ) -> NotionDatePropertyValue:
        """Build a date property.

        Args:
            start: Start date
            end: End date (optional)

        Returns:
            NotionDatePropertyValue
        """
        start_str = start.isoformat() if isinstance(start, datetime | date) else start

        end_str = None
        if end:
            end_str = end.isoformat() if isinstance(end, datetime | date) else end

        return NotionDatePropertyValue(date=NotionDate(start=start_str, end=end_str))

    @staticmethod
    def people(user_ids: list[str]) -> NotionPeoplePropertyValue:
        """Build a people property.

        Args:
            user_ids: List of user IDs

        Returns:
            NotionPeoplePropertyValue
        """
        return NotionPeoplePropertyValue(people=[NotionUser(id=user_id) for user_id in user_ids])

    @staticmethod
    def checkbox(checked: bool) -> NotionCheckboxPropertyValue:
        """Build a checkbox property.

        Args:
            checked: Checkbox state

        Returns:
            NotionCheckboxPropertyValue
        """
        return NotionCheckboxPropertyValue(checkbox=checked)

    @staticmethod
    def url(url: str) -> NotionUrlPropertyValue:
        """Build a URL property.

        Args:
            url: URL string

        Returns:
            NotionUrlPropertyValue
        """
        return NotionUrlPropertyValue(url=url)

    @staticmethod
    def email(email: str) -> NotionEmailPropertyValue:
        """Build an email property.

        Args:
            email: Email address

        Returns:
            NotionEmailPropertyValue
        """
        return NotionEmailPropertyValue(email=email)

    @staticmethod
    def phone_number(phone: str) -> NotionPhoneNumberPropertyValue:
        """Build a phone number property.

        Args:
            phone: Phone number

        Returns:
            NotionPhoneNumberPropertyValue
        """
        return NotionPhoneNumberPropertyValue(phone_number=phone)


class NotionApiError(Exception):
    """Notion API error."""

    def __init__(self, message: str, status_code: int | None = None, response_data: dict[str, Any] | None = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class NotionRateLimitError(NotionApiError):
    """Notion rate limit error."""

    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after
