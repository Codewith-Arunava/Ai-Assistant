"""Strongly-typed identifiers for domain entities.

Using NewType creates distinct types at the type-checking level while
having zero runtime overhead. This prevents mixing up identifiers
(e.g., passing a ConversationId where a MessageId is expected).

Example:
    def get_message(message_id: MessageId) -> Message:
        ...

    # Type checker will catch this:
    conv_id = ConversationId("abc")
    get_message(conv_id)  # mypy error: expected MessageId, got ConversationId
"""

from __future__ import annotations

from typing import NewType

# Entity identifiers — each is a NewType wrapping str (UUID format at runtime)
ConversationId = NewType("ConversationId", str)
MessageId = NewType("MessageId", str)
MemoryId = NewType("MemoryId", str)
TaskId = NewType("TaskId", str)
UserId = NewType("UserId", str)
AgentId = NewType("AgentId", str)
PluginId = NewType("PluginId", str)
