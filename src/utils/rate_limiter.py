"""
Rate limiter utilities for API services.
Handles rate limiting for GitHub and Notion APIs.
"""

import functools
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from threading import Lock
from typing import Any

from src.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Generic rate limiter implementation."""

    def __init__(self, requests_per_second: float = 1.0, burst_size: int | None = None):
        """Initialize rate limiter.

        Args:
            requests_per_second: Maximum requests per second
            burst_size: Maximum burst size (defaults to requests_per_second)
        """
        self.requests_per_second = requests_per_second
        self.burst_size = burst_size or max(1, int(requests_per_second))
        self.tokens = self.burst_size
        self.last_update = time.time()
        self.lock = Lock()

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a token for making a request.

        Args:
            timeout: Maximum time to wait for a token

        Returns:
            True if token acquired, False if timeout
        """
        start_time = time.time()

        while True:
            with self.lock:
                now = time.time()
                time_passed = now - self.last_update

                # Add tokens based on time passed
                self.tokens = min(self.burst_size, self.tokens + time_passed * self.requests_per_second)
                self.last_update = now

                # Check if we can consume a token
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True

            # Check timeout
            if timeout and (time.time() - start_time) >= timeout:
                return False

            # Wait before trying again
            time.sleep(0.01)

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with rate limiting.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        self.acquire()
        return func(*args, **kwargs)


class NotionRateLimiter(RateLimiter):
    """Rate limiter specifically for Notion API."""

    def __init__(self, requests_per_second: float = 3.0):
        """Initialize Notion rate limiter.

        Args:
            requests_per_second: Requests per second (Notion limit is ~3/sec)
        """
        super().__init__(requests_per_second, burst_size=10)
        self.retry_count = 0
        self.max_retries = 3

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with Notion-specific rate limiting and retry logic.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        from notion_client.errors import APIResponseError

        for attempt in range(self.max_retries + 1):
            try:
                # Wait for rate limit
                self.acquire()

                # Execute function
                result = func(*args, **kwargs)

                # Reset retry count on success
                self.retry_count = 0
                return result

            except APIResponseError as e:
                if e.code == "rate_limited":
                    # Handle rate limit with exponential backoff
                    retry_after = 1
                    if hasattr(e, "headers") and e.headers:
                        retry_after = int(e.headers.get("Retry-After", 1))

                    wait_time = retry_after * (2**attempt)
                    logger.warning(f"Notion rate limited, waiting {wait_time}s (attempt {attempt + 1})")

                    time.sleep(wait_time)

                    if attempt == self.max_retries:
                        raise
                else:
                    # Re-raise non-rate-limit errors
                    raise
            except Exception:
                # Re-raise other exceptions
                raise
        return None


class GitHubRateLimiter(RateLimiter):
    """Rate limiter specifically for GitHub API."""

    def __init__(self, requests_per_hour: int = 5000):
        """Initialize GitHub rate limiter.

        Args:
            requests_per_hour: Requests per hour (GitHub limit)
        """
        requests_per_second = requests_per_hour / 3600.0
        super().__init__(requests_per_second, burst_size=50)
        self.requests_per_hour = requests_per_hour
        self.hourly_requests = 0
        self.hour_start = datetime.now()

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a token with hourly limit checking.

        Args:
            timeout: Maximum time to wait for a token

        Returns:
            True if token acquired, False if timeout
        """
        with self.lock:
            now = datetime.now()

            # Reset hourly counter if hour has passed
            if now - self.hour_start >= timedelta(hours=1):
                self.hourly_requests = 0
                self.hour_start = now

            # Check hourly limit
            if self.hourly_requests >= self.requests_per_hour:
                wait_time = 3600 - (now - self.hour_start).total_seconds()
                if wait_time > 0:
                    logger.warning(f"GitHub hourly rate limit reached, waiting {wait_time:.0f}s")
                    if timeout and wait_time > timeout:
                        return False
                    time.sleep(wait_time)
                    self.hourly_requests = 0
                    self.hour_start = datetime.now()

        # Use parent token bucket logic
        if super().acquire(timeout):
            with self.lock:
                self.hourly_requests += 1
            return True

        return False

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with GitHub-specific rate limiting.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result
        """
        from src.models.github_models import GitHubRateLimitError

        try:
            # Wait for rate limit
            if not self.acquire(timeout=30):
                raise GitHubRateLimitError("GitHub rate limit acquisition timeout")

            # Execute function
            return func(*args, **kwargs)

        except GitHubRateLimitError as e:
            # Handle GitHub rate limit errors
            if e.reset_at:
                wait_time = (e.reset_at - datetime.utcnow()).total_seconds()
                if wait_time > 0:
                    logger.warning(f"GitHub rate limited, waiting {wait_time:.0f}s")
                    time.sleep(wait_time)
                    # Retry once after waiting
                    return func(*args, **kwargs)
            raise


def rate_limit(requests_per_second: float = 1.0, burst_size: int | None = None):
    """Decorator for rate limiting function calls.

    Args:
        requests_per_second: Maximum requests per second
        burst_size: Maximum burst size

    Returns:
        Decorated function
    """
    limiter = RateLimiter(requests_per_second, burst_size)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return limiter.execute(func, *args, **kwargs)

        return wrapper

    return decorator


def notion_rate_limit(requests_per_second: float = 3.0):
    """Decorator for Notion API rate limiting.

    Args:
        requests_per_second: Maximum requests per second

    Returns:
        Decorated function
    """
    limiter = NotionRateLimiter(requests_per_second)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return limiter.execute(func, *args, **kwargs)

        return wrapper

    return decorator


def github_rate_limit(requests_per_hour: int = 5000):
    """Decorator for GitHub API rate limiting.

    Args:
        requests_per_hour: Maximum requests per hour

    Returns:
        Decorated function
    """
    limiter = GitHubRateLimiter(requests_per_hour)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return limiter.execute(func, *args, **kwargs)

        return wrapper

    return decorator
