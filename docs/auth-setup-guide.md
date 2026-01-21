# Authentication Setup Guide

This guide explains where and how to add authentication information for the MCP server.

## Table of Contents

1. [Where to Add Auth Info](#where-to-add-auth-info)
2. [Method 1: Environment Variables](#method-1-environment-variables)
3. [Method 2: .env File](#method-2-env-file)
4. [Method 3: mcp.json Configuration](#method-3-mcpjson-configuration)
5. [Method 4: User-Based Authentication](#method-4-user-based-authentication)
6. [Quick Reference](#quick-reference)

## Where to Add Auth Info

Authentication information can be configured in multiple places:

1. **Environment Variables** - System-wide or session-specific
2. **`.env` File** - Project-specific (recommended for development)
3. **`mcp.json`** - IDE client configuration (for Cursor, VS Code, etc.)
4. **Users File** - For user-based authentication (`~/.mcp_server/users.json`)

## Method 1: Environment Variables

### Linux/macOS

**Temporary (current session only):**
```bash
export MCP_ENABLE_AUTH=true
export MCP_API_KEY="your-secure-api-key-here"
export MCP_ENABLE_USER_AUTH=true
export MCP_USERS_FILE=~/.mcp_server/users.json
```

**Permanent (add to shell profile):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export MCP_ENABLE_AUTH=true' >> ~/.bashrc
echo 'export MCP_API_KEY="your-secure-api-key-here"' >> ~/.bashrc
echo 'export MCP_ENABLE_USER_AUTH=true' >> ~/.bashrc
echo 'export MCP_USERS_FILE=~/.mcp_server/users.json' >> ~/.bashrc

# Reload shell
source ~/.bashrc
```

### Windows PowerShell

**Temporary (current session only):**
```powershell
$env:MCP_ENABLE_AUTH = "true"
$env:MCP_API_KEY = "your-secure-api-key-here"
$env:MCP_ENABLE_USER_AUTH = "true"
$env:MCP_USERS_FILE = "$env:USERPROFILE\.mcp_server\users.json"
```

**Permanent (add to PowerShell profile):**
```powershell
# Add to $PROFILE
Add-Content $PROFILE "`$env:MCP_ENABLE_AUTH = 'true'"
Add-Content $PROFILE "`$env:MCP_API_KEY = 'your-secure-api-key-here'"
Add-Content $PROFILE "`$env:MCP_ENABLE_USER_AUTH = 'true'"
Add-Content $PROFILE "`$env:MCP_USERS_FILE = '`$env:USERPROFILE\.mcp_server\users.json'"
```

### Windows CMD

```cmd
set MCP_ENABLE_AUTH=true
set MCP_API_KEY=your-secure-api-key-here
set MCP_ENABLE_USER_AUTH=true
set MCP_USERS_FILE=%USERPROFILE%\.mcp_server\users.json
```

## Method 2: .env File

Create a `.env` file in your project root directory:

**File: `.env`** (in project root)
```bash
# Authentication Settings
MCP_ENABLE_AUTH=true
MCP_API_KEY=your-secure-api-key-here

# User-Based Authentication
MCP_ENABLE_USER_AUTH=true
MCP_USERS_FILE=~/.mcp_server/users.json

# Server Settings
MCP_HOST=localhost
MCP_PORT=8000
MCP_PROJECT_ROOT=.

# Logging
MCP_LOG_LEVEL=INFO
MCP_LOG_FORMAT=json
```

**Important:**
- Add `.env` to `.gitignore` to prevent committing secrets
- The server automatically loads `.env` files using `python-dotenv`
- Use `.env.example` as a template (without actual secrets)

**Example `.env.example`:**
```bash
# Copy this file to .env and fill in your values
MCP_ENABLE_AUTH=false
MCP_API_KEY=your-api-key-here
MCP_ENABLE_USER_AUTH=false
MCP_USERS_FILE=~/.mcp_server/users.json
```

## Method 3: mcp.json Configuration

### For Cursor IDE

**File: `~/.cursor/mcp.json`** (global) or **`.cursor/mcp_config.json`** (project-specific)

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
        "MCP_ENABLE_AUTH": "true",
        "MCP_API_KEY": "your-api-key-here",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "~/.mcp_server/users.json",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
```

### For VS Code

**File: `.vscode/settings.json`**

```json
{
  "mcp.servers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "${workspaceFolder}",
        "MCP_ENABLE_AUTH": "true",
        "MCP_API_KEY": "your-api-key-here",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "~/.mcp_server/users.json",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### For Claude Desktop

**File: `~/Library/Application Support/Claude/claude_desktop_config.json`** (macOS)

```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": ".",
        "MCP_ENABLE_AUTH": "true",
        "MCP_API_KEY": "your-api-key-here",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "~/.mcp_server/users.json"
      }
    }
  }
}
```

## Method 4: User-Based Authentication

### Step 1: Create Admin Account

```bash
# Create first admin account
python -m python_package_mcp_server.cli create-admin --username admin

# Or with custom API key
python -m python_package_mcp_server.cli create-admin --username admin --api-key my-secure-key-123
```

This creates a users file at `~/.mcp_server/users.json`:

```json
{
  "users": [
    {
      "username": "admin",
      "api_key_hash": "sha256-hash-of-api-key",
      "role": "admin",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Step 2: Configure Environment

Add to your `.env` or `mcp.json`:

```bash
MCP_ENABLE_USER_AUTH=true
MCP_USERS_FILE=~/.mcp_server/users.json
MCP_API_KEY=<admin-api-key-from-step-1>
```

### Step 3: Create Additional Users

Use the `create_user` MCP tool (admin only):

```json
{
  "tool": "create_user",
  "arguments": {
    "username": "developer1",
    "role": "user"
  }
}
```

## Configuration Priority

The server reads configuration in this order (later overrides earlier):

1. **Default values** (from `config.py`)
2. **Environment variables** (system/session)
3. **`.env` file** (project root)
4. **`mcp.json` env section** (for IDE clients)

## Authentication Modes

### Mode 1: Single API Key (Legacy)

**Configuration:**
```bash
MCP_ENABLE_AUTH=true
MCP_API_KEY=your-single-api-key
MCP_SINGLE_API_KEY_MODE=true  # default
```

**Use Case:** Simple deployments with one API key for all requests

### Mode 2: User-Based Authentication

**Configuration:**
```bash
MCP_ENABLE_AUTH=true
MCP_ENABLE_USER_AUTH=true
MCP_USERS_FILE=~/.mcp_server/users.json
MCP_API_KEY=<user-api-key>
```

**Use Case:** Multi-user deployments with role-based access control

## File Locations Summary

| Configuration Type | File Location | Platform |
|-------------------|---------------|----------|
| **Environment Variables** | System/shell profile | All |
| **`.env` File** | Project root | All |
| **Cursor IDE Config** | `~/.cursor/mcp.json` or `.cursor/mcp_config.json` | All |
| **VS Code Config** | `.vscode/settings.json` | All |
| **Claude Desktop Config** | `~/Library/Application Support/Claude/claude_desktop_config.json` | macOS |
| **Users File** | `~/.mcp_server/users.json` | All |

## Security Best Practices

1. **Never commit secrets to git:**
   ```bash
   # Add to .gitignore
   .env
   *.key
   users.json
   ```

2. **Use strong API keys:**
   ```bash
   # Generate secure key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Set file permissions:**
   ```bash
   # Restrict users file access
   chmod 600 ~/.mcp_server/users.json
   ```

4. **Use environment variables in production:**
   - Prefer environment variables over `.env` files
   - Use secrets management systems (AWS Secrets Manager, HashiCorp Vault, etc.)

5. **Rotate API keys regularly:**
   - Update keys periodically
   - Revoke old keys when compromised

## Quick Reference

### Minimal Auth Setup (Single API Key)

**`.env` file:**
```bash
MCP_ENABLE_AUTH=true
MCP_API_KEY=your-api-key-here
```

**`mcp.json`:**
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_ENABLE_AUTH": "true",
        "MCP_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Full Auth Setup (User-Based)

**Step 1: Create admin**
```bash
python -m python_package_mcp_server.cli create-admin --username admin
```

**Step 2: Configure**
```json
{
  "mcpServers": {
    "python-package-manager": {
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_ENABLE_AUTH": "true",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "~/.mcp_server/users.json",
        "MCP_API_KEY": "<admin-api-key-from-create-admin>"
      }
    }
  }
}
```

## Troubleshooting

### Auth Not Working?

1. **Check environment variables:**
   ```bash
   # Linux/macOS
   env | grep MCP
   
   # Windows PowerShell
   Get-ChildItem Env: | Where-Object Name -like "MCP*"
   ```

2. **Verify users file exists:**
   ```bash
   ls -la ~/.mcp_server/users.json
   ```

3. **Check file permissions:**
   ```bash
   ls -l ~/.mcp_server/users.json
   # Should be: -rw------- (600)
   ```

4. **Test authentication:**
   ```bash
   python -m python_package_mcp_server.cli status
   ```

### Common Issues

**Issue:** "Authentication required" error
- **Solution:** Set `MCP_ENABLE_AUTH=true` and provide `MCP_API_KEY`

**Issue:** "Invalid API key" error
- **Solution:** Verify API key matches the one in users file or environment

**Issue:** Users file not found
- **Solution:** Create admin account: `python -m python_package_mcp_server.cli create-admin`

**Issue:** Permission denied on users file
- **Solution:** Fix permissions: `chmod 600 ~/.mcp_server/users.json`

## Examples

See `examples/client_config.json` for complete configuration examples.

For more details, see:
- [README.md](../README.md#authentication)
- [MCP Configuration Guide](mcp-configuration-guide.md)
- [Enterprise Guide](enterprise.md)
