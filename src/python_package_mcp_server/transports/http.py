"""HTTP/SSE transport handler for enterprise deployments."""

import asyncio
import json
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from mcp.server.sse import SseServerTransport

from ..config import config
from ..security.auth import AuthMiddleware, AuthenticationError
from ..server import server

# Initialize auth middleware
auth_middleware = AuthMiddleware(config.api_key, config.enable_auth)

# Create FastAPI app
app = FastAPI(title="Python Package MCP Server")

# Create SSE transport
sse_transport = SseServerTransport("/messages")


@app.middleware("http")
async def auth_middleware_func(request: Request, call_next):
    """Authentication middleware for HTTP requests."""
    if config.enable_auth and request.url.path != "/health":
        try:
            headers = dict(request.headers)
            api_key = auth_middleware.extract_api_key(headers)
            auth_middleware.authenticate(api_key)
        except AuthenticationError as e:
            raise HTTPException(status_code=401, detail=str(e))
    return await call_next(request)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "server": "python-package-mcp-server"}


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
