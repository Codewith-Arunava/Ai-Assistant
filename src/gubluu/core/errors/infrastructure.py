"""Infrastructure-layer exceptions.

These exceptions represent failures in external systems and infrastructure
components: databases, APIs, file systems, network calls, etc.

Infrastructure errors are always caused by something outside the domain —
they indicate that an adapter failed to fulfill its port contract.
"""

from __future__ import annotations

from typing import Any

from gubluu.core.errors.base import GubluuError


class InfrastructureError(GubluuError):
    """Base class for all infrastructure-layer exceptions.

    Raised when an external system or resource fails.
    Adapters should catch low-level exceptions (e.g., sqlite3.Error)
    and re-raise them as InfrastructureError subclasses.
    """


class DatabaseError(InfrastructureError):
    """Raised when a database operation fails.

    Attributes:
        operation: The database operation that failed (e.g., "insert", "query").
        table: The table involved, if applicable.
    """

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        table: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.operation = operation
        self.table = table
        ctx = context or {}
        if operation:
            ctx["db_operation"] = operation
        if table:
            ctx["db_table"] = table
        super().__init__(message, context=ctx)


class ExternalServiceError(InfrastructureError):
    """Raised when an external API or service call fails.

    Covers LLM API failures, TTS/STT service errors, web API errors, etc.

    Attributes:
        service_name: Name of the external service (e.g., "OpenAI", "Gemini").
        status_code: HTTP status code, if applicable.
    """

    def __init__(
        self,
        message: str,
        *,
        service_name: str,
        status_code: int | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.service_name = service_name
        self.status_code = status_code
        ctx = context or {}
        ctx["service_name"] = service_name
        if status_code is not None:
            ctx["status_code"] = status_code
        super().__init__(message, context=ctx)


class FileSystemError(InfrastructureError):
    """Raised when a file system operation fails.

    Attributes:
        path: The file or directory path involved.
        operation: The operation that failed (e.g., "read", "write", "delete").
    """

    def __init__(
        self,
        message: str,
        *,
        path: str | None = None,
        operation: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.path = path
        self.operation = operation
        ctx = context or {}
        if path:
            ctx["path"] = path
        if operation:
            ctx["fs_operation"] = operation
        super().__init__(message, context=ctx)
