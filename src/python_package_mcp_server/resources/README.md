# Resources Directory

This directory contains all MCP resources organized by category. Each resource is defined in a separate `.yaml` file, making it easy to add, modify, and manage resources.

## Directory Structure

```
resources/
├── python/          # Python package management resources
├── project/         # Project indexing resources
├── codebase/        # Codebase search and file resources
├── dart/            # Dart/Flutter standards resources
└── typescript/      # TypeScript standards resources
```

## Adding a New Resource

To add a new resource, simply create a new `.yaml` file in the appropriate category directory:

1. **Create the file**: `resources/<category>/your_resource_name.yaml`

2. **Add resource metadata**:
   ```yaml
   uri: your:resource://uri
   name: Your Resource Name
   description: What this resource provides
   mimeType: application/json
   handler:
     module: python_package_mcp_server.resources.your_module
     function: read_your_resource
   uriTemplate: your:resource://uri?param={param}
   ```

3. **Implement the handler function** in the appropriate Python module:
   ```python
   def read_your_resource(uri: str, params: dict[str, Any] | None = None) -> str:
       """Read resource content."""
       # Your implementation here
       return json.dumps({"data": "..."})
   ```

4. **That's it!** The resource will be automatically loaded when the server starts.

## Resource File Format

### YAML Structure

- **uri** (required): Unique resource URI identifier
- **name** (required): Human-readable resource name
- **description** (required): Resource description
- **mimeType** (optional): MIME type (default: "application/json")
- **handler** (required): Handler function configuration
  - **module**: Python module path (e.g., "python_package_mcp_server.resources.packages")
  - **function**: Function name in the module
- **uriTemplate** (optional): URI template for resource templates (defaults to uri)

### Examples

**Simple resource:**
```yaml
uri: python:packages://installed
name: Installed Packages
description: List of all installed Python packages
mimeType: application/json
handler:
  module: python_package_mcp_server.resources.packages
  function: read_package_resource
uriTemplate: python:packages://installed
```

**Resource with parameters:**
```yaml
uri: codebase://file
name: File Content
description: Read specific file content
mimeType: text/plain
handler:
  module: python_package_mcp_server.resources.codebase
  function: read_codebase_resource
uriTemplate: codebase://file?path={path}
```

## Handler Function Signature

Handler functions must follow this signature:

```python
def handler_function(uri: str, params: dict[str, Any] | None = None) -> str:
    """Read resource content.
    
    Args:
        uri: Resource URI
        params: Optional parameters (for template-based resources)
    
    Returns:
        Resource content as string (JSON, text, etc.)
    """
    # Implementation
    return content
```

## Categories

### Python Resources (`python/`)

Python package management resources:
- `packages_installed.yaml` - Installed packages list
- `packages_outdated.yaml` - Outdated packages list
- `dependencies_tree.yaml` - Dependency tree
- `project_info.yaml` - Project metadata
- `environment_active.yaml` - Active environment info

### Project Resources (`project/`)

Project indexing and discovery resources:
- `index.yaml` - Complete project index
- `structure.yaml` - File structure
- `config.yaml` - Configuration files
- `dependencies.yaml` - Dependency files
- `readme.yaml` - Documentation files
- `entrypoints.yaml` - Entry points
- `tests.yaml` - Test files

### Codebase Resources (`codebase/`)

Codebase search and file resources:
- `search.yaml` - Codebase search
- `file.yaml` - File content
- `symbols.yaml` - Code symbols

### Dart Resources (`dart/`)

Dart/Flutter standards resources:
- `effective_dart.yaml` - Effective Dart guidelines
- `style_guide.yaml` - Dart style guide
- `linter_rules.yaml` - Dart linter rules
- `best_practices.yaml` - Dart best practices

### TypeScript Resources (`typescript/`)

TypeScript standards resources:
- `style_guide.yaml` - TypeScript style guide
- `tsconfig_options.yaml` - tsconfig.json options
- `eslint_rules.yaml` - ESLint rules
- `best_practices.yaml` - TypeScript best practices

## Benefits of File-Based Resources

1. **Easy to Add**: Just create a `.yaml` file and implement handler
2. **Easy to Edit**: Edit YAML files directly
3. **Version Control**: Track resource changes in git
4. **Maintainability**: All resources in one place, organized by category
5. **Separation of Concerns**: Metadata in YAML, logic in Python

## Handler Implementation

Handlers are Python functions that generate resource content. They can:
- Read files
- Execute commands
- Query databases
- Generate dynamic content
- Call other services

Example handler:
```python
def read_package_resource(uri: str, params: dict[str, Any] | None = None) -> str:
    """Read package resource."""
    pm_wrapper = PackageManagerWrapper(config.project_root)
    
    if uri == "python:packages://installed":
        packages = pm_wrapper.list_installed()
        return json.dumps({"packages": packages}, indent=2)
    
    raise ValueError(f"Unknown URI: {uri}")
```

## Reloading Resources

To reload resources without restarting the server (if implemented):

```python
from python_package_mcp_server.resources.loader import get_resource_loader

loader = get_resource_loader()
loader.reload()
```

## Troubleshooting

**Resource not appearing?**
- Check file is in correct category directory
- Verify YAML is valid
- Ensure handler module/function exists
- Check server logs for errors

**Handler not found?**
- Verify module path is correct (use dot notation)
- Ensure function name matches exactly
- Check function is imported/accessible
- Verify handler signature matches expected format

**Resource read fails?**
- Check handler function implementation
- Verify handler returns string
- Check error handling in handler
- Review server logs for exceptions
