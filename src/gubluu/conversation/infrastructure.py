"""Conversation Infrastructure Layer.

Contains concrete implementations of the conversation ports (e.g. LLM Adapters).
"""

from __future__ import annotations

import asyncio

from gubluu.conversation.domain import Conversation, LLMPort, Message, Role
from gubluu.core.logging import get_logger

logger = get_logger(__name__)


class EchoLLMAdapter(LLMPort):
    """A dummy LLM adapter that echoes the user's input.
    
    Used for local testing before integrating a real provider like OpenAI.
    """

    async def generate_response(self, conversation: Conversation) -> Message:
        # Simulate network latency
        await asyncio.sleep(1.0)
        
        last_message = conversation.messages[-1].content if conversation.messages else ""
        echo_text = f"[Echo] I heard you say: {last_message}"
        
        logger.debug("Echo adapter generated response", response=echo_text)
        return Message(content=echo_text, role=Role.ASSISTANT)


class GeminiLLMAdapter(LLMPort):
    """Concrete LLM Adapter for Google Gemini."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash") -> None:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    async def generate_response(self, conversation: Conversation) -> Message:
        # Build history for Gemini
        history = []
        for msg in conversation.messages[:-1]:  # Exclude the last message
            if msg.role == Role.USER:
                history.append({"role": "user", "parts": [msg.content]})
            elif msg.role == Role.ASSISTANT:
                history.append({"role": "model", "parts": [msg.content]})
                
        last_message = conversation.messages[-1].content
        
        # We need to run it asynchronously
        chat = self.model.start_chat(history=history)
        logger.info("Sending request to Gemini API")
        
        # google-generativeai supports async out of the box via send_message_async
        response = await chat.send_message_async(last_message)
        
        if not response.text:
            raise RuntimeError("Received empty response from Gemini API")
            
        logger.debug("Received response from Gemini", length=len(response.text))
        return Message(content=response.text, role=Role.ASSISTANT)


class OllamaLLMAdapter(LLMPort):
    """Concrete LLM Adapter for local Ollama instances."""
    
    def __init__(self, model_name: str = "llama3") -> None:
        import ollama
        self.model_name = model_name
        self.client = ollama.AsyncClient()
        
    async def generate_response(self, conversation: Conversation) -> Message:
        messages = []
        for msg in conversation.messages[:-1]:
            if msg.role == Role.USER:
                messages.append({'role': 'user', 'content': msg.content})
            elif msg.role == Role.ASSISTANT:
                messages.append({'role': 'assistant', 'content': msg.content})
                
        last_message = conversation.messages[-1].content
        messages.append({'role': 'user', 'content': last_message})
        
        logger.info("Sending request to local Ollama API", model=self.model_name)
        response = await self.client.chat(model=self.model_name, messages=messages)
        
        if not response or 'message' not in response:
            raise RuntimeError("Received empty response from Ollama API")
            
        content = response['message']['content']
        logger.debug("Received response from Ollama", length=len(content))
        return Message(content=content, role=Role.ASSISTANT)
