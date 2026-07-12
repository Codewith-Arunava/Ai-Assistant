# Architecture Decision Record: ADR-001 — Hexagonal Architecture

**Status**: Accepted  
**Date**: 2026-07-12  
**Decision**: Use Hexagonal Architecture (Ports & Adapters) as the primary architectural pattern.

## Context

Gubluu is a complex desktop application with:
- Multiple external integrations (LLMs, databases, OS APIs, browser automation)
- A long development timeline (v1.0 to v10.0+)
- Need for testability (domain logic must be testable without external systems)
- Technology flexibility (LLM providers, TTS engines, databases may change)

## Decision

Every bounded context follows a three-layer structure:
1. **Domain** — Pure business logic with zero external dependencies
2. **Application** — Use cases orchestrating domain objects through injected ports
3. **Infrastructure** — Concrete adapter implementations for external systems

External systems are accessed exclusively through **ports** (interfaces defined in the domain layer) and **adapters** (implementations in the infrastructure layer).

## Consequences

**Positive:**
- Domain logic is fully testable with mocks
- Any technology can be swapped by writing a new adapter
- Clear separation of concerns
- Enforces dependency direction (domain has no external imports)

**Negative:**
- More boilerplate in early stages
- Requires discipline to maintain layer boundaries
- New contributors need to understand the pattern

## Rationale

The initial boilerplate cost is acceptable for a project targeting 100K+ lines. The ability to swap LLM providers, databases, and voice engines without touching business logic is essential for a project with a multi-year roadmap.
