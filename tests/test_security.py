"""Tests for security components."""

import pytest

from python_package_mcp_server.security.auth import AuthMiddleware, AuthenticationError
from python_package_mcp_server.security.policy import PolicyEngine, PolicyViolationError


class TestAuthMiddleware:
    """Tests for authentication middleware."""

    def test_authenticate_disabled(self):
        """Test authentication when disabled."""
        auth = AuthMiddleware(enable_auth=False)
        assert auth.authenticate(None) is True

    def test_authenticate_enabled_no_key(self):
        """Test authentication when enabled but no key provided."""
        auth = AuthMiddleware(api_key="secret", enable_auth=True)
        with pytest.raises(AuthenticationError):
            auth.authenticate(None)

    def test_authenticate_enabled_valid_key(self):
        """Test authentication with valid key."""
        auth = AuthMiddleware(api_key="secret", enable_auth=True)
        assert auth.authenticate("secret") is True

    def test_authenticate_enabled_invalid_key(self):
        """Test authentication with invalid key."""
        auth = AuthMiddleware(api_key="secret", enable_auth=True)
        with pytest.raises(AuthenticationError):
            auth.authenticate("wrong")

    def test_extract_api_key_from_headers(self):
        """Test extracting API key from headers."""
        auth = AuthMiddleware()
        headers = {"X-API-Key": "test-key"}
        assert auth.extract_api_key(headers) == "test-key"

    def test_extract_api_key_bearer(self):
        """Test extracting API key from Bearer token."""
        auth = AuthMiddleware()
        headers = {"Authorization": "Bearer test-token"}
        assert auth.extract_api_key(headers) == "test-token"


class TestPolicyEngine:
    """Tests for policy engine."""

    def test_check_package_no_restrictions(self):
        """Test checking package with no restrictions."""
        policy = PolicyEngine()
        assert policy.check_package("requests") is True

    def test_check_package_blocked(self):
        """Test checking blocked package."""
        policy = PolicyEngine(blocked_packages=["malicious.*"])
        with pytest.raises(PolicyViolationError):
            policy.check_package("malicious-package")

    def test_check_package_allowed(self):
        """Test checking allowed package."""
        policy = PolicyEngine(allowed_packages=["requests", "pytest.*"])
        assert policy.check_package("requests") is True
        assert policy.check_package("pytest-mock") is True

    def test_check_package_not_allowed(self):
        """Test checking package not in allowed list."""
        policy = PolicyEngine(allowed_packages=["requests"])
        with pytest.raises(PolicyViolationError):
            policy.check_package("malicious-package")

    def test_check_packages_multiple(self):
        """Test checking multiple packages."""
        policy = PolicyEngine(allowed_packages=["requests", "pytest"])
        policy.check_packages(["requests", "pytest"])

    def test_check_packages_with_version(self):
        """Test checking package with version spec."""
        policy = PolicyEngine(allowed_packages=["requests"])
        # Should extract package name from version spec
        policy.check_packages(["requests==2.31.0"])
