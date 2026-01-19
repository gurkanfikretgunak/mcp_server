"""Sync and lock tools."""

from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..utils.package_manager_wrapper import PackageManagerWrapper

audit_logger = AuditLogger(config.log_format)


def get_sync_tools() -> list[Tool]:
    """Get sync and lock tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="add",
            description="Add package(s) to project dependencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of package specifications to add",
                    },
                    "dev": {
                        "type": "boolean",
                        "description": "Add as dev dependencies",
                        "default": False,
                    },
                },
                "required": ["packages"],
            },
        ),
        Tool(
            name="remove",
            description="Remove package(s) from project dependencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of package names to remove",
                    },
                },
                "required": ["packages"],
            },
        ),
        Tool(
            name="sync",
            description="Sync environment with lock file",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="lock",
            description="Generate or update lock file",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


async def handle_add(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle add tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    packages = arguments.get("packages", [])
    dev = arguments.get("dev", False)

    if not packages:
        return [TextContent(type="text", text="Error: No packages specified")]

    try:
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.add_packages(packages, dev=dev)

        audit_logger.log_tool_invocation(
            "add",
            parameters={"packages": packages, "dev": dev},
            result=result,
            success=True,
        )

        return [TextContent(type="text", text=f"Successfully added packages: {', '.join(packages)}")]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "add",
            parameters={"packages": packages, "dev": dev},
            success=False,
        )
        return [TextContent(type="text", text=f"Error adding packages: {str(e)}")]


async def handle_remove(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle remove tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    packages = arguments.get("packages", [])

    if not packages:
        return [TextContent(type="text", text="Error: No packages specified")]

    try:
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.remove_packages(packages)

        audit_logger.log_tool_invocation(
            "remove",
            parameters={"packages": packages},
            result=result,
            success=True,
        )

        return [TextContent(type="text", text=f"Successfully removed packages: {', '.join(packages)}")]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "remove",
            parameters={"packages": packages},
            success=False,
        )
        return [TextContent(type="text", text=f"Error removing packages: {str(e)}")]


async def handle_sync(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle sync tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    try:
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.sync()

        audit_logger.log_tool_invocation("sync", result=result, success=True)

        return [TextContent(type="text", text="Successfully synced environment")]

    except Exception as e:
        audit_logger.log_tool_invocation("sync", success=False)
        return [TextContent(type="text", text=f"Error syncing environment: {str(e)}")]


async def handle_lock(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle lock tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    try:
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.lock()

        audit_logger.log_tool_invocation("lock", result=result, success=True)

        return [TextContent(type="text", text="Successfully generated/updated lock file")]

    except Exception as e:
        audit_logger.log_tool_invocation("lock", success=False)
        return [TextContent(type="text", text=f"Error generating lock file: {str(e)}")]
