"""Dependency injection container for Gubluu.

Uses the dependency-injector library to wire all ports
to their infrastructure implementations at application startup.

Full implementation in Milestone 3.
"""

from gubluu.core.di.container import DIContainer, container

__all__ = ["DIContainer", "container"]
