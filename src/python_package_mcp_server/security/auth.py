"""Authentication middleware for MCP server."""

from typing import Optional

import structlog

from .user_manager import User, UserManager

logger = structlog.get_logger(__name__)


class AuthenticationError(Exception):
    """Error raised when authentication fails."""

    pass


class AuthMiddleware:
    """Authentication middleware for HTTP transport."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        enable_auth: bool = False,
        user_manager: Optional[UserManager] = None,
        enable_user_auth: bool = False,
        single_api_key_mode: bool = True,
    ):
        """Initialize authentication middleware.

        Args:
            api_key: API key for authentication (legacy mode)
            enable_auth: Whether authentication is enabled
            user_manager: User manager instance (for user-based auth)
            enable_user_auth: Whether user-based authentication is enabled
            single_api_key_mode: Use legacy single API key mode
        """
        self.api_key = api_key
        self.enable_auth = enable_auth
        self.user_manager = user_manager
        self.enable_user_auth = enable_user_auth
        self.single_api_key_mode = single_api_key_mode

    def authenticate(self, provided_key: Optional[str]) -> bool:
        """Authenticate a request (legacy single API key mode).

        Args:
            provided_key: API key provided in request

        Returns:
            True if authenticated, False otherwise

        Raises:
            AuthenticationError: If authentication fails and enabled
        """
        if not self.enable_auth:
            return True

        # Use user-based authentication if enabled
        if self.enable_user_auth and self.user_manager:
            user = self.authenticate_user(provided_key)
            return user is not None

        # Legacy single API key mode
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

    def authenticate_user(self, api_key: Optional[str]) -> Optional[User]:
        """Authenticate a user by API key.

        Args:
            api_key: API key provided in request

        Returns:
            User if authenticated, None otherwise

        Raises:
            AuthenticationError: If authentication fails and enabled
        """
        if not self.enable_auth:
            return None

        if not self.enable_user_auth or not self.user_manager:
            # Fall back to legacy mode
            if self.authenticate(api_key):
                # Return a dummy admin user for backward compatibility
                return User(
                    username="legacy",
                    api_key_hash="",
                    role="admin",
                    created_at="",
                )
            return None

        if not api_key:
            logger.warning("auth_required_but_no_key_provided")
            raise AuthenticationError("Authentication required")

        user = self.user_manager.get_user_by_api_key(api_key)
        if not user:
            logger.warning("invalid_api_key")
            raise AuthenticationError("Invalid API key")

        logger.debug("authentication_successful", username=user.username, role=user.role)
        return user

    def check_permission(self, user: Optional[User], operation: str) -> bool:
        """Check if user has permission for an operation.

        Args:
            user: User object (None if not authenticated)
            operation: Operation name (e.g., 'install', 'create_user')

        Returns:
            True if allowed, False otherwise
        """
        # If user auth is disabled, allow all operations
        if not self.enable_user_auth:
            return True

        # If no user, deny access
        if not user:
            return False

        # Admin can do everything
        if user.role == "admin":
            return True

        # Regular users: read-only operations
        read_only_operations = [
            "list_resources",
            "read_resource",
            "list_resource_templates",
            "list_tools",
            "list_prompts",
            "get_prompt",
        ]

        # Check if operation is read-only
        if operation in read_only_operations:
            return True

        # Write operations require admin
        write_operations = [
            "install",
            "uninstall",
            "add",
            "remove",
            "sync",
            "lock",
            "init",
            "upgrade",
            "create_user",
            "delete_user",
            "list_users",
            "dart_format",
            "dart_analyze",
            "dart_fix",
            "typescript_format",
            "typescript_lint",
            "typescript_type_check",
            "index_project",
            "refresh_index",
            "discover_projects",
            "analyze_codebase",
        ]

        if operation in write_operations:
            return False

        # Default: allow (for unknown operations, be permissive)
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
