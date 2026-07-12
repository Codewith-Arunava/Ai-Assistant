"""Tests for shared types: identifiers, enums, and protocols.

Verifies:
- NewType identifiers maintain type identity
- Enums have correct values and are StrEnum
- Protocols are runtime-checkable
"""

from __future__ import annotations

from gubluu.core.types import (
    AgentId,
    ConversationId,
    Language,
    MemoryId,
    MessageId,
    PluginId,
    RiskLevel,
    TaskId,
    UserId,
)


class TestIdentifiers:
    """Tests for NewType identifiers."""

    def test_conversation_id_is_string(self):
        cid = ConversationId("conv-001")
        assert isinstance(cid, str)
        assert cid == "conv-001"

    def test_message_id_is_string(self):
        mid = MessageId("msg-001")
        assert isinstance(mid, str)

    def test_all_identifier_types_are_strings(self):
        """All NewType identifiers should be usable as strings at runtime."""
        ids = [
            ConversationId("c"),
            MessageId("m"),
            MemoryId("mem"),
            TaskId("t"),
            UserId("u"),
            AgentId("a"),
            PluginId("p"),
        ]
        for id_val in ids:
            assert isinstance(id_val, str)


class TestLanguageEnum:
    """Tests for the Language enum."""

    def test_should_have_three_values(self):
        assert len(Language) == 3

    def test_values(self):
        assert Language.ENGLISH == "english"
        assert Language.BENGALI == "bengali"
        assert Language.MIXED == "mixed"

    def test_is_str_enum(self):
        """Language values should be usable as strings (for JSON serialization)."""
        assert isinstance(Language.ENGLISH, str)


class TestRiskLevelEnum:
    """Tests for the RiskLevel enum."""

    def test_should_have_four_levels(self):
        assert len(RiskLevel) == 4

    def test_ordering(self):
        """Risk levels should be ordered from safe to critical."""
        levels = list(RiskLevel)
        assert levels[0] == RiskLevel.SAFE
        assert levels[1] == RiskLevel.MODERATE
        assert levels[2] == RiskLevel.SENSITIVE
        assert levels[3] == RiskLevel.CRITICAL

    def test_values(self):
        assert RiskLevel.SAFE == "safe"
        assert RiskLevel.MODERATE == "moderate"
        assert RiskLevel.SENSITIVE == "sensitive"
        assert RiskLevel.CRITICAL == "critical"

    def test_is_str_enum(self):
        assert isinstance(RiskLevel.SAFE, str)
