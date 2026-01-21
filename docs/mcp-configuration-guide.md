# MCP Configuration Guide

This guide explains how to add the Python Package Manager MCP Server to your `mcp.json` configuration file for various MCP clients.

## Table of Contents

1. [Configuration File Locations](#configuration-file-locations)
2. [Basic Configuration](#basic-configuration)
3. [Advanced Configuration](#advanced-configuration)
4. [IDE-Specific Setup](#ide-specific-setup)
5. [Using Setup Scripts](#using-setup-scripts)
6. [Manual Configuration](#manual-configuration)
7. [Troubleshooting](#troubleshooting)

## Configuration File Locations

The location of `mcp.json` depends on your MCP client:

### Cursor IDE

**Location:** `~/.cursor/mcp.json` (macOS/Linux) or `%APPDATA%\Cursor\mcp.json` (Windows)

**Alternative:** `.cursor/mcp_config.json` in your project root (project-specific)

### VS Code (with MCP Extension)

**Location:** Workspace settings or user settings

**File:** `.vscode/settings.json` or `settings.json` in your user directory

### Other MCP Clients

Check your client's documentation for the configuration file location.

## Basic Configuration

### Minimal Configuration

The simplest configuration for stdio transport:

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ]
    }
  }
}
```

### Standard Configuration

Recommended configuration with environment variables:

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

### Using Virtual Environment

If you're using a virtual environment:

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "/path/to/.venv/bin/python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": ".venv/bin/python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
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
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

## Advanced Configuration

### With Custom Project Root

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "/path/to/your/project",
        "MCP_LOG_LEVEL": "DEBUG",
        "MCP_LOG_FORMAT": "text"
      }
    }
  }
}
```

### With Package Policy

Restrict which packages can be installed:

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_ALLOWED_PACKAGES": "requests,pytest,fastapi",
        "MCP_BLOCKED_PACKAGES": "malicious-package",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

### HTTP Transport Configuration

For HTTP/SSE transport (requires server running separately):

```json
{
  "mcpServers": {
    "python-package-manager-http": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "http"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_HOST": "localhost",
        "MCP_PORT": "8000",
        "MCP_API_KEY": "your-secret-api-key",
        "MCP_ENABLE_AUTH": "true",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

**Note:** For HTTP transport, you need to start the server separately:
```bash
./scripts/run_http.sh --host localhost --port 8000
```

### Multiple Server Instances

You can configure multiple instances with different settings:

```json
{
  "mcpServers": {
    "python-package-manager-dev": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "/path/to/dev/project",
        "MCP_LOG_LEVEL": "DEBUG",
        "MCP_LOG_FORMAT": "text"
      }
    },
    "python-package-manager-prod": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "/path/to/prod/project",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json",
        "MCP_ALLOWED_PACKAGES": "requests,pytest"
      }
    }
  }
}
```

## IDE-Specific Setup

### Cursor IDE

#### Option 1: Global Configuration

**File:** `~/.cursor/mcp.json` (macOS/Linux) or `%APPDATA%\Cursor\mcp.json` (Windows)

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

#### Option 2: Project-Specific Configuration

**File:** `.cursor/mcp_config.json` in your project root

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

**Note:** Cursor IDE may use either `mcp.json` or `mcp_config.json`. Check your Cursor version.

### VS Code (with MCP Extension)

**File:** `.vscode/settings.json` in your workspace

```json
{
  "mcp.servers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "${workspaceFolder}",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

**Note:** VS Code MCP extension may use different configuration format. Check extension documentation.

### Claude Desktop

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

## Using Setup Scripts

### Automated Setup (Recommended)

The easiest way to configure the server is using the provided setup scripts:

**Linux/macOS:**
```bash
./scripts/setup_ide.sh cursor
```

**Windows PowerShell:**
```powershell
.\scripts\setup_ide.ps1 cursor
```

This will:
1. Detect your Python installation
2. Create or update the configuration file
3. Set up environment variables
4. Provide instructions for restarting your IDE

### Interactive Setup

Run the script without arguments for an interactive menu:

**Linux/macOS:**
```bash
./scripts/setup_ide.sh
```

**Windows PowerShell:**
```powershell
.\scripts\setup_ide.ps1
```

You'll be prompted to:
1. Select your IDE (Cursor, VS Code, or both)
2. Choose configuration location
3. Set environment variables

## Manual Configuration

### Step-by-Step Manual Setup

1. **Locate Configuration File**

   **Cursor IDE:**
   - macOS/Linux: `~/.cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\mcp.json`
   - Project-specific: `.cursor/mcp_config.json`

2. **Create or Edit Configuration File**

   If the file doesn't exist, create it with this structure:
   ```json
   {
     "mcpServers": {}
   }
   ```

3. **Add Server Configuration**

   Add your server to the `mcpServers` object:

   ```json
   {
     "mcpServers": {
       "python-package-manager": {
         "command": "python",
         "args": [
           "-m",
           "python_package_mcp_server.cli",
           "stdio"
         ],
         "env": {
           "MCP_PROJECT_ROOT": ".",
           "MCP_LOG_LEVEL": "INFO",
           "MCP_LOG_FORMAT": "json"
         }
       }
     }
   }
   ```

4. **Verify Python Path**

   Make sure `python` points to the correct Python installation:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

   If using a virtual environment, use the full path:
   ```json
   "command": "/absolute/path/to/.venv/bin/python"
   ```

5. **Restart Your IDE**

   After saving the configuration, restart your IDE to load the MCP server.

### Adding to Existing Configuration

If you already have other MCP servers configured:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "other-command",
      "args": ["arg1", "arg2"]
    },
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

## Configuration Options

### Environment Variables

All configuration options are set via environment variables in the `env` section:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MCP_PROJECT_ROOT` | Project root directory | `.` | `/path/to/project` |
| `MCP_LOG_LEVEL` | Logging level | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `MCP_LOG_FORMAT` | Log format | `json` | `json`, `text` |
| `MCP_HOST` | HTTP server host | `localhost` | `0.0.0.0` |
| `MCP_PORT` | HTTP server port | `8000` | `8080` |
| `MCP_API_KEY` | API key for HTTP auth (legacy mode) | `None` | `your-secret-key` |
| `MCP_ENABLE_AUTH` | Enable authentication | `false` | `true`, `false` |
| `MCP_ENABLE_USER_AUTH` | Enable user-based authentication | `false` | `true`, `false` |
| `MCP_USERS_FILE` | Path to users JSON file | `~/.mcp_server/users.json` | `/path/to/users.json` |
| `MCP_SINGLE_API_KEY_MODE` | Use legacy single API key mode | `true` | `true`, `false` |
| `MCP_ALLOWED_PACKAGES` | Allowed package patterns | `[]` | `requests,pytest.*` |
| `MCP_BLOCKED_PACKAGES` | Blocked package patterns | `[]` | `malicious.*` |

### Command Arguments

The `args` array specifies command-line arguments:

- `stdio`: Use stdio transport (default, recommended for local development)
- `http`: Use HTTP/SSE transport (for remote deployments)

### Full Configuration Example

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "/Users/username/my-project",
        "MCP_LOG_LEVEL": "DEBUG",
        "MCP_LOG_FORMAT": "text",
        "MCP_ALLOWED_PACKAGES": "requests,pytest,fastapi",
        "MCP_BLOCKED_PACKAGES": "malicious-package"
      }
    }
  }
}
```

## Troubleshooting

### Server Not Starting

**Issue:** Server doesn't start or appears offline

**Solutions:**
1. **Check Python Path:**
   ```bash
   python --version
   python -m python_package_mcp_server.cli --help
   ```

2. **Verify Installation:**
   ```bash
   pip list | grep python-package-mcp-server
   ```

3. **Check Logs:**
   - Look for error messages in IDE console
   - Check server logs if `MCP_LOG_FORMAT` is set to `text`

4. **Test Manually:**
   ```bash
   python -m python_package_mcp_server.cli stdio
   ```

### Configuration Not Loading

**Issue:** Changes to `mcp.json` not taking effect

**Solutions:**
1. **Restart IDE:** Always restart your IDE after changing configuration
2. **Check File Location:** Verify you're editing the correct file
3. **Validate JSON:** Ensure JSON is valid (no trailing commas, proper quotes)
4. **Check File Permissions:** Ensure the file is readable

### Python Path Issues

**Issue:** "python: command not found" or wrong Python version

**Solutions:**
1. **Use Full Path:**
   ```json
   "command": "/usr/bin/python3"
   ```

2. **Use Virtual Environment:**
   ```json
   "command": ".venv/bin/python"
   ```

3. **Use Python Version:**
   ```json
   "command": "python3"
   ```

### Environment Variables Not Working

**Issue:** Environment variables not being applied

**Solutions:**
1. **Check JSON Syntax:** Ensure `env` is properly formatted
2. **Use Absolute Paths:** For `MCP_PROJECT_ROOT`, use absolute paths
3. **Restart IDE:** Environment variables are loaded on startup
4. **Check Variable Names:** Ensure exact variable names (case-sensitive)

### Multiple Servers Conflict

**Issue:** Multiple server instances conflicting

**Solutions:**
1. **Use Different Names:** Give each instance a unique name
2. **Use Different Ports:** For HTTP transport, use different ports
3. **Separate Projects:** Use different `MCP_PROJECT_ROOT` values

## Verification

### Test Configuration

After adding the server, verify it's working:

1. **Check Server Status:**
   - In Cursor: Check MCP server status in settings
   - In VS Code: Check MCP extension status

2. **Test with MCP Inspector:**
   ```bash
   ./scripts/inspect.sh
   ```
   - Should show all resources, prompts, and tools
   - Should be able to read resources
   - Should be able to call tools

3. **Test in IDE:**
   - Ask your LLM assistant to list installed packages
   - Try using resources or tools through the LLM

### Common Verification Commands

```bash
# Test server directly
python -m python_package_mcp_server.cli stdio

# Test with inspector
./scripts/inspect.sh

# Check Python installation
python --version
python -m python_package_mcp_server.cli --help

# Verify package installation
pip show python-package-mcp-server
```

## Best Practices

1. **Use Virtual Environments:**
   - Always use a virtual environment for Python projects
   - Point `command` to the venv Python executable

2. **Project-Specific Configuration:**
   - Use `.cursor/mcp_config.json` for project-specific settings
   - Use global `mcp.json` for default settings

3. **Environment Variables:**
   - Use absolute paths for `MCP_PROJECT_ROOT`
   - Set appropriate log levels (DEBUG for development, INFO for production)

4. **Security:**
   - Never commit API keys to version control
   - Use environment variables or secure storage for secrets
   - Enable authentication for HTTP transport

5. **Testing:**
   - Test configuration with MCP Inspector before using in IDE
   - Verify server starts correctly
   - Test a few resources and tools

## Examples

### Development Configuration

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": ".venv/bin/python",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "${workspaceFolder}",
        "MCP_LOG_LEVEL": "DEBUG",
        "MCP_LOG_FORMAT": "text"
      }
    }
  }
}
```

### Production Configuration

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "/usr/bin/python3",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "/opt/my-project",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json",
        "MCP_ALLOWED_PACKAGES": "requests,pytest"
      }
    }
  }
}
```

### Multi-Project Configuration

```json
{
  "mcpServers": {
    "project-a": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "/path/to/project-a"
      }
    },
    "project-b": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "/path/to/project-b"
      }
    }
  }
}
```

## Authentication Configuration

### User-Based Authentication

For multi-user deployments, enable user-based authentication:

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "~/.mcp_server/users.json",
        "MCP_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

**First Admin Setup**:
```bash
python -m python_package_mcp_server.cli create-admin --username admin
```

**User Roles**:
- **Admin**: Full access to all operations
- **Regular User**: Read-only access (resources only)

For detailed authentication documentation, see the [README](../README.md#authentication).

## Additional Resources

- [Setup Scripts](../scripts/setup_ide.sh) - Automated configuration
- [Examples](../examples/client_config.json) - Example configurations
- [README](../README.md) - Server documentation
- [Inspector Guide](inspector-guide.md) - Testing your configuration

## Quick Reference

### Minimal Config
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"]
    }
  }
}
```

### Recommended Config
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

### With Virtual Environment
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": ".venv/bin/python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```
