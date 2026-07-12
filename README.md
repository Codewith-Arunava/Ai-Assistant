# Gubluu

> A production-grade AI desktop companion for Windows 11.

Gubluu is a human-like AI assistant that communicates naturally in English, Bengali, and code-switched mixtures. It performs real desktop tasks, remembers your preferences, and operates through voice or text.

## Status

🚧 **Pre-Alpha** — Milestone 1: Project Scaffold 

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```powershell
# Clone the repository
git clone <repo-url>
cd "Ai Assistant"

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# Verify installation
python -m gubluu --version
```

### Development

```powershell
# Run linter
ruff check src/ tests/

# Run formatter
ruff format src/ tests/

# Run type checker
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=gubluu --cov-report=html
```

## Architecture

Gubluu follows **Hexagonal Architecture** (Ports & Adapters) with **Domain-Driven Design** principles.

```
src/gubluu/
├── core/           # Shared kernel (config, events, logging, DI, errors, types)
├── conversation/   # LLM integration, personality, chat
├── voice/          # Wake word, STT, TTS, voice pipeline
├── memory/         # Multi-layer memory system
├── desktop/        # Windows automation, file management
├── browser/        # Web automation (Playwright)
├── coding/         # Code assistant, git integration
├── study/          # GATE CS preparation assistant
├── vision/         # Screen capture, OCR, document reading
├── planner/        # Calendar, tasks, reminders
├── plugins/        # Plugin system
├── security/       # Permission gates, audit logging
├── agents/         # Multi-agent orchestration (LangGraph)
└── ui/             # PySide6 GUI
```

See `docs/architecture/` for detailed architecture documentation.

## Version Roadmap

| Version | Name | Status |
|---------|------|--------|
| v1.0 | Foundation | 🚧 In Progress |
| v2.0 | Conversationalist | ⏳ Planned |
| v3.0 | Voice | ⏳ Planned |
| v4.0 | Memory | ⏳ Planned |
| v5.0 | Desktop Commander | ⏳ Planned |
| v6.0 | Web Navigator | ⏳ Planned |
| v7.0 | Code Companion | ⏳ Planned |
| v8.0 | Scholar | ⏳ Planned |
| v9.0 | Eyes & Planner | ⏳ Planned |
| v10.0 | Complete Platform | ⏳ Planned |

## License

Proprietary. All rights reserved.
