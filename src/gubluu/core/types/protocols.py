"""Shared protocols (interfaces) used across bounded contexts.

Protocols define structural contracts that adapters must implement.
Using Protocol instead of ABC allows structural subtyping — implementations
don't need to explicitly inherit from the protocol, they just need to
have matching method signatures.

Only protocols shared by multiple domains belong here.
Domain-specific ports should live in their own domain's ports.py.
"""

from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
IdT = TypeVar("IdT", contravariant=True)


@runtime_checkable
class Repository(Protocol[T, IdT]):
    """Generic repository protocol for CRUD operations.

    This defines the minimal contract for any entity repository.
    Domain-specific repositories extend this with additional query methods.

    Type Parameters:
        T: The entity type managed by this repository.
        IdT: The identifier type for the entity.
    """

    async def get_by_id(self, entity_id: IdT) -> T | None:
        """Retrieve an entity by its unique identifier.

        Args:
            entity_id: The entity's unique identifier.

        Returns:
            The entity if found, None otherwise.
        """
        ...

    async def save(self, entity: T) -> None:
        """Persist an entity (insert or update).

        Args:
            entity: The entity to persist.
        """
        ...

    async def delete(self, entity_id: IdT) -> bool:
        """Delete an entity by its identifier.

        Args:
            entity_id: The entity's unique identifier.

        Returns:
            True if the entity was deleted, False if not found.
        """
        ...


@runtime_checkable
class UseCase(Protocol):
    """Protocol for application use cases.

    Use cases represent single application operations. They orchestrate
    domain entities and ports to fulfill a user request.

    Every use case must implement an async execute method.
    The input/output types vary per use case, so this protocol
    uses Any — concrete use cases should define specific signatures.
    """

    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the use case.

        Args:
            *args: Use case-specific positional arguments.
            **kwargs: Use case-specific keyword arguments.

        Returns:
            Use case-specific result.
        """
        ...
