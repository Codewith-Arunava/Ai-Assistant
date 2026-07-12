"""Async event bus for inter-module communication.

Implements publish/subscribe pattern for domain events.
Modules communicate through events instead of direct imports,
ensuring loose coupling between bounded contexts.

Full implementation in Milestone 3.
"""

from gubluu.core.events.bus import Event, EventBus

__all__ = ["Event", "EventBus"]
