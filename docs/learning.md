# MCP Server Learning Guide

This guide explains how MCP (Model Context Protocol) servers work and how this implementation is structured.

## What is MCP?

MCP (Model Context Protocol) is an open protocol introduced by Anthropic that standardizes how AI models (LLMs) interact with external systems, tools, and data sources. It enables:

- **Standardized Communication**: Consistent way for LLMs to access external capabilities
- **Resource Discovery**: LLMs can discover and access data resources
- **Tool Invocation**: LLMs can invoke actions through tools
- **Secure Access**: Controlled access to system capabilities

## MCP Architecture

MCP follows a client-server architecture:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│     LLM     │────────▶│   Client   │────────▶│   Server    │
│  (Claude)   │         │  (Cursor)  │         │  (This App) │
└─────────────┘         └─────────────┘         └─────────────┘
```

1. **LLM**: The language model that needs to access external capabilities
2. **Client**: Intermediary that connects LLM to servers (e.g., Cursor IDE)
3. **Server**: Exposes resources and tools via MCP protocol

## MCP Components

### Resources

Resources are read-only data that LLMs can access. They're identified by URIs and can be:

- **Static Resources**: Fixed data like configuration files
- **Dynamic Resources**: Generated on-demand like package lists
- **Template Resources**: Parameterized resources (e.g., `codebase://file?path={path}`)

Example resource URIs:
- `python:packages://installed` - List of installed packages
- `project://index` - Complete project index
- `codebase://file?path=src/main.py` - File content

### Tools

Tools are actions that LLMs can invoke. They have:

- **Name**: Unique identifier
- **Description**: What the tool does
- **Input Schema**: JSON schema defining parameters
- **Handler Function**: Code that executes the action

Example tools:
- `install` - Install Python packages
- `index_project` - Index a project directory
- `analyze_codebase` - Analyze codebase structure

### Transports

MCP supports multiple transport mechanisms:

1. **Stdio**: Standard input/output (for local development)
2. **HTTP/SSE**: HTTP with Server-Sent Events (for remote deployments)

## How This Server Works

### 1. Server Initialization

The server is initialized in `server.py`:

```python
from mcp.server import Server

server = Server("python-package-mcp-server")
```

### 2. Resource Registration

Resources are registered using decorators:

```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    # Return list of available resources
    pass

@server.read_resource()
async def read_resource(uri: str) -> str:
    # Return resource content
    pass
```

### 3. Tool Registration

Tools are registered similarly:

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    # Return list of available tools
    pass

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    # Execute tool and return result
    pass
```

### 4. Transport Setup

The server runs with a transport:

```python
# Stdio transport
from mcp.server.stdio import stdio_server

async with stdio_server() as (read_stream, write_stream):
    await server.run(read_stream, write_stream, ...)
```

## Request/Response Flow

### Resource Request

1. LLM requests resource: `python:packages://installed`
2. Client forwards request to server
3. Server's `read_resource()` handler is called
4. Handler fetches data (e.g., runs `uv pip list`)
5. Server returns JSON response
6. Client forwards response to LLM

### Tool Invocation

1. LLM decides to invoke tool: `install` with `{"packages": ["requests"]}`
2. Client forwards tool call to server
3. Server's `call_tool()` handler is called
4. Handler executes action (e.g., runs `uv pip install requests`)
5. Server returns result
6. Client forwards result to LLM

## Extending the Server

### Adding a New Resource

1. Create resource handler in `resources/`:

```python
def get_my_resource() -> list[Resource]:
    return [Resource(
        uri="my:resource://data",
        name="My Resource",
        description="My resource description",
        mimeType="application/json",
    )]

def read_my_resource(uri: str) -> str:
    data = fetch_data()
    return json.dumps(data)
```

2. Register in `server.py`:

```python
from .resources import my_resource

@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = []
    resources.extend(my_resource.get_my_resource())
    return resources
```

### Adding a New Tool

1. Create tool handler in `tools/`:

```python
def get_my_tool() -> list[Tool]:
    return [Tool(
        name="my_tool",
        description="My tool description",
        inputSchema={
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    )]

async def handle_my_tool(arguments: dict) -> list[TextContent]:
    result = do_something(arguments["param"])
    return [TextContent(type="text", text=result)]
```

2. Register in `server.py`:

```python
from .tools import my_tool

@server.list_tools()
async def list_tools() -> list:
    tools = []
    tools.extend(my_tool.get_my_tool())
    return tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    if name == "my_tool":
        return await my_tool.handle_my_tool(arguments)
```

## Security Considerations

### Authentication

For HTTP transport, authentication is handled via API keys:

```python
from .security.auth import AuthMiddleware

auth = AuthMiddleware(api_key="secret-key", enable_auth=True)
auth.authenticate(provided_key)
```

### Policy Enforcement

Package installation can be restricted:

```python
from .security.policy import PolicyEngine

policy = PolicyEngine(
    allowed_packages=["requests", "pytest.*"],
    blocked_packages=["malicious.*"]
)
policy.check_package("requests")  # OK
policy.check_package("malicious-pkg")  # Raises PolicyViolationError
```

### Audit Logging

All tool invocations are logged:

```python
from .security.audit import AuditLogger

audit = AuditLogger()
audit.log_tool_invocation(
    "install",
    parameters={"packages": ["requests"]},
    success=True
)
```

## Best Practices

1. **Error Handling**: Always handle errors gracefully and return meaningful messages
2. **Input Validation**: Validate all inputs before processing
3. **Logging**: Use structured logging for debugging and auditing
4. **Resource Efficiency**: Cache expensive operations when possible
5. **Security**: Never trust user input; validate and sanitize
6. **Documentation**: Document all resources and tools clearly

## Learning Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)

## Next Steps

1. Read the [architecture documentation](architecture.md)
2. Explore the codebase starting with `server.py`
3. Try extending the server with your own resources or tools
4. Review the [enterprise deployment guide](enterprise.md)
