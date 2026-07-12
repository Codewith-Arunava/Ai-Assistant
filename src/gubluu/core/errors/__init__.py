"""Base error hierarchy for the Gubluu application.

All Gubluu exceptions inherit from GubluuError, enabling:
- Consistent error handling across the application
- Structured error context for logging
- Clean separation between domain and infrastructure errors

Exception hierarchy:
    GubluuError
    ├── DomainError (business rule violations)
    │   ├── EntityNotFoundError
    │   ├── ValidationError
    │   └── BusinessRuleViolationError
    ├── InfrastructureError (external system failures)
    │   ├── DatabaseError
    │   ├── ExternalServiceError
    │   └── FileSystemError
    ├── SecurityError (permission/security violations)
    │   ├── PermissionDeniedError
    │   └── ActionBlockedError
    └── ConfigurationError (configuration issues)
"""

from gubluu.core.errors.base import (
    ConfigurationError,
    GubluuError,
)
from gubluu.core.errors.domain import (
    BusinessRuleViolationError,
    DomainError,
    EntityNotFoundError,
    ValidationError,
)
from gubluu.core.errors.infrastructure import (
    DatabaseError,
    ExternalServiceError,
    FileSystemError,
    InfrastructureError,
)

__all__ = [
    "BusinessRuleViolationError",
    "ConfigurationError",
    "DatabaseError",
    "DomainError",
    "EntityNotFoundError",
    "ExternalServiceError",
    "FileSystemError",
    "GubluuError",
    "InfrastructureError",
    "ValidationError",
]
