"""Tests for TypeScript tool implementations."""

from unittest.mock import MagicMock, patch

import pytest

from python_package_mcp_server.tools import typescript


class TestTypeScriptTools:
    """Tests for TypeScript tools."""

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.typescript.TypeScriptWrapper")
    async def test_handle_typescript_format(self, mock_wrapper_class):
        """Test typescript_format tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.format_code.return_value = {"success": True, "output": "Formatted"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await typescript.handle_typescript_format({"paths": ["src/index.ts"]})

        assert len(result) == 1
        assert "Successfully formatted" in result[0].text
        mock_wrapper.format_code.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.typescript.TypeScriptWrapper")
    async def test_handle_typescript_lint(self, mock_wrapper_class):
        """Test typescript_lint tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.lint_code.return_value = {"success": True, "issues": []}
        mock_wrapper_class.return_value = mock_wrapper

        result = await typescript.handle_typescript_lint({"paths": ["src/index.ts"]})

        assert len(result) == 1
        assert "no issues found" in result[0].text
        mock_wrapper.lint_code.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.typescript.TypeScriptWrapper")
    async def test_handle_typescript_type_check(self, mock_wrapper_class):
        """Test typescript_type_check tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.type_check.return_value = {"success": True, "output": "No errors"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await typescript.handle_typescript_type_check({"project_path": "tsconfig.json"})

        assert len(result) == 1
        assert "type checking passed" in result[0].text
        mock_wrapper.type_check.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.typescript.read_typescript_resource")
    async def test_handle_typescript_generate_code(self, mock_read_resource):
        """Test typescript_generate_code tool handler."""
        import json
        mock_read_resource.return_value = json.dumps({"title": "TypeScript Style Guide"})

        result = await typescript.handle_typescript_generate_code({
            "code_description": "Create a user interface",
            "file_path": "src/user.ts",
        })

        assert len(result) == 1
        assert "Generated TypeScript code" in result[0].text

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.typescript.TypeScriptWrapper")
    async def test_handle_typescript_check_standards(self, mock_wrapper_class):
        """Test typescript_check_standards tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.check_standards.return_value = {
            "file": "src/index.ts",
            "formatted": True,
            "standards_compliant": True,
            "linting": {"issues": []},
        }
        mock_wrapper_class.return_value = mock_wrapper

        result = await typescript.handle_typescript_check_standards({"file_path": "src/index.ts"})

        assert len(result) == 1
        assert "Compliant" in result[0].text
        mock_wrapper.check_standards.assert_called_once()
