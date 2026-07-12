"""Shared enumerations used across bounded contexts.

Only enums that are referenced by two or more domains belong here.
Domain-specific enums should live in their own domain's value_objects.py.
"""

from __future__ import annotations

from enum import StrEnum, auto


class Language(StrEnum):
    """Supported languages for conversation and voice.

    Gubluu supports English, Bengali, and mixed code-switching.
    """

    ENGLISH = auto()
    BENGALI = auto()
    MIXED = auto()  # Code-switched English + Bengali


class RiskLevel(StrEnum):
    """Risk classification for actions requiring permission checks.

    Determines the confirmation behavior in the security permission gate.
    See security module for the full permission flow.
    """

    SAFE = auto()  # Auto-execute, no confirmation needed
    MODERATE = auto()  # Execute with notification
    SENSITIVE = auto()  # Requires explicit user confirmation
    CRITICAL = auto()  # Requires double confirmation with reason
