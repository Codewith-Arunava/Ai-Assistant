"""Base exception classes for the Gubluu application.

GubluuError is the root of all application-specific exceptions.
All subsystems should define their own exceptions inheriting from
the appropriate base class in this hierarchy.
"""

from __future__ import annotations

from typing import Any


class GubluuError(Exception):
    """Root exception for all Gubluu application errors.

    All application-specific exceptions must inherit from this class.
    This enables catching all Gubluu errors with a single except clause
    while allowing infrastructure or framework errors to propagate separately.

    Attributes:
        message: Human-readable error description.
        context: Additional structured context for logging and debugging.
    """

    def __init__(
        self,
        message: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.context = context or {}
        super().__init__(message)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        if self.context:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{class_name}({self.message!r}, context={{{ctx}}})"
        return f"{class_name}({self.message!r})"


class ConfigurationError(GubluuError):
    """Raised when application configuration is invalid or missing.

    Examples:
        - Missing required configuration key
        - Invalid configuration value
        - Configuration file not found
    """

    def __init__(
        self,
        message: str,
        *,
        key: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        ctx = context or {}
        if key:
            ctx["config_key"] = key
        super().__init__(message, context=ctx)
        self.key = key
