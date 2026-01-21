"""Package management resources."""

import json
from typing import Any

from mcp.types import Resource, ResourceTemplate

from ..config import config
from ..utils.package_manager_wrapper import PackageManagerWrapper


def get_package_resources() -> list[Resource]:
    """Get package management resources.

    Returns:
        List of resource definitions
    """
    # Always return resources - errors will be handled when reading
    return [
        Resource(
            uri="python:packages://installed",
            name="Installed Packages",
            description="List of all installed Python packages with versions",
            mimeType="application/json",
        ),
        Resource(
            uri="python:packages://outdated",
            name="Outdated Packages",
            description="List of packages with available updates",
            mimeType="application/json",
        ),
    ]


def read_package_resource(uri: str) -> str:
    """Read package resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    pm_wrapper = PackageManagerWrapper(config.project_root)
    
    # Convert URI to string if it's an AnyUrl object (from pydantic)
    uri_str = str(uri)

    if uri_str == "python:packages://installed":
        try:
            packages = pm_wrapper.list_installed()
            return json.dumps({"packages": packages}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to list installed packages: {str(e)}"}, indent=2)

    elif uri_str == "python:packages://outdated":
        try:
            packages = pm_wrapper.list_outdated()
            return json.dumps({"outdated": packages}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to list outdated packages: {str(e)}"}, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri_str}")


def get_package_resource_templates() -> list[ResourceTemplate]:
    """Get package resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="python:packages://installed",
            name="Installed Packages",
            description="List all installed Python packages",
        ),
        ResourceTemplate(
            uriTemplate="python:packages://outdated",
            name="Outdated Packages",
            description="List packages with available updates",
        ),
    ]
