"""Policy engine for package management restrictions."""

import re
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


class PolicyViolationError(Exception):
    """Error raised when policy is violated."""

    pass


class PolicyEngine:
    """Policy engine for enforcing package management policies."""

    def __init__(
        self,
        allowed_packages: Optional[list[str]] = None,
        blocked_packages: Optional[list[str]] = None,
    ):
        """Initialize policy engine.

        Args:
            allowed_packages: List of allowed package patterns (regex)
            blocked_packages: List of blocked package patterns (regex)
        """
        self.allowed_patterns = [re.compile(pattern) for pattern in (allowed_packages or [])]
        self.blocked_patterns = [re.compile(pattern) for pattern in (blocked_packages or [])]

    def check_package(self, package_name: str) -> bool:
        """Check if package is allowed by policy.

        Args:
            package_name: Name of package to check

        Returns:
            True if allowed, False if blocked

        Raises:
            PolicyViolationError: If package is blocked
        """
        # Check blocked patterns first
        for pattern in self.blocked_patterns:
            if pattern.search(package_name):
                logger.warning("package_blocked", package=package_name, pattern=pattern.pattern)
                raise PolicyViolationError(f"Package '{package_name}' is blocked by policy")

        # If allowed patterns exist, check them
        if self.allowed_patterns:
            allowed = any(pattern.search(package_name) for pattern in self.allowed_patterns)
            if not allowed:
                logger.warning("package_not_allowed", package=package_name)
                raise PolicyViolationError(f"Package '{package_name}' is not in allowed list")
            logger.debug("package_allowed", package=package_name)
            return True

        # No restrictions
        return True

    def check_packages(self, package_names: list[str]) -> bool:
        """Check multiple packages against policy.

        Args:
            package_names: List of package names to check

        Returns:
            True if all allowed

        Raises:
            PolicyViolationError: If any package is blocked
        """
        for package_name in package_names:
            # Extract package name from spec (e.g., "requests==2.31.0" -> "requests")
            name = package_name.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].strip()
            self.check_package(name)

        return True
