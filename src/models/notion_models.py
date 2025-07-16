"""
Data models for Notion entities.
These models represent the structure of data used with Notion's API.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class NotionPropertyType(str, Enum):
    """Notion property types."""
    TITLE = "title"
    RICH_TEXT = "rich_text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
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
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    type: str = "person"
    person: Optional[Dict[str, Any]] = None


class NotionRichText(BaseModel):
    """Notion rich text model."""
    type: str = "text"
    text: Dict[str, Any]
    annotations: Dict[str, Any] = Field(default_factory=lambda: {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default"
    })
    plain_text: Optional[str] = None
    href: Optional[str] = None


class NotionSelectOption(BaseModel):
    """Notion select option model."""
    id: Optional[str] = None
    name: str
    color: NotionColor = NotionColor.DEFAULT


class NotionSelect(BaseModel):
    """Notion select property model."""
    id: Optional[str] = None
    name: str
    color: Optional[NotionColor] = None


class NotionMultiSelect(BaseModel):
    """Notion multi-select property model."""
    id: Optional[str] = None
    name: str
    color: Optional[NotionColor] = None


class NotionDate(BaseModel):
    """Notion date property model."""
    start: str  # ISO 8601 date string
    end: Optional[str] = None
    time_zone: Optional[str] = None


class NotionTitle(BaseModel):
    """Notion title property model."""
    type: str = "text"
    text: Dict[str, str]
    annotations: Dict[str, Any] = Field(default_factory=lambda: {
        "bold": False,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default"
    })
    plain_text: Optional[str] = None
    
    class Config:
        exclude_none = True
    href: Optional[str] = None


class NotionPropertyValue(BaseModel):
    """Base class for Notion property values."""
    id: Optional[str] = None
    type: NotionPropertyType


class NotionTitlePropertyValue(NotionPropertyValue):
    """Title property value."""
    type: NotionPropertyType = NotionPropertyType.TITLE
    title: List[NotionTitle]


class NotionRichTextPropertyValue(NotionPropertyValue):
    """Rich text property value."""
    type: NotionPropertyType = NotionPropertyType.RICH_TEXT
    rich_text: List[NotionRichText]


class NotionNumberPropertyValue(NotionPropertyValue):
    """Number property value."""
    type: NotionPropertyType = NotionPropertyType.NUMBER
    number: Optional[float] = None


class NotionSelectPropertyValue(NotionPropertyValue):
    """Select property value."""
    type: NotionPropertyType = NotionPropertyType.SELECT
    select: Optional[NotionSelect] = None


class NotionMultiSelectPropertyValue(NotionPropertyValue):
    """Multi-select property value."""
    type: NotionPropertyType = NotionPropertyType.MULTI_SELECT
    multi_select: List[NotionMultiSelect]


class NotionDatePropertyValue(NotionPropertyValue):
    """Date property value."""
    type: NotionPropertyType = NotionPropertyType.DATE
    date: Optional[NotionDate] = None


class NotionPeoplePropertyValue(NotionPropertyValue):
    """People property value."""
    type: NotionPropertyType = NotionPropertyType.PEOPLE
    people: List[NotionUser]


class NotionCheckboxPropertyValue(NotionPropertyValue):
    """Checkbox property value."""
    type: NotionPropertyType = NotionPropertyType.CHECKBOX
    checkbox: bool


class NotionUrlPropertyValue(NotionPropertyValue):
    """URL property value."""
    type: NotionPropertyType = NotionPropertyType.URL
    url: Optional[str] = None


class NotionEmailPropertyValue(NotionPropertyValue):
    """Email property value."""
    type: NotionPropertyType = NotionPropertyType.EMAIL
    email: Optional[str] = None


class NotionPhoneNumberPropertyValue(NotionPropertyValue):
    """Phone number property value."""
    type: NotionPropertyType = NotionPropertyType.PHONE_NUMBER
    phone_number: Optional[str] = None


# Union type for all property values
NotionPropertyValueUnion = Union[
    NotionTitlePropertyValue,
    NotionRichTextPropertyValue,
    NotionNumberPropertyValue,
    NotionSelectPropertyValue,
    NotionMultiSelectPropertyValue,
    NotionDatePropertyValue,
    NotionPeoplePropertyValue,
    NotionCheckboxPropertyValue,
    NotionUrlPropertyValue,
    NotionEmailPropertyValue,
    NotionPhoneNumberPropertyValue
]


class NotionPage(BaseModel):
    """Notion page model."""
    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: NotionUser
    last_edited_by: NotionUser
    cover: Optional[Dict[str, Any]] = None
    icon: Optional[Dict[str, Any]] = None
    parent: Dict[str, Any]
    archived: bool = False
    properties: Dict[str, NotionPropertyValueUnion]
    url: str
    
    def get_property_value(self, property_name: str) -> Optional[Any]:
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
    title: List[NotionRichText]
    description: List[NotionRichText]
    icon: Optional[Dict[str, Any]] = None
    cover: Optional[Dict[str, Any]] = None
    properties: Dict[str, Dict[str, Any]]
    parent: Dict[str, Any]
    url: str
    archived: bool = False
    
    def get_property_config(self, property_name: str) -> Optional[Dict[str, Any]]:
        """Get the configuration of a specific property.
        
        Args:
            property_name: Name of the property
            
        Returns:
            Property configuration or None if not found
        """
        return self.properties.get(property_name)


class NotionQueryResponse(BaseModel):
    """Notion database query response model."""
    results: List[NotionPage]
    next_cursor: Optional[str] = None
    has_more: bool = False
    type: str = "page_or_database"
    page_or_database: Optional[Dict[str, Any]] = None
    
    def get_all_results(self) -> List[NotionPage]:
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
        return NotionTitlePropertyValue(
            title=[
                NotionTitle(
                    text={"content": text},
                    plain_text=text
                )
            ]
        )
    
    @staticmethod
    def rich_text(text: str) -> NotionRichTextPropertyValue:
        """Build a rich text property.
        
        Args:
            text: Rich text content
            
        Returns:
            NotionRichTextPropertyValue
        """
        return NotionRichTextPropertyValue(
            rich_text=[
                NotionRichText(
                    text={"content": text},
                    plain_text=text
                )
            ]
        )
    
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
    def select(name: str, color: Optional[NotionColor] = None) -> NotionSelectPropertyValue:
        """Build a select property.
        
        Args:
            name: Select option name
            color: Select option color
            
        Returns:
            NotionSelectPropertyValue
        """
        return NotionSelectPropertyValue(
            select=NotionSelect(name=name, color=color)
        )
    
    @staticmethod
    def multi_select(names: List[str]) -> NotionMultiSelectPropertyValue:
        """Build a multi-select property.
        
        Args:
            names: List of select option names
            
        Returns:
            NotionMultiSelectPropertyValue
        """
        return NotionMultiSelectPropertyValue(
            multi_select=[
                NotionMultiSelect(name=name) for name in names
            ]
        )
    
    @staticmethod
    def date(start: Union[str, datetime, date], end: Optional[Union[str, datetime, date]] = None) -> NotionDatePropertyValue:
        """Build a date property.
        
        Args:
            start: Start date
            end: End date (optional)
            
        Returns:
            NotionDatePropertyValue
        """
        if isinstance(start, datetime):
            start_str = start.isoformat()
        elif isinstance(start, date):
            start_str = start.isoformat()
        else:
            start_str = start
        
        end_str = None
        if end:
            if isinstance(end, datetime):
                end_str = end.isoformat()
            elif isinstance(end, date):
                end_str = end.isoformat()
            else:
                end_str = end
        
        return NotionDatePropertyValue(
            date=NotionDate(start=start_str, end=end_str)
        )
    
    @staticmethod
    def people(user_ids: List[str]) -> NotionPeoplePropertyValue:
        """Build a people property.
        
        Args:
            user_ids: List of user IDs
            
        Returns:
            NotionPeoplePropertyValue
        """
        return NotionPeoplePropertyValue(
            people=[NotionUser(id=user_id) for user_id in user_ids]
        )
    
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
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class NotionRateLimitError(NotionApiError):
    """Notion rate limit error."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after
