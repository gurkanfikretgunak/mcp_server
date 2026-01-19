# Python Package Manager MCP Server

A production-ready MCP (Model Context Protocol) server for managing Python packages using `uv`, with enterprise features including security, auditing, and support for both stdio and HTTP transports. The server exposes resources (package lists, dependency trees, project indexing) and tools (install, uninstall, sync) while maintaining learning-focused documentation.

## Features

- **Package Management**: Install, uninstall, add, remove, sync, and lock Python packages using `uv`
- **Project Indexing**: Discover and index project structure for LLM-assisted development
- **Codebase Resources**: Search codebase, read files, extract symbols
- **Enterprise Features**: Authentication, policy engine, audit logging
- **Dual Transport**: Support for stdio (local) and HTTP/SSE (enterprise) transports
- **IDE Integration**: Pre-configured for Cursor and VS Code
- **Easy Execution**: Simple scripts and CLI commands for Linux/macOS

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager installed

### Installation

```bash
# Clone the repository
git clone https://github.com/gurkanfikretgunak/mcp_server.git
cd mcp_server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Running the Server

#### Stdio Transport (Local Development)

```bash
# Using the run script
./scripts/run_stdio.sh

# Using the CLI
python -m python_package_mcp_server.cli stdio
```

#### HTTP Transport (Enterprise)

```bash
# Using the run script
./scripts/run_http.sh --host localhost --port 8000

# Using the CLI
python -m python_package_mcp_server.cli http --host localhost --port 8000
```

#### Development Mode (Hot Reload)

```bash
# Using the dev script
./scripts/dev.sh

# Using the CLI
python -m python_package_mcp_server.cli dev
```

## Configuration

The server can be configured using environment variables:

- `MCP_TRANSPORT`: Transport type (`stdio` or `http`)
- `MCP_HOST`: HTTP server host (default: `localhost`)
- `MCP_PORT`: HTTP server port (default: `8000`)
- `MCP_API_KEY`: API key for HTTP authentication
- `MCP_ENABLE_AUTH`: Enable authentication (`true`/`false`)
- `MCP_ALLOWED_PACKAGES`: Comma-separated list of allowed package patterns
- `MCP_BLOCKED_PACKAGES`: Comma-separated list of blocked package patterns
- `MCP_LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `MCP_LOG_FORMAT`: Log format (`json` or `text`)
- `MCP_PROJECT_ROOT`: Project root directory
- `MCP_WORKSPACE_ROOT`: Workspace root directory

## Resources

The server exposes the following resources:

### Package Management Resources

- `python:packages://installed` - List all installed packages with versions
- `python:packages://outdated` - List packages with available updates
- `python:dependencies://tree` - Dependency tree visualization
- `python:project://info` - Project metadata (pyproject.toml, uv.lock info)
- `python:environment://active` - Active virtual environment details

### Project Index Resources

- `project://index` - Complete project index with structure, files, and metadata
- `project://structure` - File and directory structure tree
- `project://config` - Configuration files discovery
- `project://dependencies` - All dependency files across project types
- `project://readme` - README and documentation files
- `project://entrypoints` - Entry points and main files discovery
- `project://tests` - Test files and test structure

### Codebase Resources

- `codebase://search` - Search codebase by pattern or content
- `codebase://file` - Read specific file content with line numbers
- `codebase://symbols` - Extract symbols (functions, classes) from codebase

## Tools

The server provides the following tools:

### Package Management Tools

- `install` - Install package(s) with version constraints
- `uninstall` - Remove package(s)
- `add` - Add package to project dependencies
- `remove` - Remove package from project dependencies
- `sync` - Sync environment with lock file
- `lock` - Generate/update lock file
- `init` - Initialize new Python project
- `upgrade` - Upgrade package(s) to latest versions

### Project Indexing Tools

- `index_project` - Index/scan a project directory and build resource cache
- `refresh_index` - Refresh project index cache
- `discover_projects` - Discover multiple projects in a workspace
- `analyze_codebase` - Analyze codebase structure and extract metadata

## IDE Integration

### Cursor IDE

The server is pre-configured for Cursor IDE. Configuration is in `.cursor/mcp_config.json`.

### VS Code

VS Code configuration files are provided in `.vscode/`:
- `settings.json` - Workspace settings
- `launch.json` - Debug configurations
- `extensions.json` - Recommended extensions

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Learning Guide

See [docs/learning.md](docs/learning.md) for a comprehensive guide on how MCP servers work and how to extend this server.

## Enterprise Deployment

See [docs/enterprise.md](docs/enterprise.md) for enterprise deployment guidelines and security best practices.

## Examples

See [examples/usage.md](examples/usage.md) for usage examples and [examples/client_config.json](examples/client_config.json) for client configuration examples.

## Development

### Running Tests

```bash
uv pip install -e ".[dev]"
pytest tests/
```

### Code Formatting

```bash
black src/
ruff check src/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Gurkan Fikret Gunak

## Author

**Gurkan Fikret Gunak** ([@gurkanfikretgunak](https://github.com/gurkanfikretgunak))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
