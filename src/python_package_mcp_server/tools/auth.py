"""Authentication and user management tools."""

from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..security.user_manager import UserManager

audit_logger = AuditLogger(config.log_format)
user_manager = UserManager(config.users_file)


def get_auth_tools() -> list[Tool]:
    """Get authentication and user management tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="create_user",
            description="Create a new user account (admin only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username for the new user",
                    },
                    "api_key": {
                        "type": "string",
                        "description": "API key for the user (optional, auto-generated if not provided)",
                    },
                    "role": {
                        "type": "string",
                        "description": "User role: 'admin' or 'user' (default: 'user')",
                        "enum": ["admin", "user"],
                    },
                },
                "required": ["username"],
            },
        ),
        Tool(
            name="list_users",
            description="List all users (admin only)",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="delete_user",
            description="Delete a user account (admin only, cannot delete last admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Username of the user to delete",
                    },
                },
                "required": ["username"],
            },
        ),
    ]


async def handle_create_user(arguments: dict[str, Any], current_user: Any = None) -> list[TextContent]:
    """Handle create_user tool invocation.

    Args:
        arguments: Tool arguments
        current_user: Current authenticated user

    Returns:
        Tool result
    """
    from ..security.auth import AuthMiddleware

    username = arguments.get("username")
    api_key = arguments.get("api_key")
    role = arguments.get("role", "user")

    # Check permissions
    auth_middleware = AuthMiddleware(
        enable_user_auth=config.enable_user_auth,
        user_manager=user_manager,
    )

    if not auth_middleware.check_permission(current_user, "create_user"):
        audit_logger.log_tool_invocation(
            "create_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text="Error: Only admin users can create accounts")]

    try:
        user, plain_api_key = user_manager.create_user(username, api_key, role)

        audit_logger.log_tool_invocation(
            "create_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username, "role": role},
            result={"username": user.username, "role": user.role},
            success=True,
        )

        return [
            TextContent(
                type="text",
                text=f"Successfully created user '{user.username}' with role '{user.role}'. "
                f"API key: {plain_api_key} (save this securely, it won't be shown again)",
            )
        ]

    except ValueError as e:
        audit_logger.log_tool_invocation(
            "create_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text=f"Error creating user: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "create_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text=f"Error creating user: {str(e)}")]


async def handle_list_users(arguments: dict[str, Any], current_user: Any = None) -> list[TextContent]:
    """Handle list_users tool invocation.

    Args:
        arguments: Tool arguments
        current_user: Current authenticated user

    Returns:
        Tool result
    """
    from ..security.auth import AuthMiddleware

    # Check permissions
    auth_middleware = AuthMiddleware(
        enable_user_auth=config.enable_user_auth,
        user_manager=user_manager,
    )

    if not auth_middleware.check_permission(current_user, "list_users"):
        audit_logger.log_tool_invocation(
            "list_users",
            user_context={"username": current_user.username if current_user else None},
            success=False,
        )
        return [TextContent(type="text", text="Error: Only admin users can list users")]

    try:
        users = user_manager.list_users()

        audit_logger.log_tool_invocation(
            "list_users",
            user_context={"username": current_user.username if current_user else None},
            result={"count": len(users)},
            success=True,
        )

        if not users:
            return [TextContent(type="text", text="No users found.")]

        user_list = "\n".join(
            [f"- {user.username} ({user.role}) - Created: {user.created_at}" for user in users]
        )
        return [TextContent(type="text", text=f"Users ({len(users)}):\n{user_list}")]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "list_users",
            user_context={"username": current_user.username if current_user else None},
            success=False,
        )
        return [TextContent(type="text", text=f"Error listing users: {str(e)}")]


async def handle_delete_user(arguments: dict[str, Any], current_user: Any = None) -> list[TextContent]:
    """Handle delete_user tool invocation.

    Args:
        arguments: Tool arguments
        current_user: Current authenticated user

    Returns:
        Tool result
    """
    from ..security.auth import AuthMiddleware

    username = arguments.get("username")

    # Check permissions
    auth_middleware = AuthMiddleware(
        enable_user_auth=config.enable_user_auth,
        user_manager=user_manager,
    )

    if not auth_middleware.check_permission(current_user, "delete_user"):
        audit_logger.log_tool_invocation(
            "delete_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text="Error: Only admin users can delete accounts")]

    try:
        deleted = user_manager.delete_user(username)

        if deleted:
            audit_logger.log_tool_invocation(
                "delete_user",
                user_context={"username": current_user.username if current_user else None},
                parameters={"username": username},
                success=True,
            )
            return [TextContent(type="text", text=f"Successfully deleted user '{username}'")]
        else:
            audit_logger.log_tool_invocation(
                "delete_user",
                user_context={"username": current_user.username if current_user else None},
                parameters={"username": username},
                success=False,
            )
            return [TextContent(type="text", text=f"User '{username}' not found")]

    except ValueError as e:
        audit_logger.log_tool_invocation(
            "delete_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text=f"Error deleting user: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "delete_user",
            user_context={"username": current_user.username if current_user else None},
            parameters={"username": username},
            success=False,
        )
        return [TextContent(type="text", text=f"Error deleting user: {str(e)}")]
