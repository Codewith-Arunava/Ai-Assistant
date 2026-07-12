"""Structured logging for Gubluu.

Configures structlog with JSON output for production and
colored console output for development. Supports contextual
logging with bound loggers.
"""

from gubluu.core.logging.setup import configure_logging, get_logger

__all__ = [
    "configure_logging",
    "get_logger",
]
