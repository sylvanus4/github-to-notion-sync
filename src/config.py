"""
Configuration module for GitHub to Notion sync system.
Handles environment variables, field mappings, and application settings.
"""

import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings with validation and environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_prefix="",
    )

    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")

    # Notion Configuration
    notion_token: str = Field(alias="NOTION_TOKEN")
    notion_db_id: str = Field(alias="NOTION_DB_ID")

    # GitHub Configuration
    github_token: str = Field(alias="GH_TOKEN")
    github_org: str = Field(alias="GH_ORG")
    github_project_number: int = Field(alias="GH_PROJECT_NUMBER")

    # Webhook Configuration
    webhook_secret: str = Field(alias="GH_WEBHOOK_SECRET")
    webhook_port: int = Field(default=8000, alias="WEBHOOK_PORT")
    webhook_host: str = Field(default="0.0.0.0", alias="WEBHOOK_HOST")

    # Rate Limiting
    notion_rate_limit: int = Field(default=3, alias="NOTION_RATE_LIMIT")  # requests per second
    github_rate_limit: int = Field(default=5000, alias="GITHUB_RATE_LIMIT")  # requests per hour

    # Sync Configuration
    batch_size: int = Field(default=100, alias="BATCH_SIZE")
    retry_attempts: int = Field(default=3, alias="RETRY_ATTEMPTS")
    retry_delay: int = Field(default=1, alias="RETRY_DELAY")

    # Full Sync Schedule (cron format)
    full_sync_interval: str = Field(default="0 */6 * * *", alias="FULL_SYNC_INTERVAL")

    # Backup Configuration
    backup_enabled: bool = Field(default=True, alias="BACKUP_ENABLED")
    backup_schedule: str = Field(default="0 2 * * 0", alias="BACKUP_SCHEDULE")

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")  # json or text

    # File Paths
    config_dir: str = Field(default="config", alias="CONFIG_DIR")
    queries_dir: str = Field(default="queries", alias="QUERIES_DIR")

    @field_validator("notion_db_id")
    @classmethod
    def validate_notion_db_id(cls, v):
        """Validate Notion database ID format."""
        if not v:
            raise ValueError("Notion database ID is required")

        # Remove hyphens if present
        clean_id = v.replace("-", "")

        if len(clean_id) != 32:
            raise ValueError("Notion database ID must be 32 characters long")

        return clean_id

    @field_validator("github_project_number")
    @classmethod
    def validate_github_project_number(cls, v):
        """Validate GitHub project number."""
        if v <= 0:
            raise ValueError("GitHub project number must be positive")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            msg = f"Log level must be one of {valid_levels}"
            raise ValueError(msg)
        return v.upper()


class ConfigManager:
    """Manages application configuration and field mappings."""

    def __init__(self, settings: Settings | None = None):
        """Initialize configuration manager.

        Args:
            settings: Optional pre-configured settings. If None, loads from environment.
        """
        self.settings = settings or Settings()
        self._field_mappings: dict[str, Any] | None = None
        self._webhook_events: dict[str, Any] | None = None
        self._sync_config: dict[str, Any] | None = None
        self._user_mappings: dict[str, str] | None = None

        # Load configuration files
        self._load_config_files()

    def _load_config_files(self):
        """Load configuration from YAML files."""
        try:
            # Load field mappings
            field_mappings_path = Path(self.settings.config_dir) / "field_mappings.yml"
            if field_mappings_path.exists():
                with open(field_mappings_path, encoding="utf-8") as f:
                    config_data = yaml.safe_load(f) or {}

                    self._field_mappings = config_data.get("github_to_notion", {})
                    self._webhook_events = config_data.get("webhook_events", {})
                    self._sync_config = config_data.get("sync_config", {})
                    self._user_mappings = config_data.get("user_mappings", {})

            # Load sync configuration
            sync_config_path = Path(self.settings.config_dir) / "sync_config.yml"
            if sync_config_path.exists():
                with open(sync_config_path, encoding="utf-8") as f:
                    sync_data = yaml.safe_load(f) or {}
                    if self._sync_config:
                        self._sync_config.update(sync_data)
                    else:
                        self._sync_config = sync_data

            # Load webhook events configuration
            webhook_events_path = Path(self.settings.config_dir) / "webhook_events.yml"
            if webhook_events_path.exists():
                with open(webhook_events_path, encoding="utf-8") as f:
                    webhook_data = yaml.safe_load(f) or {}
                    if self._webhook_events:
                        self._webhook_events.update(webhook_data)
                    else:
                        self._webhook_events = webhook_data

        except Exception as e:
            logger.exception(f"Error loading configuration files: {e}")
            # Set defaults if files cannot be loaded
            self._field_mappings = {}
            self._webhook_events = {}
            self._sync_config = {}
            self._user_mappings = {}

    @property
    def field_mappings(self) -> dict[str, Any]:
        """Get GitHub to Notion field mappings."""
        return self._field_mappings or {}

    @property
    def webhook_events(self) -> dict[str, Any]:
        """Get webhook event configuration."""
        return self._webhook_events or {}

    @property
    def sync_config(self) -> dict[str, Any]:
        """Get sync configuration."""
        return self._sync_config or {}

    @property
    def user_mappings(self) -> dict[str, str]:
        """Get user mappings from GitHub login to Notion user."""
        return self._user_mappings or {}

    def get_field_mapping(self, field_name: str) -> dict[str, Any] | None:
        """Get specific field mapping configuration.

        Args:
            field_name: Name of the field to get mapping for

        Returns:
            Field mapping configuration or None if not found
        """
        return self.field_mappings.get(field_name)

    def get_field_mapping_by_github_field(self, github_field: str) -> dict[str, Any] | None:
        """Get field mapping configuration by GitHub field name.

        Args:
            github_field: GitHub field name (e.g., "Status", "Priority")

        Returns:
            Field mapping configuration or None if not found
        """
        for _mapping_key, mapping_config in self.field_mappings.items():
            if mapping_config.get("github_field") == github_field:
                return mapping_config
        return None

    def get_notion_property_name(self, github_field: str) -> str | None:
        """Get Notion property name for a GitHub field.

        Args:
            github_field: GitHub field name

        Returns:
            Notion property name or None if not found
        """
        for field_config in self.field_mappings.values():
            if field_config.get("github_field") == github_field:
                return field_config.get("notion_property")
        return None

    def get_github_field_name(self, notion_property: str) -> str | None:
        """Get GitHub field name for a Notion property.

        Args:
            notion_property: Notion property name

        Returns:
            GitHub field name or None if not found
        """
        for field_config in self.field_mappings.values():
            if field_config.get("notion_property") == notion_property:
                return field_config.get("github_field")
        return None

    def is_webhook_event_enabled(self, event_type: str, action: str) -> bool:
        """Check if a webhook event and action should be processed.

        Args:
            event_type: GitHub webhook event type
            action: GitHub webhook action

        Returns:
            True if event should be processed, False otherwise
        """
        event_config = self.webhook_events.get(event_type)
        if not event_config:
            return False

        enabled_actions = event_config.get("actions", [])
        return action in enabled_actions

    def get_rate_limit(self, service: str) -> int:
        """Get rate limit for a service.

        Args:
            service: Service name ('notion' or 'github')

        Returns:
            Rate limit value
        """
        rate_limits = self.sync_config.get("rate_limits", {})
        if service == "notion":
            return rate_limits.get("notion_api", self.settings.notion_rate_limit)
        if service == "github":
            return rate_limits.get("github_api", self.settings.github_rate_limit)
        return 0

    def map_github_user_to_notion(self, github_login: str) -> str | None:
        """Map GitHub login to Notion user.

        Args:
            github_login: GitHub username

        Returns:
            Notion user ID or email, or None if not found
        """
        return self.user_mappings.get(github_login)

    def load_graphql_query(self, query_name: str) -> str | None:
        """Load GraphQL query from file.

        Args:
            query_name: Name of the query file (without .graphql extension)

        Returns:
            GraphQL query string or None if not found
        """
        try:
            query_path = Path(self.settings.queries_dir) / f"{query_name}.graphql"
            if query_path.exists():
                with open(query_path, encoding="utf-8") as f:
                    return f.read().strip()
        except Exception as e:
            logger.exception(f"Error loading GraphQL query '{query_name}': {e}")
        return None

    def validate_configuration(self) -> list[str]:
        """Validate configuration and return list of errors.

        Returns:
            List of validation error messages
        """
        errors = []

        # Check required environment variables
        required_vars = [
            "notion_token",
            "notion_db_id",
            "github_token",
            "github_org",
            "github_project_number",
            "webhook_secret",
        ]

        for var in required_vars:
            if not getattr(self.settings, var, None):
                errors.append(f"Missing required environment variable: {var.upper()}")

        # Check if field mappings are loaded
        if not self.field_mappings:
            errors.append("No field mappings loaded. Check field_mappings.yml file.")

        # Check GraphQL queries directory
        queries_path = Path(self.settings.queries_dir)
        if not queries_path.exists():
            errors.append(f"GraphQL queries directory not found: {queries_path}")

        return errors


# Global configuration instance
config = ConfigManager()


def get_config() -> ConfigManager:
    """Get the global configuration instance."""
    return config


def get_settings() -> Settings:
    """Get the application settings."""
    return config.settings
