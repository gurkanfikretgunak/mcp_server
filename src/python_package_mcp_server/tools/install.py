"""Install and uninstall package tools."""

from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..security.policy import PolicyEngine
from ..utils.package_manager_wrapper import PackageManagerWrapper

audit_logger = AuditLogger(config.log_format)
policy_engine = PolicyEngine(config.allowed_packages, config.blocked_packages)


def get_install_tools() -> list[Tool]:
    """Get install/uninstall tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="install",
            description="Install Python package(s) with optional version constraints",
            inputSchema={
                "type": "object",
                "properties": {
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of package specifications (e.g., ['requests==2.31.0', 'pytest'])",
                    },
                    "editable": {
                        "type": "boolean",
                        "description": "Install in editable mode",
                        "default": False,
                    },
                },
                "required": ["packages"],
            },
        ),
        Tool(
            name="uninstall",
            description="Uninstall Python package(s)",
            inputSchema={
                "type": "object",
                "properties": {
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of package names to uninstall",
                    },
                },
                "required": ["packages"],
            },
        ),
    ]


async def handle_install(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle install tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    packages = arguments.get("packages", [])
    editable = arguments.get("editable", False)

    if not packages:
        return [TextContent(type="text", text="Error: No packages specified")]

    try:
        # Check policy
        policy_engine.check_packages(packages)

        # Install packages
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.install_packages(packages, editable=editable)

        # Audit log
        audit_logger.log_tool_invocation(
            "install",
            parameters={"packages": packages, "editable": editable},
            result=result,
            success=True,
        )

        return [TextContent(type="text", text=f"Successfully installed packages: {', '.join(packages)}")]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "install",
            parameters={"packages": packages, "editable": editable},
            success=False,
        )
        return [TextContent(type="text", text=f"Error installing packages: {str(e)}")]


async def handle_uninstall(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle uninstall tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    packages = arguments.get("packages", [])

    if not packages:
        return [TextContent(type="text", text="Error: No packages specified")]

    try:
        # Uninstall packages
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.uninstall_packages(packages)

        # Audit log
        audit_logger.log_tool_invocation(
            "uninstall",
            parameters={"packages": packages},
            result=result,
            success=True,
        )

        return [TextContent(type="text", text=f"Successfully uninstalled packages: {', '.join(packages)}")]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "uninstall",
            parameters={"packages": packages},
            success=False,
        )
        return [TextContent(type="text", text=f"Error uninstalling packages: {str(e)}")]
