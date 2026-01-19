#!/bin/bash
# Run MCP server via HTTP transport (Linux/macOS)

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
HOST="${MCP_HOST:-localhost}"
PORT="${MCP_PORT:-8000}"
BACKGROUND="${MCP_BACKGROUND:-false}"

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
        --background|-b)
            BACKGROUND="true"
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Usage: $0 [--host HOST] [--port PORT] [--background]" >&2
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
uv pip install -e .

# Run the server
if [ "$BACKGROUND" = "true" ]; then
    echo "Starting MCP server via HTTP on $HOST:$PORT in background..." >&2
    nohup python -m python_package_mcp_server.cli http --host "$HOST" --port "$PORT" > "$PROJECT_ROOT/mcp_server.log" 2>&1 &
    echo "Server started in background. PID: $!" >&2
    echo "Logs: $PROJECT_ROOT/mcp_server.log" >&2
else
    echo "Starting MCP server via HTTP on $HOST:$PORT..." >&2
    exec python -m python_package_mcp_server.cli http --host "$HOST" --port "$PORT"
fi
