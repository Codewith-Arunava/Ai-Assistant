"""Dependency Injection Container."""

from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

from gubluu.core.config import get_settings
from gubluu.core.events.bus import EventBus
from gubluu.core.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class DIContainer:
    """Simple Dependency Injection Container.
    
    Manages singleton instances and wires dependencies together.
    """

    def __init__(self) -> None:
        self._services: Dict[Type[Any], Any] = {}
        self._is_wired = False

    def register(self, interface: Type[T], implementation: T) -> None:
        """Register a singleton implementation for an interface."""
        self._services[interface] = implementation
        logger.debug("Registered service", interface=interface.__name__)

    def resolve(self, interface: Type[T]) -> T:
        """Resolve a dependency by its interface."""
        if interface not in self._services:
            msg = f"Service {interface.__name__} not found in DI container"
            raise KeyError(msg)
        return self._services[interface]

    def wire(self) -> None:
        """Wire all dependencies together.
        
        This is called once at application startup.
        """
        if self._is_wired:
            return

        logger.info("Wiring DI container")
        
        # Register core infrastructure
        settings = get_settings()
        event_bus = EventBus()

        # (EventBus is its own interface for simplicity)
        self.register(EventBus, event_bus)

        self._is_wired = True


# Global container instance
container = DIContainer()
