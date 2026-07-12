# Gubluu — Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0-alpha.1] — 2026-07-12

### Added
  
- Project scaffold with hexagonal architecture
- `pyproject.toml` with Hatch build system, Ruff, mypy, pytest configuration
- Core error hierarchy: `GubluuError`, domain errors, infrastructure errors
- Shared types: `NewType` identifiers, `Language` and `RiskLevel` enums, `Repository` and `UseCase` protocols
- Application lifecycle manager (`GubluuApp`) with state machine
- CLI entry point with `--version` and `info` commands
- Default TOML configuration
- Development setup script (`scripts/setup.ps1`)
- Unit tests for errors, types, app lifecycle, and smoke tests
- VS Code configuration (settings, launch, extensions)
- Architecture Decision Record: ADR-001 (Hexagonal Architecture)
- Module stubs for all 12 bounded contexts
