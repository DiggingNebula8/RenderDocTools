# Optional convenience script - modern Python makes this simple!
# You can just run: pip install -e .

Write-Host "RenderDocTools Setup" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Check if Python is available
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Python version
$version = & python --version 2>&1
Write-Host "Found: $version" -ForegroundColor Green

# Install package
Write-Host ""
Write-Host "Installing RenderDocTools..." -ForegroundColor Cyan
& python -m pip install -e .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Try it:" -ForegroundColor Cyan
    Write-Host "  rdc-tools workflow --list-presets" -ForegroundColor White
    Write-Host ""
    Write-Host "Or run diagnostics:" -ForegroundColor Cyan
    Write-Host "  python diagnose.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "✗ Installation failed" -ForegroundColor Red
    Write-Host "Try manual install: pip install -e ." -ForegroundColor Yellow
    exit 1
}
