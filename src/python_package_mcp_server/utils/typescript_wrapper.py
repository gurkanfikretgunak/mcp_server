"""Safe wrapper for executing TypeScript/Node.js CLI commands."""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class TypeScriptError(Exception):
    """Error raised when TypeScript command fails."""

    pass


class TypeScriptWrapper:
    """Wrapper for executing TypeScript/Node.js commands safely."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize wrapper with optional project root.

        Args:
            project_root: Root directory of the project (for project-specific commands)
        """
        self.project_root = project_root or Path.cwd()
        self._ensure_node_available()

    def _ensure_node_available(self) -> None:
        """Check if Node.js is available in PATH."""
        try:
            result = self._run_command(["node", "--version"], check=False)
            if result.returncode != 0:
                raise TypeScriptError("Node.js is not available or not working correctly")
            logger.info("node_available", version=result.stdout.strip())
        except FileNotFoundError:
            raise TypeScriptError(
                "Node.js is not installed. Please install Node.js: https://nodejs.org/"
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
            TypeScriptError: If command fails and check=True
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
                raise TypeScriptError(f"Command failed: {error_msg}")

            return result
        except subprocess.TimeoutExpired:
            logger.error("command_timeout", command=" ".join(cmd))
            raise TypeScriptError(f"Command timed out: {' '.join(cmd)}")
        except Exception as e:
            logger.error("command_error", command=" ".join(cmd), error=str(e))
            raise TypeScriptError(f"Error running command: {str(e)}")

    def _run_npx(self, package: str, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a command via npx.

        Args:
            package: Package name to run
            args: Arguments to pass to the package
            check: Whether to raise exception on non-zero exit code

        Returns:
            CompletedProcess result
        """
        cmd = ["npx", "--yes", package] + args
        return self._run_command(cmd, check=check)

    def format_code(self, paths: Optional[list[str]] = None) -> dict[str, Any]:
        """Format TypeScript code using Prettier.

        Args:
            paths: Optional list of file/directory paths to format (formats all if None)

        Returns:
            Format result
        """
        cmd_args = ["--write"]
        if paths:
            cmd_args.extend(paths)
        else:
            cmd_args.append(".")

        result = self._run_npx("prettier", cmd_args, check=False)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def lint_code(self, paths: Optional[list[str]] = None) -> dict[str, Any]:
        """Lint TypeScript code using ESLint.

        Args:
            paths: Optional list of file/directory paths to lint (lints all if None)

        Returns:
            Lint result with issues
        """
        cmd_args = ["--format", "json"]
        if paths:
            cmd_args.extend(paths)
        else:
            cmd_args.append(".")

        result = self._run_npx("eslint", cmd_args, check=False)
        
        issues = []
        if result.stdout:
            try:
                # ESLint JSON format
                lint_data = json.loads(result.stdout)
                if isinstance(lint_data, list):
                    issues = lint_data
                else:
                    issues = [lint_data]
            except json.JSONDecodeError:
                # Fallback to parsing text output
                issues = [{"message": result.stdout, "severity": "info"}]

        return {
            "success": result.returncode == 0,
            "issues": issues,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def type_check(self, project_path: Optional[str] = None) -> dict[str, Any]:
        """Type check TypeScript code using tsc.

        Args:
            project_path: Optional path to tsconfig.json (uses default if None)

        Returns:
            Type check result
        """
        cmd = ["npx", "--yes", "typescript", "--noEmit"]
        if project_path:
            cmd.extend(["--project", project_path])

        result = self._run_command(cmd, check=False)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def check_standards(self, file_path: str) -> dict[str, Any]:
        """Check if TypeScript code follows standards.

        Args:
            file_path: Path to TypeScript file to check

        Returns:
            Standards compliance result
        """
        # Run format check, lint, and type check
        format_result = self.format_code([file_path])
        lint_result = self.lint_code([file_path])
        
        # Check formatting without writing
        format_check_result = self._run_npx("prettier", ["--check", file_path], check=False)

        return {
            "file": file_path,
            "formatted": format_check_result.returncode == 0,
            "linting": lint_result,
            "standards_compliant": (
                format_check_result.returncode == 0 
                and len(lint_result.get("issues", [])) == 0
            ),
        }
