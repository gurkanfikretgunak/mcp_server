"""Main MCP server implementation."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    ResourceTemplate,
    Prompt,
    PromptMessage,
    PromptArgument,
    GetPromptResult,
    TextContent,
)

from .config import config
# Resource handlers are imported dynamically via resource loader
# Keep imports for backward compatibility if needed
from .resources import codebase, dependencies, packages, project_index, dart_standards, typescript_standards
from .tools import env, install, sync, dart, typescript
from .security.auth import AuthMiddleware
from .security.user_manager import UserManager

# Import auth tools only if user auth is enabled
if config.enable_user_auth:
    from .tools import auth
else:
    auth = None

# Initialize server
server = Server("python-package-mcp-server")

# Initialize user manager and auth middleware
user_manager = UserManager(config.users_file) if config.enable_user_auth else None
auth_middleware = AuthMiddleware(
    api_key=config.api_key,
    enable_auth=config.enable_auth,
    user_manager=user_manager,
    enable_user_auth=config.enable_user_auth,
    single_api_key_mode=config.single_api_key_mode,
)

# Global user context (set per request)
current_user_context: dict[str, Any] = {}


# Register resources
from .resources.loader import get_resource_loader

resource_loader = get_resource_loader()

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources.
    
    Resources are loaded from YAML files in the resources/ directory.
    See resources/README.md for information on adding new resources.
    """
    return resource_loader.list_resources()


@server.read_resource()
async def read_resource(uri: str, params: dict[str, Any] | None = None) -> str:
    """Read a resource by URI.
    
    Resources are loaded from YAML files in the resources/ directory.
    Each resource file defines metadata and a handler function.
    """
    params = params or {}
    return resource_loader.read_resource(uri, params)


@server.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List all resource templates.
    
    Resource templates are loaded from YAML files in the resources/ directory.
    """
    return resource_loader.list_resource_templates()


# Register prompts
from .prompts.loader import get_prompt_loader

prompt_loader = get_prompt_loader()

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List all available prompts.
    
    Prompts are loaded from markdown files in the prompts/ directory.
    See prompts/README.md for information on adding new prompts.
    """
    return prompt_loader.list_prompts()


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
    """Get a prompt with filled arguments.
    
    Prompts are loaded from markdown files in the prompts/ directory.
    Each prompt file contains frontmatter (YAML) with metadata and a template.
    """
    arguments = arguments or {}
    
    # Use prompt loader to get prompts from files
    return prompt_loader.get_prompt(name, arguments)



# Register tools
@server.list_tools()
async def list_tools() -> list:
    """List all available tools."""
    tools = []
    tools.extend(install.get_install_tools())
    tools.extend(sync.get_sync_tools())
    tools.extend(env.get_env_tools())
    tools.extend(dart.get_dart_tools())
    tools.extend(typescript.get_typescript_tools())
    if config.enable_user_auth and auth:
        tools.extend(auth.get_auth_tools())
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list:
    """Handle tool invocation."""
    arguments = arguments or {}
    
    # Get current user from context
    current_user = current_user_context.get("user")
    
    # Check permissions for write operations
    if config.enable_user_auth and current_user:
        if not auth_middleware.check_permission(current_user, name):
            from mcp.types import TextContent
            return [
                TextContent(
                    type="text",
                    text=f"Error: Permission denied. Operation '{name}' requires admin privileges.",
                )
            ]

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

    # Dart tools
    elif name == "dart_format":
        return await dart.handle_dart_format(arguments)
    elif name == "dart_analyze":
        return await dart.handle_dart_analyze(arguments)
    elif name == "dart_fix":
        return await dart.handle_dart_fix(arguments)
    elif name == "dart_generate_code":
        return await dart.handle_dart_generate_code(arguments)
    elif name == "dart_check_standards":
        return await dart.handle_dart_check_standards(arguments)

    # TypeScript tools
    elif name == "typescript_format":
        return await typescript.handle_typescript_format(arguments)
    elif name == "typescript_lint":
        return await typescript.handle_typescript_lint(arguments)
    elif name == "typescript_type_check":
        return await typescript.handle_typescript_type_check(arguments)
    elif name == "typescript_generate_code":
        return await typescript.handle_typescript_generate_code(arguments)
    elif name == "typescript_check_standards":
        return await typescript.handle_typescript_check_standards(arguments)

    # Auth tools (only available when user auth is enabled)
    elif name == "create_user":
        if not config.enable_user_auth or not auth:
            from mcp.types import TextContent
            return [TextContent(type="text", text="Error: User authentication is not enabled")]
        return await auth.handle_create_user(arguments, current_user)
    elif name == "list_users":
        if not config.enable_user_auth or not auth:
            from mcp.types import TextContent
            return [TextContent(type="text", text="Error: User authentication is not enabled")]
        return await auth.handle_list_users(arguments, current_user)
    elif name == "delete_user":
        if not config.enable_user_auth or not auth:
            from mcp.types import TextContent
            return [TextContent(type="text", text="Error: User authentication is not enabled")]
        return await auth.handle_delete_user(arguments, current_user)

    else:
        raise ValueError(f"Unknown tool: {name}")


async def run_stdio() -> None:
    """Run server with stdio transport."""
    # Authenticate user for stdio transport if user auth is enabled
    if config.enable_user_auth and config.api_key:
        try:
            user = auth_middleware.authenticate_user(config.api_key)
            current_user_context["user"] = user
        except Exception:
            # If auth fails, continue without user (for backward compatibility)
            pass
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


async def main() -> None:
    """Main entry point."""
    await run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
