"""
Logging utility for GitHub to Notion sync system.
Provides structured logging with JSON format support for production environments.
"""

import json
import logging
import sys
from datetime import datetime
from typing import ClassVar


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        # Create base log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields from record
        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "stack_info",
                "exc_info",
                "exc_text",
            }
        }

        if extra_fields:
            log_entry.update(extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add stack info if present
        if record.stack_info:
            log_entry["stack_info"] = self.formatStack(record.stack_info)

        # Add source location in debug mode
        if record.levelno <= logging.DEBUG:
            log_entry["source"] = {"file": record.filename, "line": record.lineno, "function": record.funcName}

        return json.dumps(log_entry, ensure_ascii=False, separators=(",", ":"))


class TextFormatter(logging.Formatter):
    """Enhanced text formatter with colors and structured output."""

    # Color codes for different log levels
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET: ClassVar[str] = "\033[0m"

    def __init__(self, use_colors: bool = True):
        """Initialize text formatter.

        Args:
            use_colors: Whether to use ANSI color codes
        """
        super().__init__()
        self.use_colors = use_colors and sys.stderr.isatty()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as colored text."""
        # Create timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        # Get color for log level
        color = self.COLORS.get(record.levelname, "") if self.use_colors else ""
        reset = self.RESET if self.use_colors else ""

        # Format base message
        message = f"{timestamp} {color}[{record.levelname:8}]{reset} {record.name}: {record.getMessage()}"

        # Add extra fields if present
        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "stack_info",
                "exc_info",
                "exc_text",
            }
        }

        if extra_fields:
            extra_str = " | ".join(f"{k}={v}" for k, v in extra_fields.items())
            message += f" | {extra_str}"

        # Add exception info if present
        if record.exc_info:
            message += "\n" + self.formatException(record.exc_info)

        return message


class LoggerManager:
    """Manages application logging configuration and provides structured logging helpers."""

    def __init__(self, log_level: str = "INFO", log_format: str = "json"):
        """Initialize logger manager.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_format: Log format ('json' or 'text')
        """
        self.log_level = getattr(logging, log_level.upper())
        self.log_format = log_format.lower()
        self._configured = False

        # Configure logging
        self._configure_logging()

    def _configure_logging(self):
        """Configure root logger and handlers."""
        if self._configured:
            return

        # Clear any existing handlers
        logging.getLogger().handlers.clear()

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)

        # Set formatter based on format preference
        formatter = JSONFormatter() if self.log_format == "json" else TextFormatter()

        console_handler.setFormatter(formatter)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        root_logger.addHandler(console_handler)

        # Set specific logger levels
        logging.getLogger("notion_client").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        self._configured = True

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance with the specified name.

        Args:
            name: Logger name (usually __name__)

        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)

    def log_api_call(
        self,
        logger: logging.Logger,
        service: str,
        method: str,
        url: str,
        status_code: int | None = None,
        duration: float | None = None,
        **kwargs,
    ):
        """Log API call with structured data.

        Args:
            logger: Logger instance
            service: Service name (e.g., 'github', 'notion')
            method: HTTP method
            url: API endpoint URL
            status_code: HTTP status code
            duration: Request duration in seconds
            **kwargs: Additional fields to log
        """
        log_data = {"service": service, "method": method, "url": url, "api_call": True, **kwargs}

        if status_code is not None:
            log_data["status_code"] = status_code

        if duration is not None:
            log_data["duration_ms"] = round(duration * 1000, 2)

        # Determine log level based on status code
        if status_code is None:
            logger.info("API call started", extra=log_data)
        elif 200 <= status_code < 300:
            logger.info("API call successful", extra=log_data)
        elif 400 <= status_code < 500:
            logger.warning("API call client error", extra=log_data)
        else:
            logger.error("API call server error", extra=log_data)

    def log_sync_event(
        self,
        logger: logging.Logger,
        event_type: str,
        item_id: str,
        action: str,
        success: bool = True,
        error: str | None = None,
        **kwargs,
    ):
        """Log sync event with structured data.

        Args:
            logger: Logger instance
            event_type: Type of sync event ('webhook', 'full_sync', 'manual')
            item_id: GitHub item ID or Notion page ID
            action: Action performed ('create', 'update', 'delete')
            success: Whether the sync was successful
            error: Error message if sync failed
            **kwargs: Additional fields to log
        """
        log_data = {
            "event_type": event_type,
            "item_id": item_id,
            "action": action,
            "success": success,
            "sync_event": True,
            **kwargs,
        }

        if error:
            log_data["error"] = error

        if success:
            logger.info("Sync event completed", extra=log_data)
        else:
            logger.error("Sync event failed", extra=log_data)

    def log_rate_limit(self, logger: logging.Logger, service: str, remaining: int, reset_time: datetime | None = None):
        """Log rate limit information.

        Args:
            logger: Logger instance
            service: Service name
            remaining: Remaining requests
            reset_time: When rate limit resets
        """
        log_data = {"service": service, "remaining_requests": remaining, "rate_limit_info": True}

        if reset_time:
            log_data["reset_time"] = reset_time.isoformat()

        if remaining <= 10:
            logger.warning("Rate limit approaching", extra=log_data)
        else:
            logger.debug("Rate limit status", extra=log_data)

    def log_webhook_event(
        self,
        logger: logging.Logger,
        event_type: str,
        action: str,
        item_id: str | None = None,
        repository: str | None = None,
        **kwargs,
    ):
        """Log webhook event with structured data.

        Args:
            logger: Logger instance
            event_type: GitHub webhook event type
            action: Webhook action
            item_id: GitHub item ID
            repository: Repository name
            **kwargs: Additional fields to log
        """
        log_data = {"event_type": event_type, "action": action, "webhook_event": True, **kwargs}

        if item_id:
            log_data["item_id"] = item_id

        if repository:
            log_data["repository"] = repository

        logger.info("Webhook event received", extra=log_data)


# Global logger manager instance
_logger_manager: LoggerManager | None = None


def init_logging(log_level: str = "INFO", log_format: str = "json") -> LoggerManager:
    """Initialize global logging configuration.

    Args:
        log_level: Logging level
        log_format: Log format ('json' or 'text')

    Returns:
        LoggerManager instance
    """
    global _logger_manager
    _logger_manager = LoggerManager(log_level, log_format)
    return _logger_manager


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    if _logger_manager is None:
        init_logging()
    return _logger_manager.get_logger(name)


def get_logger_manager() -> LoggerManager:
    """Get the global logger manager instance.

    Returns:
        LoggerManager instance
    """
    if _logger_manager is None:
        init_logging()
    return _logger_manager
