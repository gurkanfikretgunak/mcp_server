"""Main MCP server implementation."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, ResourceTemplate

from .config import config
from .resources import codebase, dependencies, packages, project_index
from .tools import env, install, sync

# Initialize server
server = Server("python-package-mcp-server")


# Register resources
@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources."""
    resources = []
    resources.extend(packages.get_package_resources())
    resources.extend(dependencies.get_dependency_resources())
    resources.extend(project_index.get_project_index_resources())
    resources.extend(codebase.get_codebase_resources())
    return resources


@server.read_resource()
async def read_resource(uri: str, params: dict[str, Any] | None = None) -> str:
    """Read a resource by URI."""
    params = params or {}

    # Package resources
    if uri.startswith("python:packages://"):
        return packages.read_package_resource(uri)

    # Dependency resources
    if uri.startswith("python:dependencies://") or uri.startswith("python:project://") or uri.startswith("python:environment://"):
        return dependencies.read_dependency_resource(uri)

    # Project index resources
    if uri.startswith("project://"):
        return project_index.read_project_index_resource(uri)

    # Codebase resources
    if uri.startswith("codebase://"):
        return codebase.read_codebase_resource(uri, params)

    raise ValueError(f"Unknown resource URI: {uri}")


@server.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List all resource templates."""
    templates = []
    templates.extend(packages.get_package_resource_templates())
    templates.extend(dependencies.get_dependency_resource_templates())
    templates.extend(project_index.get_project_index_resource_templates())
    templates.extend(codebase.get_codebase_resource_templates())
    return templates


# Register tools
@server.list_tools()
async def list_tools() -> list:
    """List all available tools."""
    tools = []
    tools.extend(install.get_install_tools())
    tools.extend(sync.get_sync_tools())
    tools.extend(env.get_env_tools())
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list:
    """Handle tool invocation."""
    arguments = arguments or {}

    # Install tools
    if name == "install":
        return await install.handle_install(arguments)
    elif name == "uninstall":
        return await install.handle_uninstall(arguments)

    # Sync tools
    elif name == "add":
        return await sync.handle_add(arguments)
    elif name == "remove":
        return await sync.handle_remove(arguments)
    elif name == "sync":
        return await sync.handle_sync(arguments)
    elif name == "lock":
        return await sync.handle_lock(arguments)

    # Environment tools
    elif name == "init":
        return await env.handle_init(arguments)
    elif name == "upgrade":
        return await env.handle_upgrade(arguments)
    elif name == "index_project":
        return await env.handle_index_project(arguments)
    elif name == "refresh_index":
        return await env.handle_refresh_index(arguments)
    elif name == "discover_projects":
        return await env.handle_discover_projects(arguments)
    elif name == "analyze_codebase":
        return await env.handle_analyze_codebase(arguments)

    else:
        raise ValueError(f"Unknown tool: {name}")


async def run_stdio() -> None:
    """Run server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


async def main() -> None:
    """Main entry point."""
    await run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
