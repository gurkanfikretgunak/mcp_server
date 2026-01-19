"""Environment management tools."""

from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..security.policy import PolicyEngine
from ..utils.package_manager_wrapper import PackageManagerWrapper

audit_logger = AuditLogger(config.log_format)
policy_engine = PolicyEngine(config.allowed_packages, config.blocked_packages)


def get_env_tools() -> list[Tool]:
    """Get environment management tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="init",
            description="Initialize a new Python project",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Optional project name",
                    },
                },
            },
        ),
        Tool(
            name="upgrade",
            description="Upgrade package(s) to latest versions",
            inputSchema={
                "type": "object",
                "properties": {
                    "packages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of package names to upgrade (upgrades all if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="index_project",
            description="Index/scan a project directory and build resource cache",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional project path (uses current directory if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="refresh_index",
            description="Refresh project index cache",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="discover_projects",
            description="Discover multiple projects in a workspace",
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_path": {
                        "type": "string",
                        "description": "Optional workspace path",
                    },
                },
            },
        ),
        Tool(
            name="analyze_codebase",
            description="Analyze codebase structure and extract metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Optional project path",
                    },
                },
            },
        ),
    ]


async def handle_init(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle init tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    name = arguments.get("name")

    try:
        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.init_project(name)

        audit_logger.log_tool_invocation("init", parameters={"name": name}, result=result, success=True)

        return [TextContent(type="text", text=f"Successfully initialized project: {name or 'current directory'}")]

    except Exception as e:
        audit_logger.log_tool_invocation("init", parameters={"name": name}, success=False)
        return [TextContent(type="text", text=f"Error initializing project: {str(e)}")]


async def handle_upgrade(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle upgrade tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    packages = arguments.get("packages")

    try:
        if packages:
            # Check policy for specific packages
            policy_engine.check_packages(packages)

        pm_wrapper = PackageManagerWrapper(config.project_root)
        result = pm_wrapper.upgrade_packages(packages)

        audit_logger.log_tool_invocation(
            "upgrade",
            parameters={"packages": packages},
            result=result,
            success=True,
        )

        package_list = ", ".join(packages) if packages else "all packages"
        return [TextContent(type="text", text=f"Successfully upgraded: {package_list}")]

    except Exception as e:
        audit_logger.log_tool_invocation("upgrade", parameters={"packages": packages}, success=False)
        return [TextContent(type="text", text=f"Error upgrading packages: {str(e)}")]


async def handle_index_project(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle index_project tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    from pathlib import Path

    from ..utils.project_scanner import ProjectScanner

    path = arguments.get("path")
    project_path = Path(path).resolve() if path else config.project_root or Path.cwd()

    try:
        scanner = ProjectScanner(project_path)
        structure = scanner.scan_structure()

        audit_logger.log_tool_invocation(
            "index_project",
            parameters={"path": str(project_path)},
            result={"files_count": len(structure.get("files", []))},
            success=True,
        )

        return [
            TextContent(
                type="text",
                text=f"Successfully indexed project at {project_path}: {len(structure.get('files', []))} files found",
            )
        ]

    except Exception as e:
        audit_logger.log_tool_invocation("index_project", parameters={"path": str(project_path)}, success=False)
        return [TextContent(type="text", text=f"Error indexing project: {str(e)}")]


async def handle_refresh_index(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle refresh_index tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    from pathlib import Path

    from ..utils.project_scanner import ProjectScanner

    project_path = config.project_root or Path.cwd()

    try:
        scanner = ProjectScanner(project_path)
        structure = scanner.scan_structure()

        audit_logger.log_tool_invocation("refresh_index", result={"files_count": len(structure.get("files", []))}, success=True)

        return [
            TextContent(
                type="text",
                text=f"Successfully refreshed index: {len(structure.get('files', []))} files found",
            )
        ]

    except Exception as e:
        audit_logger.log_tool_invocation("refresh_index", success=False)
        return [TextContent(type="text", text=f"Error refreshing index: {str(e)}")]


async def handle_discover_projects(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle discover_projects tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    from pathlib import Path

    workspace_path = Path(arguments.get("workspace_path", ".")).resolve()

    try:
        projects = []
        # Look for common project indicators
        for item in workspace_path.iterdir():
            if item.is_dir():
                indicators = ["pyproject.toml", "package.json", "Cargo.toml", "go.mod", "pom.xml"]
                for indicator in indicators:
                    if (item / indicator).exists():
                        projects.append(str(item))
                        break

        audit_logger.log_tool_invocation(
            "discover_projects",
            parameters={"workspace_path": str(workspace_path)},
            result={"projects_count": len(projects)},
            success=True,
        )

        return [TextContent(type="text", text=f"Found {len(projects)} projects: {', '.join(projects)}")]

    except Exception as e:
        audit_logger.log_tool_invocation("discover_projects", parameters={"workspace_path": str(workspace_path)}, success=False)
        return [TextContent(type="text", text=f"Error discovering projects: {str(e)}")]


async def handle_analyze_codebase(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle analyze_codebase tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    from pathlib import Path

    from ..utils.project_scanner import ProjectScanner

    path = arguments.get("path")
    project_path = Path(path).resolve() if path else config.project_root or Path.cwd()

    try:
        scanner = ProjectScanner(project_path)
        structure = scanner.scan_structure()
        config_files = scanner.find_config_files()
        entry_points = scanner.find_entry_points()
        tests = scanner.find_test_files()

        analysis = {
            "files": len(structure.get("files", [])),
            "directories": len(structure.get("directories", [])),
            "config_files": len(config_files),
            "entry_points": len(entry_points),
            "test_files": len(tests),
        }

        audit_logger.log_tool_invocation(
            "analyze_codebase",
            parameters={"path": str(project_path)},
            result=analysis,
            success=True,
        )

        return [
            TextContent(
                type="text",
                text=f"Codebase analysis complete: {analysis['files']} files, {analysis['directories']} directories, "
                f"{analysis['config_files']} config files, {analysis['entry_points']} entry points, "
                f"{analysis['test_files']} test files",
            )
        ]

    except Exception as e:
        audit_logger.log_tool_invocation("analyze_codebase", parameters={"path": str(project_path)}, success=False)
        return [TextContent(type="text", text=f"Error analyzing codebase: {str(e)}")]
