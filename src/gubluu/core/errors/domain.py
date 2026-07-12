"""Domain-layer exceptions.

These exceptions represent business rule violations and domain-level errors.
They should be raised by domain services and entities when domain invariants
are violated.

Domain errors are distinct from infrastructure errors — they indicate
problems with business logic, not with external systems.
"""

from __future__ import annotations

from typing import Any

from gubluu.core.errors.base import GubluuError


class DomainError(GubluuError):
    """Base class for all domain-layer exceptions.

    Raised when a domain invariant is violated or a business rule
    cannot be satisfied.
    """


class EntityNotFoundError(DomainError):
    """Raised when a requested entity does not exist.

    Attributes:
        entity_type: The type/name of the entity that was not found.
        entity_id: The identifier used in the lookup.
    """

    def __init__(
        self,
        entity_type: str,
        entity_id: str,
        *,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        ctx = context or {}
        ctx.update({"entity_type": entity_type, "entity_id": entity_id})
        super().__init__(
            f"{entity_type} with id '{entity_id}' not found",
            context=ctx,
        )


class ValidationError(DomainError):
    """Raised when input validation fails at the domain level.

    Distinct from Pydantic's ValidationError — this is for domain-specific
    validation rules (e.g., "conversation cannot have zero messages").

    Attributes:
        field: The field that failed validation, if applicable.
        value: The invalid value, if safe to include.
    """

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        value: Any = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.field = field
        self.value = value
        ctx = context or {}
        if field:
            ctx["field"] = field
        super().__init__(message, context=ctx)


class BusinessRuleViolationError(DomainError):
    """Raised when a business rule is violated.

    Use this for domain rules that don't fit into validation or entity-not-found
    categories. For example: "Cannot delete a conversation that is currently active."

    Attributes:
        rule: A short identifier for the violated rule.
    """

    def __init__(
        self,
        message: str,
        *,
        rule: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.rule = rule
        ctx = context or {}
        ctx["rule"] = rule
        super().__init__(message, context=ctx)
