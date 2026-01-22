"""Python language standards tools."""

import json
from pathlib import Path
from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..utils.python_wrapper import PythonError, PythonWrapper

audit_logger = AuditLogger(config.log_format)


def get_python_tools() -> list[Tool]:
    """Get Python tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="python_format",
            description="Format Python code using black or autopep8",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to format (formats all if not specified)",
                    },
                    "formatter": {
                        "type": "string",
                        "enum": ["black", "autopep8"],
                        "description": "Formatter to use (default: black)",
                        "default": "black",
                    },
                },
            },
        ),
        Tool(
            name="python_lint",
            description="Lint Python code using ruff, pylint, or flake8",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to lint (lints all if not specified)",
                    },
                    "linter": {
                        "type": "string",
                        "enum": ["ruff", "pylint", "flake8"],
                        "description": "Linter to use (default: ruff)",
                        "default": "ruff",
                    },
                },
            },
        ),
        Tool(
            name="python_type_check",
            description="Type check Python code using mypy or pyright",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to type check (checks all if not specified)",
                    },
                    "type_checker": {
                        "type": "string",
                        "enum": ["mypy", "pyright"],
                        "description": "Type checker to use (default: mypy)",
                        "default": "mypy",
                    },
                },
            },
        ),
        Tool(
            name="python_generate_code",
            description="Generate Python code following PEP 8 and best practices",
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
            name="python_check_standards",
            description="Check if Python code follows PEP 8 and best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to Python file to check",
                    },
                },
                "required": ["file_path"],
            },
        ),
    ]


async def handle_python_format(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle python_format tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")
    formatter = arguments.get("formatter", "black")

    try:
        python_wrapper = PythonWrapper(config.project_root)
        result = python_wrapper.format_code(paths=paths, formatter=formatter)

        audit_logger.log_tool_invocation(
            "python_format",
            parameters={"paths": paths, "formatter": formatter},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text=f"Successfully formatted Python code using {formatter}.\n{result['output']}")]
        else:
            return [TextContent(type="text", text=f"Formatting completed with issues:\n{result.get('errors', '')}")]

    except PythonError as e:
        audit_logger.log_tool_invocation(
            "python_format",
            parameters={"paths": paths, "formatter": formatter},
            success=False,
        )
        return [TextContent(type="text", text=f"Error formatting Python code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "python_format",
            parameters={"paths": paths, "formatter": formatter},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_python_lint(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle python_lint tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")
    linter = arguments.get("linter", "ruff")

    try:
        python_wrapper = PythonWrapper(config.project_root)
        result = python_wrapper.lint_code(paths=paths, linter=linter)

        audit_logger.log_tool_invocation(
            "python_lint",
            parameters={"paths": paths, "linter": linter},
            result=result,
            success=result["success"],
        )

        issues_count = len(result.get("issues", []))
        if result["success"] and issues_count == 0:
            return [TextContent(type="text", text=f"Python linting completed with no issues found using {linter}.")]
        else:
            issues_json = json.dumps(result.get("issues", []), indent=2)
            return [TextContent(type="text", text=f"Linting found {issues_count} issue(s) using {linter}:\n{issues_json}")]

    except PythonError as e:
        audit_logger.log_tool_invocation(
            "python_lint",
            parameters={"paths": paths, "linter": linter},
            success=False,
        )
        return [TextContent(type="text", text=f"Error linting Python code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "python_lint",
            parameters={"paths": paths, "linter": linter},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_python_type_check(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle python_type_check tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")
    type_checker = arguments.get("type_checker", "mypy")

    try:
        python_wrapper = PythonWrapper(config.project_root)
        result = python_wrapper.type_check(paths=paths, type_checker=type_checker)

        audit_logger.log_tool_invocation(
            "python_type_check",
            parameters={"paths": paths, "type_checker": type_checker},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text=f"Python type checking passed with no errors using {type_checker}.")]
        else:
            return [TextContent(type="text", text=f"Type checking found errors using {type_checker}:\n{result.get('errors', result.get('output', ''))}")]

    except PythonError as e:
        audit_logger.log_tool_invocation(
            "python_type_check",
            parameters={"paths": paths, "type_checker": type_checker},
            success=False,
        )
        return [TextContent(type="text", text=f"Error type checking Python code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "python_type_check",
            parameters={"paths": paths, "type_checker": type_checker},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_python_generate_code(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle python_generate_code tool invocation.

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
        # or code generation library to generate Python code
        # For now, we'll return guidance based on standards
        
        from ..resources.python_standards import read_python_resource
        standards = json.loads(read_python_resource("python:standards://style-guide"))
        
        generated_code = f'''"""Generated Python code following PEP 8 guidelines.
Description: {code_description}
"""

# TODO: Implement based on description
# Follow these guidelines:
# - Use snake_case for variables and functions
# - Use PascalCase for classes
# - Use UPPER_CASE for constants
# - Follow PEP 8 style guide
# - Add type hints (PEP 484)
# - Use docstrings (PEP 257)
'''

        if include_tests:
            generated_code += '''
# Test code:
# TODO: Add tests following pytest conventions
# Example:
# def test_function():
#     assert function() == expected_result
'''

        result_text = f"Generated Python code following standards:\n\n{generated_code}"
        
        if file_path:
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_path_obj.write_text(generated_code)
            result_text += f"\n\nCode written to: {file_path}"

        audit_logger.log_tool_invocation(
            "python_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=True,
        )

        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "python_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=False,
        )
        return [TextContent(type="text", text=f"Error generating Python code: {str(e)}")]


async def handle_python_check_standards(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle python_check_standards tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    file_path = arguments.get("file_path")

    if not file_path:
        return [TextContent(type="text", text="Error: file_path is required")]

    try:
        python_wrapper = PythonWrapper(config.project_root)
        result = python_wrapper.check_standards(file_path)

        audit_logger.log_tool_invocation(
            "python_check_standards",
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
        
        type_checking = result.get("type_checking")
        if type_checking:
            if type_checking.get("success"):
                result_text += "\nType checking: Passed"
            else:
                result_text += f"\nType checking: Failed\n{type_checking.get('errors', '')}"

        return [TextContent(type="text", text=result_text)]

    except PythonError as e:
        audit_logger.log_tool_invocation(
            "python_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Error checking standards: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "python_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
