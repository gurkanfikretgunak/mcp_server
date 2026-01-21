# MCP Prompts Complete Guide

This comprehensive guide covers everything about MCP Prompts in the Python Package Manager MCP Server.

## Table of Contents

1. [What Are MCP Prompts?](#what-are-mcp-prompts)
2. [How Prompts Work](#how-prompts-work)
3. [Available Prompts](#available-prompts)
4. [Using Prompts in MCP Inspector](#using-prompts-in-mcp-inspector)
5. [Using Prompts Programmatically](#using-prompts-programmatically)
6. [Prompt Architecture](#prompt-architecture)
7. [Creating Custom Prompts](#creating-custom-prompts)
8. [Best Practices](#best-practices)
9. [Examples and Use Cases](#examples-and-use-cases)

## What Are MCP Prompts?

**MCP Prompts** are reusable prompt templates that servers can expose to clients. They allow LLMs to use pre-defined, structured prompts with customizable arguments, making it easier to perform common tasks consistently.

### Key Concepts

- **Prompt Template**: A reusable prompt structure with placeholders for arguments
- **Prompt Arguments**: Parameters that can be filled in to customize the prompt
- **Prompt Messages**: The final rendered prompt content (can include multiple messages with roles)
- **Prompt Roles**: `user` or `assistant` - indicates who "says" the message

### Prompts vs Resources vs Tools

| Feature | Prompts | Resources | Tools |
|---------|---------|-----------|-------|
| **Purpose** | Reusable prompt templates | Read-only data | Actions/operations |
| **Returns** | Formatted prompt text | Data (JSON, text, etc.) | Execution results |
| **Arguments** | Yes (customizable) | Query parameters | Yes (for execution) |
| **Use Case** | Guide LLM interactions | Access information | Perform actions |

### Why Use Prompts?

1. **Consistency**: Standardized prompts ensure consistent LLM interactions
2. **Reusability**: Define once, use many times with different arguments
3. **Discoverability**: Clients can discover available prompts
4. **Customization**: Arguments allow prompts to be tailored to specific needs
5. **Best Practices**: Prompts can encode domain expertise and best practices

## How Prompts Work

### MCP Prompt Protocol

The MCP protocol defines two main operations for prompts:

1. **`prompts/list`**: List all available prompts
2. **`prompts/get`**: Get a specific prompt with filled arguments

### Prompt Lifecycle

```
1. Client requests prompt list → Server returns available prompts
2. Client selects a prompt → Client provides arguments
3. Client requests prompt → Server fills in arguments and returns formatted prompt
4. Client uses prompt → LLM processes the formatted prompt
```

### Prompt Structure

A prompt consists of:

```python
Prompt(
    name="prompt_name",              # Unique identifier
    description="What it does",      # Human-readable description
    arguments=[                      # Optional arguments
        PromptArgument(
            name="arg_name",
            description="Argument description",
            required=True/False
        )
    ]
)
```

### Prompt Response Structure

When a prompt is retrieved, it returns:

```python
GetPromptResult(
    description="Prompt description",
    messages=[                       # Array of messages
        PromptMessage(
            role="user",             # or "assistant"
            content=TextContent(
                type="text",
                text="Formatted prompt text with arguments filled in"
            )
        )
    ]
)
```

## Available Prompts

This server provides 5 prompts:

### 1. analyze_package_dependencies

**Purpose**: Analyze package dependencies and suggest updates.

**Arguments**:
- `package_name` (optional): Name of specific package to analyze. If not provided, analyzes all packages.

**Example Usage**:
```json
{
  "name": "analyze_package_dependencies",
  "arguments": {
    "package_name": "requests"
  }
}
```

**Generated Prompt**:
```
Analyze the dependencies of the 'requests' package. Check for:
- Outdated packages that need updates
- Security vulnerabilities
- Unused dependencies
- Dependency conflicts
Provide recommendations for updates and improvements.
```

**Use Cases**:
- Dependency maintenance
- Security auditing
- Update planning
- Dependency cleanup

### 2. code_review

**Purpose**: Review code for best practices and potential issues.

**Arguments**:
- `file_path` (required): Path to the file to review
- `language` (optional): Programming language (python, dart, typescript). Defaults to "python".

**Example Usage**:
```json
{
  "name": "code_review",
  "arguments": {
    "file_path": "src/server.py",
    "language": "python"
  }
}
```

**Generated Prompt**:
```
Review the code in 'src/server.py' (python). Check for:
- Code quality and best practices
- Potential bugs or issues
- Performance optimizations
- Security concerns
- Code style and formatting
Provide constructive feedback and suggestions.
```

**Use Cases**:
- Code quality checks
- Pre-commit reviews
- Learning best practices
- Security audits

### 3. project_setup_guide

**Purpose**: Generate a comprehensive project setup guide.

**Arguments**:
- `include_dependencies` (optional): Include dependency installation instructions. Defaults to "true".

**Example Usage**:
```json
{
  "name": "project_setup_guide",
  "arguments": {
    "include_dependencies": "true"
  }
}
```

**Generated Prompt**:
```
Generate a comprehensive project setup guide. Include:
- Prerequisites and requirements
- Dependency installation instructions
- Environment setup steps
- Configuration instructions
- How to run the project
- Common troubleshooting tips
Make it clear and easy to follow for new developers.
```

**Use Cases**:
- Onboarding documentation
- README generation
- Setup instructions
- Developer guides

### 4. dependency_audit

**Purpose**: Audit project dependencies for security and updates.

**Arguments**: None (no arguments required)

**Example Usage**:
```json
{
  "name": "dependency_audit",
  "arguments": {}
}
```

**Generated Prompt**:
```
Perform a comprehensive dependency audit for this project. Check:
- All installed packages and their versions
- Outdated packages with available updates
- Security vulnerabilities (CVEs)
- License compatibility
- Unused or redundant dependencies
- Dependency conflicts
Provide a detailed report with recommendations.
```

**Use Cases**:
- Security audits
- Compliance checks
- Dependency health checks
- Update planning

### 5. code_formatting_check

**Purpose**: Check if code follows formatting standards.

**Arguments**:
- `file_path` (required): Path to the file or directory to check
- `language` (required): Programming language (python, dart, typescript)

**Example Usage**:
```json
{
  "name": "code_formatting_check",
  "arguments": {
    "file_path": "src/main.py",
    "language": "python"
  }
}
```

**Generated Prompt**:
```
Check if the code in 'src/main.py' follows python formatting standards. Verify:
- Indentation and spacing
- Line length
- Naming conventions
- Import organization
- Code style guidelines
Report any formatting issues and suggest fixes.
```

**Use Cases**:
- Style checking
- Formatting validation
- Code quality checks
- Pre-commit hooks

## Using Prompts in MCP Inspector

### Step-by-Step Guide

1. **Open MCP Inspector**:
   ```bash
   ./scripts/inspect.sh
   ```

2. **Navigate to Prompts Tab**:
   - Click on the "Prompts" tab in the Inspector UI
   - You should see a list of available prompts

3. **List Prompts**:
   - Click "List Prompts" button
   - All 5 prompts should appear in the list

4. **Get a Prompt**:
   - Click on a prompt name (e.g., "analyze_package_dependencies")
   - Fill in the arguments form:
     - For prompts with optional arguments, you can leave them empty
     - For required arguments, you must provide values
   - Click "Get Prompt" button

5. **View Generated Prompt**:
   - The formatted prompt text will appear in the response area
   - You can copy this text to use with an LLM

### Example: Using analyze_package_dependencies

1. Select "analyze_package_dependencies" from the list
2. Optionally fill in `package_name` field (e.g., "requests")
3. Click "Get Prompt"
4. Copy the generated prompt text
5. Use it with your LLM to analyze dependencies

### Example: Using code_review

1. Select "code_review" from the list
2. Fill in required `file_path` (e.g., "src/server.py")
3. Optionally fill in `language` (e.g., "python")
4. Click "Get Prompt"
5. Use the generated prompt with your LLM for code review

## Using Prompts Programmatically

### Python Client Example

```python
import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def use_prompts():
    # Connect to server
    async with stdio_client(
        command="python",
        args=["-m", "python_package_mcp_server.cli", "stdio"]
    ) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # List available prompts
            prompts_result = await session.list_prompts()
            print("Available prompts:")
            for prompt in prompts_result.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            
            # Get a specific prompt
            prompt_result = await session.get_prompt(
                "analyze_package_dependencies",
                arguments={"package_name": "requests"}
            )
            
            # Use the prompt
            for message in prompt_result.messages:
                print(f"{message.role}: {message.content.text}")

asyncio.run(use_prompts())
```

### JavaScript/TypeScript Client Example

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function usePrompts() {
  const transport = new StdioClientTransport({
    command: "python",
    args: ["-m", "python_package_mcp_server.cli", "stdio"],
  });

  const client = new Client({
    name: "prompt-client",
    version: "1.0.0",
  }, {
    capabilities: {},
  });

  await client.connect(transport);

  // List prompts
  const prompts = await client.listPrompts();
  console.log("Available prompts:", prompts.prompts);

  // Get a prompt
  const prompt = await client.getPrompt("code_review", {
    file_path: "src/server.py",
    language: "python",
  });

  console.log("Generated prompt:", prompt.messages);
}

usePrompts();
```

## Prompt Architecture

### Server-Side Implementation

Prompts are registered in `server.py`:

```python
from mcp.types import Prompt, PromptArgument, GetPromptResult, PromptMessage, TextContent

# 1. List prompts
@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        Prompt(
            name="prompt_name",
            description="Description",
            arguments=[
                PromptArgument(
                    name="arg_name",
                    description="Argument description",
                    required=True
                )
            ]
        )
    ]

# 2. Get prompt with arguments
@server.get_prompt()
async def get_prompt(
    name: str,
    arguments: dict[str, str] | None = None
) -> GetPromptResult:
    arguments = arguments or {}
    
    # Build prompt text with arguments
    prompt_text = f"Customized prompt with {arguments.get('arg_name')}"
    
    return GetPromptResult(
        description="Prompt description",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=prompt_text)
            )
        ]
    )
```

### Prompt Message Roles

Prompts can include multiple messages with different roles:

- **`user`**: Message from the user (most common)
- **`assistant`**: Message from the assistant (for multi-turn conversations)

Example with multiple messages:

```python
return GetPromptResult(
    description="Multi-turn prompt",
    messages=[
        PromptMessage(
            role="user",
            content=TextContent(type="text", text="First user message")
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(type="text", text="Assistant response")
        ),
        PromptMessage(
            role="user",
            content=TextContent(type="text", text="Follow-up user message")
        )
    ]
)
```

### Content Types

Currently, prompts support `TextContent`, but MCP also supports:

- **TextContent**: Plain text messages
- **ImageContent**: Image data (for future use)
- **EmbeddedResource**: Reference to a resource URI (for future use)

## Creating Custom Prompts

### Step 1: Define the Prompt

Add your prompt to `list_prompts()` in `server.py`:

```python
@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return [
        # ... existing prompts ...
        Prompt(
            name="my_custom_prompt",
            description="My custom prompt description",
            arguments=[
                PromptArgument(
                    name="custom_arg",
                    description="Custom argument description",
                    required=True
                )
            ]
        )
    ]
```

### Step 2: Implement the Handler

Add the handler to `get_prompt()`:

```python
@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> GetPromptResult:
    arguments = arguments or {}
    
    # ... existing handlers ...
    
    elif name == "my_custom_prompt":
        custom_arg = arguments.get("custom_arg", "")
        
        prompt_text = f"Custom prompt with argument: {custom_arg}\n"
        prompt_text += "Additional instructions..."
        
        return GetPromptResult(
            description="My custom prompt description",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )
```

### Step 3: Test Your Prompt

1. Restart the MCP server
2. Open MCP Inspector
3. Navigate to Prompts tab
4. Test your new prompt

### Example: Adding a Security Scan Prompt

```python
# In list_prompts()
Prompt(
    name="security_scan",
    description="Scan codebase for security vulnerabilities",
    arguments=[
        PromptArgument(
            name="scan_type",
            description="Type of scan (dependencies, code, all)",
            required=False
        )
    ]
)

# In get_prompt()
elif name == "security_scan":
    scan_type = arguments.get("scan_type", "all")
    
    prompt_text = f"Perform a {scan_type} security scan. Check for:\n"
    if scan_type in ["dependencies", "all"]:
        prompt_text += "- Vulnerable dependencies (CVEs)\n"
        prompt_text += "- Outdated packages with security fixes\n"
    if scan_type in ["code", "all"]:
        prompt_text += "- SQL injection vulnerabilities\n"
        prompt_text += "- XSS vulnerabilities\n"
        prompt_text += "- Hardcoded secrets\n"
        prompt_text += "- Insecure authentication\n"
    prompt_text += "Provide a detailed security report."
    
    return GetPromptResult(
        description="Scan codebase for security vulnerabilities",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=prompt_text)
            )
        ]
    )
```

## Best Practices

### 1. Clear Descriptions

Provide clear, concise descriptions:

```python
# Good
description="Analyze package dependencies and suggest updates"

# Bad
description="Analyzes stuff"
```

### 2. Descriptive Argument Names

Use clear argument names:

```python
# Good
PromptArgument(name="file_path", ...)

# Bad
PromptArgument(name="fp", ...)
```

### 3. Required vs Optional

Mark arguments as required only when necessary:

```python
# Required - prompt doesn't make sense without it
PromptArgument(name="file_path", required=True)

# Optional - prompt works with or without it
PromptArgument(name="language", required=False)
```

### 4. Structured Prompt Text

Organize prompt text for clarity:

```python
prompt_text = "Main instruction.\n\n"
prompt_text += "Check for:\n"
prompt_text += "- Item 1\n"
prompt_text += "- Item 2\n"
prompt_text += "\nProvide detailed feedback."
```

### 5. Error Handling

Handle missing required arguments:

```python
if name == "my_prompt":
    required_arg = arguments.get("required_arg")
    if not required_arg:
        raise ValueError("required_arg is required")
    
    # ... rest of handler
```

### 6. Argument Validation

Validate argument values:

```python
language = arguments.get("language", "python")
valid_languages = ["python", "dart", "typescript"]
if language not in valid_languages:
    raise ValueError(f"Invalid language. Must be one of: {valid_languages}")
```

## Examples and Use Cases

### Use Case 1: Automated Dependency Review

**Scenario**: Weekly dependency review workflow

1. Use `dependency_audit` prompt to generate audit request
2. LLM uses resources to check installed packages
3. LLM uses tools to check for outdated packages
4. LLM generates comprehensive report

**Workflow**:
```
Prompt → LLM → Resources (check packages) → Tools (check outdated) → Report
```

### Use Case 2: Code Review Workflow

**Scenario**: Pre-commit code review

1. Use `code_review` prompt with file path
2. LLM reads file content via resources
3. LLM checks standards via resources
4. LLM uses formatting tools if needed
5. LLM provides review feedback

**Workflow**:
```
Prompt → LLM → Resource (read file) → Resource (check standards) → Review
```

### Use Case 3: Onboarding Documentation

**Scenario**: Generate setup documentation for new developers

1. Use `project_setup_guide` prompt
2. LLM reads project structure via resources
3. LLM reads dependency files via resources
4. LLM generates comprehensive setup guide

**Workflow**:
```
Prompt → LLM → Resources (project info, dependencies) → Documentation
```

### Use Case 4: Continuous Formatting Checks

**Scenario**: Automated formatting validation in CI/CD

1. Use `code_formatting_check` prompt
2. LLM uses formatting tools to check code
3. LLM provides formatting report
4. CI/CD uses report to pass/fail build

**Workflow**:
```
Prompt → LLM → Tools (format check) → Report → CI/CD Decision
```

## Advanced Topics

### Multi-Message Prompts

Prompts can include multiple messages for conversation context:

```python
return GetPromptResult(
    description="Conversational prompt",
    messages=[
        PromptMessage(
            role="user",
            content=TextContent(type="text", text="Initial question")
        ),
        PromptMessage(
            role="assistant",
            content=TextContent(type="text", text="Contextual response")
        ),
        PromptMessage(
            role="user",
            content=TextContent(type="text", text="Follow-up question")
        )
    ]
)
```

### Dynamic Prompt Generation

Prompts can be generated dynamically based on project state:

```python
elif name == "dynamic_prompt":
    # Read project info
    project_info = pm_wrapper.get_project_info()
    
    # Generate prompt based on project state
    if project_info.get("lock_file", {}).get("exists"):
        prompt_text = "Project uses lock file. Check lock file consistency..."
    else:
        prompt_text = "Project doesn't use lock file. Consider adding one..."
    
    return GetPromptResult(...)
```

### Prompt Templates with Variables

Use string formatting for dynamic prompts:

```python
prompt_template = """
Analyze {package_name} package.
Current version: {current_version}
Latest version: {latest_version}

Check for:
- Security issues
- Breaking changes
- Migration path
"""

prompt_text = prompt_template.format(
    package_name=package_name,
    current_version=current_version,
    latest_version=latest_version
)
```

## Troubleshooting

### Prompt Not Appearing

**Issue**: Prompt doesn't show in Inspector

**Solutions**:
- Restart the MCP server
- Check server logs for errors
- Verify prompt is registered in `list_prompts()`
- Check prompt name matches in `get_prompt()`

### Prompt Returns Error

**Issue**: Getting error when retrieving prompt

**Solutions**:
- Check required arguments are provided
- Validate argument values
- Check error message in Inspector logs
- Verify prompt handler exists in `get_prompt()`

### Arguments Not Working

**Issue**: Arguments not being filled in correctly

**Solutions**:
- Verify argument names match exactly
- Check argument types (all are strings)
- Ensure required arguments are provided
- Check argument handling logic in handler

## Integration with Other MCP Features

### Prompts + Resources

Prompts can reference resources:

```python
prompt_text = "Analyze the project. "
prompt_text += "Use resource 'python:packages://installed' to get package list. "
prompt_text += "Then analyze each package for security issues."
```

### Prompts + Tools

Prompts can suggest tool usage:

```python
prompt_text = "Check code formatting. "
prompt_text += "Use the 'dart_format' tool to format the code, "
prompt_text += "then use 'dart_analyze' to check for issues."
```

### Prompts + Resources + Tools

Complete workflows combining all three:

```python
prompt_text = """
1. Read project dependencies using 'python:packages://installed' resource
2. Check for outdated packages using 'python:packages://outdated' resource
3. For each outdated package, use 'upgrade' tool to update
4. Verify updates using 'python:packages://installed' resource again
"""
```

## Summary

MCP Prompts provide a powerful way to:

- **Standardize** LLM interactions
- **Reuse** common prompt patterns
- **Customize** prompts with arguments
- **Discover** available prompts
- **Integrate** with resources and tools

The Python Package Manager MCP Server provides 5 ready-to-use prompts covering:
- Dependency analysis
- Code review
- Project setup
- Security auditing
- Formatting checks

Prompts work seamlessly with resources and tools to create powerful LLM-assisted workflows.

## Additional Resources

- [MCP Specification - Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)
- [MCP Python SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [Inspector Guide](inspector-guide.md) - How to use prompts in Inspector
- [Learning Guide](learning.md) - MCP concepts and architecture
