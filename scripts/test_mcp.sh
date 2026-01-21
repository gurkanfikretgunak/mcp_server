#!/bin/bash
# Test script to verify MCP server functionality

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Testing MCP Server..." >&2

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed or not in PATH" >&2
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Test 1: Check if CLI module can be imported
echo "Test 1: Checking CLI module import..." >&2
python -c "from python_package_mcp_server.cli import cli; print('✓ CLI module imported successfully')" || {
    echo "✗ Failed to import CLI module" >&2
    exit 1
}

# Test 2: Check if server module can be imported
echo "Test 2: Checking server module import..." >&2
python -c "from python_package_mcp_server.server import server; print('✓ Server module imported successfully')" || {
    echo "✗ Failed to import server module" >&2
    exit 1
}

# Test 3: Check if HTTP transport can be imported
echo "Test 3: Checking HTTP transport import..." >&2
python -c "from python_package_mcp_server.transports.http import app; print('✓ HTTP transport imported successfully')" || {
    echo "✗ Failed to import HTTP transport" >&2
    exit 1
}

# Test 4: Check if CLI commands are available
echo "Test 4: Checking CLI commands..." >&2
python -m python_package_mcp_server.cli --help > /dev/null || {
    echo "✗ CLI help command failed" >&2
    exit 1
}
echo "✓ CLI commands available" >&2

# Test 5: Test health endpoint
echo "Test 5: Testing HTTP server health endpoint..." >&2
# Start server in background for a quick test
python -m python_package_mcp_server.cli dev --host localhost --port 8001 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 3

# Try to hit health endpoint
if curl -s http://localhost:8001/health 2>/dev/null | grep -q "ok"; then
    echo "✓ Health endpoint responded correctly" >&2
else
    echo "✗ Health endpoint test failed" >&2
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi

# Cleanup
kill $SERVER_PID 2>/dev/null || true
wait $SERVER_PID 2>/dev/null || true
sleep 1

echo "" >&2
echo "All tests passed! ✓" >&2
