"""Tests for resource implementations."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from python_package_mcp_server.resources import codebase, dependencies, packages, project_index


class TestPackageResources:
    """Tests for package resources."""

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


class TestDependencyResources:
    """Tests for dependency resources."""

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
