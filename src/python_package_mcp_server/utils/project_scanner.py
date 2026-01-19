"""Project discovery and indexing utilities for LLM-assisted development."""

import ast
import re
from pathlib import Path
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class ProjectScanner:
    """Scans and indexes project structure for LLM-assisted development."""

    # Common ignore patterns
    DEFAULT_IGNORE_PATTERNS = [
        r"^\.git/",
        r"^\.venv/",
        r"^venv/",
        r"^env/",
        r"^__pycache__/",
        r"^\.pytest_cache/",
        r"^\.mypy_cache/",
        r"^node_modules/",
        r"^\.DS_Store$",
        r"^\.pyc$",
        r"^\.pyo$",
        r"^\.pyd$",
        r"^\.so$",
        r"^\.egg-info/",
        r"^dist/",
        r"^build/",
    ]

    def __init__(self, project_root: Path, ignore_patterns: Optional[list[str]] = None):
        """Initialize scanner.

        Args:
            project_root: Root directory of the project
            ignore_patterns: Additional ignore patterns (regex)
        """
        self.project_root = Path(project_root).resolve()
        self.ignore_patterns = (ignore_patterns or []) + self.DEFAULT_IGNORE_PATTERNS
        self._compiled_patterns = [re.compile(pattern) for pattern in self.ignore_patterns]

    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored.

        Args:
            path: Path to check

        Returns:
            True if path should be ignored
        """
        rel_path = path.relative_to(self.project_root)
        path_str = str(rel_path).replace("\\", "/")

        for pattern in self._compiled_patterns:
            if pattern.search(path_str):
                return True
        return False

    def scan_structure(self) -> dict[str, Any]:
        """Scan project file structure.

        Returns:
            Dictionary with project structure tree
        """
        structure: dict[str, Any] = {
            "root": str(self.project_root),
            "files": [],
            "directories": [],
        }

        try:
            for item in self.project_root.rglob("*"):
                if self._should_ignore(item):
                    continue

                rel_path = item.relative_to(self.project_root)
                item_info = {
                    "path": str(rel_path),
                    "name": item.name,
                }

                if item.is_file():
                    item_info["size"] = item.stat().st_size
                    item_info["extension"] = item.suffix
                    structure["files"].append(item_info)
                elif item.is_dir():
                    structure["directories"].append(item_info)

            # Sort for consistent output
            structure["files"].sort(key=lambda x: x["path"])
            structure["directories"].sort(key=lambda x: x["path"])

        except Exception as e:
            logger.error("scan_structure_error", error=str(e))
            structure["error"] = str(e)

        return structure

    def find_config_files(self) -> list[dict[str, Any]]:
        """Find configuration files in project.

        Returns:
            List of configuration files with metadata
        """
        config_patterns = [
            "pyproject.toml",
            "package.json",
            "requirements.txt",
            "requirements-dev.txt",
            "setup.py",
            "setup.cfg",
            "Pipfile",
            "Pipfile.lock",
            "poetry.lock",
            "uv.lock",
            ".env",
            ".env.example",
            "docker-compose.yml",
            "Dockerfile",
            "Makefile",
            "CMakeLists.txt",
            "Cargo.toml",
            "go.mod",
            "go.sum",
        ]

        config_files = []
        for pattern in config_patterns:
            for path in self.project_root.rglob(pattern):
                if self._should_ignore(path):
                    continue

                rel_path = path.relative_to(self.project_root)
                config_files.append(
                    {
                        "path": str(rel_path),
                        "name": path.name,
                        "type": pattern,
                        "size": path.stat().st_size,
                    }
                )

        return config_files

    def find_dependency_files(self) -> list[dict[str, Any]]:
        """Find dependency files across project types.

        Returns:
            List of dependency files
        """
        dependency_patterns = [
            "requirements*.txt",
            "Pipfile",
            "Pipfile.lock",
            "poetry.lock",
            "uv.lock",
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "Cargo.toml",
            "Cargo.lock",
            "go.mod",
            "go.sum",
            "pom.xml",
            "build.gradle",
        ]

        dependency_files = []
        for pattern in dependency_patterns:
            for path in self.project_root.rglob(pattern):
                if self._should_ignore(path):
                    continue

                rel_path = path.relative_to(self.project_root)
                dependency_files.append(
                    {
                        "path": str(rel_path),
                        "name": path.name,
                        "type": self._detect_dependency_type(path),
                    }
                )

        return dependency_files

    def _detect_dependency_type(self, path: Path) -> str:
        """Detect dependency file type.

        Args:
            path: Path to dependency file

        Returns:
            Dependency type string
        """
        name = path.name.lower()
        if "requirements" in name:
            return "python-requirements"
        elif name in ["pipfile", "pipfile.lock"]:
            return "python-pipenv"
        elif name in ["poetry.lock", "pyproject.toml"]:
            return "python-poetry"
        elif name in ["uv.lock", "pyproject.toml"]:
            return "python-uv"
        elif name in ["package.json", "package-lock.json", "yarn.lock"]:
            return "nodejs"
        elif name in ["cargo.toml", "cargo.lock"]:
            return "rust"
        elif name in ["go.mod", "go.sum"]:
            return "go"
        elif name in ["pom.xml", "build.gradle"]:
            return "java"
        return "unknown"

    def find_readme_files(self) -> list[dict[str, Any]]:
        """Find README and documentation files.

        Returns:
            List of README/documentation files
        """
        readme_patterns = [
            "README*",
            "CHANGELOG*",
            "CONTRIBUTING*",
            "LICENSE*",
            "LICENCE*",
            "*.md",
            "*.rst",
            "*.txt",
        ]

        readme_files = []
        for pattern in readme_patterns:
            for path in self.project_root.rglob(pattern):
                if self._should_ignore(path):
                    continue

                rel_path = path.relative_to(self.project_root)
                readme_files.append(
                    {
                        "path": str(rel_path),
                        "name": path.name,
                        "size": path.stat().st_size,
                    }
                )

        return readme_files

    def find_entry_points(self) -> list[dict[str, Any]]:
        """Find entry points and main files.

        Returns:
            List of entry point files
        """
        entry_points = []

        # Check pyproject.toml for entry points
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomli

                with open(pyproject_path, "rb") as f:
                    pyproject = tomli.load(f)
                    if "project" in pyproject and "scripts" in pyproject["project"]:
                        for name, module_path in pyproject["project"]["scripts"].items():
                            entry_points.append(
                                {
                                    "name": name,
                                    "type": "script",
                                    "module": module_path,
                                }
                            )
            except Exception as e:
                logger.debug("failed_to_parse_pyproject", error=str(e))

        # Find main.py, __main__.py, app.py, etc.
        main_patterns = ["main.py", "__main__.py", "app.py", "run.py", "server.py"]
        for pattern in main_patterns:
            for path in self.project_root.rglob(pattern):
                if self._should_ignore(path):
                    continue
                rel_path = path.relative_to(self.project_root)
                entry_points.append(
                    {
                        "path": str(rel_path),
                        "name": path.name,
                        "type": "main_file",
                    }
                )

        return entry_points

    def find_test_files(self) -> list[dict[str, Any]]:
        """Find test files and test structure.

        Returns:
            List of test files with metadata
        """
        test_patterns = [
            "test_*.py",
            "*_test.py",
            "tests/",
            "test/",
            "spec/",
            "*.test.js",
            "*.spec.js",
        ]

        test_files = []
        for pattern in test_patterns:
            for path in self.project_root.rglob(pattern):
                if self._should_ignore(path):
                    continue

                rel_path = path.relative_to(self.project_root)
                if path.is_file():
                    test_files.append(
                        {
                            "path": str(rel_path),
                            "name": path.name,
                            "type": "test_file",
                        }
                    )
                elif path.is_dir():
                    test_files.append(
                        {
                            "path": str(rel_path),
                            "name": path.name,
                            "type": "test_directory",
                        }
                    )

        return test_files

    def extract_symbols(self, file_path: Path) -> list[dict[str, Any]]:
        """Extract symbols (functions, classes) from Python file.

        Args:
            file_path: Path to Python file

        Returns:
            List of symbols with metadata
        """
        symbols = []

        if not file_path.suffix == ".py":
            return symbols

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    symbols.append(
                        {
                            "name": node.name,
                            "type": "function",
                            "line": node.lineno,
                            "col_offset": node.col_offset,
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    symbols.append(
                        {
                            "name": node.name,
                            "type": "class",
                            "line": node.lineno,
                            "col_offset": node.col_offset,
                        }
                    )

        except Exception as e:
            logger.debug("failed_to_extract_symbols", file=str(file_path), error=str(e))

        return symbols

    def search_codebase(self, pattern: str, file_extensions: Optional[list[str]] = None) -> list[dict[str, Any]]:
        """Search codebase for pattern.

        Args:
            pattern: Search pattern (regex)
            file_extensions: Optional list of file extensions to search (e.g., [".py", ".js"])

        Returns:
            List of matches with file and line information
        """
        matches = []
        compiled_pattern = re.compile(pattern, re.IGNORECASE)

        extensions = file_extensions or [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs"]

        for path in self.project_root.rglob("*"):
            if self._should_ignore(path) or not path.is_file():
                continue

            if file_extensions and path.suffix not in extensions:
                continue

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if compiled_pattern.search(line):
                            rel_path = path.relative_to(self.project_root)
                            matches.append(
                                {
                                    "file": str(rel_path),
                                    "line": line_num,
                                    "content": line.strip(),
                                }
                            )
            except Exception as e:
                logger.debug("search_error", file=str(path), error=str(e))

        return matches
