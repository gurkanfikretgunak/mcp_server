"""Project indexing and discovery resources."""

import json
from pathlib import Path
from typing import Any

from mcp.types import Resource, ResourceTemplate

from ..config import config
from ..utils.project_scanner import ProjectScanner


def get_project_index_resources() -> list[Resource]:
    """Get project indexing resources.

    Returns:
        List of resource definitions
    """
    project_root = config.project_root or Path.cwd()
    scanner = ProjectScanner(project_root)

    resources = []

    # Project index resource
    resources.append(
        Resource(
            uri="project://index",
            name="Project Index",
            description="Complete project index with structure, files, and metadata",
            mimeType="application/json",
        )
    )

    # Project structure resource
    resources.append(
        Resource(
            uri="project://structure",
            name="Project Structure",
            description="File and directory structure tree",
            mimeType="application/json",
        )
    )

    # Config files resource
    resources.append(
        Resource(
            uri="project://config",
            name="Configuration Files",
            description="Configuration files discovery",
            mimeType="application/json",
        )
    )

    # Dependencies resource
    resources.append(
        Resource(
            uri="project://dependencies",
            name="Dependency Files",
            description="All dependency files across project types",
            mimeType="application/json",
        )
    )

    # README resource
    resources.append(
        Resource(
            uri="project://readme",
            name="Documentation Files",
            description="README and documentation files",
            mimeType="application/json",
        )
    )

    # Entry points resource
    resources.append(
        Resource(
            uri="project://entrypoints",
            name="Entry Points",
            description="Entry points and main files discovery",
            mimeType="application/json",
        )
    )

    # Tests resource
    resources.append(
        Resource(
            uri="project://tests",
            name="Test Files",
            description="Test files and test structure",
            mimeType="application/json",
        )
    )

    return resources


def read_project_index_resource(uri: str) -> str:
    """Read project index resource content.

    Args:
        uri: Resource URI

    Returns:
        Resource content as JSON string
    """
    project_root = config.project_root or Path.cwd()
    scanner = ProjectScanner(project_root)

    if uri == "project://index":
        structure = scanner.scan_structure()
        config_files = scanner.find_config_files()
        dependencies = scanner.find_dependency_files()
        readmes = scanner.find_readme_files()
        entry_points = scanner.find_entry_points()
        tests = scanner.find_test_files()

        index = {
            "root": str(project_root),
            "structure": structure,
            "config_files": config_files,
            "dependencies": dependencies,
            "readmes": readmes,
            "entry_points": entry_points,
            "tests": tests,
        }
        return json.dumps(index, indent=2)

    elif uri == "project://structure":
        structure = scanner.scan_structure()
        return json.dumps(structure, indent=2)

    elif uri == "project://config":
        config_files = scanner.find_config_files()
        return json.dumps({"config_files": config_files}, indent=2)

    elif uri == "project://dependencies":
        dependencies = scanner.find_dependency_files()
        return json.dumps({"dependencies": dependencies}, indent=2)

    elif uri == "project://readme":
        readmes = scanner.find_readme_files()
        return json.dumps({"readmes": readmes}, indent=2)

    elif uri == "project://entrypoints":
        entry_points = scanner.find_entry_points()
        return json.dumps({"entry_points": entry_points}, indent=2)

    elif uri == "project://tests":
        tests = scanner.find_test_files()
        return json.dumps({"tests": tests}, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


def get_project_index_resource_templates() -> list[ResourceTemplate]:
    """Get project index resource templates.

    Returns:
        List of resource templates
    """
    return [
        ResourceTemplate(
            uriTemplate="project://index",
            name="Project Index",
            description="Get complete project index",
        ),
        ResourceTemplate(
            uriTemplate="project://structure",
            name="Project Structure",
            description="Get project file structure",
        ),
        ResourceTemplate(
            uriTemplate="project://config",
            name="Configuration Files",
            description="Find configuration files",
        ),
        ResourceTemplate(
            uriTemplate="project://dependencies",
            name="Dependency Files",
            description="Find dependency files",
        ),
        ResourceTemplate(
            uriTemplate="project://readme",
            name="Documentation Files",
            description="Find README and docs",
        ),
        ResourceTemplate(
            uriTemplate="project://entrypoints",
            name="Entry Points",
            description="Find entry points",
        ),
        ResourceTemplate(
            uriTemplate="project://tests",
            name="Test Files",
            description="Find test files",
        ),
    ]
