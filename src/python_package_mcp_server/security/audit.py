"""Audit logging for enterprise features."""

import json
from datetime import datetime
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class AuditLogger:
    """Audit logger for tracking tool invocations and actions."""

    def __init__(self, log_format: str = "json"):
        """Initialize audit logger.

        Args:
            log_format: Log format ("json" or "text")
        """
        self.log_format = log_format
        self.configure_logging()

    def configure_logging(self) -> None:
        """Configure structured logging."""
        if self.log_format == "json":
            structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.add_log_level,
                    structlog.processors.JSONRenderer(),
                ]
            )
        else:
            structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.add_log_level,
                    structlog.dev.ConsoleRenderer(),
                ]
            )

    def log_tool_invocation(
        self,
        tool_name: str,
        user_context: Optional[dict[str, Any]] = None,
        parameters: Optional[dict[str, Any]] = None,
        result: Optional[dict[str, Any]] = None,
        success: bool = True,
    ) -> None:
        """Log a tool invocation.

        Args:
            tool_name: Name of the tool invoked
            user_context: User context information
            parameters: Tool parameters
            result: Tool result
            success: Whether invocation was successful
        """
        audit_entry = {
            "event": "tool_invocation",
            "tool": tool_name,
            "timestamp": datetime.utcnow().isoformat(),
            "success": success,
        }

        if user_context:
            audit_entry["user"] = user_context

        if parameters:
            # Sanitize parameters (remove sensitive data)
            sanitized_params = self._sanitize_parameters(parameters)
            audit_entry["parameters"] = sanitized_params

        if result:
            audit_entry["result"] = result

        logger.info("audit_tool_invocation", **audit_entry)

    def log_resource_access(
        self,
        resource_uri: str,
        user_context: Optional[dict[str, Any]] = None,
    ) -> None:
        """Log resource access.

        Args:
            resource_uri: URI of accessed resource
            user_context: User context information
        """
        audit_entry = {
            "event": "resource_access",
            "resource": resource_uri,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if user_context:
            audit_entry["user"] = user_context

        logger.info("audit_resource_access", **audit_entry)

    def log_security_event(
        self,
        event_type: str,
        details: dict[str, Any],
        user_context: Optional[dict[str, Any]] = None,
    ) -> None:
        """Log security-related event.

        Args:
            event_type: Type of security event
            details: Event details
            user_context: User context information
        """
        audit_entry = {
            "event": "security_event",
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        }

        if user_context:
            audit_entry["user"] = user_context

        logger.warning("audit_security_event", **audit_entry)

    def _sanitize_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Sanitize parameters to remove sensitive data.

        Args:
            parameters: Parameters to sanitize

        Returns:
            Sanitized parameters
        """
        sanitized = parameters.copy()
        sensitive_keys = ["password", "api_key", "token", "secret", "key"]

        for key in sanitized:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = "***REDACTED***"

        return sanitized
