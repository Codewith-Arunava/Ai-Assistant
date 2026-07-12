"""Tests for the GubluuApp lifecycle.

Verifies:
- Application state transitions
- Start/stop lifecycle
- Cannot start from invalid states
"""

from __future__ import annotations

import pytest

from gubluu.app import AppState, GubluuApp


class TestAppLifecycle:
    """Tests for GubluuApp state machine."""

    @pytest.mark.asyncio
    async def test_should_start_in_created_state(self):
        app = GubluuApp()
        assert app.state == AppState.CREATED

    @pytest.mark.asyncio
    async def test_should_transition_to_running_on_start(self):
        app = GubluuApp()
        await app.start()
        assert app.state == AppState.RUNNING

    @pytest.mark.asyncio
    async def test_should_transition_to_stopped_on_stop(self):
        app = GubluuApp()
        await app.start()
        await app.stop()
        assert app.state == AppState.STOPPED

    @pytest.mark.asyncio
    async def test_should_raise_error_if_started_twice(self):
        app = GubluuApp()
        await app.start()
        with pytest.raises(RuntimeError, match="Cannot start app"):
            await app.start()

    @pytest.mark.asyncio
    async def test_stop_should_be_idempotent_when_not_running(self):
        """Stopping an app that isn't running should be a no-op."""
        app = GubluuApp()
        await app.stop()  # Should not raise
        assert app.state == AppState.CREATED

    @pytest.mark.asyncio
    async def test_shutdown_event_should_be_set_on_stop(self):
        app = GubluuApp()
        await app.start()
        assert not app._shutdown_event.is_set()  # noqa: SLF001
        await app.stop()
        assert app._shutdown_event.is_set()  # noqa: SLF001


class TestAppState:
    """Tests for the AppState enum."""

    def test_should_have_five_states(self):
        assert len(AppState) == 5

    def test_state_names(self):
        states = [s.name for s in AppState]
        assert "CREATED" in states
        assert "INITIALIZING" in states
        assert "RUNNING" in states
        assert "SHUTTING_DOWN" in states
        assert "STOPPED" in states
