"""CLI entry point for MCP server."""

import asyncio
import os
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

import click

from .config import config
from .server import run_stdio
from .transports.http import run_http_server
from .security.user_manager import UserManager


def print_header(title: str):
    """Print a formatted header."""
    click.echo(click.style(f"\n{'=' * 60}", fg="cyan", bold=True))
    click.echo(click.style(f"  {title}", fg="cyan", bold=True))
    click.echo(click.style(f"{'=' * 60}\n", fg="cyan", bold=True))


def print_section(title: str):
    """Print a formatted section title."""
    click.echo(click.style(f"\n{title}", fg="yellow", bold=True))
    click.echo(click.style("-" * len(title), fg="yellow"))


def print_info(label: str, value: str, indent: int = 2):
    """Print formatted info line."""
    spaces = " " * indent
    click.echo(f"{spaces}{click.style(label + ':', fg='blue', bold=True)} {value}")


def print_success(message: str):
    """Print success message."""
    click.echo(click.style(f"✓ {message}", fg="green", bold=True))


def print_warning(message: str):
    """Print warning message."""
    click.echo(click.style(f"⚠️  {message}", fg="yellow", bold=True))


def print_error(message: str):
    """Print error message."""
    click.echo(click.style(f"✗ {message}", fg="red", bold=True))


def launch_inspector(transport: str = "stdio", host: str = "localhost", port: int = 8000):
    """Launch MCP Inspector in a subprocess.
    
    Args:
        transport: Transport type (stdio or http)
        host: HTTP server host (for http transport)
        port: HTTP server port (for http transport)
    """
    try:
        script_dir = Path(__file__).parent.parent.parent / "scripts"
        
        if sys.platform == "win32":
            script_path = script_dir / "inspect.ps1"
            if transport == "http":
                cmd = [
                    "powershell",
                    "-ExecutionPolicy", "Bypass",
                    "-File", str(script_path),
                    "-Transport", "http",
                    "-ServerHost", host,
                    "-Port", str(port)
                ]
            else:
                cmd = [
                    "powershell",
                    "-ExecutionPolicy", "Bypass",
                    "-File", str(script_path),
                    "-Transport", "stdio"
                ]
        else:
            script_path = script_dir / "inspect.sh"
            if not script_path.exists():
                print_error("Inspector script not found")
                return False
            
            if transport == "http":
                cmd = ["bash", str(script_path), "--transport", "http", "--host", host, "--port", str(port)]
            else:
                cmd = ["bash", str(script_path)]
        
        print_section("Launching MCP Inspector")
        print_info("Status", "Starting inspector in new process...")
        print_info("Transport", transport)
        if transport == "http":
            print_info("URL", f"http://{host}:{port}")
        print_info("UI", "http://localhost:5173")
        click.echo()
        
        # Launch in background
        subprocess.Popen(cmd, cwd=script_dir.parent)
        print_success("Inspector launched successfully")
        print_info("Browser", "Inspector UI should open automatically")
        print_info("Action", "Press Ctrl+C in inspector window to stop")
        return True
        
    except Exception as e:
        print_error(f"Failed to launch inspector: {str(e)}")
        print_info("Manual", "Run: ./scripts/inspect.sh")
        return False


def show_inspector_instructions(transport: str = "stdio", host: str = "localhost", port: int = 8000):
    """Show instructions for launching the inspector.
    
    Args:
        transport: Transport type
        host: HTTP server host
        port: HTTP server port
    """
    print_section("MCP Inspector")
    print_info("Quick Launch", "Open a new terminal and run:")
    if transport == "http":
        click.echo(click.style(f"  python -m python_package_mcp_server.cli inspector --transport http --host {host} --port {port}", fg="cyan"))
    else:
        click.echo(click.style("  python -m python_package_mcp_server.cli inspector", fg="cyan"))
    print_info("Or", "Run: ./scripts/inspect.sh")
    print_info("URL", "http://localhost:5173 (will open automatically)")


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Python Package Manager MCP Server CLI.
    
    A production-ready MCP server for managing Python packages using uv.
    Supports both stdio (local) and HTTP/SSE (enterprise) transports.
    """
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--interactive", "-i", is_flag=True, help="Enable interactive mode (press 'i' to launch inspector)")
def stdio(verbose, interactive):
    """Run server via stdio transport (for local development).
    
    This is the recommended transport for local development and IDE integration.
    The server communicates via standard input/output (stdio).
    
    Examples:
    
        # Basic usage
        python -m python_package_mcp_server.cli stdio
        
        # With verbose output
        python -m python_package_mcp_server.cli stdio --verbose
        
        # With interactive mode (press 'i' to launch inspector)
        python -m python_package_mcp_server.cli stdio --interactive
    """
    print_header("MCP Server - Stdio Transport")
    
    print_section("Configuration")
    print_info("Transport", "stdio")
    print_info("Project Root", str(config.project_root or Path.cwd()))
    print_info("Log Level", config.log_level)
    print_info("Log Format", config.log_format)
    
    if config.enable_auth:
        print_info("Authentication", "Enabled")
        if config.enable_user_auth:
            print_info("Auth Mode", "User-based")
            print_info("Users File", str(config.users_file))
        else:
            print_info("Auth Mode", "Single API Key")
    else:
        print_info("Authentication", "Disabled")
    
    if verbose:
        print_section("Environment Variables")
        env_vars = [
            "MCP_PROJECT_ROOT",
            "MCP_LOG_LEVEL",
            "MCP_LOG_FORMAT",
            "MCP_ENABLE_AUTH",
            "MCP_ENABLE_USER_AUTH",
            "MCP_API_KEY",
        ]
        for var in env_vars:
            value = os.getenv(var, "Not set")
            if var == "MCP_API_KEY" and value != "Not set":
                value = "***REDACTED***"
            print_info(var, value)
    
    print_section("Starting Server")
    print_success("Server starting...")
    print_info("Status", "Ready to accept connections")
    
    if interactive:
        print_section("Interactive Mode")
        print_success("Interactive mode enabled")
        show_inspector_instructions("stdio")
        print_warning("Note: Launch inspector in a separate terminal while server is running")
    else:
        print_warning("Press Ctrl+C to stop the server")
        show_inspector_instructions("stdio")
    
    click.echo()
    
    try:
        asyncio.run(run_stdio())
    except KeyboardInterrupt:
        click.echo()
        print_section("Shutting Down")
        print_success("Server stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print_error(f"Server error: {str(e)}")
        if verbose:
            import traceback
            click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--host", default=None, help="HTTP server host (default: localhost)")
@click.option("--port", default=None, type=int, help="HTTP server port (default: 8000)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--interactive", "-i", is_flag=True, help="Enable interactive mode (press 'i' to launch inspector)")
def http(host, port, verbose, interactive):
    """Run server via HTTP/SSE transport (for enterprise deployments).
    
    This transport is recommended for remote deployments and multi-client scenarios.
    The server exposes HTTP endpoints with Server-Sent Events (SSE) support.
    
    Examples:
    
        # Basic usage (localhost:8000)
        python -m python_package_mcp_server.cli http
        
        # Custom host and port
        python -m python_package_mcp_server.cli http --host 0.0.0.0 --port 8080
        
        # With verbose output
        python -m python_package_mcp_server.cli http --verbose
    """
    if host:
        config.host = host
    if port:
        config.port = port

    print_header("MCP Server - HTTP Transport")
    
    print_section("Configuration")
    print_info("Transport", "HTTP/SSE")
    print_info("Host", config.host)
    print_info("Port", str(config.port))
    print_info("URL", f"http://{config.host}:{config.port}")
    print_info("Project Root", str(config.project_root or Path.cwd()))
    print_info("Log Level", config.log_level)
    print_info("Log Format", config.log_format)
    
    if config.enable_auth:
        print_info("Authentication", "Enabled")
        if config.enable_user_auth:
            print_info("Auth Mode", "User-based")
            print_info("Users File", str(config.users_file))
        else:
            print_info("Auth Mode", "Single API Key")
        print_warning("API key required in request headers (X-API-Key or Authorization)")
    else:
        print_info("Authentication", "Disabled")
        print_warning("Authentication is disabled - not recommended for production!")
    
    print_section("Endpoints")
    print_info("Health Check", f"GET http://{config.host}:{config.port}/health")
    print_info("SSE Messages", f"GET http://{config.host}:{config.port}/messages")
    
    if verbose:
        print_section("Environment Variables")
        env_vars = [
            "MCP_HOST",
            "MCP_PORT",
            "MCP_PROJECT_ROOT",
            "MCP_LOG_LEVEL",
            "MCP_LOG_FORMAT",
            "MCP_ENABLE_AUTH",
            "MCP_ENABLE_USER_AUTH",
            "MCP_API_KEY",
        ]
        for var in env_vars:
            value = os.getenv(var, "Not set")
            if var == "MCP_API_KEY" and value != "Not set":
                value = "***REDACTED***"
            print_info(var, value)
    
    print_section("Starting Server")
    print_success(f"Server starting on http://{config.host}:{config.port}")
    print_info("Status", "Ready to accept connections")
    
    if interactive:
        print_section("Interactive Mode")
        print_success("Interactive mode enabled")
        show_inspector_instructions("http", config.host, config.port)
        print_warning("Note: Launch inspector in a separate terminal while server is running")
    else:
        print_warning("Press Ctrl+C to stop the server")
        show_inspector_instructions("http", config.host, config.port)
    
    click.echo()
    
    try:
        asyncio.run(run_http_server())
    except KeyboardInterrupt:
        click.echo()
        print_section("Shutting Down")
        print_success("Server stopped gracefully")
        sys.exit(0)
    except Exception as e:
        print_error(f"Server error: {str(e)}")
        if verbose:
            import traceback
            click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--host", default="localhost", help="HTTP server host (default: localhost)")
@click.option("--port", default=8000, type=int, help="HTTP server port (default: 8000)")
@click.option("--reload-dirs", default="src", help="Directories to watch for changes (default: src)")
def dev(host, port, reload_dirs):
    """Run server in development mode with hot reload.
    
    This mode automatically reloads the server when code changes are detected.
    Perfect for development and testing.
    
    Examples:
    
        # Basic usage
        python -m python_package_mcp_server.cli dev
        
        # Custom port
        python -m python_package_mcp_server.cli dev --port 9000
        
        # Watch multiple directories
        python -m python_package_mcp_server.cli dev --reload-dirs "src,tests"
    """
    import uvicorn

    config.host = host
    config.port = port

    print_header("MCP Server - Development Mode")
    
    print_section("Configuration")
    print_info("Mode", "Development (Hot Reload Enabled)")
    print_info("Host", host)
    print_info("Port", str(port))
    print_info("URL", f"http://{host}:{port}")
    print_info("Watch Directories", reload_dirs)
    print_info("Auto Reload", "Enabled")
    
    print_section("Features")
    print_success("Code changes will automatically reload the server")
    print_info("Status", "Ready for development")
    print_warning("Press Ctrl+C to stop the server")
    click.echo()

    try:
        # Use import string for reload to work properly
        uvicorn.run(
            "python_package_mcp_server.transports.http:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=reload_dirs.split(","),
        )
    except KeyboardInterrupt:
        click.echo()
        print_section("Shutting Down")
        print_success("Development server stopped")
        sys.exit(0)
    except Exception as e:
        print_error(f"Server error: {str(e)}")
        import traceback
        click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--username", default="admin", help="Username for the admin account (default: admin)")
@click.option("--api-key", default=None, help="API key for the admin account (auto-generated if not provided)")
@click.option("--users-file", default=None, help="Path to users file (uses config default if not provided)")
@click.option("--show-example", is_flag=True, help="Show example configuration after creation")
def create_admin(username, api_key, users_file, show_example):
    """Create the first admin account.
    
    This command creates the initial admin account for user-based authentication.
    Only the first account can be created via CLI - subsequent accounts must be
    created by admin users using the create_user MCP tool.
    
    Examples:
    
        # Create admin with auto-generated API key
        python -m python_package_mcp_server.cli create-admin
        
        # Create admin with custom username and API key
        python -m python_package_mcp_server.cli create-admin --username admin --api-key my-secure-key
        
        # Create admin and show configuration example
        python -m python_package_mcp_server.cli create-admin --show-example
    """
    print_header("Create Admin Account")
    
    try:
        # Use provided users file or config default
        if users_file:
            users_file_path = Path(users_file).expanduser().resolve()
        else:
            users_file_path = config.users_file

        print_section("Configuration")
        print_info("Username", username)
        print_info("Role", "admin (level 1)")
        print_info("Users File", str(users_file_path))
        if api_key:
            print_info("API Key", "Custom (provided)")
        else:
            print_info("API Key", "Auto-generated")
        
        print_section("Creating Account")
        print_info("Status", "Initializing user manager...")
        
        user_manager = UserManager(users_file_path)
        
        # Check if users already exist
        existing_users = user_manager.list_users()
        if existing_users:
            print_error("Users already exist!")
            print_info("Count", str(len(existing_users)))
            print_warning("Cannot create first admin when users already exist.")
            print_info("Action", "Use the 'create_user' MCP tool instead (admin only)")
            sys.exit(1)
        
        print_info("Status", "Creating admin account...")
        user, plain_api_key = user_manager.create_first_admin(username, api_key)
        
        print_section("Account Created Successfully")
        print_success(f"Admin account '{user.username}' created")
        print_info("Username", user.username)
        print_info("Role", user.role)
        print_info("Created At", user.created_at)
        print_info("API Key", plain_api_key)
        print_info("Users File", str(users_file_path))
        
        print_section("Security Information")
        print_warning("IMPORTANT: Save this API key securely!")
        print_info("Storage", "API keys are stored as SHA-256 hashes")
        print_info("File Permissions", "Users file has restrictive permissions (chmod 600)")
        print_info("Next Steps", "Use this API key to authenticate with the server")
        
        print_section("Next Steps")
        print_info("1", "Enable user authentication:")
        print_info("", f"  export MCP_ENABLE_USER_AUTH=true")
        print_info("2", "Set the API key in your environment:")
        print_info("", f"  export MCP_API_KEY={plain_api_key}")
        print_info("3", "Start the server:")
        print_info("", "  python -m python_package_mcp_server.cli stdio")
        print_info("4", "Create additional users using the 'create_user' MCP tool")
        
        if show_example:
            print_section("Example Configuration")
            click.echo("Add this to your mcp.json:")
            click.echo()
            example_config = f'''{{
  "mcpServers": {{
    "python-package-manager": {{
      "command": "python",
      "args": ["-m", "python_package_mcp_server.cli", "stdio"],
      "env": {{
        "MCP_PROJECT_ROOT": ".",
        "MCP_ENABLE_USER_AUTH": "true",
        "MCP_USERS_FILE": "{users_file_path}",
        "MCP_API_KEY": "{plain_api_key}",
        "MCP_LOG_LEVEL": "INFO",
        "MCP_LOG_FORMAT": "json"
      }}
    }}
  }}
}}'''
            click.echo(click.style(example_config, fg="cyan"))
            click.echo()
        
        print_section("Important Notes")
        print_warning("This API key will NOT be shown again")
        print_info("Backup", "Save it in a secure password manager")
        print_info("Permissions", "Admin users have full access to all operations")
        print_info("User Creation", "Only admin users can create new accounts")
        
    except ValueError as e:
        print_section("Error")
        print_error(str(e))
        print_info("Help", "Run with --help for usage information")
        sys.exit(1)
    except Exception as e:
        print_section("Unexpected Error")
        print_error(str(e))
        import traceback
        click.echo()
        click.echo(click.style("Traceback:", fg="red"))
        click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--users-file", default=None, help="Path to users file (uses config default if not provided)")
def list_users(users_file):
    """List all users in the system.
    
    Shows all registered users with their roles and creation dates.
    Requires user authentication to be enabled.
    
    Examples:
    
        # List users from default location
        python -m python_package_mcp_server.cli list-users
        
        # List users from custom file
        python -m python_package_mcp_server.cli list-users --users-file /path/to/users.json
    """
    print_header("List Users")
    
    try:
        if users_file:
            users_file_path = Path(users_file).expanduser().resolve()
        else:
            users_file_path = config.users_file
        
        print_section("Configuration")
        print_info("Users File", str(users_file_path))
        
        if not users_file_path.exists():
            print_warning("Users file does not exist")
            print_info("Action", "Create an admin account first:")
            print_info("", "python -m python_package_mcp_server.cli create-admin")
            sys.exit(1)
        
        print_section("Loading Users")
        user_manager = UserManager(users_file_path)
        users = user_manager.list_users()
        
        if not users:
            print_section("No Users Found")
            print_warning("No users found in the system")
            print_info("Action", "Create an admin account:")
            print_info("", "python -m python_package_mcp_server.cli create-admin")
            sys.exit(0)
        
        print_section(f"Users ({len(users)})")
        
        admin_count = sum(1 for u in users if u.role == "admin")
        user_count = len(users) - admin_count
        
        print_info("Total Users", str(len(users)))
        print_info("Admins", str(admin_count))
        print_info("Regular Users", str(user_count))
        click.echo()
        
        for i, user in enumerate(users, 1):
            role_color = "red" if user.role == "admin" else "blue"
            click.echo(click.style(f"  {i}. {user.username}", fg="cyan", bold=True))
            print_info("    Role", click.style(user.role, fg=role_color, bold=True))
            print_info("    Created", user.created_at)
            click.echo()
        
        print_section("Summary")
        if admin_count > 0:
            print_success(f"{admin_count} admin user(s) with full access")
        if user_count > 0:
            print_info(f"{user_count} regular user(s) with read-only access")
        
    except Exception as e:
        print_section("Error")
        print_error(str(e))
        import traceback
        click.echo()
        click.echo(click.style("Traceback:", fg="red"))
        click.echo(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "http"]), help="Transport type for inspector")
@click.option("--host", default="localhost", help="HTTP server host (for http transport)")
@click.option("--port", default=8000, type=int, help="HTTP server port (for http transport)")
def inspector(transport, host, port):
    """Launch MCP Inspector for testing and debugging.
    
    This command launches the MCP Inspector UI in your browser, allowing you to
    test resources, tools, and prompts interactively.
    
    Examples:
    
        # Launch inspector with stdio transport
        python -m python_package_mcp_server.cli inspector
        
        # Launch inspector connected to HTTP server
        python -m python_package_mcp_server.cli inspector --transport http --host localhost --port 8000
    """
    print_header("MCP Inspector Launcher")
    
    print_section("Configuration")
    print_info("Transport", transport)
    if transport == "http":
        print_info("Server URL", f"http://{host}:{port}")
        print_warning("Make sure the HTTP server is running first!")
        print_info("Start Server", f"python -m python_package_mcp_server.cli http --host {host} --port {port}")
    else:
        print_info("Mode", "Stdio (will start server automatically)")
    
    print_section("Launching Inspector")
    success = launch_inspector(transport, host, port)
    
    if success:
        print_section("Inspector Running")
        print_success("Inspector should open in your browser")
        print_info("URL", "http://localhost:5173")
        print_info("Status", "Ready for testing")
        print_warning("Press Ctrl+C in the inspector window to stop")
    else:
        print_section("Manual Launch")
        print_info("Command", "./scripts/inspect.sh" if transport == "stdio" else f"./scripts/inspect.sh --transport http --host {host} --port {port}")


@cli.command()
def status():
    """Show server status and configuration.
    
    Displays current server configuration, authentication status,
    and system information.
    
    Examples:
    
        # Show server status
        python -m python_package_mcp_server.cli status
    """
    print_header("MCP Server Status")
    
    print_section("Server Information")
    print_info("Version", "0.1.0")
    print_info("Python", f"{sys.version.split()[0]}")
    print_info("Project Root", str(config.project_root or Path.cwd()))
    
    print_section("Transport Configuration")
    print_info("Default Transport", config.transport)
    print_info("HTTP Host", config.host)
    print_info("HTTP Port", str(config.port))
    
    print_section("Authentication")
    if config.enable_auth:
        print_success("Authentication: Enabled")
        if config.enable_user_auth:
            print_info("Mode", "User-based authentication")
            print_info("Users File", str(config.users_file))
            if config.users_file.exists():
                try:
                    user_manager = UserManager(config.users_file)
                    users = user_manager.list_users()
                    admin_count = sum(1 for u in users if u.role == "admin")
                    user_count = len(users) - admin_count
                    print_info("Total Users", str(len(users)))
                    print_info("Admins", str(admin_count))
                    print_info("Regular Users", str(user_count))
                except Exception:
                    print_warning("Could not read users file")
            else:
                print_warning("Users file does not exist")
                print_info("Action", "Create admin: python -m python_package_mcp_server.cli create-admin")
        else:
            print_info("Mode", "Single API Key (Legacy)")
            if config.api_key:
                print_info("API Key", "***CONFIGURED***")
            else:
                print_warning("API key not configured")
    else:
        print_warning("Authentication: Disabled")
        print_info("Recommendation", "Enable authentication for production use")
    
    print_section("Policy Configuration")
    if config.allowed_packages:
        print_info("Allowed Packages", ", ".join(config.allowed_packages))
    else:
        print_info("Allowed Packages", "None (all allowed)")
    
    if config.blocked_packages:
        print_info("Blocked Packages", ", ".join(config.blocked_packages))
    else:
        print_info("Blocked Packages", "None")
    
    print_section("Logging")
    print_info("Log Level", config.log_level)
    print_info("Log Format", config.log_format)
    
    print_section("System Information")
    print_info("Current Directory", str(Path.cwd()))
    print_info("Users File", str(config.users_file))
    print_info("Users File Exists", "Yes" if config.users_file.exists() else "No")
    
    if config.users_file.exists():
        try:
            stat = config.users_file.stat()
            print_info("File Size", f"{stat.st_size} bytes")
            print_info("Modified", datetime.fromtimestamp(stat.st_mtime).isoformat())
            # Check permissions
            mode = oct(stat.st_mode)[-3:]
            print_info("Permissions", mode)
        except Exception:
            pass


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
