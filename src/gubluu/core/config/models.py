"""Pydantic models representing the application configuration."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PersonalitySettings(BaseModel):
    """Configuration for Gubluu's personality."""

    name: str = "Gubluu"
    default_language: str = "english"
    tone: str = "friendly"


class AppSettings(BaseModel):
    """Core application settings."""

    name: str = "Gubluu"
    version: str = "1.0.0-alpha.1"
    debug: bool = False
    data_dir: Path = Field(default_factory=lambda: Path("data"))
    personality: PersonalitySettings = Field(default_factory=PersonalitySettings)


class LoggingSettings(BaseModel):
    """Logging subsystem configuration."""

    level: str = "INFO"
    format: str = "console"
    file_enabled: bool = True
    file_path: Path = Field(default_factory=lambda: Path("data/logs/gubluu.log"))
    max_file_size_mb: int = 10
    backup_count: int = 5


class LLMSettings(BaseModel):
    """Configuration for LLM providers."""
    
    provider: str = "ollama"  # Defaulting to ollama as per user request
    gemini_api_key: str | None = None
    model_name: str = "gemini-2.5-flash"
    ollama_model_name: str = "llama3"


class GubluuSettings(BaseSettings):
    """Root configuration object for the Gubluu application.

    Loads configuration in this order:
    1. Default values (from these models and default.toml)
    2. Overrides from development.toml or production.toml
    3. Environment variables (prefix GUBLUU_, nested delimiter __)
    """

    app: AppSettings = Field(default_factory=AppSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)

    model_config = SettingsConfigDict(
        env_prefix="GUBLUU_",
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )
