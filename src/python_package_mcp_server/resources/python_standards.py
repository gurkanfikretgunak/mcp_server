"""Python language standards resources."""

import json
from typing import Any

from mcp.types import Resource, ResourceTemplate


def get_python_resources() -> list[Resource]:
    """Get Python standards resources.

    Returns:
        List of resource definitions
    """
    return [
        Resource(
            uri="python:standards://style-guide",
            name="Python Style Guide (PEP 8)",
            description="PEP 8 style guide with naming conventions and formatting rules",
            mimeType="application/json",
        ),
        Resource(
            uri="python:standards://type-hints",
            name="Python Type Hints",
            description="Type hinting guidelines (PEP 484, 526, 544, 585, 604)",
            mimeType="application/json",
        ),
        Resource(
            uri="python:standards://linting-rules",
            name="Python Linting Rules",
            description="Linting rules for ruff, pylint, and flake8",
            mimeType="application/json",
        ),
        Resource(
            uri="python:standards://best-practices",
            name="Python Best Practices",
            description="Python best practices for code quality and maintainability",
            mimeType="application/json",
        ),
    ]


def read_python_resource(uri: str) -> str:
    """Read Python standards resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)
    
    if uri_str == "python:standards://style-guide":
        return json.dumps({
            "title": "Python Style Guide (PEP 8)",
            "naming_conventions": {
                "variables": "snake_case (e.g., user_name)",
                "functions": "snake_case (e.g., get_user_data)",
                "classes": "PascalCase (e.g., UserProfile)",
                "constants": "UPPER_SNAKE_CASE (e.g., API_BASE_URL)",
                "private": "leading underscore (_private_method)",
                "protected": "leading underscore (no trailing underscore)",
                "dunder": "leading and trailing double underscore (__special__)",
            },
            "formatting": {
                "indentation": "4 spaces (no tabs)",
                "line_length": "79 characters (or 88 with black)",
                "blank_lines": {
                    "top_level": "2 blank lines",
                    "class_methods": "1 blank line",
                    "function_inner": "1 blank line for logical sections",
                },
                "imports": {
                    "order": "1. Standard library, 2. Related third party, 3. Local application",
                    "grouping": "Separate groups with blank lines",
                    "style": "Use absolute imports, avoid wildcard imports",
                },
                "whitespace": {
                    "around_operators": "Use spaces around operators",
                    "function_def": "No spaces around = in default arguments",
                    "trailing_commas": "Use trailing commas in multi-line collections",
                },
            },
            "code_organization": {
                "imports": "Order: standard library, third-party, local",
                "constants": "Module-level constants after imports",
                "classes": "Class definitions",
                "functions": "Function definitions",
                "main": "if __name__ == '__main__': at end",
            },
            "docstrings": {
                "style": "Use triple double quotes",
                "format": "Google style or NumPy style",
                "summary": "First line should be a brief summary",
                "sections": "Args, Returns, Raises, Examples",
            },
        }, indent=2)

    elif uri_str == "python:standards://type-hints":
        return json.dumps({
            "title": "Python Type Hints",
            "peps": {
                "pep_484": "Type Hints (original proposal)",
                "pep_526": "Syntax for Variable Annotations",
                "pep_544": "Protocols: Structural subtyping (static duck typing)",
                "pep_585": "Type Hinting Generics In Standard Collections",
                "pep_604": "Union Types: X | Y syntax",
            },
            "basic_types": {
                "primitives": "int, float, str, bool, bytes",
                "collections": "list[T], dict[K, V], tuple[T, ...], set[T]",
                "optional": "Optional[T] or T | None",
                "union": "Union[T, U] or T | U",
                "any": "Any (use sparingly)",
            },
            "function_annotations": {
                "parameters": "def func(param: int) -> str:",
                "return_type": "Always annotate return type (use None for no return)",
                "defaults": "def func(param: int = 0) -> str:",
                "varargs": "def func(*args: int) -> None:",
                "kwargs": "def func(**kwargs: str) -> None:",
            },
            "class_annotations": {
                "attributes": "class_var: int = 0",
                "methods": "def method(self) -> None:",
                "class_methods": "@classmethod def method(cls) -> None:",
                "static_methods": "@staticmethod def method() -> None:",
            },
            "advanced_types": {
                "generic": "class Container[T]:",
                "protocol": "class Drawable(Protocol):",
                "typed_dict": "class User(TypedDict): name: str",
                "literal": "Literal['a', 'b', 'c']",
                "final": "Final[int] = 42",
            },
            "best_practices": {
                "use_type_hints": "Always use type hints for public APIs",
                "avoid_any": "Avoid Any, use Union or Protocol instead",
                "use_typing_module": "Import from typing module for complex types",
                "gradual_typing": "Add type hints incrementally",
                "type_checkers": "Use mypy or pyright for type checking",
            },
        }, indent=2)

    elif uri_str == "python:standards://linting-rules":
        return json.dumps({
            "title": "Python Linting Rules",
            "tools": {
                "ruff": {
                    "description": "Fast, modern linter written in Rust",
                    "replaces": "flake8, isort, and more",
                    "recommended": True,
                },
                "pylint": {
                    "description": "Comprehensive linter with extensive checks",
                    "focus": "Code quality and style",
                },
                "flake8": {
                    "description": "Style guide enforcement",
                    "focus": "PEP 8 compliance",
                },
            },
            "common_rules": {
                "line_length": "E501: Line too long (79 or 88 characters)",
                "imports": "E401: Multiple imports on one line",
                "whitespace": "E302: Expected 2 blank lines",
                "naming": "N802: Function name should be lowercase",
                "unused": "F401: Module imported but unused",
                "undefined": "F821: Undefined name",
            },
            "ruff_specific": {
                "enabled_by_default": "Most rules enabled by default",
                "config_file": "pyproject.toml or ruff.toml",
                "categories": [
                    "E: pycodestyle errors",
                    "W: pycodestyle warnings",
                    "F: Pyflakes",
                    "I: isort",
                    "N: pep8-naming",
                    "UP: pyupgrade",
                    "B: flake8-bugbear",
                    "C4: flake8-comprehensions",
                ],
            },
            "pylint_specific": {
                "categories": [
                    "C: Convention (PEP 8)",
                    "R: Refactor",
                    "W: Warning",
                    "E: Error",
                    "F: Fatal",
                ],
                "common_checks": [
                    "missing-docstring",
                    "invalid-name",
                    "too-many-arguments",
                    "too-many-locals",
                    "too-many-branches",
                ],
            },
            "flake8_specific": {
                "plugins": [
                    "flake8-docstrings",
                    "flake8-import-order",
                    "flake8-bugbear",
                ],
            },
            "recommended_config": {
                "ruff": {
                    "line-length": 88,
                    "select": ["E", "F", "I", "N", "UP", "B", "C4"],
                },
                "pylint": {
                    "max-line-length": 88,
                    "disable": ["missing-docstring"],
                },
            },
        }, indent=2)

    elif uri_str == "python:standards://best-practices":
        return json.dumps({
            "title": "Python Best Practices",
            "code_organization": {
                "summary": "Organize code effectively",
                "practices": [
                    "Use modules and packages for organization",
                    "Keep functions and classes focused (single responsibility)",
                    "Use __init__.py for package initialization",
                    "Separate concerns (models, views, controllers)",
                ],
            },
            "error_handling": {
                "summary": "Handle errors gracefully",
                "practices": [
                    "Use specific exceptions, not bare except",
                    "Let exceptions propagate when appropriate",
                    "Use try/except/finally for resource cleanup",
                    "Use context managers (with statement) for resources",
                    "Create custom exceptions when needed",
                ],
            },
            "performance": {
                "summary": "Write efficient Python code",
                "practices": [
                    "Use list comprehensions for simple transformations",
                    "Use generators for large datasets",
                    "Use built-in functions (map, filter, reduce)",
                    "Avoid premature optimization",
                    "Profile before optimizing",
                    "Use appropriate data structures (set for membership, dict for lookups)",
                ],
            },
            "async_programming": {
                "summary": "Best practices for async/await",
                "practices": [
                    "Use async/await instead of callbacks",
                    "Use asyncio.gather() for parallel operations",
                    "Handle errors with try/except in async functions",
                    "Use async context managers",
                    "Avoid blocking I/O in async functions",
                ],
            },
            "testing": {
                "summary": "Python testing best practices",
                "practices": [
                    "Use pytest for testing",
                    "Follow Arrange-Act-Assert pattern",
                    "Use descriptive test names",
                    "Test edge cases and error conditions",
                    "Use fixtures for test setup",
                    "Mock external dependencies",
                    "Aim for high test coverage",
                ],
            },
            "documentation": {
                "summary": "Document code effectively",
                "practices": [
                    "Write docstrings for all public functions and classes",
                    "Use Google or NumPy style docstrings",
                    "Include examples in docstrings",
                    "Keep comments up to date",
                    "Document complex algorithms",
                ],
            },
            "security": {
                "summary": "Security best practices",
                "practices": [
                    "Validate and sanitize user input",
                    "Use parameterized queries for databases",
                    "Avoid eval() and exec() with user input",
                    "Keep dependencies updated",
                    "Use secrets module for sensitive data",
                    "Follow principle of least privilege",
                ],
            },
            "dependencies": {
                "summary": "Manage dependencies effectively",
                "practices": [
                    "Use virtual environments",
                    "Pin dependency versions in requirements.txt",
                    "Use pyproject.toml for modern projects",
                    "Keep dependencies minimal",
                    "Regularly update dependencies",
                    "Use dependency management tools (pip, poetry, uv)",
                ],
            },
        }, indent=2)

    else:
        raise ValueError(f"Unknown Python resource URI: {uri_str}")


def get_python_resource_templates() -> list[ResourceTemplate]:
    """Get Python resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="python:standards://style-guide",
            name="Python Style Guide (PEP 8)",
            description="PEP 8 style guide with naming conventions and formatting rules",
        ),
        ResourceTemplate(
            uriTemplate="python:standards://type-hints",
            name="Python Type Hints",
            description="Type hinting guidelines (PEP 484, 526, 544, 585, 604)",
        ),
        ResourceTemplate(
            uriTemplate="python:standards://linting-rules",
            name="Python Linting Rules",
            description="Linting rules for ruff, pylint, and flake8",
        ),
        ResourceTemplate(
            uriTemplate="python:standards://best-practices",
            name="Python Best Practices",
            description="Python best practices for code quality and maintainability",
        ),
    ]
