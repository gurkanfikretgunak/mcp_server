"""Dart language standards resources."""

import json
from typing import Any

from mcp.types import Resource, ResourceTemplate


def get_dart_resources() -> list[Resource]:
    """Get Dart standards resources.

    Returns:
        List of resource definitions
    """
    return [
        Resource(
            uri="dart:standards://effective-dart",
            name="Effective Dart Guidelines",
            description="Official Effective Dart style guide and best practices",
            mimeType="application/json",
        ),
        Resource(
            uri="dart:standards://style-guide",
            name="Dart Style Guide",
            description="Dart style guide with naming conventions and formatting rules",
            mimeType="application/json",
        ),
        Resource(
            uri="dart:standards://linter-rules",
            name="Dart Linter Rules",
            description="Complete list of Dart linter rules and their descriptions",
            mimeType="application/json",
        ),
        Resource(
            uri="dart:standards://best-practices",
            name="Dart Best Practices",
            description="Dart best practices for code quality and maintainability",
            mimeType="application/json",
        ),
    ]


def read_dart_resource(uri: str) -> str:
    """Read Dart standards resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)
    
    if uri_str == "dart:standards://effective-dart":
        return json.dumps({
            "title": "Effective Dart Guidelines",
            "sections": {
                "style": {
                    "summary": "Guidelines for writing consistent, readable Dart code",
                    "key_points": [
                        "Use lowerCamelCase for variable names, function names, and parameters",
                        "Use UpperCamelCase for class names, enum types, and type parameters",
                        "Use lowercase_with_underscores for library names and file names",
                        "Use SCREAMING_CAPS for constants",
                        "Prefer final for variables that are not reassigned",
                        "Use const for compile-time constants",
                    ],
                },
                "documentation": {
                    "summary": "Best practices for documenting Dart code",
                    "key_points": [
                        "Write documentation comments for public APIs",
                        "Use /// for documentation comments",
                        "Include examples in documentation when helpful",
                        "Document parameters and return values",
                    ],
                },
                "usage": {
                    "summary": "Guidelines for using Dart language features effectively",
                    "key_points": [
                        "Prefer using collection literals",
                        "Use async/await instead of Future.then()",
                        "Use ?? and ??= for null-aware operators",
                        "Prefer using final and const",
                        "Use cascade notation (..) when appropriate",
                    ],
                },
            },
        }, indent=2)

    elif uri_str == "dart:standards://style-guide":
        return json.dumps({
            "title": "Dart Style Guide",
            "naming_conventions": {
                "variables": "lowerCamelCase",
                "classes": "UpperCamelCase",
                "libraries": "lowercase_with_underscores",
                "constants": "SCREAMING_CAPS",
                "private": "leading underscore (_private)",
            },
            "formatting": {
                "indentation": "2 spaces",
                "line_length": "80 characters (recommended)",
                "trailing_commas": "Use trailing commas in multi-line collections",
                "blank_lines": "Use blank lines to separate logical sections",
            },
            "code_organization": {
                "imports": "Order: dart: imports, package: imports, relative imports",
                "exports": "Place exports after imports",
                "declarations": "Order: constants, variables, constructors, methods",
            },
        }, indent=2)

    elif uri_str == "dart:standards://linter-rules":
        return json.dumps({
            "title": "Dart Linter Rules",
            "recommended_packages": [
                "package:pedantic",
                "package:effective_dart",
                "package:lints",
            ],
            "common_rules": {
                "always_declare_return_types": "Always declare return types for functions",
                "avoid_print": "Avoid using print() in production code",
                "prefer_const_constructors": "Prefer const constructors when possible",
                "prefer_final_locals": "Prefer final for local variables",
                "use_key_in_widget_constructors": "Use key parameter in widget constructors (Flutter)",
                "avoid_empty_else": "Avoid empty else blocks",
                "prefer_single_quotes": "Prefer single quotes for strings",
                "sort_pub_dependencies": "Sort pubspec.yaml dependencies alphabetically",
            },
            "error_rules": [
                "avoid_relative_lib_imports",
                "avoid_types_as_parameter_names",
                "cancel_subscriptions",
                "close_sinks",
            ],
            "style_rules": [
                "always_put_required_named_parameters_first",
                "always_put_super_last",
                "always_specify_types",
                "avoid_annotating_with_dynamic",
            ],
        }, indent=2)

    elif uri_str == "dart:standards://best-practices":
        return json.dumps({
            "title": "Dart Best Practices",
            "null_safety": {
                "summary": "Use null safety features effectively",
                "practices": [
                    "Use ? for nullable types",
                    "Use ! for non-null assertion when certain",
                    "Use ?? for null coalescing",
                    "Use ??= for null-aware assignment",
                ],
            },
            "async_programming": {
                "summary": "Best practices for async/await",
                "practices": [
                    "Prefer async/await over Future.then()",
                    "Use Future.wait() for parallel operations",
                    "Handle errors with try-catch",
                    "Use Future.timeout() for timeouts",
                ],
            },
            "collections": {
                "summary": "Effective use of collections",
                "practices": [
                    "Use collection literals when possible",
                    "Prefer List.generate() for generated lists",
                    "Use Map.from() for copying maps",
                    "Use Set for unique collections",
                ],
            },
            "performance": {
                "summary": "Performance optimization tips",
                "practices": [
                    "Use const constructors when possible",
                    "Prefer final over var",
                    "Use const collections for immutable data",
                    "Avoid unnecessary object creation",
                ],
            },
        }, indent=2)

    else:
        raise ValueError(f"Unknown Dart resource URI: {uri_str}")


def get_dart_resource_templates() -> list[ResourceTemplate]:
    """Get Dart resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="dart:standards://effective-dart",
            name="Effective Dart Guidelines",
            description="Official Effective Dart style guide and best practices",
        ),
        ResourceTemplate(
            uriTemplate="dart:standards://style-guide",
            name="Dart Style Guide",
            description="Dart style guide with naming conventions and formatting rules",
        ),
        ResourceTemplate(
            uriTemplate="dart:standards://linter-rules",
            name="Dart Linter Rules",
            description="Complete list of Dart linter rules and their descriptions",
        ),
        ResourceTemplate(
            uriTemplate="dart:standards://best-practices",
            name="Dart Best Practices",
            description="Dart best practices for code quality and maintainability",
        ),
    ]
