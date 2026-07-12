"""Smoke tests for the Gubluu package.

These tests verify that the package is importable and
the basic entry point works correctly.
"""

from __future__ import annotations

import subprocess
import sys


class TestPackageImport:
    """Verify the package is importable."""

    def test_should_import_gubluu(self):
        import gubluu

        assert gubluu.__app_name__ == "Gubluu"

    def test_should_have_version(self):
        import gubluu

        assert gubluu.__version__
        assert "." in gubluu.__version__

    def test_should_import_core_errors(self):
        from gubluu.core.errors import GubluuError

        assert issubclass(GubluuError, Exception)

    def test_should_import_core_types(self):
        from gubluu.core.types import ConversationId, Language, RiskLevel

        assert ConversationId is not None
        assert Language is not None
        assert RiskLevel is not None


class TestEntryPoint:
    """Verify the CLI entry point works."""

    def test_version_flag(self):
        result = subprocess.run(
            [sys.executable, "-m", "gubluu", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Gubluu" in result.stdout
        assert "1.0.0" in result.stdout

    def test_info_command(self):
        result = subprocess.run(
            [sys.executable, "-m", "gubluu", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Gubluu" in result.stdout
        assert "Python" in result.stdout
