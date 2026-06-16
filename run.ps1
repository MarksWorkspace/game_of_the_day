# GameNight API — one-command dev server
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    $python = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
}

Write-Host "Installing dependencies..." -ForegroundColor Cyan
& $python -m pip install -q -r requirements.txt

$port = if ($env:PORT) { [int]$env:PORT } else { 8000 }
$portInUse = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "Port $port is already in use, switching to 8080..." -ForegroundColor Yellow
    $port = 8080
}

$baseUrl = "http://127.0.0.1:$port"
Write-Host ""
Write-Host "GameNight API starting at $baseUrl" -ForegroundColor Green
Write-Host "  API docs:  $baseUrl/docs" -ForegroundColor Green
Write-Host "  Health:    $baseUrl/api/health" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop." -ForegroundColor DarkGray
Write-Host ""

Start-Process "$baseUrl/docs"
& $python -m uvicorn main:app --reload --host 127.0.0.1 --port $port
