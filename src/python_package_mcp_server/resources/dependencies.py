"""Dependency management resources."""

import json
from typing import Any

from mcp.types import Resource, ResourceTemplate

from ..config import config
from ..utils.package_manager_wrapper import PackageManagerWrapper


def get_dependency_resources() -> list[Resource]:
    """Get dependency management resources.

    Returns:
        List of resource definitions
    """
    # Always return resources - errors will be handled when reading
    return [
        Resource(
            uri="python:dependencies://tree",
            name="Dependency Tree",
            description="Visualization of project dependency tree",
            mimeType="application/json",
        ),
        Resource(
            uri="python:project://info",
            name="Project Information",
            description="Project metadata including pyproject.toml and lock file info",
            mimeType="application/json",
        ),
        Resource(
            uri="python:environment://active",
            name="Active Environment",
            description="Details about the active Python environment",
            mimeType="application/json",
        ),
    ]


def read_dependency_resource(uri: str) -> str:
    """Read dependency resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    pm_wrapper = PackageManagerWrapper(config.project_root)
    
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)

    if uri_str == "python:dependencies://tree":
        try:
            tree = pm_wrapper.get_dependency_tree()
            return json.dumps(tree, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get dependency tree: {str(e)}"}, indent=2)

    elif uri_str == "python:project://info":
        try:
            info = pm_wrapper.get_project_info()
            return json.dumps(info, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get project info: {str(e)}"}, indent=2)

    elif uri_str == "python:environment://active":
        try:
            import sys
            import os

            env_info = {
                "python_version": sys.version,
                "python_executable": sys.executable,
                "virtual_env": os.environ.get("VIRTUAL_ENV"),
                "path": sys.path[:5],  # First 5 entries
            }
            return json.dumps(env_info, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get environment info: {str(e)}"}, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri_str}")


def get_dependency_resource_templates() -> list[ResourceTemplate]:
    """Get dependency resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="python:dependencies://tree",
            name="Dependency Tree",
            description="Visualize project dependency tree",
        ),
        ResourceTemplate(
            uriTemplate="python:project://info",
            name="Project Information",
            description="Get project metadata",
        ),
        ResourceTemplate(
            uriTemplate="python:environment://active",
            name="Active Environment",
            description="Get active Python environment details",
        ),
    ]
