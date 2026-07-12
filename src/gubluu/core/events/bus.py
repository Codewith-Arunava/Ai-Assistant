"""Asynchronous Event Bus implementation."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, List, Type, TypeVar

from gubluu.core.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True, kw_only=True)
class Event:
    """Base class for all domain events."""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


TEvent = TypeVar("TEvent", bound=Event)
EventHandler = Callable[[TEvent], Awaitable[None]]


class EventBus:
    """Publish-subscribe event bus for inter-module communication."""

    def __init__(self) -> None:
        """Initialize the event bus."""
        self._subscribers: Dict[Type[Event], List[EventHandler[Any]]] = defaultdict(list)
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._task: asyncio.Task[None] | None = None

    def subscribe(self, event_type: Type[TEvent], handler: EventHandler[TEvent]) -> None:
        """Subscribe a handler to a specific event type.

        Args:
            event_type: The class of the event to subscribe to.
            handler: Async callback function that takes the event as its argument.
        """
        self._subscribers[event_type].append(handler)
        logger.debug("Subscribed handler to event", event_type=event_type.__name__, handler=handler.__name__)

    async def publish(self, event: Event) -> None:
        """Publish an event to be processed asynchronously.

        Args:
            event: The event instance to publish.
        """
        await self._queue.put(event)
        logger.debug("Event queued", event_type=type(event).__name__)

    async def start(self) -> None:
        """Start the event processing loop."""
        if self._task is not None:
            return
        
        self._task = asyncio.create_task(self._process_events())
        logger.info("Event Bus started")

    async def stop(self) -> None:
        """Stop the event processing loop."""
        if self._task is None:
            return

        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None
        logger.info("Event Bus stopped")

    async def _process_events(self) -> None:
        """Background loop to process events from the queue."""
        while True:
            event = await self._queue.get()
            event_type = type(event)
            handlers = self._subscribers.get(event_type, [])

            if not handlers:
                logger.debug("No handlers for event", event_type=event_type.__name__)
                self._queue.task_done()
                continue

            for handler in handlers:
                try:
                    await handler(event)
                except Exception as e:
                    logger.exception("Error in event handler", event_type=event_type.__name__, error=str(e))
            
            self._queue.task_done()
