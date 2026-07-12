"""Core shared kernel for the Gubluu application.

The core module contains cross-cutting concerns shared by all bounded contexts:
- Configuration management
- Event bus
- Structured logging
- Dependency injection
- Error hierarchy
- Shared types and protocols
- Utility functions

All other modules may depend on core. Core depends on nothing else within Gubluu.
"""
