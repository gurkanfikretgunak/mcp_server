# PowerShell script for Windows - Run MCP Inspector for testing and debugging

param(
    [Parameter()]
    [ValidateSet("stdio", "http")]
    [string]$Transport = "stdio",
    
    [Parameter()]
    [string]$ServerHost = "localhost",
    
    [Parameter()]
    [int]$Port = 8000,
    
    [Parameter()]
    [int]$ClientPort = 5173,
    
    [Parameter()]
    [int]$ServerPort = 3000,
    
    [Parameter()]
    [switch]$Help
)

$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "Usage: .\scripts\inspect.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Run MCP Inspector for testing and debugging the MCP server."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Transport TYPE        Transport type: stdio (default) or http"
    Write-Host "  -ServerHost HOST       HTTP server host (default: localhost)"
    Write-Host "  -Port PORT             HTTP server port (default: 8000)"
    Write-Host "  -ClientPort PORT       Inspector UI port (default: 5173)"
    Write-Host "  -ServerPort PORT       MCP proxy port (default: 3000)"
    Write-Host "  -Help                  Show this help message"
    Write-Host ""
    Write-Host "Environment Variables:"
    Write-Host "  MCP_PROJECT_ROOT       Project root directory"
    Write-Host "  MCP_LOG_LEVEL         Logging level (DEBUG, INFO, WARNING, ERROR)"
    Write-Host "  MCP_LOG_FORMAT        Log format (json, text)"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\scripts\inspect.ps1"
    Write-Host "  .\scripts\inspect.ps1 -Transport http"
    Write-Host "  .\scripts\inspect.ps1 -ClientPort 8080"
    exit 0
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Check if Node.js/npx is available
try {
    $null = Get-Command npx -ErrorAction Stop
} catch {
    Write-Host "Error: npx is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "MCP Inspector requires Node.js to run." -ForegroundColor Yellow
    exit 1
}

# Check if uv is available
try {
    $null = Get-Command uv -ErrorAction Stop
} catch {
    Write-Host "Error: uv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install uv: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists, create if not
$VenvPath = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Blue
    Set-Location $ProjectRoot
    uv venv
}

# Activate virtual environment
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
if (Test-Path $VenvPython) {
    $env:VIRTUAL_ENV = $VenvPath
    $env:PATH = "$VenvPath\Scripts;$env:PATH"
}

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Blue
Set-Location $ProjectRoot
uv pip install -e . | Out-Null

# Set up environment variables
if (-not $env:MCP_PROJECT_ROOT) {
    $env:MCP_PROJECT_ROOT = $ProjectRoot
}
if (-not $env:MCP_LOG_LEVEL) {
    $env:MCP_LOG_LEVEL = "INFO"
}
if (-not $env:MCP_LOG_FORMAT) {
    $env:MCP_LOG_FORMAT = "json"
}

# Run inspector based on transport mode
if ($Transport -eq "http") {
    Write-Host "Starting MCP Inspector connected to HTTP server at ${ServerHost}:${Port}..." -ForegroundColor Blue
    Write-Host "Make sure the HTTP server is running first!" -ForegroundColor Yellow
    Write-Host "Run: .\scripts\run_http.sh -Host $ServerHost -Port $Port" -ForegroundColor Yellow
    Write-Host ""
    
    $env:CLIENT_PORT = $ClientPort
    $env:SERVER_PORT = $ServerPort
    
    $AuthHeader = ""
    if ($env:MCP_API_KEY) {
        $AuthHeader = "--header `"Authorization: Bearer $env:MCP_API_KEY`""
    }
    
    npx @modelcontextprotocol/inspector `
        --url "http://${ServerHost}:${Port}/sse" `
        $AuthHeader
} else {
    Write-Host "Starting MCP Inspector with stdio transport..." -ForegroundColor Blue
    Write-Host "Inspector UI will open in your browser at http://localhost:$ClientPort" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
    Write-Host ""
    
    $env:CLIENT_PORT = $ClientPort
    $env:SERVER_PORT = $ServerPort
    
    npx @modelcontextprotocol/inspector `
        -e "MCP_PROJECT_ROOT=$env:MCP_PROJECT_ROOT" `
        -e "MCP_LOG_LEVEL=$env:MCP_LOG_LEVEL" `
        -e "MCP_LOG_FORMAT=$env:MCP_LOG_FORMAT" `
        python -m python_package_mcp_server.cli stdio
}
