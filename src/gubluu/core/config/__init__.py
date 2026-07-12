"""Configuration management for Gubluu.

Loads TOML configuration files, merges environment-specific overrides,
and exposes typed Pydantic Settings models.
"""

from gubluu.core.config.loader import get_settings
from gubluu.core.config.models import (
    AppSettings,
    GubluuSettings,
    LoggingSettings,
    PersonalitySettings,
)

__all__ = [
    "AppSettings",
    "GubluuSettings",
    "LoggingSettings",
    "PersonalitySettings",
    "get_settings",
]
