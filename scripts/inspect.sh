#!/bin/bash
# Run MCP Inspector for testing and debugging the MCP server (Linux/macOS)

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
TRANSPORT="${MCP_TRANSPORT:-stdio}"
HOST="${MCP_HOST:-localhost}"
PORT="${MCP_PORT:-8000}"
CLIENT_PORT="${CLIENT_PORT:-5173}"
SERVER_PORT="${SERVER_PORT:-3000}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --transport|-t)
            TRANSPORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --client-port)
            CLIENT_PORT="$2"
            shift 2
            ;;
        --server-port)
            SERVER_PORT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Run MCP Inspector for testing and debugging the MCP server."
            echo ""
            echo "Options:"
            echo "  --transport, -t TYPE    Transport type: stdio (default) or http"
            echo "  --host HOST            HTTP server host (default: localhost)"
            echo "  --port PORT            HTTP server port (default: 8000)"
            echo "  --client-port PORT     Inspector UI port (default: 5173)"
            echo "  --server-port PORT     MCP proxy port (default: 3000)"
            echo "  --help, -h             Show this help message"
            echo ""
            echo "Environment Variables:"
            echo "  MCP_PROJECT_ROOT      Project root directory"
            echo "  MCP_LOG_LEVEL         Logging level (DEBUG, INFO, WARNING, ERROR)"
            echo "  MCP_LOG_FORMAT        Log format (json, text)"
            echo "  CLIENT_PORT           Inspector UI port"
            echo "  SERVER_PORT           MCP proxy port"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Run with stdio transport"
            echo "  $0 --transport http                  # Connect to HTTP server"
            echo "  $0 --client-port 8080                # Use custom UI port"
            echo "  MCP_LOG_LEVEL=DEBUG $0               # Run with debug logging"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Check if Node.js/npx is available
if ! command -v npx &> /dev/null; then
    echo "Error: npx is not installed or not in PATH" >&2
    echo "Please install Node.js: https://nodejs.org/" >&2
    echo "MCP Inspector requires Node.js to run." >&2
    exit 1
fi

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
uv pip install -e . > /dev/null 2>&1

# Set up environment variables
export MCP_PROJECT_ROOT="${MCP_PROJECT_ROOT:-$PROJECT_ROOT}"
export MCP_LOG_LEVEL="${MCP_LOG_LEVEL:-INFO}"
export MCP_LOG_FORMAT="${MCP_LOG_FORMAT:-json}"

# Run inspector based on transport mode
if [ "$TRANSPORT" = "http" ]; then
    echo "Starting MCP Inspector connected to HTTP server at $HOST:$PORT..." >&2
    echo "Make sure the HTTP server is running first!" >&2
    echo "Run: ./scripts/run_http.sh --host $HOST --port $PORT" >&2
    echo ""
    
    # Build inspector command for HTTP transport
    CLIENT_PORT=$CLIENT_PORT SERVER_PORT=$SERVER_PORT \
        npx @modelcontextprotocol/inspector \
        --url "http://$HOST:$PORT/sse" \
        --header "Authorization: Bearer ${MCP_API_KEY:-}" \
        2>&1
else
    echo "Starting MCP Inspector with stdio transport..." >&2
    echo "Inspector UI will open in your browser at http://localhost:$CLIENT_PORT" >&2
    echo "Press Ctrl+C to stop." >&2
    echo ""
    
    # Build inspector command for stdio transport
    CLIENT_PORT=$CLIENT_PORT SERVER_PORT=$SERVER_PORT \
        npx @modelcontextprotocol/inspector \
        -e MCP_PROJECT_ROOT="$MCP_PROJECT_ROOT" \
        -e MCP_LOG_LEVEL="$MCP_LOG_LEVEL" \
        -e MCP_LOG_FORMAT="$MCP_LOG_FORMAT" \
        python -m python_package_mcp_server.cli stdio
fi
