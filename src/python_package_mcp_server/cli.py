"""CLI entry point for MCP server."""

import asyncio
import sys
from pathlib import Path

import click

from .config import config
from .server import run_stdio
from .transports.http import run_http_server


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Python Package Manager MCP Server CLI."""
    pass


@cli.command()
def stdio():
    """Run server via stdio transport (for local development)."""
    click.echo("Starting MCP server via stdio transport...", err=True)
    try:
        asyncio.run(run_stdio())
    except KeyboardInterrupt:
        click.echo("\nShutting down...", err=True)
        sys.exit(0)


@cli.command()
@click.option("--host", default=None, help="HTTP server host")
@click.option("--port", default=None, type=int, help="HTTP server port")
def http(host, port):
    """Run server via HTTP/SSE transport (for enterprise deployments)."""
    if host:
        config.host = host
    if port:
        config.port = port

    click.echo(f"Starting MCP server via HTTP transport on {config.host}:{config.port}...", err=True)
    try:
        asyncio.run(run_http_server())
    except KeyboardInterrupt:
        click.echo("\nShutting down...", err=True)
        sys.exit(0)


@cli.command()
@click.option("--host", default="localhost", help="HTTP server host")
@click.option("--port", default=8000, type=int, help="HTTP server port")
def dev(host, port):
    """Run server in development mode with hot reload."""
    import uvicorn

    config.host = host
    config.port = port

    click.echo(f"Starting MCP server in development mode on {host}:{port}...", err=True)
    click.echo("Hot reload enabled. Press Ctrl+C to stop.", err=True)

    try:
        # Use import string for reload to work properly
        uvicorn.run(
            "python_package_mcp_server.transports.http:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=["src"],
        )
    except KeyboardInterrupt:
        click.echo("\nShutting down...", err=True)
        sys.exit(0)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
