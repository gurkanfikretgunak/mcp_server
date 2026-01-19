# Architecture Documentation

This document provides a detailed overview of the Python Package Manager MCP Server architecture.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (Cursor/VS Code)              │
└──────────────────────┬──────────────────────────────────────┘
                       │ JSON-RPC over Transport
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼─────┐                ┌─────▼─────┐
   │  Stdio   │                │   HTTP    │
   │Transport │                │Transport  │
   └────┬─────┘                └─────┬─────┘
        │                             │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │     MCP Server Core          │
        │  (server.py)                 │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
   ┌────▼─────┐                ┌─────▼─────┐
   │Resources│                │   Tools    │
   │ Manager │                │  Manager   │
   └────┬─────┘                └─────┬─────┘
        │                             │
   ┌────┴─────────────────────────────┴────┐
   │                                       │
┌──▼──────────┐              ┌─────────────▼──┐
│ Package     │              │ Project        │
│ Manager     │              │ Scanner        │
│ Wrapper     │              │                │
└──┬──────────┘              └─────────────┬──┘
   │                                       │
   │                                       │
┌──▼──────────┐              ┌─────────────▼──┐
│   UV CLI    │              │  File System   │
│ (subprocess)│              │                │
└─────────────┘              └────────────────┘
```

## Component Overview

### Core Server (`server.py`)

The main server component that:
- Initializes the MCP server
- Registers resources and tools
- Handles transport setup
- Routes requests to appropriate handlers

### Resources

Resources are organized by domain:

#### Package Resources (`resources/packages.py`)
- `python:packages://installed` - Installed packages list
- `python:packages://outdated` - Outdated packages list

#### Dependency Resources (`resources/dependencies.py`)
- `python:dependencies://tree` - Dependency tree
- `python:project://info` - Project metadata
- `python:environment://active` - Environment info

#### Project Index Resources (`resources/project_index.py`)
- `project://index` - Complete project index
- `project://structure` - File structure
- `project://config` - Config files
- `project://dependencies` - Dependency files
- `project://readme` - Documentation files
- `project://entrypoints` - Entry points
- `project://tests` - Test files

#### Codebase Resources (`resources/codebase.py`)
- `codebase://search` - Codebase search
- `codebase://file` - File content
- `codebase://symbols` - Code symbols

### Tools

Tools are organized by functionality:

#### Install Tools (`tools/install.py`)
- `install` - Install packages
- `uninstall` - Uninstall packages

#### Sync Tools (`tools/sync.py`)
- `add` - Add to project dependencies
- `remove` - Remove from project dependencies
- `sync` - Sync environment
- `lock` - Generate lock file

#### Environment Tools (`tools/env.py`)
- `init` - Initialize project
- `upgrade` - Upgrade packages
- `index_project` - Index project
- `refresh_index` - Refresh index
- `discover_projects` - Discover projects
- `analyze_codebase` - Analyze codebase

### Utilities

#### Package Manager Wrapper (`utils/package_manager_wrapper.py`)
- Safe execution of `uv` commands
- Command result parsing
- Error handling

#### Project Scanner (`utils/project_scanner.py`)
- File system scanning
- Project structure analysis
- Symbol extraction
- Codebase search

### Security

#### Authentication (`security/auth.py`)
- API key validation
- Request authentication middleware

#### Policy Engine (`security/policy.py`)
- Package allow/block lists
- Policy enforcement

#### Audit Logger (`security/audit.py`)
- Tool invocation logging
- Resource access logging
- Security event logging

### Configuration (`config.py`)

Centralized configuration management:
- Environment variable loading
- Configuration validation
- Default values

### Transports

#### Stdio Transport (`transports/stdio.py`)
- Standard input/output communication
- Local development use case

#### HTTP Transport (`transports/http.py`)
- HTTP/SSE communication
- Enterprise deployment use case
- FastAPI integration

## Data Flow

### Resource Request Flow

1. Client sends resource request: `python:packages://installed`
2. Server routes to `read_resource()` handler
3. Handler calls `PackageManagerWrapper.list_installed()`
4. Wrapper executes `uv pip list --format json`
5. Result parsed and returned as JSON
6. Server sends response to client

### Tool Invocation Flow

1. Client sends tool call: `install` with `{"packages": ["requests"]}`
2. Server routes to `call_tool()` handler
3. Handler validates input and checks policy
4. Handler calls `PackageManagerWrapper.install_packages()`
5. Wrapper executes `uv pip install requests`
6. Result logged via audit logger
7. Server sends response to client

## Security Architecture

### Authentication Flow

```
Request → Auth Middleware → Policy Check → Tool Execution → Audit Log
```

1. Request arrives with API key (if HTTP transport)
2. Auth middleware validates API key
3. Policy engine checks if action is allowed
4. Tool executes if authorized
5. Audit logger records the action

### Policy Enforcement

Policies are checked at multiple levels:

1. **Package Level**: Before installing/adding packages
2. **Tool Level**: Before executing tools
3. **Resource Level**: Before accessing sensitive resources

## Error Handling

Errors are handled at multiple layers:

1. **Command Execution**: Wrapper catches subprocess errors
2. **Resource Access**: Resources handle file system errors
3. **Tool Execution**: Tools handle business logic errors
4. **Server Level**: Server handles protocol errors

All errors are:
- Logged with context
- Returned with meaningful messages
- Audited for security review

## Performance Considerations

### Caching

- Project index can be cached
- Package lists can be cached (with TTL)
- Dependency trees can be cached

### Optimization

- Lazy loading of resources
- Parallel execution where possible
- Efficient file system scanning

## Extension Points

### Adding Resources

1. Create resource module in `resources/`
2. Implement `get_*_resources()` and `read_*_resource()`
3. Register in `server.py`

### Adding Tools

1. Create tool module in `tools/`
2. Implement `get_*_tools()` and `handle_*()`
3. Register in `server.py`

### Adding Security Features

1. Extend `AuthMiddleware` for custom auth
2. Extend `PolicyEngine` for custom policies
3. Extend `AuditLogger` for custom logging

## Deployment Architecture

### Local Development

```
Developer Machine
  └─ Stdio Transport
      └─ MCP Server
          └─ UV CLI
```

### Enterprise Deployment

```
Load Balancer
  └─ HTTP Transport (Multiple Instances)
      └─ MCP Server
          ├─ Auth Middleware
          ├─ Policy Engine
          └─ UV CLI (Isolated)
```

## Monitoring and Observability

### Logging

- Structured logging with `structlog`
- JSON format for log aggregation
- Different log levels (DEBUG, INFO, WARNING, ERROR)

### Metrics

- Tool invocation counts
- Resource access counts
- Error rates
- Response times

### Health Checks

- `/health` endpoint for HTTP transport
- Dependency checks (uv availability)
- Configuration validation

## Future Enhancements

- WebSocket transport support
- GraphQL API for resources
- Plugin system for extensions
- Distributed caching
- Rate limiting per client
- Multi-project workspace support
