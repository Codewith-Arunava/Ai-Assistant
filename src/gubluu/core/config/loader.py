"""Configuration loading and merging logic."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from gubluu.core.config.models import GubluuSettings


def _merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionaries. dict2 overrides dict1."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def _load_toml_if_exists(path: Path) -> dict[str, Any]:
    """Load a TOML file if it exists, otherwise return an empty dict."""
    if not path.is_file():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def get_settings() -> GubluuSettings:
    """Load and merge all configuration sources.

    Order of precedence (highest to lowest):
    1. Environment variables (GUBLUU_*) and .env file
    2. Environment-specific TOML (e.g., development.toml)
    3. default.toml
    4. Pydantic model defaults
    """
    # Assuming config is relative to the current working directory for now
    config_dir = Path("config")

    # Load default config
    default_config = _load_toml_if_exists(config_dir / "default.toml")

    # Determine environment and load specific overrides
    env = os.getenv("GUBLUU_ENV", "development").lower()
    env_config = _load_toml_if_exists(config_dir / f"{env}.toml")

    # Merge configs
    merged_config = _merge_dicts(default_config, env_config)

    # Create settings object
    return GubluuSettings(**merged_config)
