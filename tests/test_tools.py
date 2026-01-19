"""Tests for tool implementations."""

from unittest.mock import MagicMock, patch

import pytest

from python_package_mcp_server.tools import env, install, sync


class TestInstallTools:
    """Tests for install/uninstall tools."""

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.install.PackageManagerWrapper")
    @patch("python_package_mcp_server.tools.install.policy_engine")
    async def test_handle_install(self, mock_policy, mock_wrapper_class):
        """Test install tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.install_packages.return_value = {"success": True, "output": "Installed"}
        mock_wrapper_class.return_value = mock_wrapper
        mock_policy.check_packages.return_value = True

        result = await install.handle_install({"packages": ["requests"]})

        assert len(result) == 1
        assert "Successfully installed" in result[0].text
        mock_wrapper.install_packages.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.install.PackageManagerWrapper")
    async def test_handle_uninstall(self, mock_wrapper_class):
        """Test uninstall tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.uninstall_packages.return_value = {"success": True, "output": "Uninstalled"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await install.handle_uninstall({"packages": ["requests"]})

        assert len(result) == 1
        assert "Successfully uninstalled" in result[0].text


class TestSyncTools:
    """Tests for sync tools."""

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.sync.PackageManagerWrapper")
    async def test_handle_add(self, mock_wrapper_class):
        """Test add tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.add_packages.return_value = {"success": True, "output": "Added"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await sync.handle_add({"packages": ["requests"], "dev": False})

        assert len(result) == 1
        assert "Successfully added" in result[0].text

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.sync.PackageManagerWrapper")
    async def test_handle_sync(self, mock_wrapper_class):
        """Test sync tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.sync.return_value = {"success": True, "output": "Synced"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await sync.handle_sync({})

        assert len(result) == 1
        assert "Successfully synced" in result[0].text


class TestEnvTools:
    """Tests for environment tools."""

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.env.PackageManagerWrapper")
    async def test_handle_init(self, mock_wrapper_class):
        """Test init tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.init_project.return_value = {"success": True, "output": "Initialized"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await env.handle_init({"name": "test-project"})

        assert len(result) == 1
        assert "Successfully initialized" in result[0].text

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.env.ProjectScanner")
    async def test_handle_index_project(self, mock_scanner_class):
        """Test index_project tool handler."""
        mock_scanner = MagicMock()
        mock_scanner.scan_structure.return_value = {"files": [{"name": "test.py"}], "directories": []}
        mock_scanner_class.return_value = mock_scanner

        result = await env.handle_index_project({"path": "/test"})

        assert len(result) == 1
        assert "Successfully indexed" in result[0].text
