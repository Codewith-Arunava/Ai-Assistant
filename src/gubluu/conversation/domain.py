"""Conversation Domain.

Contains pure business logic, entities, and port definitions for the conversation context.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from gubluu.core.types import ConversationId, MessageId


class Role(str, Enum):
    """The role of the message author."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """A single message in a conversation."""
    content: str
    role: Role
    id: MessageId = field(default_factory=lambda: MessageId("msg_" + str(datetime.now(timezone.utc).timestamp())))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Conversation:
    """An ongoing conversation entity."""
    id: ConversationId
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)


class LLMPort(abc.ABC):
    """Port for Language Model providers.
    
    Infrastructure layer must implement this adapter.
    """

    @abc.abstractmethod
    async def generate_response(self, conversation: Conversation) -> Message:
        """Generate a response given the conversation history.
        
        Args:
            conversation: The ongoing conversation.
            
        Returns:
            The generated assistant message.
        """
        pass
