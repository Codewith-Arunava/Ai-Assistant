"""Tests for the base error hierarchy.

Verifies:
- GubluuError is the root of all application exceptions
- Error context is properly structured for logging
- Exception hierarchy is correct
- Repr includes structured context
"""

from __future__ import annotations

import pytest

from gubluu.core.errors import (
    BusinessRuleViolationError,
    ConfigurationError,
    DatabaseError,
    DomainError,
    EntityNotFoundError,
    ExternalServiceError,
    FileSystemError,
    GubluuError,
    InfrastructureError,
    ValidationError,
)


class TestGubluuError:
    """Tests for the root GubluuError class."""

    def test_should_store_message(self):
        error = GubluuError("something went wrong")
        assert error.message == "something went wrong"
        assert str(error) == "something went wrong"

    def test_should_store_context(self):
        error = GubluuError("failed", context={"key": "value", "count": 42})
        assert error.context == {"key": "value", "count": 42}

    def test_should_default_to_empty_context(self):
        error = GubluuError("failed")
        assert error.context == {}

    def test_repr_without_context(self):
        error = GubluuError("test error")
        assert repr(error) == "GubluuError('test error')"

    def test_repr_with_context(self):
        error = GubluuError("test error", context={"key": "val"})
        assert "GubluuError" in repr(error)
        assert "key='val'" in repr(error)

    def test_should_be_catchable_as_exception(self):
        with pytest.raises(Exception):
            raise GubluuError("test")


class TestEntityNotFoundError:
    """Tests for EntityNotFoundError."""

    def test_should_include_entity_info_in_message(self):
        error = EntityNotFoundError("Conversation", "abc-123")
        assert "Conversation" in str(error)
        assert "abc-123" in str(error)

    def test_should_store_entity_type_and_id(self):
        error = EntityNotFoundError("Conversation", "abc-123")
        assert error.entity_type == "Conversation"
        assert error.entity_id == "abc-123"

    def test_should_include_entity_info_in_context(self):
        error = EntityNotFoundError("Memory", "mem-456")
        assert error.context["entity_type"] == "Memory"
        assert error.context["entity_id"] == "mem-456"

    def test_should_be_catchable_as_domain_error(self):
        with pytest.raises(DomainError):
            raise EntityNotFoundError("Task", "task-1")

    def test_should_be_catchable_as_gubluu_error(self):
        with pytest.raises(GubluuError):
            raise EntityNotFoundError("Task", "task-1")


class TestValidationError:
    """Tests for ValidationError."""

    def test_should_store_field_info(self):
        error = ValidationError("Invalid email", field="email")
        assert error.field == "email"
        assert error.context["field"] == "email"

    def test_should_work_without_field(self):
        error = ValidationError("Invalid input")
        assert error.field is None


class TestBusinessRuleViolationError:
    """Tests for BusinessRuleViolationError."""

    def test_should_store_rule(self):
        error = BusinessRuleViolationError(
            "Cannot delete active conversation",
            rule="conversation_must_be_inactive_for_deletion",
        )
        assert error.rule == "conversation_must_be_inactive_for_deletion"
        assert error.context["rule"] == "conversation_must_be_inactive_for_deletion"


class TestInfrastructureErrors:
    """Tests for infrastructure error subclasses."""

    def test_database_error_stores_operation(self):
        error = DatabaseError("Insert failed", operation="insert", table="messages")
        assert error.operation == "insert"
        assert error.table == "messages"
        assert error.context["db_operation"] == "insert"
        assert error.context["db_table"] == "messages"

    def test_external_service_error_stores_service_name(self):
        error = ExternalServiceError(
            "API rate limited",
            service_name="OpenAI",
            status_code=429,
        )
        assert error.service_name == "OpenAI"
        assert error.status_code == 429
        assert error.context["service_name"] == "OpenAI"
        assert error.context["status_code"] == 429

    def test_file_system_error_stores_path(self):
        error = FileSystemError(
            "Permission denied",
            path="C:\\Windows\\system32",
            operation="delete",
        )
        assert error.path == "C:\\Windows\\system32"
        assert error.operation == "delete"

    def test_infrastructure_errors_are_gubluu_errors(self):
        with pytest.raises(GubluuError):
            raise DatabaseError("fail", operation="query")

        with pytest.raises(GubluuError):
            raise ExternalServiceError("fail", service_name="test")

        with pytest.raises(GubluuError):
            raise FileSystemError("fail")


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_should_store_config_key(self):
        error = ConfigurationError("Missing API key", key="llm.openai.api_key")
        assert error.key == "llm.openai.api_key"
        assert error.context["config_key"] == "llm.openai.api_key"

    def test_should_be_catchable_as_gubluu_error(self):
        with pytest.raises(GubluuError):
            raise ConfigurationError("bad config")


class TestExceptionHierarchy:
    """Verify the exception hierarchy is correctly structured."""

    def test_domain_errors_inherit_from_gubluu_error(self):
        assert issubclass(DomainError, GubluuError)
        assert issubclass(EntityNotFoundError, DomainError)
        assert issubclass(ValidationError, DomainError)
        assert issubclass(BusinessRuleViolationError, DomainError)

    def test_infrastructure_errors_inherit_from_gubluu_error(self):
        assert issubclass(InfrastructureError, GubluuError)
        assert issubclass(DatabaseError, InfrastructureError)
        assert issubclass(ExternalServiceError, InfrastructureError)
        assert issubclass(FileSystemError, InfrastructureError)

    def test_configuration_error_inherits_from_gubluu_error(self):
        assert issubclass(ConfigurationError, GubluuError)

    def test_domain_and_infrastructure_are_distinct_branches(self):
        """Domain and infrastructure errors should not be interchangeable."""
        assert not issubclass(DomainError, InfrastructureError)
        assert not issubclass(InfrastructureError, DomainError)
