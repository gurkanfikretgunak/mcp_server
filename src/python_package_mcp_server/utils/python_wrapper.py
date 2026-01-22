"""Safe wrapper for executing Python CLI commands."""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class PythonError(Exception):
    """Error raised when Python command fails."""

    pass


class PythonWrapper:
    """Wrapper for executing Python CLI commands safely."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize wrapper with optional project root.

        Args:
            project_root: Root directory of the project (for project-specific commands)
        """
        self.project_root = project_root or Path.cwd()
        self.python_cmd: str = "python3"  # Default, will be set by _ensure_python_available
        self._ensure_python_available()

    def _ensure_python_available(self) -> None:
        """Check if Python is available in PATH."""
        # Try python3 first, then python
        for cmd_name in ["python3", "python"]:
            try:
                result = self._run_command([cmd_name, "--version"], check=False)
                if result.returncode == 0:
                    logger.info("python_available", version=result.stdout.strip())
                    self.python_cmd = cmd_name
                    return
            except FileNotFoundError:
                continue
        
        raise PythonError(
            "Python is not installed. Please install Python: https://www.python.org/downloads/"
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
            PythonError: If command fails and check=True
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
                raise PythonError(f"Command failed: {error_msg}")

            return result
        except subprocess.TimeoutExpired:
            logger.error("command_timeout", command=" ".join(cmd))
            raise PythonError(f"Command timed out: {' '.join(cmd)}")
        except Exception as e:
            logger.error("command_error", command=" ".join(cmd), error=str(e))
            raise PythonError(f"Error running command: {str(e)}")

    def _run_python_module(
        self, module: str, args: list[str], check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a Python module via -m flag.

        Args:
            module: Module name to run
            args: Arguments to pass to the module
            check: Whether to raise exception on non-zero exit code

        Returns:
            CompletedProcess result
        """
        cmd = [self.python_cmd, "-m", module] + args
        return self._run_command(cmd, check=check)

    def format_code(
        self, paths: Optional[list[str]] = None, formatter: str = "black"
    ) -> dict[str, Any]:
        """Format Python code.

        Args:
            paths: Optional list of file/directory paths to format (formats all if None)
            formatter: Formatter to use ('black' or 'autopep8')

        Returns:
            Format result
        """
        if formatter == "black":
            cmd = ["black"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("black", cmd[1:], check=False)
        elif formatter == "autopep8":
            cmd = ["autopep8", "--in-place", "--aggressive", "--aggressive"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("autopep8", cmd[1:], check=False)
        else:
            raise PythonError(f"Unknown formatter: {formatter}")

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def lint_code(
        self, paths: Optional[list[str]] = None, linter: str = "ruff"
    ) -> dict[str, Any]:
        """Lint Python code.

        Args:
            paths: Optional list of file/directory paths to lint (lints all if None)
            linter: Linter to use ('ruff', 'pylint', or 'flake8')

        Returns:
            Lint result with issues
        """
        if linter == "ruff":
            cmd = ["ruff", "check", "--output-format", "json"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("ruff", cmd[1:], check=False)
        elif linter == "pylint":
            cmd = ["pylint", "--output-format=json"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("pylint", cmd[1:], check=False)
        elif linter == "flake8":
            cmd = ["flake8", "--format=json"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("flake8", cmd[1:], check=False)
        else:
            raise PythonError(f"Unknown linter: {linter}")

        issues = []
        if result.stdout:
            try:
                # Try to parse JSON output
                lint_data = json.loads(result.stdout)
                if isinstance(lint_data, list):
                    issues = lint_data
                elif isinstance(lint_data, dict):
                    # Ruff format: {"violations": [...]}
                    if "violations" in lint_data:
                        issues = lint_data["violations"]
                    else:
                        issues = [lint_data]
                else:
                    issues = [{"message": result.stdout, "severity": "info"}]
            except json.JSONDecodeError:
                # Fallback to parsing text output
                issues = [{"message": result.stdout, "severity": "info"}]

        return {
            "success": result.returncode == 0,
            "issues": issues,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def type_check(
        self, paths: Optional[list[str]] = None, type_checker: str = "mypy"
    ) -> dict[str, Any]:
        """Type check Python code.

        Args:
            paths: Optional list of file/directory paths to type check (checks all if None)
            type_checker: Type checker to use ('mypy' or 'pyright')

        Returns:
            Type check result
        """
        if type_checker == "mypy":
            cmd = ["mypy", "--show-error-codes", "--no-error-summary"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            result = self._run_python_module("mypy", cmd[1:], check=False)
        elif type_checker == "pyright":
            cmd = ["pyright", "--outputjson"]
            if paths:
                cmd.extend(paths)
            else:
                cmd.append(".")
            # Pyright is a Node.js tool, not a Python module
            result = self._run_command(["npx", "--yes", "pyright"] + cmd[1:], check=False)
        else:
            raise PythonError(f"Unknown type checker: {type_checker}")

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def check_standards(self, file_path: str) -> dict[str, Any]:
        """Check if Python code follows standards.

        Args:
            file_path: Path to Python file to check

        Returns:
            Standards compliance result
        """
        # Run format check (without modifying)
        format_check_cmd = ["black", "--check", "--diff", file_path]
        format_check = self._run_python_module("black", format_check_cmd[1:], check=False)

        # Run lint check
        lint_result = self.lint_code([file_path])

        # Run type check if mypy is available
        type_check_result = None
        try:
            type_check_result = self.type_check([file_path])
        except Exception:
            # Type checking is optional
            pass

        return {
            "file": file_path,
            "formatted": format_check.returncode == 0,
            "linting": lint_result,
            "type_checking": type_check_result,
            "standards_compliant": (
                format_check.returncode == 0
                and len(lint_result.get("issues", [])) == 0
                and (type_check_result is None or type_check_result.get("success", False))
            ),
        }
