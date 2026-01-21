# MCP Inspector Usage Guide

This comprehensive guide will help you use the MCP Inspector to test and debug the Python Package Manager MCP Server. The inspector provides an interactive web-based UI for exploring resources, testing tools, and monitoring server communication.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Resources Tab - Detailed Walkthrough](#resources-tab---detailed-walkthrough)
3. [Tools Tab - Detailed Walkthrough](#tools-tab---detailed-walkthrough)
4. [Logs Tab - Understanding Communication](#logs-tab---understanding-communication)
5. [Practical Examples](#practical-examples)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

## Getting Started

### Prerequisites

Before using the MCP Inspector, ensure you have:

- **Node.js** installed (for `npx` command)
  - Check: `node --version`
  - Install: https://nodejs.org/
- **Python 3.10+** installed
- **uv** package manager installed
  - Check: `uv --version`
  - Install: https://github.com/astral-sh/uv
- **Virtual environment** set up (will be created automatically if missing)

### Launching the Inspector

**Linux/macOS:**
```bash
./scripts/inspect.sh
```

**Windows PowerShell:**
```powershell
.\scripts\inspect.ps1
```

The inspector will:
1. Check prerequisites
2. Set up the Python virtual environment if needed
3. Start the MCP server via stdio transport
4. Launch the web UI at `http://localhost:5173`
5. Open the UI in your default browser

### Understanding the UI Layout

The MCP Inspector UI consists of three main tabs:

1. **Resources Tab**: Browse and read available resources
2. **Tools Tab**: Invoke tools and see results
3. **Logs Tab**: Monitor JSON-RPC communication

### Navigation Basics

- **List Resources**: Click to refresh the list of available resources
- **Clear**: Clear the current selection or search results
- **Search**: Use the search icon to filter resources
- **Read Resource**: Click on a resource and use "Read Resource" to fetch content
- **Call Tool**: Select a tool, fill in parameters, and click "Call Tool"

## Resources Tab - Detailed Walkthrough

Resources are read-only data that provide information about your project, packages, and codebase. Each resource has a unique URI and returns JSON data.

### Python Package Management Resources

#### python:packages://installed

**Purpose:** Lists all installed Python packages with their versions.

**How to Access:**
1. Open MCP Inspector
2. Navigate to Resources tab
3. Click on "Installed Packages" in the list
4. Click "Read Resource" button

**Example Output:**
```json
{
  "packages": [
    {
      "name": "requests",
      "version": "2.31.0"
    },
    {
      "name": "pytest",
      "version": "7.4.0"
    },
    {
      "name": "mcp",
      "version": "1.0.0"
    }
  ]
}
```

**Interpreting Results:**
- Each package object contains `name` and `version` fields
- Use this to verify installed dependencies
- Compare with `requirements.txt` or `pyproject.toml`
- Useful for debugging dependency issues

**Common Use Cases:**
- Verify package installation after running `install` tool
- Check if specific packages are available
- Audit installed packages for security

#### python:packages://outdated

**Purpose:** Lists packages that have available updates.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Outdated Packages"
3. Click "Read Resource"

**Example Output:**
```json
{
  "outdated": [
    {
      "name": "requests",
      "version": "2.31.0",
      "latest": "2.32.0"
    },
    {
      "name": "pytest",
      "version": "7.4.0",
      "latest": "8.0.0"
    }
  ]
}
```

**Interpreting Results:**
- Shows current version vs latest available version
- Use `upgrade` tool to update packages
- Check for security updates regularly

**Common Use Cases:**
- Identify packages needing updates
- Plan dependency upgrades
- Security audit

#### python:dependencies://tree

**Purpose:** Visualizes the complete dependency tree of your project.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Dependency Tree"
3. Click "Read Resource"

**Example Output:**
```json
{
  "root": "python-package-mcp-server",
  "dependencies": {
    "mcp": {
      "version": "1.0.0",
      "dependencies": {
        "pydantic": "2.0.0",
        "httpx": "0.27.0"
      }
    },
    "structlog": {
      "version": "24.0.0",
      "dependencies": {}
    }
  }
}
```

**Interpreting Results:**
- Shows hierarchical dependency structure
- Helps identify transitive dependencies
- Useful for understanding dependency conflicts

**Common Use Cases:**
- Debug dependency conflicts
- Understand project dependencies
- Plan dependency updates

**Note:** Requires `pyproject.toml` in project root.

#### python:project://info

**Purpose:** Provides project metadata including `pyproject.toml` and lock file information.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Project Information"
3. Click "Read Resource"

**Example Output:**
```json
{
  "pyproject": {
    "project": {
      "name": "python-package-mcp-server",
      "version": "0.1.0",
      "description": "Production-ready MCP server",
      "dependencies": [
        "mcp>=1.0.0",
        "pydantic>=2.0.0"
      ]
    }
  },
  "lock_file": {
    "exists": true,
    "size": 45678,
    "modified": 1704067200.0
  }
}
```

**Interpreting Results:**
- `pyproject` contains parsed `pyproject.toml` data
- `lock_file` shows lock file status and metadata
- Use to verify project configuration

**Common Use Cases:**
- Verify project configuration
- Check lock file status
- Debug configuration issues

#### python:environment://active

**Purpose:** Shows details about the active Python environment.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Active Environment"
3. Click "Read Resource"

**Example Output:**
```json
{
  "python_version": "3.11.5 (main, Aug 24 2023, 15:08:48)",
  "python_executable": "/path/to/.venv/bin/python",
  "virtual_env": "/path/to/.venv",
  "path": [
    "/path/to/.venv/lib/python3.11/site-packages",
    "/usr/lib/python3.11",
    ...
  ]
}
```

**Interpreting Results:**
- `python_version`: Python interpreter version
- `python_executable`: Path to Python executable
- `virtual_env`: Virtual environment path (if active)
- `path`: First 5 entries of Python path

**Common Use Cases:**
- Verify Python version
- Check if virtual environment is active
- Debug import issues

### Project Index Resources

#### project://index

**Purpose:** Complete project index with structure, files, and metadata.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Project Index"
3. Click "Read Resource"

**Example Output:**
```json
{
  "root": "/path/to/project",
  "structure": {
    "src": {
      "type": "directory",
      "files": ["server.py", "cli.py"]
    }
  },
  "config_files": ["pyproject.toml", ".gitignore"],
  "dependencies": ["pyproject.toml"],
  "readmes": ["README.md"],
  "entry_points": ["src/python_package_mcp_server/cli.py"],
  "tests": ["tests/test_server.py"]
}
```

**Interpreting Results:**
- Complete overview of project structure
- Lists all important files and directories
- Useful for LLM-assisted development

**Common Use Cases:**
- Get project overview
- Discover project structure
- Find configuration files

#### project://structure

**Purpose:** File and directory structure tree.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Project Structure"
3. Click "Read Resource"

**Example Output:**
```json
{
  "src": {
    "type": "directory",
    "children": {
      "python_package_mcp_server": {
        "type": "directory",
        "children": {
          "server.py": {"type": "file"},
          "cli.py": {"type": "file"}
        }
      }
    }
  },
  "tests": {
    "type": "directory",
    "children": {}
  }
}
```

**Interpreting Results:**
- Hierarchical tree structure
- Shows directories and files
- Helps navigate project structure

#### project://config

**Purpose:** Lists all configuration files in the project.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Configuration Files"
3. Click "Read Resource"

**Example Output:**
```json
{
  "config_files": [
    "pyproject.toml",
    ".gitignore",
    ".cursor/mcp_config.json",
    ".vscode/settings.json"
  ]
}
```

**Interpreting Results:**
- Lists all discovered configuration files
- Includes common config file patterns
- Useful for understanding project setup

#### project://dependencies

**Purpose:** Lists all dependency files across project types.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Dependency Files"
3. Click "Read Resource"

**Example Output:**
```json
{
  "dependencies": [
    "pyproject.toml",
    "uv.lock",
    "package.json",
    "pubspec.yaml"
  ]
}
```

**Interpreting Results:**
- Lists dependency files for multiple languages
- Supports Python, Node.js, Dart, etc.
- Useful for multi-language projects

#### project://readme

**Purpose:** Lists README and documentation files.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Documentation Files"
3. Click "Read Resource"

**Example Output:**
```json
{
  "readmes": [
    "README.md",
    "docs/README.md",
    "CONTRIBUTING.md"
  ]
}
```

**Interpreting Results:**
- Lists all documentation files
- Helps discover project documentation
- Useful for onboarding

#### project://entrypoints

**Purpose:** Lists entry points and main files.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Entry Points"
3. Click "Read Resource"

**Example Output:**
```json
{
  "entry_points": [
    "src/python_package_mcp_server/cli.py",
    "src/python_package_mcp_server/server.py"
  ]
}
```

**Interpreting Results:**
- Identifies main application files
- Helps understand project entry points
- Useful for debugging startup issues

#### project://tests

**Purpose:** Lists test files and test structure.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Test Files"
3. Click "Read Resource"

**Example Output:**
```json
{
  "tests": [
    "tests/test_server.py",
    "tests/test_tools.py",
    "tests/test_resources.py"
  ]
}
```

**Interpreting Results:**
- Lists all test files
- Helps discover test structure
- Useful for test coverage analysis

### Codebase Resources

#### codebase://search

**Purpose:** Search codebase by pattern or content.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Codebase Search"
3. Use query parameters: `?pattern={pattern}&extensions={extensions}`
4. Click "Read Resource"

**Query Parameters:**
- `pattern`: Search pattern (required)
- `extensions`: Comma-separated file extensions (optional, e.g., `.py,.js`)

**Example Usage:**
- URI: `codebase://search?pattern=def.*&extensions=.py`
- Searches for all function definitions in Python files

**Example Output:**
```json
{
  "matches": [
    {
      "file": "src/server.py",
      "line": 20,
      "content": "def list_resources():"
    }
  ],
  "count": 1
}
```

**Interpreting Results:**
- `matches`: Array of matching results
- Each match contains file, line number, and content
- `count`: Total number of matches

**Common Use Cases:**
- Find function definitions
- Search for specific patterns
- Code exploration

#### codebase://file

**Purpose:** Read specific file content with line numbers.

**How to Access:**
1. Navigate to Resources tab
2. Click on "File Content"
3. Use query parameter: `?path={file_path}`
4. Click "Read Resource"

**Query Parameters:**
- `path`: Relative path to file (required)

**Example Usage:**
- URI: `codebase://file?path=src/server.py`

**Example Output:**
```
   1: """Main MCP server implementation."""
   2:
   3: import asyncio
   4: from typing import Any
   5:
   6: from mcp.server import Server
   ...
```

**Interpreting Results:**
- Returns file content with line numbers
- Useful for reading specific files
- Helps with code review

**Common Use Cases:**
- Read specific files
- Code review
- Understanding code structure

#### codebase://symbols

**Purpose:** Extract symbols (functions, classes) from codebase.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Code Symbols"
3. Use query parameter: `?path={file_path}`
4. Click "Read Resource"

**Query Parameters:**
- `path`: Relative path to file (required)

**Example Usage:**
- URI: `codebase://symbols?path=src/server.py`

**Example Output:**
```json
{
  "symbols": [
    {
      "name": "list_resources",
      "type": "function",
      "line": 20
    },
    {
      "name": "Server",
      "type": "class",
      "line": 15
    }
  ],
  "count": 2
}
```

**Interpreting Results:**
- `symbols`: Array of extracted symbols
- Each symbol has name, type, and line number
- `count`: Total number of symbols

**Common Use Cases:**
- Extract API surface
- Understand code structure
- Generate documentation

### Dart Standards Resources

#### dart:standards://effective-dart

**Purpose:** Official Effective Dart style guide and best practices.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Effective Dart Guidelines"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "Effective Dart Guidelines",
  "sections": {
    "style": {
      "summary": "Guidelines for writing consistent, readable Dart code",
      "key_points": [
        "Use lowerCamelCase for variable names",
        "Use UpperCamelCase for class names",
        "Prefer final for variables that are not reassigned"
      ]
    },
    "documentation": {
      "summary": "Best practices for documenting Dart code",
      "key_points": [
        "Write documentation comments for public APIs",
        "Use /// for documentation comments"
      ]
    }
  }
}
```

**Common Use Cases:**
- Reference style guidelines
- Code review
- Learning Dart best practices

#### dart:standards://style-guide

**Purpose:** Dart style guide with naming conventions and formatting rules.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Dart Style Guide"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "Dart Style Guide",
  "naming_conventions": {
    "variables": "lowerCamelCase",
    "classes": "UpperCamelCase",
    "libraries": "lowercase_with_underscores",
    "constants": "SCREAMING_CAPS"
  },
  "formatting": {
    "indentation": "2 spaces",
    "line_length": "80 characters (recommended)"
  }
}
```

**Common Use Cases:**
- Formatting reference
- Naming conventions
- Code style validation

#### dart:standards://linter-rules

**Purpose:** Complete list of Dart linter rules and descriptions.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Dart Linter Rules"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "Dart Linter Rules",
  "recommended_packages": [
    "package:pedantic",
    "package:effective_dart",
    "package:lints"
  ],
  "common_rules": {
    "always_declare_return_types": "Always declare return types",
    "avoid_print": "Avoid using print() in production code",
    "prefer_const_constructors": "Prefer const constructors when possible"
  }
}
```

**Common Use Cases:**
- Linter configuration
- Code quality rules
- Best practices reference

#### dart:standards://best-practices

**Purpose:** Dart best practices for code quality and maintainability.

**How to Access:**
1. Navigate to Resources tab
2. Click on "Dart Best Practices"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "Dart Best Practices",
  "null_safety": {
    "summary": "Use null safety features effectively",
    "practices": [
      "Use ? for nullable types",
      "Use ?? for null coalescing"
    ]
  },
  "async_programming": {
    "summary": "Best practices for async/await",
    "practices": [
      "Prefer async/await over Future.then()",
      "Use Future.wait() for parallel operations"
    ]
  }
}
```

**Common Use Cases:**
- Code quality reference
- Learning best practices
- Code review guidelines

### TypeScript Standards Resources

#### typescript:standards://style-guide

**Purpose:** TypeScript style guide with naming conventions and formatting rules.

**How to Access:**
1. Navigate to Resources tab
2. Click on "TypeScript Style Guide"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "TypeScript Style Guide",
  "naming_conventions": {
    "interfaces": "PascalCase",
    "variables": "camelCase",
    "constants": "UPPER_SNAKE_CASE"
  },
  "formatting": {
    "indentation": "2 spaces",
    "semicolons": "Use semicolons consistently"
  }
}
```

**Common Use Cases:**
- Style reference
- Formatting guidelines
- Naming conventions

#### typescript:standards://tsconfig-options

**Purpose:** Recommended tsconfig.json compiler options and meanings.

**How to Access:**
1. Navigate to Resources tab
2. Click on "TypeScript tsconfig Options"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "TypeScript tsconfig.json Options",
  "recommended_config": {
    "compilerOptions": {
      "target": "ES2020",
      "module": "ESNext",
      "strict": true,
      "esModuleInterop": true
    }
  },
  "strict_mode_options": {
    "strict": "Enables all strict type checking options",
    "noImplicitAny": "Raise error on expressions with implied 'any'"
  }
}
```

**Common Use Cases:**
- tsconfig.json reference
- Compiler options guide
- TypeScript configuration

#### typescript:standards://eslint-rules

**Purpose:** ESLint rules for TypeScript code quality and consistency.

**How to Access:**
1. Navigate to Resources tab
2. Click on "TypeScript ESLint Rules"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "TypeScript ESLint Rules",
  "recommended_packages": [
    "@typescript-eslint/eslint-plugin",
    "@typescript-eslint/parser"
  ],
  "common_rules": {
    "@typescript-eslint/no-explicit-any": "Disallow 'any' type",
    "@typescript-eslint/explicit-function-return-type": "Require explicit return types"
  }
}
```

**Common Use Cases:**
- ESLint configuration
- Code quality rules
- Linting setup

#### typescript:standards://best-practices

**Purpose:** TypeScript best practices for type safety and code quality.

**How to Access:**
1. Navigate to Resources tab
2. Click on "TypeScript Best Practices"
3. Click "Read Resource"

**Example Output:**
```json
{
  "title": "TypeScript Best Practices",
  "type_safety": {
    "summary": "Maximize type safety",
    "practices": [
      "Enable strict mode in tsconfig.json",
      "Avoid 'any' type - use 'unknown' if needed"
    ]
  },
  "code_organization": {
    "summary": "Organize code effectively",
    "practices": [
      "Use barrel exports (index.ts) for modules",
      "Separate types into dedicated files"
    ]
  }
}
```

**Common Use Cases:**
- Best practices reference
- Type safety guidelines
- Code organization

## Tools Tab - Detailed Walkthrough

Tools are actions that can be invoked to perform operations. Each tool has a name, description, and input schema defining required and optional parameters.

### Package Management Tools

#### install

**Purpose:** Install Python package(s) with optional version constraints.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| packages | array[string] | Yes | List of package specifications (e.g., `["requests==2.31.0", "pytest"]`) |
| editable | boolean | No | Install in editable mode (default: false) |

**How to Invoke:**
1. Navigate to Tools tab
2. Select "install" from the tools list
3. Fill in the parameters:
   ```json
   {
     "packages": ["requests==2.31.0", "pytest"],
     "editable": false
   }
   ```
4. Click "Call Tool"

**Example Invocation:**
```json
{
  "name": "install",
  "arguments": {
    "packages": ["requests==2.31.0", "pytest"],
    "editable": false
  }
}
```

**Expected Output:**
```
Successfully installed packages: requests==2.31.0, pytest
```

**Error Handling:**
- If packages are blocked by policy: Returns error message
- If package not found: Returns installation error
- If no packages specified: Returns validation error

**Common Use Cases:**
- Install project dependencies
- Add new packages to environment
- Install packages in editable mode for development

#### uninstall

**Purpose:** Uninstall Python package(s).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| packages | array[string] | Yes | List of package names to uninstall |

**Example Invocation:**
```json
{
  "name": "uninstall",
  "arguments": {
    "packages": ["requests", "pytest"]
  }
}
```

**Expected Output:**
```
Successfully uninstalled packages: requests, pytest
```

**Common Use Cases:**
- Remove unused packages
- Clean up environment
- Remove conflicting packages

#### add

**Purpose:** Add package(s) to project dependencies.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| packages | array[string] | Yes | List of package specifications |
| dev | boolean | No | Add as dev dependencies (default: false) |

**Example Invocation:**
```json
{
  "name": "add",
  "arguments": {
    "packages": ["fastapi"],
    "dev": false
  }
}
```

**Expected Output:**
```
Successfully added packages to project dependencies
```

**Common Use Cases:**
- Add dependencies to `pyproject.toml`
- Add development dependencies
- Update project dependencies

#### remove

**Purpose:** Remove package(s) from project dependencies.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| packages | array[string] | Yes | List of package names to remove |

**Example Invocation:**
```json
{
  "name": "remove",
  "arguments": {
    "packages": ["fastapi"]
  }
}
```

**Expected Output:**
```
Successfully removed packages from project dependencies
```

**Common Use Cases:**
- Remove unused dependencies
- Clean up `pyproject.toml`
- Update project dependencies

#### sync

**Purpose:** Sync environment with lock file.

**Parameters:** None

**Example Invocation:**
```json
{
  "name": "sync",
  "arguments": {}
}
```

**Expected Output:**
```
Successfully synced environment with lock file
```

**Common Use Cases:**
- Sync environment after lock file changes
- Reproduce exact environment
- Install all dependencies from lock file

#### lock

**Purpose:** Generate or update lock file.

**Parameters:** None

**Example Invocation:**
```json
{
  "name": "lock",
  "arguments": {}
}
```

**Expected Output:**
```
Successfully generated/updated lock file
```

**Common Use Cases:**
- Generate lock file for reproducible builds
- Update lock file after dependency changes
- Lock dependency versions

#### init

**Purpose:** Initialize a new Python project.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Optional project name |

**Example Invocation:**
```json
{
  "name": "init",
  "arguments": {
    "name": "my-project"
  }
}
```

**Expected Output:**
```
Successfully initialized Python project
```

**Common Use Cases:**
- Create new Python projects
- Set up project structure
- Initialize with uv

#### upgrade

**Purpose:** Upgrade package(s) to latest versions.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| packages | array[string] | No | List of package names to upgrade (upgrades all if not specified) |

**Example Invocation:**
```json
{
  "name": "upgrade",
  "arguments": {
    "packages": ["requests", "pytest"]
  }
}
```

**Expected Output:**
```
Successfully upgraded packages
```

**Common Use Cases:**
- Update specific packages
- Update all packages
- Apply security updates

### Project Indexing Tools

#### index_project

**Purpose:** Index/scan a project directory and build resource cache.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | No | Optional project path (uses current directory if not specified) |

**Example Invocation:**
```json
{
  "name": "index_project",
  "arguments": {
    "path": "/path/to/project"
  }
}
```

**Expected Output:**
```
Successfully indexed project
```

**Common Use Cases:**
- Build project index
- Cache project structure
- Prepare for LLM-assisted development

#### refresh_index

**Purpose:** Refresh project index cache.

**Parameters:** None

**Example Invocation:**
```json
{
  "name": "refresh_index",
  "arguments": {}
}
```

**Expected Output:**
```
Successfully refreshed project index
```

**Common Use Cases:**
- Update cached index
- Refresh after file changes
- Rebuild project cache

#### discover_projects

**Purpose:** Discover multiple projects in a workspace.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace_path | string | No | Optional workspace path |

**Example Invocation:**
```json
{
  "name": "discover_projects",
  "arguments": {
    "workspace_path": "/path/to/workspace"
  }
}
```

**Expected Output:**
```
Successfully discovered projects in workspace
```

**Common Use Cases:**
- Multi-project workspaces
- Discover all projects
- Workspace analysis

#### analyze_codebase

**Purpose:** Analyze codebase structure and extract metadata.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| path | string | No | Optional project path |

**Example Invocation:**
```json
{
  "name": "analyze_codebase",
  "arguments": {
    "path": "/path/to/project"
  }
}
```

**Expected Output:**
```
Successfully analyzed codebase structure
```

**Common Use Cases:**
- Codebase analysis
- Extract metadata
- Understand project structure

### Dart Tools

#### dart_format

**Purpose:** Format Dart code according to Dart style guide.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | array[string] | No | List of file/directory paths to format (formats all if not specified) |
| line_length | integer | No | Line length for formatting (default: 80) |

**Example Invocation:**
```json
{
  "name": "dart_format",
  "arguments": {
    "paths": ["lib/main.dart"],
    "line_length": 80
  }
}
```

**Expected Output:**
```
Successfully formatted Dart code.
```

**Common Use Cases:**
- Format Dart code
- Enforce style guide
- Code cleanup

#### dart_analyze

**Purpose:** Analyze Dart code for errors and warnings.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | array[string] | No | List of file/directory paths to analyze (analyzes all if not specified) |

**Example Invocation:**
```json
{
  "name": "dart_analyze",
  "arguments": {
    "paths": ["lib/"]
  }
}
```

**Expected Output:**
```
Analysis found 2 issue(s):
[
  {
    "severity": "warning",
    "message": "Unused import",
    "file": "lib/main.dart",
    "line": 5
  }
]
```

**Common Use Cases:**
- Find code issues
- Static analysis
- Code quality checks

#### dart_fix

**Purpose:** Apply automated fixes to Dart code.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | array[string] | No | List of file/directory paths to fix (fixes all if not specified) |

**Example Invocation:**
```json
{
  "name": "dart_fix",
  "arguments": {
    "paths": ["lib/main.dart"]
  }
}
```

**Expected Output:**
```
Successfully applied fixes to Dart code.
```

**Common Use Cases:**
- Auto-fix issues
- Apply linter fixes
- Code cleanup

#### dart_generate_code

**Purpose:** Generate Dart code following standards and best practices.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code_description | string | Yes | Description of the code to generate |
| file_path | string | No | Optional file path where code should be written |
| include_tests | boolean | No | Whether to include test code (default: false) |

**Example Invocation:**
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

**Expected Output:**
```
Generated Dart code following standards:

// Generated Dart code following Effective Dart guidelines
// Description: Create a User class with name and email fields

// TODO: Implement based on description
```

**Common Use Cases:**
- Code generation
- Scaffold code
- Generate boilerplate

#### dart_check_standards

**Purpose:** Check if Dart code follows standards and best practices.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | Yes | Path to Dart file to check |

**Example Invocation:**
```json
{
  "name": "dart_check_standards",
  "arguments": {
    "file_path": "lib/main.dart"
  }
}
```

**Expected Output:**
```
Standards check for lib/main.dart:
Status: ✓ Compliant
Properly formatted: Yes
Issues found: 0
```

**Common Use Cases:**
- Standards compliance
- Code quality checks
- Style validation

### TypeScript Tools

#### typescript_format

**Purpose:** Format TypeScript code using Prettier.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | array[string] | No | List of file/directory paths to format (formats all if not specified) |

**Example Invocation:**
```json
{
  "name": "typescript_format",
  "arguments": {
    "paths": ["src/index.ts"]
  }
}
```

**Expected Output:**
```
Successfully formatted TypeScript code
```

**Common Use Cases:**
- Format TypeScript code
- Enforce formatting
- Code cleanup

#### typescript_lint

**Purpose:** Lint TypeScript code using ESLint.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| paths | array[string] | No | List of file/directory paths to lint (lints all if not specified) |

**Example Invocation:**
```json
{
  "name": "typescript_lint",
  "arguments": {
    "paths": ["src/"]
  }
}
```

**Expected Output:**
```
Linting completed with 0 errors, 2 warnings
```

**Common Use Cases:**
- Lint TypeScript code
- Find code issues
- Code quality checks

#### typescript_type_check

**Purpose:** Type check TypeScript code using tsc.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_path | string | No | Optional path to tsconfig.json (uses default if not specified) |

**Example Invocation:**
```json
{
  "name": "typescript_type_check",
  "arguments": {
    "project_path": "tsconfig.json"
  }
}
```

**Expected Output:**
```
Type checking completed with 0 errors
```

**Common Use Cases:**
- Type checking
- Find type errors
- Validate types

#### typescript_generate_code

**Purpose:** Generate TypeScript code following standards and best practices.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code_description | string | Yes | Description of the code to generate |
| file_path | string | No | Optional file path where code should be written |
| include_tests | boolean | No | Whether to include test code (default: false) |

**Example Invocation:**
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

**Expected Output:**
```
Generated TypeScript code following standards
```

**Common Use Cases:**
- Code generation
- Scaffold code
- Generate boilerplate

#### typescript_check_standards

**Purpose:** Check if TypeScript code follows standards and best practices.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file_path | string | Yes | Path to TypeScript file to check |

**Example Invocation:**
```json
{
  "name": "typescript_check_standards",
  "arguments": {
    "file_path": "src/index.ts"
  }
}
```

**Expected Output:**
```
Standards check for src/index.ts:
Status: ✓ Compliant
Properly formatted: Yes
```

**Common Use Cases:**
- Standards compliance
- Code quality checks
- Style validation

## Logs Tab - Understanding Communication

The Logs tab shows real-time JSON-RPC communication between the inspector and the MCP server. This is invaluable for debugging and understanding how the protocol works.

### Reading JSON-RPC Messages

**Request Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/read",
  "params": {
    "uri": "python:packages://installed"
  }
}
```

**Response Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "contents": [
      {
        "uri": "python:packages://installed",
        "mimeType": "application/json",
        "text": "{\"packages\": [...]}"
      }
    ]
  }
}
```

**Error Format:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "Unknown resource URI: invalid://uri"
  }
}
```

### Understanding Request/Response Flow

1. **Initialization**: Server and client exchange capabilities
2. **Resource Listing**: Client requests list of available resources
3. **Resource Reading**: Client requests specific resource content
4. **Tool Invocation**: Client calls tools with parameters
5. **Notifications**: Server may send notifications for updates

### Identifying Errors

Common error codes:
- `-32600`: Invalid Request
- `-32601`: Method Not Found
- `-32602`: Invalid Params
- `-32603`: Internal Error
- `-32000`: Server Error

### Debugging Tips

1. **Filter Logs**: Use search to filter specific messages
2. **Check Request IDs**: Match requests with responses
3. **Look for Errors**: Red-highlighted errors indicate issues
4. **Check Timing**: Response times can indicate performance issues
5. **Validate JSON**: Ensure JSON is properly formatted

## Practical Examples

### Example 1: Checking Installed Packages and Updating Outdated Ones

**Workflow:**
1. **Check installed packages:**
   - Navigate to Resources tab
   - Click "Installed Packages"
   - Read resource to see current packages

2. **Check for outdated packages:**
   - Click "Outdated Packages"
   - Read resource to see available updates

3. **Upgrade packages:**
   - Navigate to Tools tab
   - Select "upgrade" tool
   - Specify packages to upgrade or leave empty for all
   - Call tool

4. **Verify updates:**
   - Return to Resources tab
   - Read "Installed Packages" again to verify versions

### Example 2: Exploring Project Structure

**Workflow:**
1. **Get project overview:**
   - Navigate to Resources tab
   - Click "Project Index"
   - Read resource for complete overview

2. **Explore structure:**
   - Click "Project Structure"
   - Read resource to see file tree

3. **Find configuration:**
   - Click "Configuration Files"
   - Read resource to see all config files

4. **Read specific file:**
   - Click "File Content"
   - Use query parameter: `?path=pyproject.toml`
   - Read resource to see file content

### Example 3: Formatting and Analyzing Dart Code

**Workflow:**
1. **Check standards:**
   - Navigate to Resources tab
   - Click "Dart Best Practices"
   - Read resource for reference

2. **Analyze code:**
   - Navigate to Tools tab
   - Select "dart_analyze"
   - Specify paths: `["lib/"]`
   - Call tool to see issues

3. **Apply fixes:**
   - Select "dart_fix"
   - Specify paths: `["lib/"]`
   - Call tool to auto-fix issues

4. **Format code:**
   - Select "dart_format"
   - Specify paths: `["lib/"]`
   - Call tool to format code

5. **Verify standards:**
   - Select "dart_check_standards"
   - Specify file: `"lib/main.dart"`
   - Call tool to verify compliance

### Example 4: Searching Codebase for Specific Patterns

**Workflow:**
1. **Search for functions:**
   - Navigate to Resources tab
   - Click "Codebase Search"
   - Use URI: `codebase://search?pattern=def.*&extensions=.py`
   - Read resource to see matches

2. **Read specific file:**
   - Click "File Content"
   - Use URI: `codebase://file?path=src/server.py`
   - Read resource to see file content

3. **Extract symbols:**
   - Click "Code Symbols"
   - Use URI: `codebase://symbols?path=src/server.py`
   - Read resource to see extracted symbols

### Example 5: Installing and Managing Dependencies

**Workflow:**
1. **Check current dependencies:**
   - Navigate to Resources tab
   - Click "Project Information"
   - Read resource to see `pyproject.toml` dependencies

2. **Add new dependency:**
   - Navigate to Tools tab
   - Select "add" tool
   - Specify packages: `["fastapi"]`
   - Call tool

3. **Install dependencies:**
   - Select "sync" tool
   - Call tool to install all dependencies

4. **Verify installation:**
   - Return to Resources tab
   - Click "Installed Packages"
   - Read resource to verify fastapi is installed

5. **Generate lock file:**
   - Return to Tools tab
   - Select "lock" tool
   - Call tool to generate/update lock file

## Troubleshooting

### Common Issues

#### Inspector doesn't start

**Symptoms:**
- Error: "npx is not installed"
- Script fails immediately

**Solutions:**
- Install Node.js: https://nodejs.org/
- Verify installation: `node --version`
- Try: `npx -y @modelcontextprotocol/inspector@latest`

#### Port conflicts

**Symptoms:**
- Error: "Port already in use"
- Inspector UI doesn't open

**Solutions:**
- Use custom ports: `./scripts/inspect.sh --client-port 8080`
- Check what's using the port: `lsof -i :5173`
- Kill conflicting process or use different port

#### Resources not loading

**Symptoms:**
- Resources list is empty
- "Read Resource" returns errors

**Solutions:**
- Check server is running: Look for server process
- Check logs tab for error messages
- Verify project root: Set `MCP_PROJECT_ROOT` environment variable
- Check virtual environment is active

#### Tools return errors

**Symptoms:**
- Tool invocation fails
- Error messages in response

**Solutions:**
- Check tool parameters: Verify required parameters are provided
- Check logs tab: Look for detailed error messages
- Verify dependencies: Ensure required tools are installed (e.g., `uv`, `dart`)
- Check permissions: Ensure write permissions for install/format operations

#### HTTP mode connection fails

**Symptoms:**
- Can't connect to HTTP server
- Connection timeout

**Solutions:**
- Ensure HTTP server is running: `./scripts/run_http.sh`
- Check host and port match: Verify `--host` and `--port` parameters
- Check firewall: Ensure ports are not blocked
- Verify authentication: If auth is enabled, provide API key

### Resource-Specific Troubleshooting

#### python:packages://installed returns empty

**Cause:** No packages installed or `uv` not working

**Solutions:**
- Verify `uv` is installed: `uv --version`
- Check virtual environment: Ensure venv is active
- Try installing a package: Use `install` tool first

#### python:dependencies://tree returns error

**Cause:** No `pyproject.toml` in project root

**Solutions:**
- Ensure `pyproject.toml` exists
- Set `MCP_PROJECT_ROOT` to correct directory
- Initialize project: Use `init` tool

#### codebase://search returns no results

**Cause:** Invalid pattern or no matching files

**Solutions:**
- Check pattern syntax: Use valid regex
- Verify file extensions: Ensure files with those extensions exist
- Try broader search: Remove extension filter

### Tool-Specific Troubleshooting

#### install tool fails

**Cause:** Package blocked by policy or not found

**Solutions:**
- Check policy settings: Verify `MCP_ALLOWED_PACKAGES` and `MCP_BLOCKED_PACKAGES`
- Check package name: Verify package exists on PyPI
- Check network: Ensure internet connection for package download

#### dart_format fails

**Cause:** Dart SDK not installed or path not found

**Solutions:**
- Install Dart SDK: https://dart.dev/get-dart
- Verify installation: `dart --version`
- Check PATH: Ensure `dart` is in system PATH

#### typescript_lint fails

**Cause:** ESLint not configured or TypeScript not found

**Solutions:**
- Install dependencies: `npm install`
- Check `tsconfig.json`: Ensure it exists and is valid
- Verify ESLint config: Ensure `.eslintrc` exists

### Environment Variable Issues

**Common Variables:**
- `MCP_PROJECT_ROOT`: Project root directory
- `MCP_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `MCP_LOG_FORMAT`: Log format (json, text)

**Setting Variables:**
```bash
# Linux/macOS
MCP_PROJECT_ROOT=/path/to/project ./scripts/inspect.sh

# Windows PowerShell
$env:MCP_PROJECT_ROOT = "C:\path\to\project"
.\scripts\inspect.ps1
```

## Best Practices

### When to Use Resources vs Tools

**Use Resources when:**
- You need read-only information
- You want to explore available data
- You need to understand project state
- You're debugging or investigating

**Use Tools when:**
- You need to perform actions
- You want to modify state
- You need to execute commands
- You're implementing functionality

### Efficient Testing Strategies

1. **Start with Resources:**
   - Understand current state before making changes
   - Use resources to verify tool results
   - Explore available data first

2. **Test Tools Incrementally:**
   - Test one tool at a time
   - Verify results after each tool call
   - Use resources to check state changes

3. **Use Logs for Debugging:**
   - Monitor logs tab during testing
   - Check for errors immediately
   - Understand request/response flow

4. **Combine Resources and Tools:**
   - Read resources before tool invocation
   - Verify changes with resources after tools
   - Use resources to plan tool usage

### Debugging Workflows

1. **Check Prerequisites:**
   - Verify all tools are installed
   - Check environment variables
   - Ensure server is running

2. **Start Simple:**
   - Test basic resources first
   - Try simple tool invocations
   - Build up to complex workflows

3. **Monitor Logs:**
   - Keep logs tab open
   - Watch for errors
   - Understand communication flow

4. **Isolate Issues:**
   - Test resources individually
   - Test tools with minimal parameters
   - Identify specific failing components

### Performance Considerations

1. **Resource Caching:**
   - Some resources are cached
   - Use `refresh_index` to update cache
   - Large resources may take time to load

2. **Tool Execution:**
   - Some tools are slow (e.g., `install`, `sync`)
   - Monitor execution time in logs
   - Use async operations when possible

3. **Network Operations:**
   - Package installation requires network
   - Check network connectivity
   - Consider using local package cache

## Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Inspector Documentation](https://modelcontextprotocol.io/docs/tools/inspector)
- [Project README](../README.md) - Setup and configuration
- [Usage Examples](../examples/usage.md) - More examples
- [Learning Guide](learning.md) - MCP concepts
- [Architecture Guide](architecture.md) - Server architecture

---

**Need Help?** If you encounter issues not covered in this guide, check the [Troubleshooting](#troubleshooting) section or review the logs tab for detailed error messages.
