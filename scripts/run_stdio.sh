#!/bin/bash
# Run MCP server via stdio transport (Linux/macOS)

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed or not in PATH" >&2
    echo "Please install uv: https://github.com/astral-sh/uv" >&2
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Creating virtual environment..." >&2
    cd "$PROJECT_ROOT"
    uv venv
fi

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Install/update dependencies
echo "Installing dependencies..." >&2
cd "$PROJECT_ROOT"
uv pip install -e .

# Run the server
echo "Starting MCP server via stdio..." >&2
exec python -m python_package_mcp_server.cli stdio
