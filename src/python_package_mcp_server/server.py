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
@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources."""
    resources = []
    resources.extend(packages.get_package_resources())
    resources.extend(dependencies.get_dependency_resources())
    resources.extend(project_index.get_project_index_resources())
    resources.extend(codebase.get_codebase_resources())
    resources.extend(dart_standards.get_dart_resources())
    resources.extend(typescript_standards.get_typescript_resources())
    return resources


@server.read_resource()
async def read_resource(uri: str, params: dict[str, Any] | None = None) -> str:
    """Read a resource by URI."""
    params = params or {} 
    
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)

    # Package resources
    if uri_str.startswith("python:packages://"):
        return packages.read_package_resource(uri_str)

    # Dependency resources
    if uri_str.startswith("python:dependencies://") or uri_str.startswith("python:project://") or uri_str.startswith("python:environment://"):
        return dependencies.read_dependency_resource(uri_str)

    # Project index resources
    if uri_str.startswith("project://"):
        return project_index.read_project_index_resource(uri_str)

    # Codebase resources
    if uri_str.startswith("codebase://"):
        return codebase.read_codebase_resource(uri_str, params)

    # Dart standards resources
    if uri_str.startswith("dart:standards://"):
        return dart_standards.read_dart_resource(uri_str)

    # TypeScript standards resources
    if uri_str.startswith("typescript:standards://"):
        return typescript_standards.read_typescript_resource(uri_str)

    raise ValueError(f"Unknown resource URI: {uri_str}")


@server.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """List all resource templates."""
    templates = []
    templates.extend(packages.get_package_resource_templates())
    templates.extend(dependencies.get_dependency_resource_templates())
    templates.extend(project_index.get_project_index_resource_templates())
    templates.extend(codebase.get_codebase_resource_templates())
    templates.extend(dart_standards.get_dart_resource_templates())
    templates.extend(typescript_standards.get_typescript_resource_templates())
    return templates


# Register prompts
@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List all available prompts."""
    return [
        Prompt(
            name="analyze_package_dependencies",
            description="Analyze package dependencies and suggest updates",
            arguments=[
                PromptArgument(
                    name="package_name",
                    description="Name of the package to analyze (optional, analyzes all if not provided)",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="code_review",
            description="Review code for best practices and potential issues",
            arguments=[
                PromptArgument(
                    name="file_path",
                    description="Path to the file to review",
                    required=True,
                ),
                PromptArgument(
                    name="language",
                    description="Programming language (python, dart, typescript)",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="project_setup_guide",
            description="Generate a setup guide for the project",
            arguments=[
                PromptArgument(
                    name="include_dependencies",
                    description="Include dependency installation instructions",
                    required=False,
                ),
            ],
        ),
        Prompt(
            name="dependency_audit",
            description="Audit project dependencies for security and updates",
            arguments=[],
        ),
        Prompt(
            name="code_formatting_check",
            description="Check if code follows formatting standards",
            arguments=[
                PromptArgument(
                    name="file_path",
                    description="Path to the file or directory to check",
                    required=True,
                ),
                PromptArgument(
                    name="language",
                    description="Programming language (python, dart, typescript)",
                    required=True,
                ),
            ],
        ),
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
    """Get a prompt with filled arguments."""
    arguments = arguments or {}
    
    if name == "analyze_package_dependencies":
        package_name = arguments.get("package_name", "")
        if package_name:
            prompt_text = f"Analyze the dependencies of the '{package_name}' package. Check for:\n"
        else:
            prompt_text = "Analyze all project dependencies. Check for:\n"
        prompt_text += "- Outdated packages that need updates\n"
        prompt_text += "- Security vulnerabilities\n"
        prompt_text += "- Unused dependencies\n"
        prompt_text += "- Dependency conflicts\n"
        prompt_text += "Provide recommendations for updates and improvements."
        
        return GetPromptResult(
            description="Analyze package dependencies and suggest updates",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )
    
    elif name == "code_review":
        file_path = arguments.get("file_path", "")
        language = arguments.get("language", "python")
        
        prompt_text = f"Review the code in '{file_path}' ({language}). "
        prompt_text += "Check for:\n"
        prompt_text += "- Code quality and best practices\n"
        prompt_text += "- Potential bugs or issues\n"
        prompt_text += "- Performance optimizations\n"
        prompt_text += "- Security concerns\n"
        prompt_text += "- Code style and formatting\n"
        prompt_text += "Provide constructive feedback and suggestions."
        
        return GetPromptResult(
            description="Review code for best practices and potential issues",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )
    
    elif name == "project_setup_guide":
        include_deps = arguments.get("include_dependencies", "true").lower() == "true"
        
        prompt_text = "Generate a comprehensive project setup guide. Include:\n"
        prompt_text += "- Prerequisites and requirements\n"
        if include_deps:
            prompt_text += "- Dependency installation instructions\n"
        prompt_text += "- Environment setup steps\n"
        prompt_text += "- Configuration instructions\n"
        prompt_text += "- How to run the project\n"
        prompt_text += "- Common troubleshooting tips\n"
        prompt_text += "Make it clear and easy to follow for new developers."
        
        return GetPromptResult(
            description="Generate a setup guide for the project",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )
    
    elif name == "dependency_audit":
        prompt_text = "Perform a comprehensive dependency audit for this project. Check:\n"
        prompt_text += "- All installed packages and their versions\n"
        prompt_text += "- Outdated packages with available updates\n"
        prompt_text += "- Security vulnerabilities (CVEs)\n"
        prompt_text += "- License compatibility\n"
        prompt_text += "- Unused or redundant dependencies\n"
        prompt_text += "- Dependency conflicts\n"
        prompt_text += "Provide a detailed report with recommendations."
        
        return GetPromptResult(
            description="Audit project dependencies for security and updates",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )
    
    elif name == "code_formatting_check":
        file_path = arguments.get("file_path", "")
        language = arguments.get("language", "python")
        
        prompt_text = f"Check if the code in '{file_path}' follows {language} formatting standards. "
        prompt_text += "Verify:\n"
        prompt_text += "- Indentation and spacing\n"
        prompt_text += "- Line length\n"
        prompt_text += "- Naming conventions\n"
        prompt_text += "- Import organization\n"
        prompt_text += "- Code style guidelines\n"
        prompt_text += "Report any formatting issues and suggest fixes."
        
        return GetPromptResult(
            description="Check if code follows formatting standards",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text),
                ),
            ],
        )
    
    else:
        raise ValueError(f"Unknown prompt: {name}")


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
