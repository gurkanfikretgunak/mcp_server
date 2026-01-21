"""TypeScript language standards tools."""

import json
from pathlib import Path
from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..utils.typescript_wrapper import TypeScriptError, TypeScriptWrapper

audit_logger = AuditLogger(config.log_format)


def get_typescript_tools() -> list[Tool]:
    """Get TypeScript tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="typescript_format",
            description="Format TypeScript code using Prettier",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to format (formats all if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="typescript_lint",
            description="Lint TypeScript code using ESLint",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to lint (lints all if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="typescript_type_check",
            description="Type check TypeScript code using tsc",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Optional path to tsconfig.json (uses default if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="typescript_generate_code",
            description="Generate TypeScript code following standards and best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_description": {
                        "type": "string",
                        "description": "Description of the code to generate",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Optional file path where code should be written",
                    },
                    "include_tests": {
                        "type": "boolean",
                        "description": "Whether to include test code",
                        "default": False,
                    },
                },
                "required": ["code_description"],
            },
        ),
        Tool(
            name="typescript_check_standards",
            description="Check if TypeScript code follows standards and best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to TypeScript file to check",
                    },
                },
                "required": ["file_path"],
            },
        ),
    ]


async def handle_typescript_format(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle typescript_format tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")

    try:
        ts_wrapper = TypeScriptWrapper(config.project_root)
        result = ts_wrapper.format_code(paths=paths)

        audit_logger.log_tool_invocation(
            "typescript_format",
            parameters={"paths": paths},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text=f"Successfully formatted TypeScript code.\n{result['output']}")]
        else:
            return [TextContent(type="text", text=f"Formatting completed with issues:\n{result.get('errors', '')}")]

    except TypeScriptError as e:
        audit_logger.log_tool_invocation(
            "typescript_format",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Error formatting TypeScript code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "typescript_format",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_typescript_lint(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle typescript_lint tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")

    try:
        ts_wrapper = TypeScriptWrapper(config.project_root)
        result = ts_wrapper.lint_code(paths=paths)

        audit_logger.log_tool_invocation(
            "typescript_lint",
            parameters={"paths": paths},
            result=result,
            success=result["success"],
        )

        issues_count = len(result.get("issues", []))
        if result["success"] and issues_count == 0:
            return [TextContent(type="text", text="TypeScript linting completed with no issues found.")]
        else:
            issues_json = json.dumps(result.get("issues", []), indent=2)
            return [TextContent(type="text", text=f"Linting found {issues_count} issue(s):\n{issues_json}")]

    except TypeScriptError as e:
        audit_logger.log_tool_invocation(
            "typescript_lint",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Error linting TypeScript code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "typescript_lint",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_typescript_type_check(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle typescript_type_check tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    project_path = arguments.get("project_path")

    try:
        ts_wrapper = TypeScriptWrapper(config.project_root)
        result = ts_wrapper.type_check(project_path=project_path)

        audit_logger.log_tool_invocation(
            "typescript_type_check",
            parameters={"project_path": project_path},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text="TypeScript type checking passed with no errors.")]
        else:
            return [TextContent(type="text", text=f"Type checking found errors:\n{result.get('errors', '')}")]

    except TypeScriptError as e:
        audit_logger.log_tool_invocation(
            "typescript_type_check",
            parameters={"project_path": project_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Error type checking TypeScript code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "typescript_type_check",
            parameters={"project_path": project_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_typescript_generate_code(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle typescript_generate_code tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    code_description = arguments.get("code_description", "")
    file_path = arguments.get("file_path")
    include_tests = arguments.get("include_tests", False)

    if not code_description:
        return [TextContent(type="text", text="Error: code_description is required")]

    try:
        # This is a placeholder - in a real implementation, you might use an LLM
        # or code generation library to generate TypeScript code
        # For now, we'll return guidance based on standards
        
        from ..resources.typescript_standards import read_typescript_resource
        standards = json.loads(read_typescript_resource("typescript:standards://style-guide"))
        
        generated_code = f"""// Generated TypeScript code following style guide
// Description: {code_description}

// TODO: Implement based on description
// Follow these guidelines:
// - Use PascalCase for interfaces and types
// - Use camelCase for variables and functions
// - Avoid 'any' type - use proper types
// - Use interfaces for object shapes
// - Enable strict mode in tsconfig.json
"""

        if include_tests:
            generated_code += """
// Test code:
// TODO: Add tests following TypeScript testing conventions
"""

        result_text = f"Generated TypeScript code following standards:\n\n{generated_code}"
        
        if file_path:
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_path_obj.write_text(generated_code)
            result_text += f"\n\nCode written to: {file_path}"

        audit_logger.log_tool_invocation(
            "typescript_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=True,
        )

        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "typescript_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=False,
        )
        return [TextContent(type="text", text=f"Error generating TypeScript code: {str(e)}")]


async def handle_typescript_check_standards(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle typescript_check_standards tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    file_path = arguments.get("file_path")

    if not file_path:
        return [TextContent(type="text", text="Error: file_path is required")]

    try:
        ts_wrapper = TypeScriptWrapper(config.project_root)
        result = ts_wrapper.check_standards(file_path)

        audit_logger.log_tool_invocation(
            "typescript_check_standards",
            parameters={"file_path": file_path},
            result=result,
            success=True,
        )

        compliance_status = "✓ Compliant" if result["standards_compliant"] else "✗ Not Compliant"
        result_text = f"Standards check for {file_path}:\n"
        result_text += f"Status: {compliance_status}\n"
        result_text += f"Properly formatted: {'Yes' if result['formatted'] else 'No'}\n"
        
        linting = result.get("linting", {})
        issues = linting.get("issues", [])
        if issues:
            result_text += f"Linting issues found: {len(issues)}\n"
            result_text += json.dumps(issues, indent=2)

        return [TextContent(type="text", text=result_text)]

    except TypeScriptError as e:
        audit_logger.log_tool_invocation(
            "typescript_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Error checking standards: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "typescript_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
