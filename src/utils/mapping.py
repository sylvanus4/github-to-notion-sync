"""
Field mapping utilities for GitHub to Notion synchronization.
Handles field mapping, validation, and transformation.
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from ..config import ConfigManager
from ..utils.logger import get_logger

logger = get_logger(__name__)


class FieldMapper:
    """Handles field mapping between GitHub and Notion."""
    
    def __init__(self, config: ConfigManager):
        """Initialize field mapper.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.field_mappings = config.field_mappings
    
    def get_notion_property_name(self, github_field: str) -> Optional[str]:
        """Get Notion property name for a GitHub field.
        
        Args:
            github_field: GitHub field name
            
        Returns:
            Notion property name or None if not found
        """
        return self.config.get_notion_property_name(github_field)
    
    def get_github_field_name(self, notion_property: str) -> Optional[str]:
        """Get GitHub field name for a Notion property.
        
        Args:
            notion_property: Notion property name
            
        Returns:
            GitHub field name or None if not found
        """
        return self.config.get_github_field_name(notion_property)
    
    def get_field_mapping(self, field_name: str) -> Optional[Dict[str, Any]]:
        """Get field mapping configuration.
        
        Args:
            field_name: Field name (can be mapping key or GitHub field name)
            
        Returns:
            Field mapping configuration or None if not found
        """
        # First try as mapping key
        mapping = self.config.get_field_mapping(field_name)
        if mapping:
            return mapping
        
        # If not found, try as GitHub field name
        return self.config.get_field_mapping_by_github_field(field_name)
    
    def validate_field_mapping(self, field_name: str, value: Any) -> bool:
        """Validate a field value against its mapping configuration.
        
        Args:
            field_name: Field name
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        field_config = self.get_field_mapping(field_name)
        if not field_config:
            return False
        
        field_type = field_config.get("type")
        required = field_config.get("required", False)
        
        # Check if required field is missing
        if required and value is None:
            logger.warning(f"Required field '{field_name}' is missing")
            return False
        
        # Skip validation if value is None and field is not required
        if value is None:
            return True
        
        # Type-specific validation
        try:
            if field_type == "title":
                return isinstance(value, str) and len(value) > 0
            elif field_type == "rich_text":
                return isinstance(value, str)
            elif field_type == "number":
                return isinstance(value, (int, float))
            elif field_type == "select":
                if isinstance(value, str):
                    options = field_config.get("options", [])
                    return not options or value in options
                return False
            elif field_type == "multi_select":
                if isinstance(value, list):
                    options = field_config.get("options", [])
                    if not options:
                        return True
                    return all(v in options for v in value)
                return False
            elif field_type == "date":
                return isinstance(value, (str, datetime))
            elif field_type == "people":
                return isinstance(value, list)
            elif field_type == "url":
                return isinstance(value, str) and value.startswith(("http://", "https://"))
            elif field_type == "checkbox":
                return isinstance(value, bool)
            elif field_type == "email":
                return isinstance(value, str) and "@" in value
            elif field_type == "phone_number":
                return isinstance(value, str)
            else:
                logger.warning(f"Unknown field type '{field_type}' for field '{field_name}'")
                return True
                
        except Exception as e:
            logger.error(f"Error validating field '{field_name}': {e}")
            return False
    
    def transform_value(self, field_name: str, value: Any) -> Any:
        """Transform a value based on field mapping configuration.
        
        Args:
            field_name: Field name
            value: Value to transform
            
        Returns:
            Transformed value
        """
        field_config = self.get_field_mapping(field_name)
        if not field_config:
            return value
        
        field_type = field_config.get("type")
        
        try:
            if field_type == "title" or field_type == "rich_text":
                return str(value) if value is not None else ""
            elif field_type == "number":
                if isinstance(value, str):
                    try:
                        return float(value)
                    except ValueError:
                        return 0.0
                return float(value) if value is not None else 0.0
            elif field_type == "select":
                if value is None:
                    return ""
                
                # Check for value mappings (GitHub value -> Notion value)
                value_mappings = field_config.get("value_mappings", {})
                if value_mappings and str(value) in value_mappings:
                    return value_mappings[str(value)]
                
                return str(value)
            elif field_type == "status":
                if value is None:
                    return ""
                
                # Check for value mappings (GitHub value -> Notion value)
                value_mappings = field_config.get("value_mappings", {})
                if value_mappings and str(value) in value_mappings:
                    return value_mappings[str(value)]
                
                return str(value)
            elif field_type == "multi_select":
                if isinstance(value, list):
                    # Apply value mappings to each item in the list
                    value_mappings = field_config.get("value_mappings", {})
                    if value_mappings:
                        return [value_mappings.get(str(v), str(v)) for v in value]
                    return [str(v) for v in value]
                elif value is not None:
                    # Apply value mapping to single value
                    value_mappings = field_config.get("value_mappings", {})
                    if value_mappings and str(value) in value_mappings:
                        return [value_mappings[str(value)]]
                    return [str(value)]
                else:
                    return []
            elif field_type == "date":
                if isinstance(value, datetime):
                    return value.isoformat()
                elif isinstance(value, str):
                    return value
                else:
                    return None
            elif field_type == "checkbox":
                return bool(value) if value is not None else False
            elif field_type == "url":
                return str(value) if value is not None else ""
            elif field_type == "email":
                return str(value) if value is not None else ""
            elif field_type == "phone_number":
                return str(value) if value is not None else ""
            else:
                return value
                
        except Exception as e:
            logger.error(f"Error transforming value for field '{field_name}': {e}")
            return value
    
    def get_mapped_fields(self) -> List[str]:
        """Get list of all mapped field names.
        
        Returns:
            List of field names
        """
        return list(self.field_mappings.keys())
    
    def get_required_fields(self) -> List[str]:
        """Get list of required field names.
        
        Returns:
            List of required field names
        """
        required_fields = []
        for field_name, field_config in self.field_mappings.items():
            if field_config.get("required", False):
                required_fields.append(field_name)
        return required_fields
    
    def get_unique_fields(self) -> List[str]:
        """Get list of unique field names.
        
        Returns:
            List of unique field names
        """
        unique_fields = []
        for field_name, field_config in self.field_mappings.items():
            if field_config.get("unique", False):
                unique_fields.append(field_name)
        return unique_fields
    
    def map_github_user_to_notion(self, github_login: str) -> Optional[str]:
        """Map GitHub user login to Notion user.
        
        Args:
            github_login: GitHub username
            
        Returns:
            Notion user ID or email, or None if not found
        """
        return self.config.map_github_user_to_notion(github_login)
    
    def build_filter_for_github_id(self, github_node_id: str) -> Optional[Dict[str, Any]]:
        """Build Notion query filter for GitHub node ID.
        
        Args:
            github_node_id: GitHub project item node ID
            
        Returns:
            Notion filter dictionary or None if field not mapped
        """
        github_id_property = self.get_notion_property_name("id")
        if not github_id_property:
            return None
        
        return {
            "property": github_id_property,
            "rich_text": {
                "equals": github_node_id
            }
        }
    
    def validate_mapping_configuration(self) -> List[str]:
        """Validate the field mapping configuration.
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Check for required mappings
        required_mappings = ["title"]  # github_node_id temporarily disabled
        for required_field in required_mappings:
            if required_field not in self.field_mappings:
                errors.append(f"Required field mapping '{required_field}' is missing")
            else:
                field_config = self.field_mappings[required_field]
                if not field_config.get("notion_property"):
                    errors.append(f"Field '{required_field}' is missing notion_property")
                if not field_config.get("github_field"):
                    errors.append(f"Field '{required_field}' is missing github_field")
                if not field_config.get("type"):
                    errors.append(f"Field '{required_field}' is missing type")
        
        # Check for duplicate Notion properties
        notion_properties = []
        for field_name, field_config in self.field_mappings.items():
            notion_property = field_config.get("notion_property")
            if notion_property:
                if notion_property in notion_properties:
                    errors.append(f"Duplicate Notion property '{notion_property}' in field '{field_name}'")
                else:
                    notion_properties.append(notion_property)
        
        # Check for duplicate GitHub fields
        github_fields = []
        for field_name, field_config in self.field_mappings.items():
            github_field = field_config.get("github_field")
            if github_field:
                if github_field in github_fields:
                    errors.append(f"Duplicate GitHub field '{github_field}' in field '{field_name}'")
                else:
                    github_fields.append(github_field)
        
        # Validate field types
        valid_types = [
            "title", "rich_text", "number", "select", "multi_select",
            "date", "people", "checkbox", "url", "email", "phone_number"
        ]
        for field_name, field_config in self.field_mappings.items():
            field_type = field_config.get("type")
            if field_type and field_type not in valid_types:
                errors.append(f"Invalid field type '{field_type}' in field '{field_name}'")
        
        return errors
