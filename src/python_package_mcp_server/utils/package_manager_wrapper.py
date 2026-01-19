"""Safe wrapper for executing uv CLI commands."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class PackageManagerError(Exception):
    """Error raised when package manager command fails."""

    pass


class PackageManagerWrapper:
    """Wrapper for executing uv commands safely."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize wrapper with optional project root.

        Args:
            project_root: Root directory of the project (for project-specific commands)
        """
        self.project_root = project_root or Path.cwd()
        self._ensure_uv_available()

    def _ensure_uv_available(self) -> None:
        """Check if uv is available in PATH."""
        try:
            result = self._run_command(["uv", "--version"], check=False)
            if result.returncode != 0:
                raise PackageManagerError("uv is not available or not working correctly")
            logger.info("uv_package_manager_available", version=result.stdout.strip())
        except FileNotFoundError:
            raise PackageManagerError(
                "uv is not installed. Please install uv: https://github.com/astral-sh/uv"
            )

    def _run_command(
        self,
        cmd: list[str],
        check: bool = True,
        cwd: Optional[Path] = None,
        capture_output: bool = True,
    ) -> subprocess.CompletedProcess:
        """Run a command safely.

        Args:
            cmd: Command to run
            check: Whether to raise exception on non-zero exit code
            cwd: Working directory for command
            capture_output: Whether to capture stdout/stderr

        Returns:
            CompletedProcess result

        Raises:
            PackageManagerError: If command fails and check=True
        """
        cwd = cwd or self.project_root
        logger.debug("running_command", command=" ".join(cmd), cwd=str(cwd))

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=False,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode != 0 and check:
                error_msg = result.stderr or result.stdout or "Unknown error"
                logger.error(
                    "command_failed",
                    command=" ".join(cmd),
                    returncode=result.returncode,
                    error=error_msg,
                )
                raise PackageManagerError(f"Command failed: {error_msg}")

            return result
        except subprocess.TimeoutExpired:
            logger.error("command_timeout", command=" ".join(cmd))
            raise PackageManagerError(f"Command timed out: {' '.join(cmd)}")
        except Exception as e:
            logger.error("command_error", command=" ".join(cmd), error=str(e))
            raise PackageManagerError(f"Error running command: {str(e)}")

    def list_installed(self) -> list[dict[str, Any]]:
        """List installed packages.

        Returns:
            List of packages with name and version
        """
        result = self._run_command(["uv", "pip", "list", "--format", "json"])
        try:
            packages = json.loads(result.stdout)
            return packages
        except json.JSONDecodeError as e:
            logger.error("failed_to_parse_packages", error=str(e))
            raise PackageManagerError(f"Failed to parse package list: {str(e)}")

    def list_outdated(self) -> list[dict[str, Any]]:
        """List outdated packages.

        Returns:
            List of outdated packages with current and latest versions
        """
        result = self._run_command(["uv", "pip", "list", "--outdated", "--format", "json"])
        try:
            packages = json.loads(result.stdout)
            return packages
        except json.JSONDecodeError as e:
            logger.error("failed_to_parse_outdated", error=str(e))
            raise PackageManagerError(f"Failed to parse outdated packages: {str(e)}")

    def get_dependency_tree(self) -> dict[str, Any]:
        """Get dependency tree for the project.

        Returns:
            Dependency tree structure
        """
        if not (self.project_root / "pyproject.toml").exists():
            return {"error": "No pyproject.toml found in project root"}

        result = self._run_command(["uv", "tree", "--format", "json"], check=False)
        if result.returncode != 0:
            return {"error": result.stderr or "Failed to generate dependency tree"}

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "Failed to parse dependency tree"}

    def get_project_info(self) -> dict[str, Any]:
        """Get project metadata.

        Returns:
            Project information including pyproject.toml and lock file info
        """
        info: dict[str, Any] = {}

        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomli

                with open(pyproject_path, "rb") as f:
                    pyproject_data = tomli.load(f)
                    info["pyproject"] = pyproject_data
            except ImportError:
                logger.warning("tomli_not_available", message="Cannot parse pyproject.toml without tomli")
            except Exception as e:
                logger.error("failed_to_read_pyproject", error=str(e))

        lock_path = self.project_root / "uv.lock"
        if lock_path.exists():
            info["lock_file"] = {
                "exists": True,
                "size": lock_path.stat().st_size,
                "modified": lock_path.stat().st_mtime,
            }
        else:
            info["lock_file"] = {"exists": False}

        return info

    def install_packages(self, packages: list[str], editable: bool = False) -> dict[str, Any]:
        """Install packages.

        Args:
            packages: List of package specifications (e.g., ["requests==2.31.0", "pytest"])
            editable: Whether to install in editable mode

        Returns:
            Installation result
        """
        cmd = ["uv", "pip", "install"] + packages
        if editable:
            cmd.append("--editable")

        result = self._run_command(cmd)
        return {"success": True, "output": result.stdout}

    def uninstall_packages(self, packages: list[str]) -> dict[str, Any]:
        """Uninstall packages.

        Args:
            packages: List of package names to uninstall

        Returns:
            Uninstallation result
        """
        cmd = ["uv", "pip", "uninstall", "-y"] + packages
        result = self._run_command(cmd)
        return {"success": True, "output": result.stdout}

    def add_packages(self, packages: list[str], dev: bool = False) -> dict[str, Any]:
        """Add packages to project dependencies.

        Args:
            packages: List of package specifications
            dev: Whether to add as dev dependencies

        Returns:
            Addition result
        """
        cmd = ["uv", "add"]
        if dev:
            cmd.append("--dev")
        cmd.extend(packages)

        result = self._run_command(cmd)
        return {"success": True, "output": result.stdout}

    def remove_packages(self, packages: list[str]) -> dict[str, Any]:
        """Remove packages from project dependencies.

        Args:
            packages: List of package names to remove

        Returns:
            Removal result
        """
        cmd = ["uv", "remove"] + packages
        result = self._run_command(cmd)
        return {"success": True, "output": result.stdout}

    def sync(self) -> dict[str, Any]:
        """Sync environment with lock file.

        Returns:
            Sync result
        """
        result = self._run_command(["uv", "sync"])
        return {"success": True, "output": result.stdout}

    def lock(self) -> dict[str, Any]:
        """Generate or update lock file.

        Returns:
            Lock result
        """
        result = self._run_command(["uv", "lock"])
        return {"success": True, "output": result.stdout}

    def init_project(self, name: Optional[str] = None) -> dict[str, Any]:
        """Initialize a new Python project.

        Args:
            name: Optional project name

        Returns:
            Initialization result
        """
        cmd = ["uv", "init"]
        if name:
            cmd.append(name)

        result = self._run_command(cmd, cwd=self.project_root.parent if name else self.project_root)
        return {"success": True, "output": result.stdout}

    def upgrade_packages(self, packages: Optional[list[str]] = None) -> dict[str, Any]:
        """Upgrade packages.

        Args:
            packages: Optional list of package names to upgrade (upgrades all if None)

        Returns:
            Upgrade result
        """
        if packages:
            # Upgrade specific packages
            cmd = ["uv", "pip", "install", "--upgrade"] + packages
        else:
            # Upgrade all packages
            cmd = ["uv", "pip", "install", "--upgrade", "--upgrade-package", "all"]

        result = self._run_command(cmd)
        return {"success": True, "output": result.stdout}
