"""Tests for resource implementations."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from python_package_mcp_server.resources import codebase, dependencies, packages, project_index


class TestPackageResources:
    """Tests for package resources."""

    def test_get_package_resources_always_returns_resources(self):
        """Test that package resources are always returned."""
        resources = packages.get_package_resources()
        
        assert len(resources) == 2
        assert any(r.uri == "python:packages://installed" for r in resources)
        assert any(r.uri == "python:packages://outdated" for r in resources)

    def test_get_package_resource_templates_matches_resources(self):
        """Test that resource templates match available resources."""
        resources = packages.get_package_resources()
        templates = packages.get_package_resource_templates()
        
        resource_uris = {r.uri for r in resources}
        template_uris = {t.uriTemplate for t in templates}
        
        assert resource_uris == template_uris

    @patch("python_package_mcp_server.resources.packages.PackageManagerWrapper")
    def test_read_installed_packages(self, mock_wrapper_class):
        """Test reading installed packages resource."""
        mock_wrapper = MagicMock()
        mock_wrapper.list_installed.return_value = [{"name": "requests", "version": "2.31.0"}]
        mock_wrapper_class.return_value = mock_wrapper

        result = packages.read_package_resource("python:packages://installed")
        data = json.loads(result)

        assert "packages" in data
        assert len(data["packages"]) == 1
        assert data["packages"][0]["name"] == "requests"

    @patch("python_package_mcp_server.resources.packages.PackageManagerWrapper")
    def test_read_outdated_packages(self, mock_wrapper_class):
        """Test reading outdated packages resource."""
        mock_wrapper = MagicMock()
        mock_wrapper.list_outdated.return_value = [{"name": "requests", "version": "2.31.0", "latest": "2.32.0"}]
        mock_wrapper_class.return_value = mock_wrapper

        result = packages.read_package_resource("python:packages://outdated")
        data = json.loads(result)

        assert "outdated" in data
        assert len(data["outdated"]) == 1

    @patch("python_package_mcp_server.resources.packages.PackageManagerWrapper")
    def test_read_package_resource_handles_errors(self, mock_wrapper_class):
        """Test that reading package resources handles errors gracefully."""
        mock_wrapper = MagicMock()
        mock_wrapper.list_installed.side_effect = Exception("Test error")
        mock_wrapper_class.return_value = mock_wrapper

        result = packages.read_package_resource("python:packages://installed")
        data = json.loads(result)

        assert "error" in data
        assert "Failed to list installed packages" in data["error"]


class TestDependencyResources:
    """Tests for dependency resources."""

    def test_get_dependency_resources_always_returns_resources(self):
        """Test that dependency resources are always returned."""
        resources = dependencies.get_dependency_resources()
        
        assert len(resources) == 3
        assert any(r.uri == "python:dependencies://tree" for r in resources)
        assert any(r.uri == "python:project://info" for r in resources)
        assert any(r.uri == "python:environment://active" for r in resources)

    def test_get_dependency_resource_templates_matches_resources(self):
        """Test that resource templates match available resources."""
        resources = dependencies.get_dependency_resources()
        templates = dependencies.get_dependency_resource_templates()
        
        resource_uris = {r.uri for r in resources}
        template_uris = {t.uriTemplate for t in templates}
        
        assert resource_uris == template_uris

    @patch("python_package_mcp_server.resources.dependencies.PackageManagerWrapper")
    def test_read_dependency_tree(self, mock_wrapper_class):
        """Test reading dependency tree resource."""
        mock_wrapper = MagicMock()
        mock_wrapper.get_dependency_tree.return_value = {"root": "test-project", "dependencies": []}
        mock_wrapper_class.return_value = mock_wrapper

        result = dependencies.read_dependency_resource("python:dependencies://tree")
        data = json.loads(result)

        assert "root" in data
        assert "dependencies" in data

    @patch("python_package_mcp_server.resources.dependencies.PackageManagerWrapper")
    def test_read_project_info(self, mock_wrapper_class):
        """Test reading project info resource."""
        mock_wrapper = MagicMock()
        mock_wrapper.get_project_info.return_value = {"pyproject": {}, "lock_file": {"exists": True}}
        mock_wrapper_class.return_value = mock_wrapper

        result = dependencies.read_dependency_resource("python:project://info")
        data = json.loads(result)

        assert "pyproject" in data
        assert "lock_file" in data

    def test_read_environment_resource(self):
        """Test reading active environment resource."""
        result = dependencies.read_dependency_resource("python:environment://active")
        data = json.loads(result)

        assert "python_version" in data
        assert "python_executable" in data


class TestProjectIndexResources:
    """Tests for project index resources."""

    @patch("python_package_mcp_server.resources.project_index.ProjectScanner")
    def test_read_project_index(self, mock_scanner_class):
        """Test reading project index resource."""
        mock_scanner = MagicMock()
        mock_scanner.scan_structure.return_value = {"files": [], "directories": []}
        mock_scanner.find_config_files.return_value = []
        mock_scanner.find_dependency_files.return_value = []
        mock_scanner.find_readme_files.return_value = []
        mock_scanner.find_entry_points.return_value = []
        mock_scanner.find_test_files.return_value = []
        mock_scanner_class.return_value = mock_scanner

        result = project_index.read_project_index_resource("project://index")
        data = json.loads(result)

        assert "structure" in data
        assert "config_files" in data
        assert "dependencies" in data


class TestCodebaseResources:
    """Tests for codebase resources."""

    @patch("python_package_mcp_server.resources.codebase.ProjectScanner")
    def test_read_codebase_search(self, mock_scanner_class):
        """Test reading codebase search resource."""
        mock_scanner = MagicMock()
        mock_scanner.search_codebase.return_value = [{"file": "test.py", "line": 1, "content": "def test():"}]
        mock_scanner_class.return_value = mock_scanner

        result = codebase.read_codebase_resource("codebase://search", {"pattern": "def"})
        data = json.loads(result)

        assert "matches" in data
        assert len(data["matches"]) == 1
