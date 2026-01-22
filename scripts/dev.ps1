# PowerShell script for Windows
# Development mode script with hot reload

param(
    [Parameter()]
    [Alias("host")]
    [string]$HostName = "",
    
    [Parameter()]
    [int]$Port = 0
)

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Set default values from environment variables or defaults
if ([string]::IsNullOrEmpty($HostName)) {
    $HostName = if ($env:MCP_HOST) { $env:MCP_HOST } else { "localhost" }
}

if ($Port -eq 0) {
    $Port = if ($env:MCP_PORT) { [int]$env:MCP_PORT } else { 8000 }
}

# Check if uv is available
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCommand) {
    Write-Host "Error: uv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install uv: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists, create if not
$venvPath = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    Set-Location $ProjectRoot
    uv venv
}

# Determine Python executable to use
$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (Test-Path $venvPython) {
    $PythonExe = $venvPython
    Write-Host "Using Python from virtual environment: $PythonExe" -ForegroundColor Green
} else {
    # Fallback to system Python
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCommand) {
        Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
        exit 1
    }
    $PythonExe = "python"
    Write-Host "Using system Python: $($pythonCommand.Source)" -ForegroundColor Yellow
}

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Set-Location $ProjectRoot
uv pip install -e ".[dev]"

# Run tests if requested
if ($env:RUN_TESTS -eq "true") {
    Write-Host "Running tests..." -ForegroundColor Yellow
    uv pip install pytest pytest-asyncio
    pytest tests/ 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Tests completed with some failures (continuing anyway)" -ForegroundColor Yellow
    }
}

# Run the server in development mode
Write-Host ""
Write-Host "Starting MCP server in development mode on ${HostName}:${Port}..." -ForegroundColor Green
Write-Host "Hot reload enabled. Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

try {
    & $PythonExe -m python_package_mcp_server.cli dev --host $HostName --port $Port
} catch {
    Write-Host "Error running server: $_" -ForegroundColor Red
    exit 1
}
