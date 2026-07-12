# ─────────────────────────────────────────────
# Gubluu — Development Setup Script
# ─────────────────────────────────────────────
# Run this script once to set up your development environment.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "  Gubluu Development Setup" -ForegroundColor Cyan
Write-Host "  ========================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "[1/5] Python: $pythonVersion" -ForegroundColor Green

$versionMatch = $pythonVersion -match "3\.(\d+)"
if ($versionMatch) {
    $minor = [int]$Matches[1]
    if ($minor -lt 12) {
        Write-Host "  ERROR: Python 3.12+ required. Found $pythonVersion" -ForegroundColor Red
        exit 1
    }
}

# Check for uv
$uvAvailable = Get-Command uv -ErrorAction SilentlyContinue
if ($uvAvailable) {
    Write-Host "[2/5] Using uv package manager" -ForegroundColor Green

    # Create virtual environment
    Write-Host "[3/5] Creating virtual environment..." -ForegroundColor Yellow
    uv venv

    # Install dependencies
    Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
    uv pip install -e ".[dev]"
} else {
    Write-Host "[2/5] uv not found, using pip" -ForegroundColor Yellow

    # Create virtual environment
    Write-Host "[3/5] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv

    # Activate and install
    Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
    pip install -e ".[dev]"
}

# Create data directories
Write-Host "[5/5] Creating data directories..." -ForegroundColor Yellow
$dirs = @("data\db", "data\vectors", "data\cache", "data\logs", "data\models")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host ""
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Activate your environment:" -ForegroundColor Cyan
Write-Host "    .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  Verify installation:" -ForegroundColor Cyan
Write-Host "    python -m gubluu --version" -ForegroundColor White
Write-Host "    pytest" -ForegroundColor White
Write-Host ""
