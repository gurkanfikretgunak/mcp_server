"""Tests for Dart resources."""

import json
import pytest

from python_package_mcp_server.resources import dart_standards


class TestDartResources:
    """Tests for Dart standards resources."""

    def test_get_dart_resources(self):
        """Test getting Dart resources."""
        resources = dart_standards.get_dart_resources()
        
        assert len(resources) == 4
        assert any(r.uri == "dart:standards://effective-dart" for r in resources)
        assert any(r.uri == "dart:standards://style-guide" for r in resources)
        assert any(r.uri == "dart:standards://linter-rules" for r in resources)
        assert any(r.uri == "dart:standards://best-practices" for r in resources)

    def test_read_effective_dart(self):
        """Test reading Effective Dart resource."""
        result = dart_standards.read_dart_resource("dart:standards://effective-dart")
        data = json.loads(result)
        
        assert "title" in data
        assert "sections" in data
        assert "style" in data["sections"]
        assert "documentation" in data["sections"]
        assert "usage" in data["sections"]

    def test_read_style_guide(self):
        """Test reading Dart style guide resource."""
        result = dart_standards.read_dart_resource("dart:standards://style-guide")
        data = json.loads(result)
        
        assert "title" in data
        assert "naming_conventions" in data
        assert "formatting" in data
        assert "code_organization" in data

    def test_read_linter_rules(self):
        """Test reading Dart linter rules resource."""
        result = dart_standards.read_dart_resource("dart:standards://linter-rules")
        data = json.loads(result)
        
        assert "title" in data
        assert "recommended_packages" in data
        assert "common_rules" in data

    def test_read_best_practices(self):
        """Test reading Dart best practices resource."""
        result = dart_standards.read_dart_resource("dart:standards://best-practices")
        data = json.loads(result)
        
        assert "title" in data
        assert "null_safety" in data
        assert "async_programming" in data
        assert "collections" in data

    def test_read_invalid_resource(self):
        """Test reading invalid resource URI."""
        with pytest.raises(ValueError, match="Unknown Dart resource URI"):
            dart_standards.read_dart_resource("dart:standards://invalid")

    def test_get_dart_resource_templates(self):
        """Test getting Dart resource templates."""
        templates = dart_standards.get_dart_resource_templates()
        
        assert len(templates) == 4
        assert any(t.uriTemplate == "dart:standards://effective-dart" for t in templates)
