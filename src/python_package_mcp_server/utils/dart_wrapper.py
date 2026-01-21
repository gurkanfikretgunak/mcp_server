"""Safe wrapper for executing Dart CLI commands."""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class DartError(Exception):
    """Error raised when Dart command fails."""

    pass


class DartWrapper:
    """Wrapper for executing Dart commands safely."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize wrapper with optional project root.

        Args:
            project_root: Root directory of the project (for project-specific commands)
        """
        self.project_root = project_root or Path.cwd()
        self._ensure_dart_available()

    def _ensure_dart_available(self) -> None:
        """Check if Dart is available in PATH."""
        try:
            result = self._run_command(["dart", "--version"], check=False)
            if result.returncode != 0:
                raise DartError("Dart is not available or not working correctly")
            logger.info("dart_available", version=result.stdout.strip())
        except FileNotFoundError:
            raise DartError(
                "Dart is not installed. Please install Dart SDK: https://dart.dev/get-dart"
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
            DartError: If command fails and check=True
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
                raise DartError(f"Command failed: {error_msg}")

            return result
        except subprocess.TimeoutExpired:
            logger.error("command_timeout", command=" ".join(cmd))
            raise DartError(f"Command timed out: {' '.join(cmd)}")
        except Exception as e:
            logger.error("command_error", command=" ".join(cmd), error=str(e))
            raise DartError(f"Error running command: {str(e)}")

    def format_code(self, paths: Optional[list[str]] = None, line_length: int = 80) -> dict[str, Any]:
        """Format Dart code.

        Args:
            paths: Optional list of file/directory paths to format (formats all if None)
            line_length: Line length for formatting

        Returns:
            Format result
        """
        cmd = ["dart", "format", "--line-length", str(line_length)]
        if paths:
            cmd.extend(paths)
        else:
            cmd.append(".")

        result = self._run_command(cmd, check=False)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def analyze_code(self, paths: Optional[list[str]] = None) -> dict[str, Any]:
        """Analyze Dart code for errors and warnings.

        Args:
            paths: Optional list of file/directory paths to analyze (analyzes all if None)

        Returns:
            Analysis result with issues
        """
        cmd = ["dart", "analyze", "--format", "json"]
        if paths:
            cmd.extend(paths)
        else:
            cmd.append(".")

        result = self._run_command(cmd, check=False)
        
        issues = []
        if result.stdout:
            try:
                # Dart analyze JSON format
                analysis_data = json.loads(result.stdout)
                issues = analysis_data.get("issues", [])
            except json.JSONDecodeError:
                # Fallback to parsing text output
                issues = [{"message": result.stdout, "severity": "info"}]

        return {
            "success": result.returncode == 0,
            "issues": issues,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def fix_code(self, paths: Optional[list[str]] = None) -> dict[str, Any]:
        """Apply automated fixes to Dart code.

        Args:
            paths: Optional list of file/directory paths to fix (fixes all if None)

        Returns:
            Fix result
        """
        cmd = ["dart", "fix", "--apply"]
        if paths:
            cmd.extend(paths)
        else:
            cmd.append(".")

        result = self._run_command(cmd, check=False)
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr if result.returncode != 0 else None,
        }

    def check_standards(self, file_path: str) -> dict[str, Any]:
        """Check if Dart code follows standards.

        Args:
            file_path: Path to Dart file to check

        Returns:
            Standards compliance result
        """
        # Run both format check and analyze
        format_result = self.format_code([file_path])
        analyze_result = self.analyze_code([file_path])

        # Check if file is properly formatted
        format_check_cmd = ["dart", "format", "--set-exit-if-changed", file_path]
        format_check = self._run_command(format_check_cmd, check=False)

        return {
            "file": file_path,
            "formatted": format_check.returncode == 0,
            "analysis": analyze_result,
            "standards_compliant": format_check.returncode == 0 and len(analyze_result.get("issues", [])) == 0,
        }
