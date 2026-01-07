# Quick setup script for Python 3.6 virtual environment (required for RenderDoc Meta Fork)

Write-Host "Setting up Python 3.6 virtual environment for RenderDoc tools..." -ForegroundColor Cyan
Write-Host "(RenderDoc Meta Fork requires Python 3.6)" -ForegroundColor Yellow

# Find Python 3.6
$python36 = $null

$python36Paths = @(
    "python3.6",
    "python36",
    "$env:USERPROFILE\scoop\apps\python36\current\python.exe",
    "C:\Python36\python.exe",
    "C:\Program Files\Python36\python.exe"
)

foreach ($path in $python36Paths) {
    try {
        if ($path -match "^python") {
            # Try as command
            $version = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $version -match "3\.6") {
                $python36 = $path
                break
            }
        } elseif (Test-Path $path) {
            # Try as file path
            $version = & $path --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $version -match "3\.6") {
                $python36 = $path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $python36) {
    Write-Host "ERROR: Python 3.6 not found!" -ForegroundColor Red
    Write-Host "RenderDoc Meta Fork requires Python 3.6 (exact version)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Installation options:" -ForegroundColor Cyan
    Write-Host "1. Download from: https://www.python.org/downloads/release/python-3615/" -ForegroundColor White
    Write-Host "2. Or try: scoop bucket add versions; scoop install versions/python36" -ForegroundColor White
    Write-Host ""
    Write-Host "See INSTALL_PYTHON36.md for detailed instructions" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found Python 3.6: $python36" -ForegroundColor Green

# Create venv
if (Test-Path "venv36") {
    Write-Host "Virtual environment already exists at venv36/" -ForegroundColor Yellow
    $response = Read-Host "Delete and recreate? (y/n)"
    if ($response -eq "y") {
        Remove-Item -Recurse -Force "venv36"
    } else {
        Write-Host "Using existing virtual environment." -ForegroundColor Green
        Write-Host ""
        Write-Host "To activate:" -ForegroundColor Cyan
        Write-Host "  .\venv36\Scripts\Activate.ps1" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Creating virtual environment..." -ForegroundColor Cyan
& $python36 -m venv venv36

if (Test-Path "venv36") {
    Write-Host ""
    Write-Host "✓ Virtual environment created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Activate the virtual environment:" -ForegroundColor Yellow
    Write-Host "   .\venv36\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Test RenderDoc import:" -ForegroundColor Yellow
    Write-Host "   python test_renderdoc.py" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Process your capture:" -ForegroundColor Yellow
    Write-Host "   python -m renderdoc_tools.cli workflow 2.rdc --preset quick" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Deactivate when done:" -ForegroundColor Yellow
    Write-Host "   deactivate" -ForegroundColor White
    Write-Host "=" * 60 -ForegroundColor Cyan
} else {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}
