"""User management system for MCP server."""

import hashlib
import json
import os
import secrets
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


class User:
    """User model."""

    def __init__(self, username: str, api_key_hash: str, role: str, created_at: str):
        """Initialize user.

        Args:
            username: Username
            api_key_hash: Hashed API key
            role: User role (admin or user)
            created_at: Creation timestamp
        """
        self.username = username
        self.api_key_hash = api_key_hash
        self.role = role
        self.created_at = created_at

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "username": self.username,
            "api_key_hash": self.api_key_hash,
            "role": self.role,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create user from dictionary."""
        return cls(
            username=data["username"],
            api_key_hash=data["api_key_hash"],
            role=data["role"],
            created_at=data["created_at"],
        )

    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key using SHA-256.

        Args:
            api_key: API key to hash

        Returns:
            Hashed API key
        """
        return hashlib.sha256(api_key.encode()).hexdigest()

    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure random API key.

        Returns:
            Generated API key
        """
        return secrets.token_urlsafe(32)


class UserManager:
    """User management system."""

    def __init__(self, users_file: Path):
        """Initialize user manager.

        Args:
            users_file: Path to users JSON file
        """
        self.users_file = users_file
        self._lock = threading.Lock()
        self._ensure_users_file()

    def _ensure_users_file(self) -> None:
        """Ensure users file exists and has correct permissions."""
        # Create directory if it doesn't exist
        self.users_file.parent.mkdir(parents=True, exist_ok=True)

        # Create file with empty users list if it doesn't exist
        if not self.users_file.exists():
            self._write_users([])
            # Set restrictive permissions (read/write for owner only)
            os.chmod(self.users_file, 0o600)

    def _read_users(self) -> list[dict]:
        """Read users from file.

        Returns:
            List of user dictionaries
        """
        try:
            if not self.users_file.exists():
                return []

            with open(self.users_file, "r") as f:
                data = json.load(f)
                return data.get("users", [])
        except (json.JSONDecodeError, IOError) as e:
            logger.error("failed_to_read_users_file", error=str(e))
            return []

    def _write_users(self, users: list[dict]) -> None:
        """Write users to file atomically.

        Args:
            users: List of user dictionaries
        """
        # Write to temporary file first
        temp_file = self.users_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w") as f:
                json.dump({"users": users}, f, indent=2)
            # Atomic rename
            temp_file.replace(self.users_file)
            # Ensure restrictive permissions
            os.chmod(self.users_file, 0o600)
        except IOError as e:
            logger.error("failed_to_write_users_file", error=str(e))
            if temp_file.exists():
                temp_file.unlink()
            raise

    def get_user_by_api_key(self, api_key: str) -> Optional[User]:
        """Get user by API key.

        Args:
            api_key: API key to look up

        Returns:
            User if found, None otherwise
        """
        api_key_hash = User.hash_api_key(api_key)
        users = self._read_users()

        for user_data in users:
            if user_data["api_key_hash"] == api_key_hash:
                return User.from_dict(user_data)

        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username.

        Args:
            username: Username to look up

        Returns:
            User if found, None otherwise
        """
        users = self._read_users()

        for user_data in users:
            if user_data["username"] == username:
                return User.from_dict(user_data)

        return None

    def create_user(self, username: str, api_key: Optional[str] = None, role: str = "user") -> tuple[User, str]:
        """Create a new user.

        Args:
            username: Username
            api_key: API key (generated if not provided)
            role: User role (admin or user)

        Returns:
            Tuple of (User object, plain API key)

        Raises:
            ValueError: If username already exists or invalid role
        """
        with self._lock:
            # Validate username
            if not username or not username.strip():
                raise ValueError("Username cannot be empty")

            # Validate role
            if role not in ["admin", "user"]:
                raise ValueError(f"Invalid role: {role}. Must be 'admin' or 'user'")

            # Check if user already exists
            if self.get_user_by_username(username):
                raise ValueError(f"User '{username}' already exists")

            # Generate API key if not provided
            if not api_key:
                api_key = User.generate_api_key()

            # Hash API key
            api_key_hash = User.hash_api_key(api_key)

            # Create user
            user = User(
                username=username,
                api_key_hash=api_key_hash,
                role=role,
                created_at=datetime.utcnow().isoformat(),
            )

            # Add to users list
            users = self._read_users()
            users.append(user.to_dict())
            self._write_users(users)

            logger.info("user_created", username=username, role=role)
            return user, api_key

    def create_first_admin(self, username: str, api_key: Optional[str] = None) -> tuple[User, str]:
        """Create the first admin account.

        Args:
            username: Username for admin
            api_key: API key (generated if not provided)

        Returns:
            Tuple of (User object, plain API key)

        Raises:
            ValueError: If users already exist
        """
        with self._lock:
            users = self._read_users()
            if users:
                raise ValueError("Users already exist. Cannot create first admin. Use create_user tool instead.")

            return self.create_user(username, api_key, role="admin")

    def list_users(self) -> list[User]:
        """List all users.

        Returns:
            List of User objects
        """
        users_data = self._read_users()
        return [User.from_dict(user_data) for user_data in users_data]

    def delete_user(self, username: str) -> bool:
        """Delete a user.

        Args:
            username: Username to delete

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If trying to delete the last admin
        """
        with self._lock:
            users = self._read_users()

            # Check if user exists
            user_to_delete = None
            for user_data in users:
                if user_data["username"] == username:
                    user_to_delete = User.from_dict(user_data)
                    break

            if not user_to_delete:
                return False

            # Check if deleting last admin
            admin_count = sum(1 for u in users if u["role"] == "admin")
            if user_to_delete.role == "admin" and admin_count == 1:
                raise ValueError("Cannot delete the last admin user")

            # Remove user
            users = [u for u in users if u["username"] != username]
            self._write_users(users)

            logger.info("user_deleted", username=username)
            return True

    def has_admin(self) -> bool:
        """Check if any admin user exists.

        Returns:
            True if admin exists, False otherwise
        """
        users = self._read_users()
        return any(user["role"] == "admin" for user in users)

    def is_admin(self, user: User) -> bool:
        """Check if user is admin.

        Args:
            user: User to check

        Returns:
            True if admin, False otherwise
        """
        return user.role == "admin"
