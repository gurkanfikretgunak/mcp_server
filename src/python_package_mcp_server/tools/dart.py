"""Dart language standards tools."""

import json
from pathlib import Path
from typing import Any

from mcp.types import Tool, TextContent

from ..config import config
from ..security.audit import AuditLogger
from ..utils.dart_wrapper import DartError, DartWrapper

audit_logger = AuditLogger(config.log_format)


def get_dart_tools() -> list[Tool]:
    """Get Dart tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name="dart_format",
            description="Format Dart code according to Dart style guide",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to format (formats all if not specified)",
                    },
                    "line_length": {
                        "type": "integer",
                        "description": "Line length for formatting",
                        "default": 80,
                    },
                },
            },
        ),
        Tool(
            name="dart_analyze",
            description="Analyze Dart code for errors and warnings",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to analyze (analyzes all if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="dart_fix",
            description="Apply automated fixes to Dart code",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of file/directory paths to fix (fixes all if not specified)",
                    },
                },
            },
        ),
        Tool(
            name="dart_generate_code",
            description="Generate Dart code following standards and best practices",
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
            name="dart_check_standards",
            description="Check if Dart code follows standards and best practices",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to Dart file to check",
                    },
                },
                "required": ["file_path"],
            },
        ),
    ]


async def handle_dart_format(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle dart_format tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")
    line_length = arguments.get("line_length", 80)

    try:
        dart_wrapper = DartWrapper(config.project_root)
        result = dart_wrapper.format_code(paths=paths, line_length=line_length)

        audit_logger.log_tool_invocation(
            "dart_format",
            parameters={"paths": paths, "line_length": line_length},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text=f"Successfully formatted Dart code.\n{result['output']}")]
        else:
            return [TextContent(type="text", text=f"Formatting completed with issues:\n{result.get('errors', '')}")]

    except DartError as e:
        audit_logger.log_tool_invocation(
            "dart_format",
            parameters={"paths": paths, "line_length": line_length},
            success=False,
        )
        return [TextContent(type="text", text=f"Error formatting Dart code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "dart_format",
            parameters={"paths": paths, "line_length": line_length},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_dart_analyze(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle dart_analyze tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")

    try:
        dart_wrapper = DartWrapper(config.project_root)
        result = dart_wrapper.analyze_code(paths=paths)

        audit_logger.log_tool_invocation(
            "dart_analyze",
            parameters={"paths": paths},
            result=result,
            success=result["success"],
        )

        issues_count = len(result.get("issues", []))
        if result["success"] and issues_count == 0:
            return [TextContent(type="text", text="Dart code analysis completed with no issues found.")]
        else:
            issues_json = json.dumps(result.get("issues", []), indent=2)
            return [TextContent(type="text", text=f"Analysis found {issues_count} issue(s):\n{issues_json}")]

    except DartError as e:
        audit_logger.log_tool_invocation(
            "dart_analyze",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Error analyzing Dart code: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "dart_analyze",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_dart_fix(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle dart_fix tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    paths = arguments.get("paths")

    try:
        dart_wrapper = DartWrapper(config.project_root)
        result = dart_wrapper.fix_code(paths=paths)

        audit_logger.log_tool_invocation(
            "dart_fix",
            parameters={"paths": paths},
            result=result,
            success=result["success"],
        )

        if result["success"]:
            return [TextContent(type="text", text=f"Successfully applied fixes to Dart code.\n{result['output']}")]
        else:
            return [TextContent(type="text", text=f"Fixes applied with issues:\n{result.get('errors', '')}")]

    except DartError as e:
        audit_logger.log_tool_invocation(
            "dart_fix",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Error applying fixes: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "dart_fix",
            parameters={"paths": paths},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def handle_dart_generate_code(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle dart_generate_code tool invocation.

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
        # or code generation library to generate Dart code
        # For now, we'll return guidance based on standards
        
        from ..resources.dart_standards import read_dart_resource
        standards = json.loads(read_dart_resource("dart:standards://effective-dart"))
        
        generated_code = f"""// Generated Dart code following Effective Dart guidelines
// Description: {code_description}

// TODO: Implement based on description
// Follow these guidelines:
// - Use lowerCamelCase for variables and functions
// - Use UpperCamelCase for classes
// - Prefer final and const
// - Use async/await for asynchronous code
"""

        if include_tests:
            generated_code += """
// Test code:
// TODO: Add tests following Dart testing conventions
"""

        result_text = f"Generated Dart code following standards:\n\n{generated_code}"
        
        if file_path:
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_path_obj.write_text(generated_code)
            result_text += f"\n\nCode written to: {file_path}"

        audit_logger.log_tool_invocation(
            "dart_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=True,
        )

        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        audit_logger.log_tool_invocation(
            "dart_generate_code",
            parameters={"code_description": code_description, "file_path": file_path, "include_tests": include_tests},
            success=False,
        )
        return [TextContent(type="text", text=f"Error generating Dart code: {str(e)}")]


async def handle_dart_check_standards(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle dart_check_standards tool invocation.

    Args:
        arguments: Tool arguments

    Returns:
        Tool result
    """
    file_path = arguments.get("file_path")

    if not file_path:
        return [TextContent(type="text", text="Error: file_path is required")]

    try:
        dart_wrapper = DartWrapper(config.project_root)
        result = dart_wrapper.check_standards(file_path)

        audit_logger.log_tool_invocation(
            "dart_check_standards",
            parameters={"file_path": file_path},
            result=result,
            success=True,
        )

        compliance_status = "✓ Compliant" if result["standards_compliant"] else "✗ Not Compliant"
        result_text = f"Standards check for {file_path}:\n"
        result_text += f"Status: {compliance_status}\n"
        result_text += f"Properly formatted: {'Yes' if result['formatted'] else 'No'}\n"
        
        issues = result.get("analysis", {}).get("issues", [])
        if issues:
            result_text += f"Issues found: {len(issues)}\n"
            result_text += json.dumps(issues, indent=2)

        return [TextContent(type="text", text=result_text)]

    except DartError as e:
        audit_logger.log_tool_invocation(
            "dart_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Error checking standards: {str(e)}")]
    except Exception as e:
        audit_logger.log_tool_invocation(
            "dart_check_standards",
            parameters={"file_path": file_path},
            success=False,
        )
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
