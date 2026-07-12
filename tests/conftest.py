"""Shared test fixtures for the Gubluu test suite.

This conftest.py is the root-level test configuration. It provides:
- Shared fixtures available to all tests
- Test markers configuration
- Common test utilities

Test organization:
    tests/
    ├── conftest.py          ← You are here (shared fixtures)
    ├── unit/                ← Fast, isolated, all deps mocked
    ├── integration/         ← Real DB, mocked APIs
    └── e2e/                 ← Full pipeline tests
"""

from __future__ import annotations

import pytest


@pytest.fixture
def app_name() -> str:
    """Provide the application name for tests."""
    return "Gubluu"


@pytest.fixture
def app_version() -> str:
    """Provide the current application version for tests."""
    return "1.0.0-alpha.1"
