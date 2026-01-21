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

### Quick Setup

**Automated Setup (Recommended):**
```bash
# Linux/macOS
./scripts/setup_ide.sh cursor

# Windows PowerShell
.\scripts\setup_ide.ps1 cursor
```

### Manual Configuration

#### Cursor IDE

**Option 1: Global Configuration** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

**Option 2: Project-Specific** (`.cursor/mcp_config.json`):
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

#### VS Code

The server can be configured in VS Code using the MCP extension. See `.vscode/launch.json` for debug configurations.

**Configuration** (`.vscode/settings.json`):
```json
{
  "mcp.servers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "${workspaceFolder}",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Using Virtual Environment

If using a virtual environment, use the venv Python path:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": ".venv/bin/python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "."
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": ".venv\\Scripts\\python.exe",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "."
      }
    }
  }
}
```

For detailed configuration options, see the [MCP Configuration Guide](../docs/mcp-configuration-guide.md).

## Authentication Examples

### Setting Up User Authentication

1. **Enable User Authentication**:
   ```bash
   export MCP_ENABLE_USER_AUTH=true
   export MCP_USERS_FILE=~/.mcp_server/users.json
   ```

2. **Create First Admin Account**:
   ```bash
   # With auto-generated API key
   python -m python_package_mcp_server.cli create-admin --username admin
   
   # With custom API key
   python -m python_package_mcp_server.cli create-admin --username admin --api-key my-secure-key-123
   ```

3. **Create Additional Users** (via MCP tool, admin only):
   ```json
   {
     "tool": "create_user",
     "arguments": {
       "username": "developer1",
       "role": "user"
     }
   }
   ```

### Using Authentication

**HTTP Transport**:
```bash
# Include API key in request headers
curl -H "X-API-Key: your-api-key" http://localhost:8000/health
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/health
```

**Stdio Transport**:
```bash
# Set API key in environment
export MCP_API_KEY=your-api-key
python -m python_package_mcp_server.cli stdio
```

**Client Configuration with API Key**:
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### User Management Examples

**List All Users** (admin only):
```json
{
  "tool": "list_users",
  "arguments": {}
}
```

**Delete a User** (admin only):
```json
{
  "tool": "delete_user",
  "arguments": {
    "username": "user1"
  }
}
```

**Note**: Cannot delete the last admin user.

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

## Dart Tool Examples

### Format Dart Code

```json
{
  "name": "dart_format",
  "arguments": {
    "paths": ["lib/main.dart"],
    "line_length": 80
  }
}
```

### Analyze Dart Code

```json
{
  "name": "dart_analyze",
  "arguments": {
    "paths": ["lib/"]
  }
}
```

### Apply Dart Fixes

```json
{
  "name": "dart_fix",
  "arguments": {
    "paths": ["lib/main.dart"]
  }
}
```

### Generate Dart Code

```json
{
  "name": "dart_generate_code",
  "arguments": {
    "code_description": "Create a User class with name and email fields",
    "file_path": "lib/models/user.dart",
    "include_tests": true
  }
}
```

### Check Dart Standards

```json
{
  "name": "dart_check_standards",
  "arguments": {
    "file_path": "lib/main.dart"
  }
}
```

## TypeScript Tool Examples

### Format TypeScript Code

```json
{
  "name": "typescript_format",
  "arguments": {
    "paths": ["src/index.ts"]
  }
}
```

### Lint TypeScript Code

```json
{
  "name": "typescript_lint",
  "arguments": {
    "paths": ["src/"]
  }
}
```

### Type Check TypeScript Code

```json
{
  "name": "typescript_type_check",
  "arguments": {
    "project_path": "tsconfig.json"
  }
}
```

### Generate TypeScript Code

```json
{
  "name": "typescript_generate_code",
  "arguments": {
    "code_description": "Create a User interface with name and email properties",
    "file_path": "src/types/user.ts",
    "include_tests": true
  }
}
```

### Check TypeScript Standards

```json
{
  "name": "typescript_check_standards",
  "arguments": {
    "file_path": "src/index.ts"
  }
}
```

## Resource Examples (Dart & TypeScript)

### Read Dart Standards

```python
# Resource URI: dart:standards://effective-dart
# Returns Effective Dart guidelines

# Resource URI: dart:standards://style-guide
# Returns Dart style guide

# Resource URI: dart:standards://linter-rules
# Returns Dart linter rules

# Resource URI: dart:standards://best-practices
# Returns Dart best practices
```

### Read TypeScript Standards

```python
# Resource URI: typescript:standards://style-guide
# Returns TypeScript style guide

# Resource URI: typescript:standards://tsconfig-options
# Returns TypeScript tsconfig options

# Resource URI: typescript:standards://eslint-rules
# Returns TypeScript ESLint rules

# Resource URI: typescript:standards://best-practices
# Returns TypeScript best practices
```

## Testing with MCP Inspector

MCP Inspector provides an interactive web-based UI for testing and debugging the MCP server. It's an excellent tool for exploring available resources and tools.

### Running Inspector

**Basic usage:**
```bash
# Linux/macOS
./scripts/inspect.sh

# Windows PowerShell
.\scripts\inspect.ps1
```

The inspector will:
1. Start the MCP server via stdio transport
2. Launch a web UI at `http://localhost:5173`
3. Open the UI in your default browser

### Testing Resources

In the Inspector UI, navigate to the **Resources** tab to:

1. **Browse available resources:**
   - `python:packages://installed` - View installed packages
   - `python:packages://outdated` - Check for outdated packages
   - `project://index` - Explore project structure
   - `dart:standards://effective-dart` - Read Dart guidelines
   - `typescript:standards://style-guide` - Read TypeScript style guide

2. **Read resource content:**
   - Click on any resource to fetch its content
   - View JSON responses in formatted view
   - Test resource subscriptions

### Testing Tools

In the **Tools** tab, you can:

1. **Test package management:**
   ```json
   {
     "name": "install",
     "arguments": {
       "packages": ["requests"],
       "editable": false
     }
   }
   ```

2. **Test Dart tools:**
   ```json
   {
     "name": "dart_format",
     "arguments": {
       "paths": ["lib/main.dart"],
       "line_length": 80
     }
   }
   ```

3. **Test TypeScript tools:**
   ```json
   {
     "name": "typescript_lint",
     "arguments": {
       "paths": ["src/"]
     }
   }
   ```

### Monitoring Communication

The **Logs** tab shows:
- Real-time JSON-RPC messages
- Request/response pairs
- Error messages and warnings
- Server state changes

### HTTP Transport Mode

To test with HTTP transport:

1. **Start HTTP server in one terminal:**
   ```bash
   ./scripts/run_http.sh --host localhost --port 8000
   ```

2. **Run inspector in another terminal:**
   ```bash
   ./scripts/inspect.sh --transport http --host localhost --port 8000
   ```

### Environment Variables

You can configure the inspector with environment variables:

```bash
# Set project root
MCP_PROJECT_ROOT=/path/to/project ./scripts/inspect.sh

# Enable debug logging
MCP_LOG_LEVEL=DEBUG ./scripts/inspect.sh

# Use custom ports
CLIENT_PORT=8080 SERVER_PORT=9000 ./scripts/inspect.sh
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
- "Format my Dart code according to style guide"
- "Check if my TypeScript code follows best practices"
- "Show me the Dart linter rules"
- "Generate TypeScript code for a User interface"
- "Analyze my Dart code for errors"

The LLM will use the MCP server's resources and tools to answer these questions and perform actions.
