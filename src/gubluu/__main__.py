"""Gubluu entry point.

Allows running the application via: python -m gubluu
"""

from __future__ import annotations

import argparse
import sys

from gubluu import __app_name__, __version__


def _build_argument_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser.

    Returns:
        Configured argument parser with all top-level commands.
    """
    parser = argparse.ArgumentParser(
        prog="gubluu",
        description=f"{__app_name__} — A production-grade AI desktop companion",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__app_name__} v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("start", help="Start the Gubluu application")
    subparsers.add_parser("chat", help="Start an interactive CLI chat session")
    subparsers.add_parser("info", help="Show system information and configuration status")

    return parser


def main() -> None:
    """Application entry point."""
    parser = _build_argument_parser()
    args = parser.parse_args()

    if args.command == "info":
        _show_info()
    elif args.command == "start":
        import asyncio
        from gubluu.app import GubluuApp
        app = GubluuApp()
        asyncio.run(app.start())
    elif args.command == "chat":
        import asyncio
        from gubluu.app import GubluuApp
        
        async def _run_chat() -> None:
            app = GubluuApp()
            await app.start()
            
            from gubluu.core.di import container
            from gubluu.core.events import EventBus
            from gubluu.core.config import get_settings
            from gubluu.conversation import ChatUseCase, Conversation, GeminiLLMAdapter, OllamaLLMAdapter, EchoLLMAdapter
            from gubluu.core.types import ConversationId
            import uuid
            
            settings = get_settings()
            event_bus = container.resolve(EventBus)
            
            if settings.llm.provider == "ollama":
                llm_adapter = OllamaLLMAdapter(model_name=settings.llm.ollama_model_name)
                print("\n================================================")
                print(f"Gubluu CLI Chat Started (Ollama Mode - {settings.llm.ollama_model_name}). Type 'exit' to quit.")
                print("================================================\n")
            elif settings.llm.provider == "gemini" and settings.llm.gemini_api_key:
                llm_adapter = GeminiLLMAdapter(api_key=settings.llm.gemini_api_key, model_name=settings.llm.model_name)
                print("\n================================================")
                print("Gubluu CLI Chat Started (Gemini Mode). Type 'exit' to quit.")
                print("================================================\n")
            else:
                llm_adapter = EchoLLMAdapter()
                print("\n================================================")
                print("WARNING: Valid API key or local provider not configured!")
                print("Gubluu CLI Chat Started (Echo Mode). Type 'exit' to quit.")
                print("================================================\n")
                
            chat_use_case = ChatUseCase(llm_port=llm_adapter, event_bus=event_bus)
            
            conv_id = ConversationId(str(uuid.uuid4()))
            conversation = Conversation(id=conv_id)
            
            while True:
                try:
                    user_input = input("You: ")
                    if user_input.lower().strip() in ('exit', 'quit'):
                        break
                    if not user_input.strip():
                        continue
                        
                    response = await chat_use_case.handle_user_input(conversation, user_input)
                    print(f"Gubluu: {response.content}")
                except (KeyboardInterrupt, EOFError):
                    break
            
            await app.stop()
            
        asyncio.run(_run_chat())
    elif args.command is None:
        parser.print_help()
        sys.exit(0)


def _show_info() -> None:
    """Display system information and Gubluu configuration status."""
    import platform

    print(f"\n  {__app_name__} v{__version__}")
    print(f"  Python {platform.python_version()}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Architecture: {platform.machine()}")
    print()


if __name__ == "__main__":
    main()
