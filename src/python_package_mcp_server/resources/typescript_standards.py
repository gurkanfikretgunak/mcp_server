"""TypeScript language standards resources."""

import json
from typing import Any

from mcp.types import Resource, ResourceTemplate


def get_typescript_resources() -> list[Resource]:
    """Get TypeScript standards resources.

    Returns:
        List of resource definitions
    """
    return [
        Resource(
            uri="typescript:standards://style-guide",
            name="TypeScript Style Guide",
            description="TypeScript style guide with naming conventions and formatting rules",
            mimeType="application/json",
        ),
        Resource(
            uri="typescript:standards://tsconfig-options",
            name="TypeScript tsconfig Options",
            description="Recommended tsconfig.json compiler options and their meanings",
            mimeType="application/json",
        ),
        Resource(
            uri="typescript:standards://eslint-rules",
            name="TypeScript ESLint Rules",
            description="ESLint rules for TypeScript code quality and consistency",
            mimeType="application/json",
        ),
        Resource(
            uri="typescript:standards://best-practices",
            name="TypeScript Best Practices",
            description="TypeScript best practices for type safety and code quality",
            mimeType="application/json",
        ),
    ]


def read_typescript_resource(uri: str) -> str:
    """Read TypeScript standards resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    if uri == "typescript:standards://style-guide":
        return json.dumps({
            "title": "TypeScript Style Guide",
            "naming_conventions": {
                "interfaces": "PascalCase (e.g., UserProfile)",
                "types": "PascalCase (e.g., ApiResponse)",
                "classes": "PascalCase (e.g., UserService)",
                "variables": "camelCase (e.g., userName)",
                "constants": "UPPER_SNAKE_CASE (e.g., API_BASE_URL)",
                "private_members": "leading underscore (_privateMethod)",
            },
            "formatting": {
                "indentation": "2 spaces",
                "semicolons": "Use semicolons consistently",
                "quotes": "Use double quotes for strings",
                "trailing_commas": "Use trailing commas in multi-line objects/arrays",
            },
            "type_definitions": {
                "prefer_interfaces": "Use interfaces for object shapes",
                "avoid_any": "Avoid using 'any' type",
                "use_union_types": "Use union types for multiple possible types",
                "prefer_type_aliases": "Use type aliases for complex types",
            },
        }, indent=2)

    elif uri == "typescript:standards://tsconfig-options":
        return json.dumps({
            "title": "TypeScript tsconfig.json Options",
            "recommended_config": {
                "compilerOptions": {
                    "target": "ES2020 or higher",
                    "module": "ESNext or CommonJS",
                    "lib": ["ES2020", "DOM"],
                    "strict": True,
                    "esModuleInterop": True,
                    "skipLibCheck": True,
                    "forceConsistentCasingInFileNames": True,
                    "resolveJsonModule": True,
                    "moduleResolution": "node",
                    "allowSyntheticDefaultImports": True,
                    "noEmit": False,
                    "declaration": True,
                    "outDir": "./dist",
                },
            },
            "strict_mode_options": {
                "strict": "Enables all strict type checking options",
                "noImplicitAny": "Raise error on expressions with implied 'any'",
                "strictNullChecks": "Enable strict null checks",
                "strictFunctionTypes": "Enable strict checking of function types",
                "strictPropertyInitialization": "Ensure class properties are initialized",
            },
            "common_options": {
                "target": "ECMAScript target version",
                "module": "Module system to use",
                "lib": "Library files to include",
                "outDir": "Output directory for compiled files",
                "rootDir": "Root directory of input files",
            },
        }, indent=2)

    elif uri == "typescript:standards://eslint-rules":
        return json.dumps({
            "title": "TypeScript ESLint Rules",
            "recommended_packages": [
                "@typescript-eslint/eslint-plugin",
                "@typescript-eslint/parser",
                "eslint-config-prettier",
            ],
            "common_rules": {
                "@typescript-eslint/no-explicit-any": "Disallow 'any' type",
                "@typescript-eslint/explicit-function-return-type": "Require explicit return types",
                "@typescript-eslint/no-unused-vars": "Disallow unused variables",
                "@typescript-eslint/prefer-const": "Require const for variables never reassigned",
                "@typescript-eslint/no-non-null-assertion": "Disallow non-null assertions",
                "@typescript-eslint/prefer-nullish-coalescing": "Prefer ?? over ||",
                "@typescript-eslint/prefer-optional-chain": "Prefer optional chaining",
            },
            "style_rules": {
                "@typescript-eslint/naming-convention": "Enforce naming conventions",
                "@typescript-eslint/consistent-type-definitions": "Prefer interface or type",
                "@typescript-eslint/consistent-type-imports": "Enforce consistent type imports",
            },
            "error_rules": {
                "@typescript-eslint/no-unsafe-assignment": "Disallow unsafe assignments",
                "@typescript-eslint/no-unsafe-member-access": "Disallow unsafe member access",
                "@typescript-eslint/no-unsafe-call": "Disallow unsafe function calls",
            },
        }, indent=2)

    elif uri == "typescript:standards://best-practices":
        return json.dumps({
            "title": "TypeScript Best Practices",
            "type_safety": {
                "summary": "Maximize type safety",
                "practices": [
                    "Enable strict mode in tsconfig.json",
                    "Avoid 'any' type - use 'unknown' if needed",
                    "Use type guards for runtime type checking",
                    "Prefer interfaces over type aliases for object shapes",
                ],
            },
            "code_organization": {
                "summary": "Organize code effectively",
                "practices": [
                    "Use barrel exports (index.ts) for modules",
                    "Separate types into dedicated files",
                    "Use namespaces for internal organization",
                    "Group related functionality together",
                ],
            },
            "async_programming": {
                "summary": "Best practices for async/await",
                "practices": [
                    "Prefer async/await over Promises",
                    "Use Promise.all() for parallel operations",
                    "Handle errors with try-catch",
                    "Type async functions explicitly",
                ],
            },
            "performance": {
                "summary": "Performance optimization tips",
                "practices": [
                    "Use const assertions for literal types",
                    "Prefer const over let",
                    "Use readonly for immutable data structures",
                    "Avoid unnecessary type assertions",
                ],
            },
            "testing": {
                "summary": "TypeScript testing best practices",
                "practices": [
                    "Use type-safe test utilities",
                    "Mock with proper types",
                    "Use type assertions in tests when needed",
                    "Test type definitions separately",
                ],
            },
        }, indent=2)

    else:
        raise ValueError(f"Unknown TypeScript resource URI: {uri}")


def get_typescript_resource_templates() -> list[ResourceTemplate]:
    """Get TypeScript resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="typescript:standards://style-guide",
            name="TypeScript Style Guide",
            description="TypeScript style guide with naming conventions and formatting rules",
        ),
        ResourceTemplate(
            uriTemplate="typescript:standards://tsconfig-options",
            name="TypeScript tsconfig Options",
            description="Recommended tsconfig.json compiler options and their meanings",
        ),
        ResourceTemplate(
            uriTemplate="typescript:standards://eslint-rules",
            name="TypeScript ESLint Rules",
            description="ESLint rules for TypeScript code quality and consistency",
        ),
        ResourceTemplate(
            uriTemplate="typescript:standards://best-practices",
            name="TypeScript Best Practices",
            description="TypeScript best practices for type safety and code quality",
        ),
    ]
