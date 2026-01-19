# Usage Examples

This document provides examples of how to use the Python Package Manager MCP Server.

## Running the Server

### Stdio Transport (Local Development)

```bash
# Using the run script
./scripts/run_stdio.sh

# Using the CLI
python -m python_package_mcp_server.cli stdio

# Using uv directly
uv run python -m python_package_mcp_server.cli stdio
```

### HTTP Transport (Enterprise)

```bash
# Using the run script
./scripts/run_http.sh --host localhost --port 8000

# Using the CLI
python -m python_package_mcp_server.cli http --host localhost --port 8000

# In background
./scripts/run_http.sh --background
```

### Development Mode (Hot Reload)

```bash
# Using the dev script
./scripts/dev.sh

# Using the CLI
python -m python_package_mcp_server.cli dev --host localhost --port 8000
```

## Client Configuration

### Cursor IDE

Add to your Cursor settings (`.cursor/mcp_config.json`):

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "."
      }
    }
  }
}
```

### VS Code

The server can be configured in VS Code using the MCP extension. See `.vscode/launch.json` for debug configurations.

## Resource Examples

### List Installed Packages

```python
# Resource URI: python:packages://installed
# Returns JSON with list of installed packages
```

### Get Dependency Tree

```python
# Resource URI: python:dependencies://tree
# Returns JSON with dependency tree visualization
```

### Project Index

```python
# Resource URI: project://index
# Returns complete project index with structure, files, and metadata
```

### Search Codebase

```python
# Resource URI: codebase://search?pattern=def.*&extensions=.py
# Returns search results matching the pattern
```

## Tool Examples

### Install Packages

```json
{
  "name": "install",
  "arguments": {
    "packages": ["requests==2.31.0", "pytest"],
    "editable": false
  }
}
```

### Add Package to Project

```json
{
  "name": "add",
  "arguments": {
    "packages": ["fastapi"],
    "dev": false
  }
}
```

### Sync Environment

```json
{
  "name": "sync",
  "arguments": {}
}
```

### Index Project

```json
{
  "name": "index_project",
  "arguments": {
    "path": "/path/to/project"
  }
}
```

### Analyze Codebase

```json
{
  "name": "analyze_codebase",
  "arguments": {
    "path": "/path/to/project"
  }
}
```

## Environment Variables

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

## Example: Using with LLM

When integrated with an LLM assistant, you can ask questions like:

- "What packages are installed in this project?"
- "Show me the dependency tree"
- "Install the requests package"
- "What files are in this project?"
- "Search for all functions named 'handle_*'"
- "Show me the project structure"

The LLM will use the MCP server's resources and tools to answer these questions and perform actions.
