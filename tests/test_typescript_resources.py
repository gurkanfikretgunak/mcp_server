"""Tests for TypeScript resources."""

import json
import pytest

from python_package_mcp_server.resources import typescript_standards


class TestTypeScriptResources:
    """Tests for TypeScript standards resources."""

    def test_get_typescript_resources(self):
        """Test getting TypeScript resources."""
        resources = typescript_standards.get_typescript_resources()
        
        assert len(resources) == 4
        assert any(r.uri == "typescript:standards://style-guide" for r in resources)
        assert any(r.uri == "typescript:standards://tsconfig-options" for r in resources)
        assert any(r.uri == "typescript:standards://eslint-rules" for r in resources)
        assert any(r.uri == "typescript:standards://best-practices" for r in resources)

    def test_read_style_guide(self):
        """Test reading TypeScript style guide resource."""
        result = typescript_standards.read_typescript_resource("typescript:standards://style-guide")
        data = json.loads(result)
        
        assert "title" in data
        assert "naming_conventions" in data
        assert "formatting" in data
        assert "type_definitions" in data

    def test_read_tsconfig_options(self):
        """Test reading TypeScript tsconfig options resource."""
        result = typescript_standards.read_typescript_resource("typescript:standards://tsconfig-options")
        data = json.loads(result)
        
        assert "title" in data
        assert "recommended_config" in data
        assert "strict_mode_options" in data
        assert "common_options" in data

    def test_read_eslint_rules(self):
        """Test reading TypeScript ESLint rules resource."""
        result = typescript_standards.read_typescript_resource("typescript:standards://eslint-rules")
        data = json.loads(result)
        
        assert "title" in data
        assert "recommended_packages" in data
        assert "common_rules" in data
        assert "style_rules" in data

    def test_read_best_practices(self):
        """Test reading TypeScript best practices resource."""
        result = typescript_standards.read_typescript_resource("typescript:standards://best-practices")
        data = json.loads(result)
        
        assert "title" in data
        assert "type_safety" in data
        assert "code_organization" in data
        assert "async_programming" in data

    def test_read_invalid_resource(self):
        """Test reading invalid resource URI."""
        with pytest.raises(ValueError, match="Unknown TypeScript resource URI"):
            typescript_standards.read_typescript_resource("typescript:standards://invalid")

    def test_get_typescript_resource_templates(self):
        """Test getting TypeScript resource templates."""
        templates = typescript_standards.get_typescript_resource_templates()
        
        assert len(templates) == 4
        assert any(t.uriTemplate == "typescript:standards://style-guide" for t in templates)
