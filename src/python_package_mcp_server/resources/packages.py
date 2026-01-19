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
    pm_wrapper = PackageManagerWrapper(config.project_root)

    resources = []

    # Installed packages resource
    try:
        installed = pm_wrapper.list_installed()
        resources.append(
            Resource(
                uri="python:packages://installed",
                name="Installed Packages",
                description="List of all installed Python packages with versions",
                mimeType="application/json",
            )
        )
    except Exception:
        pass

    # Outdated packages resource
    try:
        outdated = pm_wrapper.list_outdated()
        resources.append(
            Resource(
                uri="python:packages://outdated",
                name="Outdated Packages",
                description="List of packages with available updates",
                mimeType="application/json",
            )
        )
    except Exception:
        pass

    return resources


def read_package_resource(uri: str) -> str:
    """Read package resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    pm_wrapper = PackageManagerWrapper(config.project_root)

    if uri == "python:packages://installed":
        packages = pm_wrapper.list_installed()
        return json.dumps({"packages": packages}, indent=2)

    elif uri == "python:packages://outdated":
        packages = pm_wrapper.list_outdated()
        return json.dumps({"outdated": packages}, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


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
