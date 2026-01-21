"""Configuration management for MCP server."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file if present
load_dotenv()


class ServerConfig(BaseModel):
    """Server configuration."""

    # Transport settings
    transport: str = Field(default="stdio", description="Transport type: stdio or http")
    host: str = Field(default="localhost", description="HTTP server host")
    port: int = Field(default=8000, description="HTTP server port")

    # Security settings
    api_key: Optional[str] = Field(default=None, description="API key for HTTP transport")
    enable_auth: bool = Field(default=False, description="Enable authentication")
    
    # User authentication settings
    enable_user_auth: bool = Field(default=False, description="Enable user-based authentication")
    users_file: Optional[Path] = Field(default=None, description="Path to users JSON file")
    single_api_key_mode: bool = Field(default=True, description="Use legacy single API key mode")

    # Policy settings
    allowed_packages: list[str] = Field(default_factory=list, description="Allowed package patterns")
    blocked_packages: list[str] = Field(default_factory=list, description="Blocked package patterns")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")

    # Project settings
    project_root: Optional[Path] = Field(default=None, description="Project root directory")
    workspace_root: Optional[Path] = Field(default=None, description="Workspace root directory")

    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Create configuration from environment variables."""
        return cls(
            transport=os.getenv("MCP_TRANSPORT", "stdio"),
            host=os.getenv("MCP_HOST", "localhost"),
            port=int(os.getenv("MCP_PORT", "8000")),
            api_key=os.getenv("MCP_API_KEY"),
            enable_auth=os.getenv("MCP_ENABLE_AUTH", "false").lower() == "true",
            allowed_packages=os.getenv("MCP_ALLOWED_PACKAGES", "").split(",")
            if os.getenv("MCP_ALLOWED_PACKAGES")
            else [],
            blocked_packages=os.getenv("MCP_BLOCKED_PACKAGES", "").split(",")
            if os.getenv("MCP_BLOCKED_PACKAGES")
            else [],
            log_level=os.getenv("MCP_LOG_LEVEL", "INFO"),
            log_format=os.getenv("MCP_LOG_FORMAT", "json"),
            project_root=Path(os.getenv("MCP_PROJECT_ROOT", ".")).resolve()
            if os.getenv("MCP_PROJECT_ROOT")
            else None,
            workspace_root=Path(os.getenv("MCP_WORKSPACE_ROOT", ".")).resolve()
            if os.getenv("MCP_WORKSPACE_ROOT")
            else None,
            enable_user_auth=os.getenv("MCP_ENABLE_USER_AUTH", "false").lower() == "true",
            users_file=Path(os.getenv("MCP_USERS_FILE", "~/.mcp_server/users.json")).expanduser().resolve()
            if os.getenv("MCP_USERS_FILE")
            else Path.home() / ".mcp_server" / "users.json",
            single_api_key_mode=os.getenv("MCP_SINGLE_API_KEY_MODE", "true").lower() == "true",
        )


# Global configuration instance
config = ServerConfig.from_env()
