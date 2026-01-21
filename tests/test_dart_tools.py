"""Tests for Dart tool implementations."""

from unittest.mock import MagicMock, patch

import pytest

from python_package_mcp_server.tools import dart


class TestDartTools:
    """Tests for Dart tools."""

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.dart.DartWrapper")
    async def test_handle_dart_format(self, mock_wrapper_class):
        """Test dart_format tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.format_code.return_value = {"success": True, "output": "Formatted"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await dart.handle_dart_format({"paths": ["lib/main.dart"], "line_length": 80})

        assert len(result) == 1
        assert "Successfully formatted" in result[0].text
        mock_wrapper.format_code.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.dart.DartWrapper")
    async def test_handle_dart_analyze(self, mock_wrapper_class):
        """Test dart_analyze tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.analyze_code.return_value = {"success": True, "issues": []}
        mock_wrapper_class.return_value = mock_wrapper

        result = await dart.handle_dart_analyze({"paths": ["lib/main.dart"]})

        assert len(result) == 1
        assert "no issues found" in result[0].text
        mock_wrapper.analyze_code.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.dart.DartWrapper")
    async def test_handle_dart_fix(self, mock_wrapper_class):
        """Test dart_fix tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.fix_code.return_value = {"success": True, "output": "Fixed"}
        mock_wrapper_class.return_value = mock_wrapper

        result = await dart.handle_dart_fix({"paths": ["lib/main.dart"]})

        assert len(result) == 1
        assert "Successfully applied fixes" in result[0].text
        mock_wrapper.fix_code.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.dart.read_dart_resource")
    async def test_handle_dart_generate_code(self, mock_read_resource):
        """Test dart_generate_code tool handler."""
        import json
        mock_read_resource.return_value = json.dumps({"title": "Effective Dart Guidelines"})

        result = await dart.handle_dart_generate_code({
            "code_description": "Create a user class",
            "file_path": "lib/user.dart",
        })

        assert len(result) == 1
        assert "Generated Dart code" in result[0].text

    @pytest.mark.asyncio
    @patch("python_package_mcp_server.tools.dart.DartWrapper")
    async def test_handle_dart_check_standards(self, mock_wrapper_class):
        """Test dart_check_standards tool handler."""
        mock_wrapper = MagicMock()
        mock_wrapper.check_standards.return_value = {
            "file": "lib/main.dart",
            "formatted": True,
            "standards_compliant": True,
            "analysis": {"issues": []},
        }
        mock_wrapper_class.return_value = mock_wrapper

        result = await dart.handle_dart_check_standards({"file_path": "lib/main.dart"})

        assert len(result) == 1
        assert "Compliant" in result[0].text
        mock_wrapper.check_standards.assert_called_once()
