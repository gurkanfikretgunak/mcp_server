"""Authentication middleware for MCP server."""

from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


class AuthenticationError(Exception):
    """Error raised when authentication fails."""

    pass


class AuthMiddleware:
    """Authentication middleware for HTTP transport."""

    def __init__(self, api_key: Optional[str] = None, enable_auth: bool = False):
        """Initialize authentication middleware.

        Args:
            api_key: API key for authentication
            enable_auth: Whether authentication is enabled
        """
        self.api_key = api_key
        self.enable_auth = enable_auth

    def authenticate(self, provided_key: Optional[str]) -> bool:
        """Authenticate a request.

        Args:
            provided_key: API key provided in request

        Returns:
            True if authenticated, False otherwise

        Raises:
            AuthenticationError: If authentication fails and enabled
        """
        if not self.enable_auth:
            return True

        if not self.api_key:
            logger.warning("auth_enabled_but_no_key_configured")
            return False

        if not provided_key:
            logger.warning("auth_required_but_no_key_provided")
            raise AuthenticationError("Authentication required")

        if provided_key != self.api_key:
            logger.warning("invalid_api_key")
            raise AuthenticationError("Invalid API key")

        logger.debug("authentication_successful")
        return True

    def extract_api_key(self, headers: dict[str, str]) -> Optional[str]:
        """Extract API key from request headers.

        Args:
            headers: Request headers

        Returns:
            API key if found, None otherwise
        """
        # Check common header names for API key
        for header_name in ["X-API-Key", "Authorization", "X-Auth-Token"]:
            if header_name in headers:
                value = headers[header_name]
                # Handle "Bearer <token>" format
                if value.startswith("Bearer "):
                    return value[7:]
                return value

        return None
