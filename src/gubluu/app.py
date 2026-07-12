"""Gubluu application bootstrap and lifecycle management.

This module is responsible for:
- Initializing all subsystems in the correct order
- Wiring dependencies via the DI container
- Managing application lifecycle (startup, running, shutdown)
- Coordinating graceful shutdown on signals

This is NOT the entry point. See __main__.py for CLI handling.
The entry point calls into this module after parsing arguments.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum, auto

from gubluu.core.config import get_settings
from gubluu.core.logging import configure_logging, get_logger


class AppState(Enum):
    """Application lifecycle states."""

    CREATED = auto()
    INITIALIZING = auto()
    RUNNING = auto()
    SHUTTING_DOWN = auto()
    STOPPED = auto()


@dataclass
class GubluuApp:
    """Main application class managing the Gubluu lifecycle.

    Follows the application service pattern — this is the composition root
    that wires together all bounded contexts and manages their lifecycle.

    Usage:
        app = GubluuApp()
        await app.start()
        # ... app is running ...
        await app.stop()

    Attributes:
        state: Current application lifecycle state.
    """

    state: AppState = field(default=AppState.CREATED, init=False)
    _shutdown_event: asyncio.Event = field(default_factory=asyncio.Event, init=False)

    async def start(self) -> None:
        """Initialize all subsystems and start the application.

        Raises:
            RuntimeError: If the application is not in the CREATED state.
        """
        if self.state != AppState.CREATED:
            msg = f"Cannot start app in state {self.state.name}. Expected CREATED."
            raise RuntimeError(msg)

        self.state = AppState.INITIALIZING

        # Future milestones will add initialization steps here:
        # 1. Load configuration (M2)
        settings = get_settings()

        # 2. Initialize logging (M2)
        configure_logging(settings.logging)
        logger = get_logger("gubluu.app")
        logger.info(
            "Starting Gubluu application",
            version=settings.app.version,
            debug=settings.app.debug,
        )
        # 3. Wire DI container (M3)
        from gubluu.core.di import container
        from gubluu.core.events import EventBus
        container.wire()

        # 4. Set up event bus (M3)
        event_bus = container.resolve(EventBus)
        await event_bus.start()

        # 5. Initialize database (M12)
        # 6. Start scheduler (M28)
        # 7. Start voice pipeline (M11)
        # 8. Start UI (M29)

        self.state = AppState.RUNNING

    async def stop(self) -> None:
        """Gracefully shut down all subsystems.

        Ensures resources are released in reverse initialization order.
        """
        if self.state != AppState.RUNNING:
            return

        self.state = AppState.SHUTTING_DOWN

        # Future milestones will add shutdown steps here (reverse order):
        # 1. Stop UI
        # 2. Stop voice pipeline
        # 3. Stop scheduler
        # 4. Flush audit log
        
        from gubluu.core.di import container
        from gubluu.core.events import EventBus
        event_bus = container.resolve(EventBus)
        await event_bus.stop()

        self.state = AppState.STOPPED
        # 5. Close database connections
        # 6. Shut down event bus

        self._shutdown_event.set()
        self.state = AppState.STOPPED

    async def wait_for_shutdown(self) -> None:
        """Block until the application receives a shutdown signal."""
        await self._shutdown_event.wait()
