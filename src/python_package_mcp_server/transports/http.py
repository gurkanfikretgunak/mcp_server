"""HTTP/SSE transport handler for enterprise deployments."""

import asyncio
import json
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from mcp.server.sse import SseServerTransport

from .. import __version__
from ..config import config
from ..security.auth import AuthMiddleware, AuthenticationError
from ..security.user_manager import UserManager
from ..server import server, current_user_context, list_resources, list_tools, list_prompts, list_resource_templates

# Initialize user manager and auth middleware
user_manager = UserManager(config.users_file) if config.enable_user_auth else None
auth_middleware = AuthMiddleware(
    api_key=config.api_key,
    enable_auth=config.enable_auth,
    user_manager=user_manager,
    enable_user_auth=config.enable_user_auth,
    single_api_key_mode=config.single_api_key_mode,
)

# Create FastAPI app
app = FastAPI(title="Python Package MCP Server")

# Create SSE transport
sse_transport = SseServerTransport("/messages")


@app.middleware("http")
async def auth_middleware_func(request: Request, call_next):
    """Authentication middleware for HTTP requests."""
    # Clear user context for each request
    current_user_context.clear()
    
    if config.enable_auth and request.url.path != "/health":
        try:
            headers = dict(request.headers)
            api_key = auth_middleware.extract_api_key(headers)
            
            # Use user-based authentication if enabled
            if config.enable_user_auth:
                user = auth_middleware.authenticate_user(api_key)
                if user:
                    current_user_context["user"] = user
            else:
                # Legacy single API key mode
                auth_middleware.authenticate(api_key)
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=str(e))
    
    response = await call_next(request)
    
    # Check permissions for write operations (if user auth enabled)
    if config.enable_user_auth and current_user_context.get("user"):
        user = current_user_context["user"]
        # Permission checking is done in server.py call_tool handler
        # Here we just ensure user context is available
    
    return response


@app.get("/health")
@app.get("/")
async def health_check():
    """Health check endpoint with rich server information."""
    import importlib.metadata
    
    # Get server metadata
    try:
        metadata = importlib.metadata.metadata("python-package-mcp-server")
        author_name = metadata.get("Author", "Gurkan Fikret Gunak")
        author_email = metadata.get("Author-email", "gurkanfikretgunak@example.com")
        description = metadata.get("Summary", "Production-ready MCP server for managing Python packages using uv")
        license_info = metadata.get("License", "MIT")
    except Exception:
        # Fallback if metadata not available
        author_name = "Gurkan Fikret Gunak"
        author_email = "gurkanfikretgunak@example.com"
        description = "Production-ready MCP server for managing Python packages using uv"
        license_info = "MIT"
    
    # Get server capabilities
    resources = []
    tools = []
    prompts = []
    resource_templates = []
    
    try:
        resources = await list_resources()
        tools = await list_tools()
        prompts = await list_prompts()
        resource_templates = await list_resource_templates()
    except Exception:
        # If handlers fail, continue with empty lists
        pass
    
    # Get authentication info
    auth_info = {
        "enabled": config.enable_auth,
        "mode": "user-based" if config.enable_user_auth else "single-api-key" if config.enable_auth else "disabled",
    }
    
    if config.enable_user_auth and user_manager:
        try:
            users = user_manager.list_users()
            admin_count = sum(1 for u in users if u.role == "admin")
            user_count = len(users) - admin_count
            auth_info["users"] = {
                "total": len(users),
                "admins": admin_count,
                "regular_users": user_count,
            }
        except Exception:
            pass
    
    # Get system information
    system_info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": sys.version.split()[0],
        "architecture": platform.machine(),
    }
    
    # Get project information
    project_info = {
        "root": str(config.project_root or Path.cwd()),
        "workspace_root": str(config.workspace_root) if config.workspace_root else None,
    }
    
    # Build comprehensive response
    response = {
        "status": "ok",
        "server": {
            "name": "python-package-mcp-server",
            "version": __version__,
            "description": description,
            "author": {
                "name": author_name,
                "email": author_email,
            },
            "license": license_info,
            "repository": "https://github.com/gurkanfikretgunak/mcp_server",
        },
        "capabilities": {
            "resources": {
                "count": len(resources),
                "categories": {
                    "packages": len([r for r in resources if str(r.uri).startswith("python:packages://")]),
                    "dependencies": len([r for r in resources if str(r.uri).startswith("python:dependencies://")]),
                    "project": len([r for r in resources if str(r.uri).startswith("project://")]),
                    "codebase": len([r for r in resources if str(r.uri).startswith("codebase://")]),
                    "dart": len([r for r in resources if str(r.uri).startswith("dart:standards://")]),
                    "typescript": len([r for r in resources if str(r.uri).startswith("typescript:standards://")]),
                },
            },
            "resource_templates": {
                "count": len(resource_templates),
            },
            "tools": {
                "count": len(tools),
                "categories": {
                    "package_management": len([t for t in tools if t.name in ["install", "uninstall", "add", "remove", "sync", "lock"]]),
                    "environment": len([t for t in tools if t.name in ["init", "upgrade", "index_project", "refresh_index", "discover_projects", "analyze_codebase"]]),
                    "dart": len([t for t in tools if t.name.startswith("dart_")]),
                    "typescript": len([t for t in tools if t.name.startswith("typescript_")]),
                    "auth": len([t for t in tools if t.name in ["create_user", "list_users", "delete_user"]]),
                },
            },
            "prompts": {
                "count": len(prompts),
                "available": [p.name for p in prompts],
            },
        },
        "configuration": {
            "transport": {
                "type": "http",
                "host": config.host,
                "port": config.port,
                "url": f"http://{config.host}:{config.port}",
            },
            "authentication": auth_info,
            "logging": {
                "level": config.log_level,
                "format": config.log_format,
            },
            "policy": {
                "allowed_packages": config.allowed_packages if config.allowed_packages else None,
                "blocked_packages": config.blocked_packages if config.blocked_packages else None,
            },
            "project": project_info,
        },
        "system": system_info,
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "messages": "/messages",
            "docs": "/docs",
            "openapi": "/openapi.json",
        },
    }
    
    return response


@app.get("/messages")
async def messages_endpoint(request: Request):
    """SSE messages endpoint."""
    # Note: Full SSE integration requires additional setup with MCP SDK
    # This is a placeholder for the actual implementation
    # For production use, integrate with MCP SDK's SSE transport properly
    return {"message": "SSE endpoint - integration with MCP SDK SSE transport required"}


async def run_http_server() -> None:
    """Run HTTP server with SSE transport."""
    import uvicorn

    uvicorn.run(app, host=config.host, port=config.port)


if __name__ == "__main__":
    asyncio.run(run_http_server())
