"""Conversation domain — LLM integration, personality, and chat management.

Bounded context responsible for:
- LLM provider abstraction (OpenAI, Gemini, Ollama)
- Conversation lifecycle management
- Prompt engineering and personality system
- Bengali/English/mixed language handling
- Streaming response generation

Implementation begins in Milestone 4 (M4).
"""

from gubluu.conversation.application import ChatUseCase, MessageGeneratedEvent
from gubluu.conversation.domain import Conversation, LLMPort, Message, Role
from gubluu.conversation.infrastructure import EchoLLMAdapter, GeminiLLMAdapter, OllamaLLMAdapter

__all__ = [
    "ChatUseCase",
    "MessageGeneratedEvent",
    "Conversation",
    "LLMPort",
    "Message",
    "Role",
    "EchoLLMAdapter",
    "GeminiLLMAdapter",
    "OllamaLLMAdapter",
]
