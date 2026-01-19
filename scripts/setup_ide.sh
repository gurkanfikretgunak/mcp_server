#!/bin/bash
# Setup MCP server configuration for various IDEs
# Supports: Cursor, VS Code, and other MCP-compatible IDEs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SERVER_NAME="python-package-manager"
SERVER_COMMAND="python"
SERVER_ARGS="-m python_package_mcp_server.cli stdio"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}MCP Server IDE Setup Script${NC}"
echo "=================================="
echo ""

# Detect Python path
detect_python() {
    if [ -d "$PROJECT_ROOT/.venv" ]; then
        echo "$PROJECT_ROOT/.venv/bin/python"
    elif command -v python3 &> /dev/null; then
        which python3
    elif command -v python &> /dev/null; then
        which python
    else
        echo "python"
    fi
}

PYTHON_PATH=$(detect_python)
echo -e "${GREEN}Detected Python:${NC} $PYTHON_PATH"
echo ""

# Function to setup Cursor IDE
setup_cursor() {
    echo -e "${BLUE}Setting up Cursor IDE...${NC}"
    
    CURSOR_CONFIG_DIR="$HOME/.cursor"
    CURSOR_MCP_CONFIG="$CURSOR_CONFIG_DIR/mcp.json"
    
    # Create config directory if it doesn't exist
    mkdir -p "$CURSOR_CONFIG_DIR"
    
    # Check if config exists
    if [ -f "$CURSOR_MCP_CONFIG" ]; then
        echo "Cursor MCP config exists. Checking if server is already configured..."
        
        if grep -q "\"$SERVER_NAME\"" "$CURSOR_MCP_CONFIG" 2>/dev/null; then
            echo -e "${YELLOW}Server '$SERVER_NAME' already configured in Cursor.${NC}"
            read -p "Update existing configuration? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                return
            fi
        fi
    fi
    
    # Create or update config
    if [ ! -f "$CURSOR_MCP_CONFIG" ]; then
        echo "Creating new Cursor MCP configuration..."
        cat > "$CURSOR_MCP_CONFIG" << EOF
{
  "mcpServers": {
    "$SERVER_NAME": {
      "command": "$PYTHON_PATH",
      "args": [
        "-m",
        "python_package_mcp_server.cli",
        "stdio"
      ],
      "env": {
        "MCP_PROJECT_ROOT": "$PROJECT_ROOT",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
EOF
    else
        echo "Updating existing Cursor MCP configuration..."
        # Use jq if available, otherwise provide manual instructions
        if command -v jq &> /dev/null; then
            jq ".mcpServers[\"$SERVER_NAME\"] = {
                \"command\": \"$PYTHON_PATH\",
                \"args\": [\"-m\", \"python_package_mcp_server.cli\", \"stdio\"],
                \"env\": {
                    \"MCP_PROJECT_ROOT\": \"$PROJECT_ROOT\",
                    \"MCP_LOG_LEVEL\": \"INFO\",
                    \"MCP_LOG_FORMAT\": \"json\"
                }
            }" "$CURSOR_MCP_CONFIG" > "$CURSOR_MCP_CONFIG.tmp" && mv "$CURSOR_MCP_CONFIG.tmp" "$CURSOR_MCP_CONFIG"
        else
            echo -e "${YELLOW}jq not found. Please manually add the server configuration to:${NC}"
            echo "$CURSOR_MCP_CONFIG"
            echo ""
            echo "Add this to mcpServers:"
            cat << EOF
    "$SERVER_NAME": {
      "command": "$PYTHON_PATH",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "$PROJECT_ROOT",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
EOF
        fi
    fi
    
    echo -e "${GREEN}✓ Cursor IDE configured!${NC}"
    echo "  Config location: $CURSOR_MCP_CONFIG"
    echo "  Restart Cursor to apply changes."
    echo ""
}

# Function to setup VS Code
setup_vscode() {
    echo -e "${BLUE}Setting up VS Code...${NC}"
    
    VSCODE_CONFIG_DIR="$PROJECT_ROOT/.vscode"
    VSCODE_SETTINGS="$VSCODE_CONFIG_DIR/settings.json"
    
    mkdir -p "$VSCODE_CONFIG_DIR"
    
    # Check if settings.json exists
    if [ -f "$VSCODE_SETTINGS" ]; then
        echo "VS Code settings.json exists."
    else
        echo "Creating VS Code settings.json..."
        cat > "$VSCODE_SETTINGS" << EOF
{
  "python.defaultInterpreterPath": "$PROJECT_ROOT/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic"
}
EOF
    fi
    
    echo -e "${GREEN}✓ VS Code workspace configured!${NC}"
    echo "  Note: VS Code MCP integration requires the MCP extension."
    echo "  Install: https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.mcp"
    echo ""
}

# Function to generate deep link
generate_deeplink() {
    IDE=$1
    CONFIG_DATA=$(cat << EOF
{
  "mcpServers": {
    "$SERVER_NAME": {
      "command": "$PYTHON_PATH",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {
        "MCP_PROJECT_ROOT": "$PROJECT_ROOT",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }
    }
  }
}
EOF
)
    
    # Base64 encode the config
    ENCODED_CONFIG=$(echo "$CONFIG_DATA" | base64 | tr -d '\n')
    
    case $IDE in
        cursor)
            echo "cursor://mcp/add?config=$ENCODED_CONFIG"
            ;;
        *)
            echo "Deep link not available for $IDE"
            ;;
    esac
}

# Function to print manual instructions
print_manual_instructions() {
    echo -e "${BLUE}Manual Configuration Instructions${NC}"
    echo "======================================"
    echo ""
    echo "For any IDE, add this configuration:"
    echo ""
    echo "Server Name: $SERVER_NAME"
    echo "Command: $PYTHON_PATH"
    echo "Args: -m python_package_mcp_server.cli stdio"
    echo ""
    echo "Environment Variables:"
    echo "  MCP_PROJECT_ROOT=$PROJECT_ROOT"
    echo "  MCP_LOG_LEVEL=INFO"
    echo "  MCP_LOG_FORMAT=json"
    echo ""
}

# Main menu
show_menu() {
    echo "Select IDE to configure:"
    echo "1) Cursor IDE"
    echo "2) VS Code"
    echo "3) Generate deep link for Cursor"
    echo "4) Show manual instructions"
    echo "5) Setup all supported IDEs"
    echo "6) Exit"
    echo ""
    read -p "Enter choice [1-6]: " choice
    
    case $choice in
        1)
            setup_cursor
            ;;
        2)
            setup_vscode
            ;;
        3)
            echo ""
            echo -e "${GREEN}Deep Link for Cursor:${NC}"
            echo "$(generate_deeplink cursor)"
            echo ""
            echo "Copy this link and open it in Cursor to add the MCP server."
            echo ""
            ;;
        4)
            print_manual_instructions
            ;;
        5)
            setup_cursor
            setup_vscode
            echo -e "${GREEN}✓ All supported IDEs configured!${NC}"
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Check if running interactively or with arguments
if [ $# -eq 0 ]; then
    show_menu
else
    case $1 in
        cursor)
            setup_cursor
            ;;
        vscode|code)
            setup_vscode
            ;;
        deeplink)
            generate_deeplink "${2:-cursor}"
            ;;
        all)
            setup_cursor
            setup_vscode
            ;;
        *)
            echo "Usage: $0 [cursor|vscode|deeplink|all]"
            echo ""
            echo "Options:"
            echo "  cursor    - Setup Cursor IDE"
            echo "  vscode    - Setup VS Code"
            echo "  deeplink  - Generate deep link for Cursor"
            echo "  all       - Setup all supported IDEs"
            echo ""
            echo "Run without arguments for interactive menu."
            exit 1
            ;;
    esac
fi

echo ""
echo -e "${GREEN}Setup complete!${NC}"
