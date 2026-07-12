"""Security domain — permissions, confirmation, and audit trail.

Bounded context responsible for:
- 4-tier risk classification (SAFE, MODERATE, SENSITIVE, CRITICAL)
- Permission gate (central checkpoint for all actions)
- User confirmation dialogs
- Audit logging (every action logged)
- Plugin sandboxing
- Prompt injection defense

Implementation begins in Milestone 15 (M15).
"""
