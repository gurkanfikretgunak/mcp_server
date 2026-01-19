#!/bin/bash
# Development mode script with hot reload (Linux/macOS)

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
HOST="${MCP_HOST:-localhost}"
PORT="${MCP_PORT:-8000}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: $0 [--host HOST] [--port PORT]" >&2
            exit 1
            ;;
    esac
done

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
uv pip install -e ".[dev]"

# Run tests if requested
if [ "${RUN_TESTS:-false}" = "true" ]; then
    echo "Running tests..." >&2
    uv pip install pytest pytest-asyncio
    pytest tests/ || true
fi

# Run the server in development mode
echo "Starting MCP server in development mode on $HOST:$PORT..." >&2
echo "Hot reload enabled. Press Ctrl+C to stop." >&2
exec python -m python_package_mcp_server.cli dev --host "$HOST" --port "$PORT"
