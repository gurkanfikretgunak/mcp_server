# Python Package Manager MCP Server

A production-ready MCP (Model Context Protocol) server for managing Python packages using `uv`, with enterprise features including security, auditing, and support for both stdio and HTTP transports. The server exposes resources (package lists, dependency trees, project indexing) and tools (install, uninstall, sync) while maintaining learning-focused documentation.

## Features

- **Package Management**: Install, uninstall, add, remove, sync, and lock Python packages using `uv`
- **Project Indexing**: Discover and index project structure for LLM-assisted development
- **Codebase Resources**: Search codebase, read files, extract symbols
- **Language Standards Support**: Dart and TypeScript language standards, style guides, and best practices
- **Code Quality Tools**: Format, lint, analyze, and validate code for Dart and TypeScript
- **Enterprise Features**: Role-based authentication (admin/user), policy engine, audit logging
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
- `MCP_API_KEY`: API key for HTTP authentication (legacy single API key mode)
- `MCP_ENABLE_AUTH`: Enable authentication (`true`/`false`)
- `MCP_ENABLE_USER_AUTH`: Enable user-based authentication (`true`/`false`)
- `MCP_USERS_FILE`: Path to users JSON file (default: `~/.mcp_server/users.json`)
- `MCP_SINGLE_API_KEY_MODE`: Use legacy single API key mode (`true`/`false`, default: `true`)
- `MCP_ALLOWED_PACKAGES`: Comma-separated list of allowed package patterns
- `MCP_BLOCKED_PACKAGES`: Comma-separated list of blocked package patterns
- `MCP_LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `MCP_LOG_FORMAT`: Log format (`json` or `text`)
- `MCP_PROJECT_ROOT`: Project root directory
- `MCP_WORKSPACE_ROOT`: Workspace root directory

## Authentication

The server supports role-based authentication with admin and regular user roles.

### Quick Setup

1. **Enable User Authentication**:
   ```bash
   export MCP_ENABLE_USER_AUTH=true
   export MCP_USERS_FILE=~/.mcp_server/users.json
   ```

2. **Create First Admin Account**:
   ```bash
   python -m python_package_mcp_server.cli create-admin --username admin --api-key <your-api-key>
   ```
   
   If you don't provide an API key, one will be auto-generated. **Save it securely** - it won't be shown again!

3. **Create Additional Users** (admin only):
   Use the `create_user` MCP tool via your client:
   ```json
   {
     "tool": "create_user",
     "arguments": {
       "username": "user1",
       "role": "user"
     }
   }
   ```

### User Roles

- **Admin (Level 1)**: Full access to all operations
  - Can create/delete users
  - Can execute all tools (install, uninstall, sync, etc.)
  - Can access all resources
  
- **Regular User**: Read-only access
  - Can read resources (packages, dependencies, codebase)
  - Cannot execute write operations (install, uninstall, sync, etc.)
  - Cannot create or delete users

### Permissions Matrix

| Operation | Admin | Regular User |
|-----------|-------|--------------|
| Read resources | ✅ | ✅ |
| Install packages | ✅ | ❌ |
| Uninstall packages | ✅ | ❌ |
| Sync dependencies | ✅ | ❌ |
| Create users | ✅ | ❌ |
| Delete users | ✅ | ❌ |
| List users | ✅ | ❌ |

### User Management Tools

The server provides the following user management tools (admin only):

- `create_user`: Create a new user account
  - Parameters: `username` (required), `api_key` (optional), `role` (admin/user, default: user)
  - Returns: Created user info with API key (save it securely!)

- `list_users`: List all users
  - Returns: List of all users with their roles and creation dates

- `delete_user`: Delete a user account
  - Parameters: `username` (required)
  - Note: Cannot delete the last admin user

### Configuration

**Environment Variables**:
```bash
# Enable user-based authentication
export MCP_ENABLE_USER_AUTH=true

# Set users file location (optional, defaults to ~/.mcp_server/users.json)
export MCP_USERS_FILE=~/.mcp_server/users.json

# For stdio transport, set API key for authentication
export MCP_API_KEY=<your-api-key>
```

**Users File** (`~/.mcp_server/users.json`):
```json
{
  "users": [
    {
      "username": "admin",
      "api_key_hash": "hashed-api-key",
      "role": "admin",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "username": "user1",
      "api_key_hash": "hashed-api-key-2",
      "role": "user",
      "created_at": "2024-01-02T00:00:00Z"
    }
  ]
}
```

**Security Notes**:
- API keys are stored as SHA-256 hashes
- Users file has restrictive permissions (`chmod 600`)
- Only the first account can be created via CLI (becomes admin)
- Subsequent accounts must be created by admin users via `create_user` tool
- The last admin user cannot be deleted

### Backward Compatibility

The server maintains backward compatibility with the legacy single API key mode:
- If `MCP_ENABLE_USER_AUTH=false` (default), uses single API key authentication
- If `MCP_ENABLE_USER_AUTH=true`, uses user-based authentication
- Existing installations continue working without changes

For detailed authentication setup instructions, see the [Authentication Setup Guide](docs/auth-setup-guide.md).

For configuration options, see the [MCP Configuration Guide](docs/mcp-configuration-guide.md).

## Prompts

The server provides the following prompts (reusable prompt templates):

- `analyze_package_dependencies` - Analyze package dependencies and suggest updates (optional: package_name)
- `code_review` - Review code for best practices and potential issues (required: file_path, optional: language)
- `project_setup_guide` - Generate a comprehensive project setup guide (optional: include_dependencies)
- `dependency_audit` - Audit project dependencies for security and updates (no arguments)
- `code_formatting_check` - Check if code follows formatting standards (required: file_path, language)

For detailed information about prompts, see the [Prompts Guide](docs/prompts-guide.md).

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

### Dart Standards Resources

- `dart:standards://effective-dart` - Effective Dart guidelines (style, documentation, usage)
- `dart:standards://style-guide` - Dart style guide with naming conventions and formatting rules
- `dart:standards://linter-rules` - Complete list of Dart linter rules and descriptions
- `dart:standards://best-practices` - Dart best practices for code quality and maintainability

### TypeScript Standards Resources

- `typescript:standards://style-guide` - TypeScript style guide with naming conventions and formatting rules
- `typescript:standards://tsconfig-options` - Recommended tsconfig.json compiler options and meanings
- `typescript:standards://eslint-rules` - ESLint rules for TypeScript code quality and consistency
- `typescript:standards://best-practices` - TypeScript best practices for type safety and code quality

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

### Dart Tools

- `dart_format` - Format Dart code according to Dart style guide
- `dart_analyze` - Analyze Dart code for errors and warnings
- `dart_fix` - Apply automated fixes to Dart code
- `dart_generate_code` - Generate Dart code following standards and best practices
- `dart_check_standards` - Check if Dart code follows standards and best practices

### TypeScript Tools

- `typescript_format` - Format TypeScript code using Prettier
- `typescript_lint` - Lint TypeScript code using ESLint
- `typescript_type_check` - Type check TypeScript code using tsc
- `typescript_generate_code` - Generate TypeScript code following standards and best practices
- `typescript_check_standards` - Check if TypeScript code follows standards and best practices

## Configuration

### Adding to mcp.json

To add this server to your `mcp.json` configuration file, see the [MCP Configuration Guide](docs/mcp-configuration-guide.md) for detailed instructions.

**Quick Start:**
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

**File Locations:**
- **Cursor IDE**: `~/.cursor/mcp.json` or `.cursor/mcp_config.json`
- **VS Code**: `.vscode/settings.json` (with MCP extension)
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## IDE Integration

### Quick Setup Script

Use the setup script to automatically configure your IDE:

```bash
# Interactive menu
./scripts/setup_ide.sh

# Or specify IDE directly
./scripts/setup_ide.sh cursor      # Setup Cursor IDE
./scripts/setup_ide.sh vscode      # Setup VS Code
./scripts/setup_ide.sh deeplink    # Generate deep link for Cursor
./scripts/setup_ide.sh all         # Setup all supported IDEs
```

**Windows PowerShell:**
```powershell
.\scripts\setup_ide.ps1 cursor
.\scripts\setup_ide.ps1 vscode
.\scripts\setup_ide.ps1 deeplink
.\scripts\setup_ide.ps1 all
```

### Cursor IDE

The server is pre-configured for Cursor IDE. Configuration is in `.cursor/mcp_config.json`.

**Deep Link Setup:**
Run `./scripts/setup_ide.sh deeplink` to generate a deep link that you can open in Cursor to automatically add the MCP server.

### VS Code

VS Code configuration files are provided in `.vscode/`:
- `settings.json` - Workspace settings
- `launch.json` - Debug configurations
- `extensions.json` - Recommended extensions

**Note:** VS Code MCP integration requires the [MCP Extension](https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.mcp).

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

### Testing Tools

- **Unit Tests**: Run `pytest tests/` for automated test suite
- **MCP Inspector**: Use `./scripts/inspect.sh` for interactive testing and debugging (see below)

### Testing with MCP Inspector

MCP Inspector is an interactive developer tool for testing and debugging MCP servers. It provides a web-based UI to inspect resources, test tools, and monitor server communication in real-time.

#### Prerequisites

- Node.js installed (for `npx` command)
- Python virtual environment set up

#### Running Inspector

**Linux/macOS:**
```bash
# Run inspector with stdio transport (default)
./scripts/inspect.sh

# Run inspector with HTTP transport
./scripts/inspect.sh --transport http --host localhost --port 8000

# Use custom ports
./scripts/inspect.sh --client-port 8080 --server-port 9000

# Run with debug logging
MCP_LOG_LEVEL=DEBUG ./scripts/inspect.sh
```

**Windows PowerShell:**
```powershell
# Run inspector with stdio transport (default)
.\scripts\inspect.ps1

# Run inspector with HTTP transport
.\scripts\inspect.ps1 -Transport http -Host localhost -Port 8000

# Use custom ports
.\scripts\inspect.ps1 -ClientPort 8080 -ServerPort 9000
```

#### Inspector Features

Once the inspector starts, it will open a web UI in your browser (default: `http://localhost:5173`). You can:

- **Resources Tab**: Browse and test all available resources
  - View `python:packages://installed` and `python:packages://outdated`
  - Test project index resources
  - Read Dart and TypeScript standards resources

- **Tools Tab**: Test all available tools interactively
  - Test package management tools (`install`, `uninstall`, `sync`)
  - Test Dart tools (`dart_format`, `dart_analyze`, `dart_fix`)
  - Test TypeScript tools (`typescript_format`, `typescript_lint`)

- **Logs Tab**: Monitor real-time JSON-RPC communication
  - View all requests and responses
  - Debug server communication
  - See errors and warnings

#### Transport Modes

1. **Stdio Mode** (default): Direct connection to Python server
   - Best for local development and testing
   - No separate server process needed

2. **HTTP Mode**: Connect to running HTTP server
   - Requires server to be running separately: `./scripts/run_http.sh`
   - Useful for testing enterprise deployments
   - Supports authentication headers

#### Troubleshooting

**Inspector doesn't start:**
- Ensure Node.js is installed: `node --version`
- Try: `npx -y @modelcontextprotocol/inspector@latest`

**Port conflicts:**
- Use custom ports: `./scripts/inspect.sh --client-port 8080`
- Check if ports are already in use

**HTTP mode connection fails:**
- Ensure HTTP server is running: `./scripts/run_http.sh`
- Check host and port match server configuration
- Verify authentication if enabled

#### Comprehensive Guide

For detailed step-by-step instructions, examples, and troubleshooting, see the [MCP Inspector Usage Guide](docs/inspector-guide.md). This guide covers:
- Detailed walkthrough of all resources and tools
- Practical workflow examples
- Troubleshooting common issues
- Best practices for using the inspector

For more information, see the [official MCP Inspector documentation](https://modelcontextprotocol.io/docs/tools/inspector).

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Gurkan Fikret Gunak

## Author

**Gurkan Fikret Gunak** ([@gurkanfikretgunak](https://github.com/gurkanfikretgunak))

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
