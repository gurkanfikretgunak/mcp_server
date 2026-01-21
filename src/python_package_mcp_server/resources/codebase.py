"""Codebase structure and file resources."""

import json
from pathlib import Path
from typing import Any, Optional

from mcp.types import Resource, ResourceTemplate

from ..config import config
from ..utils.project_scanner import ProjectScanner


def get_codebase_resources() -> list[Resource]:
    """Get codebase resources.

    Returns:
        List of resource definitions
    """
    resources = []

    # Codebase search resource (template-based)
    resources.append(
        Resource(
            uri="codebase://search",
            name="Codebase Search",
            description="Search codebase by pattern or content",
            mimeType="application/json",
        )
    )

    # File content resource (template-based)
    resources.append(
        Resource(
            uri="codebase://file",
            name="File Content",
            description="Read specific file content with line numbers",
            mimeType="text/plain",
        )
    )

    # Symbols resource (template-based)
    resources.append(
        Resource(
            uri="codebase://symbols",
            name="Code Symbols",
            description="Extract symbols (functions, classes) from codebase",
            mimeType="application/json",
        )
    )

    return resources


def read_codebase_resource(uri: str, query_params: Optional[dict[str, str]] = None) -> str:
    """Read codebase resource content.

    Args:
        uri: Resource URI
        query_params: Optional query parameters

    Returns:
        Resource content
    """
    project_root = config.project_root or Path.cwd()
    scanner = ProjectScanner(project_root)
    query_params = query_params or {}
    
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)

    if uri_str.startswith("codebase://search"):
        pattern = query_params.get("pattern", query_params.get("q", ""))
        if not pattern:
            return json.dumps({"error": "Pattern parameter required"}, indent=2)

        extensions = query_params.get("extensions", "").split(",") if query_params.get("extensions") else None
        matches = scanner.search_codebase(pattern, extensions)
        return json.dumps({"matches": matches, "count": len(matches)}, indent=2)

    elif uri_str.startswith("codebase://file"):
        file_path = query_params.get("path", query_params.get("file", ""))
        if not file_path:
            return json.dumps({"error": "File path parameter required"}, indent=2)

        full_path = project_root / file_path
        if not full_path.exists() or not full_path.is_file():
            return json.dumps({"error": f"File not found: {file_path}"}, indent=2)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                content = "".join(f"{i+1:4d}: {line}" for i, line in enumerate(lines))
                return content
        except Exception as e:
            return json.dumps({"error": f"Failed to read file: {str(e)}"}, indent=2)

    elif uri_str.startswith("codebase://symbols"):
        file_path = query_params.get("path", query_params.get("file", ""))
        if not file_path:
            return json.dumps({"error": "File path parameter required"}, indent=2)

        full_path = project_root / file_path
        if not full_path.exists():
            return json.dumps({"error": f"File not found: {file_path}"}, indent=2)

        symbols = scanner.extract_symbols(full_path)
        return json.dumps({"symbols": symbols, "count": len(symbols)}, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri_str}")


def get_codebase_resource_templates() -> list[ResourceTemplate]:
    """Get codebase resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="codebase://search?pattern={pattern}&extensions={extensions}",
            name="Codebase Search",
            description="Search codebase by pattern",
        ),
        ResourceTemplate(
            uriTemplate="codebase://file?path={path}",
            name="File Content",
            description="Read file content",
        ),
        ResourceTemplate(
            uriTemplate="codebase://symbols?path={path}",
            name="Code Symbols",
            description="Extract symbols from file",
        ),
    ]
