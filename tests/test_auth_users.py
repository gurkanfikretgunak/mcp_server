"""Tests for user authentication system."""

import json
import tempfile
from pathlib import Path

import pytest

from python_package_mcp_server.security.auth import AuthMiddleware, AuthenticationError
from python_package_mcp_server.security.user_manager import User, UserManager


class TestUser:
    """Tests for User model."""

    def test_user_creation(self):
        """Test user creation."""
        user = User(
            username="testuser",
            api_key_hash="hash123",
            role="user",
            created_at="2024-01-01T00:00:00Z",
        )
        assert user.username == "testuser"
        assert user.api_key_hash == "hash123"
        assert user.role == "user"

    def test_user_to_dict(self):
        """Test user to dictionary conversion."""
        user = User(
            username="testuser",
            api_key_hash="hash123",
            role="admin",
            created_at="2024-01-01T00:00:00Z",
        )
        data = user.to_dict()
        assert data["username"] == "testuser"
        assert data["role"] == "admin"

    def test_user_from_dict(self):
        """Test user from dictionary creation."""
        data = {
            "username": "testuser",
            "api_key_hash": "hash123",
            "role": "user",
            "created_at": "2024-01-01T00:00:00Z",
        }
        user = User.from_dict(data)
        assert user.username == "testuser"
        assert user.role == "user"

    def test_hash_api_key(self):
        """Test API key hashing."""
        api_key = "test-key-123"
        hash1 = User.hash_api_key(api_key)
        hash2 = User.hash_api_key(api_key)
        assert hash1 == hash2
        assert hash1 != api_key
        assert len(hash1) == 64  # SHA-256 hex digest length

    def test_generate_api_key(self):
        """Test API key generation."""
        key1 = User.generate_api_key()
        key2 = User.generate_api_key()
        assert key1 != key2
        assert len(key1) > 20  # Should be reasonably long


class TestUserManager:
    """Tests for UserManager."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = Path(tmpdir) / "users.json"
            yield users_file

    def test_create_first_admin(self, temp_users_file):
        """Test creating first admin account."""
        manager = UserManager(temp_users_file)
        user, api_key = manager.create_first_admin("admin", "test-key")

        assert user.username == "admin"
        assert user.role == "admin"
        assert api_key == "test-key"

        # Verify user can be retrieved
        retrieved_user = manager.get_user_by_api_key("test-key")
        assert retrieved_user is not None
        assert retrieved_user.username == "admin"

    def test_create_first_admin_auto_generate_key(self, temp_users_file):
        """Test creating first admin with auto-generated key."""
        manager = UserManager(temp_users_file)
        user, api_key = manager.create_first_admin("admin")

        assert user.username == "admin"
        assert api_key is not None
        assert len(api_key) > 0

    def test_create_first_admin_fails_if_users_exist(self, temp_users_file):
        """Test that creating first admin fails if users already exist."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin1")

        with pytest.raises(ValueError, match="Users already exist"):
            manager.create_first_admin("admin2")

    def test_create_user(self, temp_users_file):
        """Test creating regular user."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")

        user, api_key = manager.create_user("user1", "user-key", "user")
        assert user.username == "user1"
        assert user.role == "user"
        assert api_key == "user-key"

    def test_create_user_invalid_role(self, temp_users_file):
        """Test creating user with invalid role."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")

        with pytest.raises(ValueError, match="Invalid role"):
            manager.create_user("user1", "key", "invalid_role")

    def test_create_user_duplicate_username(self, temp_users_file):
        """Test creating user with duplicate username."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")
        manager.create_user("user1", "key1")

        with pytest.raises(ValueError, match="already exists"):
            manager.create_user("user1", "key2")

    def test_get_user_by_api_key(self, temp_users_file):
        """Test retrieving user by API key."""
        manager = UserManager(temp_users_file)
        _, api_key = manager.create_first_admin("admin", "admin-key")

        user = manager.get_user_by_api_key("admin-key")
        assert user is not None
        assert user.username == "admin"

        # Invalid key
        assert manager.get_user_by_api_key("invalid-key") is None

    def test_get_user_by_username(self, temp_users_file):
        """Test retrieving user by username."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin", "admin-key")

        user = manager.get_user_by_username("admin")
        assert user is not None
        assert user.username == "admin"

        # Non-existent user
        assert manager.get_user_by_username("nonexistent") is None

    def test_list_users(self, temp_users_file):
        """Test listing all users."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")
        manager.create_user("user1", "key1")
        manager.create_user("user2", "key2")

        users = manager.list_users()
        assert len(users) == 3
        usernames = [u.username for u in users]
        assert "admin" in usernames
        assert "user1" in usernames
        assert "user2" in usernames

    def test_delete_user(self, temp_users_file):
        """Test deleting a user."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")
        manager.create_user("user1", "key1")

        deleted = manager.delete_user("user1")
        assert deleted is True

        assert manager.get_user_by_username("user1") is None
        assert manager.get_user_by_username("admin") is not None

    def test_delete_user_not_found(self, temp_users_file):
        """Test deleting non-existent user."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")

        deleted = manager.delete_user("nonexistent")
        assert deleted is False

    def test_delete_last_admin_fails(self, temp_users_file):
        """Test that deleting last admin fails."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")

        with pytest.raises(ValueError, match="Cannot delete the last admin"):
            manager.delete_user("admin")

    def test_delete_admin_with_multiple_admins(self, temp_users_file):
        """Test deleting admin when multiple admins exist."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin1")
        manager.create_user("admin2", "key2", "admin")

        # Should be able to delete one admin
        deleted = manager.delete_user("admin1")
        assert deleted is True

    def test_has_admin(self, temp_users_file):
        """Test checking if admin exists."""
        manager = UserManager(temp_users_file)
        assert manager.has_admin() is False

        manager.create_first_admin("admin")
        assert manager.has_admin() is True

    def test_is_admin(self, temp_users_file):
        """Test checking if user is admin."""
        manager = UserManager(temp_users_file)
        admin_user, _ = manager.create_first_admin("admin")
        regular_user, _ = manager.create_user("user1", "key1")

        assert manager.is_admin(admin_user) is True
        assert manager.is_admin(regular_user) is False


class TestAuthMiddleware:
    """Tests for authentication middleware with users."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            users_file = Path(tmpdir) / "users.json"
            yield users_file

    def test_authenticate_user_valid(self, temp_users_file):
        """Test authenticating with valid user API key."""
        manager = UserManager(temp_users_file)
        _, api_key = manager.create_first_admin("admin", "test-key")

        auth = AuthMiddleware(
            enable_auth=True,
            user_manager=manager,
            enable_user_auth=True,
        )

        user = auth.authenticate_user("test-key")
        assert user is not None
        assert user.username == "admin"

    def test_authenticate_user_invalid_key(self, temp_users_file):
        """Test authenticating with invalid API key."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin", "valid-key")

        auth = AuthMiddleware(
            enable_auth=True,
            user_manager=manager,
            enable_user_auth=True,
        )

        with pytest.raises(AuthenticationError, match="Invalid API key"):
            auth.authenticate_user("invalid-key")

    def test_authenticate_user_no_key(self, temp_users_file):
        """Test authenticating without API key."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")

        auth = AuthMiddleware(
            enable_auth=True,
            user_manager=manager,
            enable_user_auth=True,
        )

        with pytest.raises(AuthenticationError, match="Authentication required"):
            auth.authenticate_user(None)

    def test_check_permission_admin(self, temp_users_file):
        """Test permission checking for admin user."""
        manager = UserManager(temp_users_file)
        admin_user, _ = manager.create_first_admin("admin")

        auth = AuthMiddleware(
            enable_user_auth=True,
            user_manager=manager,
        )

        # Admin should have access to all operations
        assert auth.check_permission(admin_user, "install") is True
        assert auth.check_permission(admin_user, "create_user") is True
        assert auth.check_permission(admin_user, "list_resources") is True

    def test_check_permission_regular_user(self, temp_users_file):
        """Test permission checking for regular user."""
        manager = UserManager(temp_users_file)
        manager.create_first_admin("admin")
        regular_user, _ = manager.create_user("user1", "key1")

        auth = AuthMiddleware(
            enable_user_auth=True,
            user_manager=manager,
        )

        # Regular user should have read access
        assert auth.check_permission(regular_user, "list_resources") is True
        assert auth.check_permission(regular_user, "read_resource") is True

        # Regular user should NOT have write access
        assert auth.check_permission(regular_user, "install") is False
        assert auth.check_permission(regular_user, "create_user") is False
        assert auth.check_permission(regular_user, "uninstall") is False

    def test_check_permission_no_user(self, temp_users_file):
        """Test permission checking without user."""
        manager = UserManager(temp_users_file)

        auth = AuthMiddleware(
            enable_user_auth=True,
            user_manager=manager,
        )

        # No user should be denied
        assert auth.check_permission(None, "install") is False
        assert auth.check_permission(None, "list_resources") is False

    def test_check_permission_user_auth_disabled(self, temp_users_file):
        """Test permission checking when user auth is disabled."""
        auth = AuthMiddleware(enable_user_auth=False)

        # When user auth is disabled, all operations should be allowed
        assert auth.check_permission(None, "install") is True
        assert auth.check_permission(None, "create_user") is True
