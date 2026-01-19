# PowerShell script for Windows IDE setup
# Setup MCP server configuration for various IDEs

param(
    [Parameter(Position=0)]
    [ValidateSet("cursor", "vscode", "deeplink", "all")]
    [string]$IDE = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$ServerName = "python-package-manager"

# Detect Python path
function Get-PythonPath {
    $venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        return $venvPython
    }
    
    $python3 = Get-Command python3 -ErrorAction SilentlyContinue
    if ($python3) {
        return $python3.Source
    }
    
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return $python.Source
    }
    
    return "python"
}

$PythonPath = Get-PythonPath
Write-Host "Detected Python: $PythonPath" -ForegroundColor Green
Write-Host ""

# Setup Cursor IDE
function Setup-Cursor {
    Write-Host "Setting up Cursor IDE..." -ForegroundColor Blue
    
    $CursorConfigDir = Join-Path $env:USERPROFILE ".cursor"
    $CursorMcpConfig = Join-Path $CursorConfigDir "mcp.json"
    
    # Create config directory if it doesn't exist
    if (-not (Test-Path $CursorConfigDir)) {
        New-Item -ItemType Directory -Path $CursorConfigDir | Out-Null
    }
    
    # Check if config exists
    if (Test-Path $CursorMcpConfig) {
        Write-Host "Cursor MCP config exists. Checking if server is already configured..."
        $config = Get-Content $CursorMcpConfig | ConvertFrom-Json
        
        if ($config.mcpServers.PSObject.Properties.Name -contains $ServerName) {
            Write-Host "Server '$ServerName' already configured in Cursor." -ForegroundColor Yellow
            $response = Read-Host "Update existing configuration? (y/n)"
            if ($response -ne "y" -and $response -ne "Y") {
                return
            }
        }
    }
    
    # Create server configuration
    $serverConfig = @{
        command = $PythonPath
        args = @("-m", "python_package_mcp_server.cli", "stdio")
        env = @{
            MCP_PROJECT_ROOT = $ProjectRoot
            MCP_LOG_LEVEL = "INFO"
            MCP_LOG_FORMAT = "json"
        }
    }
    
    # Read or create config
    if (Test-Path $CursorMcpConfig) {
        $config = Get-Content $CursorMcpConfig | ConvertFrom-Json
    } else {
        $config = @{
            mcpServers = @{}
        } | ConvertTo-Json -Depth 10 | ConvertFrom-Json
    }
    
    # Add or update server
    if (-not $config.mcpServers) {
        $config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
    }
    $config.mcpServers | Add-Member -MemberType NoteProperty -Name $ServerName -Value $serverConfig -Force
    
    # Save config
    $config | ConvertTo-Json -Depth 10 | Set-Content $CursorMcpConfig
    
    Write-Host "✓ Cursor IDE configured!" -ForegroundColor Green
    Write-Host "  Config location: $CursorMcpConfig"
    Write-Host "  Restart Cursor to apply changes."
    Write-Host ""
}

# Setup VS Code
function Setup-VSCode {
    Write-Host "Setting up VS Code..." -ForegroundColor Blue
    
    $VSCodeConfigDir = Join-Path $ProjectRoot ".vscode"
    $VSCodeSettings = Join-Path $VSCodeConfigDir "settings.json"
    
    if (-not (Test-Path $VSCodeConfigDir)) {
        New-Item -ItemType Directory -Path $VSCodeConfigDir | Out-Null
    }
    
    $venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
    $settings = @{
        "python.defaultInterpreterPath" = $venvPython
        "python.analysis.typeCheckingMode" = "basic"
    }
    
    if (Test-Path $VSCodeSettings) {
        $existingSettings = Get-Content $VSCodeSettings | ConvertFrom-Json
        foreach ($key in $settings.Keys) {
            $existingSettings | Add-Member -MemberType NoteProperty -Name $key -Value $settings[$key] -Force
        }
        $existingSettings | ConvertTo-Json -Depth 10 | Set-Content $VSCodeSettings
    } else {
        $settings | ConvertTo-Json -Depth 10 | Set-Content $VSCodeSettings
    }
    
    Write-Host "✓ VS Code workspace configured!" -ForegroundColor Green
    Write-Host "  Note: VS Code MCP integration requires the MCP extension."
    Write-Host ""
}

# Generate deep link
function Get-DeepLink {
    param([string]$Ide = "cursor")
    
    $configData = @{
        mcpServers = @{
            $ServerName = @{
                command = $PythonPath
                args = @("-m", "python_package_mcp_server.cli", "stdio")
                env = @{
                    MCP_PROJECT_ROOT = $ProjectRoot
                    MCP_LOG_LEVEL = "INFO"
                    MCP_LOG_FORMAT = "json"
                }
            }
        }
    }
    
    $json = $configData | ConvertTo-Json -Depth 10 -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $encoded = [Convert]::ToBase64String($bytes)
    
    switch ($Ide) {
        "cursor" {
            return "cursor://mcp/add?config=$encoded"
        }
        default {
            return "Deep link not available for $Ide"
        }
    }
}

# Main execution
if ($IDE -eq "") {
    Write-Host "MCP Server IDE Setup Script" -ForegroundColor Blue
    Write-Host "===========================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Select IDE to configure:"
    Write-Host "1) Cursor IDE"
    Write-Host "2) VS Code"
    Write-Host "3) Generate deep link for Cursor"
    Write-Host "4) Setup all supported IDEs"
    Write-Host ""
    
    $choice = Read-Host "Enter choice [1-4]"
    
    switch ($choice) {
        "1" { Setup-Cursor }
        "2" { Setup-VSCode }
        "3" {
            Write-Host ""
            Write-Host "Deep Link for Cursor:" -ForegroundColor Green
            Write-Host (Get-DeepLink)
            Write-Host ""
            Write-Host "Copy this link and open it in Cursor to add the MCP server."
            Write-Host ""
        }
        "4" {
            Setup-Cursor
            Setup-VSCode
            Write-Host "✓ All supported IDEs configured!" -ForegroundColor Green
        }
        default {
            Write-Host "Invalid choice."
            exit 1
        }
    }
} else {
    switch ($IDE) {
        "cursor" { Setup-Cursor }
        "vscode" { Setup-VSCode }
        "deeplink" { Get-DeepLink }
        "all" {
            Setup-Cursor
            Setup-VSCode
            Write-Host "✓ All supported IDEs configured!" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
