# Complete setup script for RenderDoc Tools
# Handles venv creation, activation, and package installation

param(
    [switch]$SkipVenv,
    [switch]$Help
)

if ($Help) {
    Write-Host "RenderDoc Tools Setup Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\setup.ps1 [options]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -SkipVenv    Skip venv creation (use existing venv36)"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "This script will:"
    Write-Host "  1. Create Python 3.6 virtual environment (venv36)"
    Write-Host "  2. Activate the virtual environment"
    Write-Host "  3. Install the package with pip install -e ."
    Write-Host "  4. Create convenience wrapper scripts"
    exit 0
}

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "RenderDoc Tools Setup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Step 1: Create virtual environment (if not skipping)
if (-not $SkipVenv) {
    Write-Host "Step 1: Setting up Python 3.6 virtual environment..." -ForegroundColor Yellow
    
    if (Test-Path "venv36") {
        Write-Host "  venv36 already exists, skipping creation" -ForegroundColor Green
        Write-Host "  (Use -SkipVenv to skip this check)" -ForegroundColor Gray
    } else {
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
                    $version = & $path --version 2>&1
                    if ($LASTEXITCODE -eq 0 -and $version -match "3\.6") {
                        $python36 = $path
                        break
                    }
                } elseif (Test-Path $path) {
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
            Write-Host "  ERROR: Python 3.6 not found!" -ForegroundColor Red
            Write-Host "  RenderDoc Meta Fork requires Python 3.6 (exact version)" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "  Installation options:" -ForegroundColor Cyan
            Write-Host "  1. Download from: https://www.python.org/downloads/release/python-3615/" -ForegroundColor White
            Write-Host "  2. Or try: scoop bucket add versions; scoop install versions/python36" -ForegroundColor White
            Write-Host ""
            Write-Host "  See INSTALL_PYTHON36.md for detailed instructions" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "  Found Python 3.6: $python36" -ForegroundColor Green
        Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
        & $python36 -m venv venv36
        
        if (-not (Test-Path "venv36")) {
            Write-Host "  ERROR: Failed to create virtual environment" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
    }
} else {
    Write-Host "Step 1: Skipping venv creation (using existing venv36)" -ForegroundColor Yellow
    if (-not (Test-Path "venv36")) {
        Write-Host "  ERROR: venv36 not found! Cannot skip venv creation." -ForegroundColor Red
        exit 1
    }
}

# Step 2: Install package
Write-Host ""
Write-Host "Step 2: Installing package..." -ForegroundColor Yellow

if (-not (Test-Path "venv36\Scripts\python.exe")) {
    Write-Host "  ERROR: venv36\Scripts\python.exe not found!" -ForegroundColor Red
    exit 1
}

Write-Host "  Running: pip install -e ." -ForegroundColor Cyan
& "venv36\Scripts\python.exe" -m pip install --upgrade pip
& "venv36\Scripts\python.exe" -m pip install --upgrade setuptools wheel
& "venv36\Scripts\python.exe" -m pip install -e .

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Package installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Package installed successfully" -ForegroundColor Green

# Step 3: Verify installation
Write-Host ""
Write-Host "Step 3: Verifying installation..." -ForegroundColor Yellow

try {
    $version = & "venv36\Scripts\python.exe" -c "import renderdoc_tools; print(renderdoc_tools.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Package version: $version" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Could not verify package version" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Could not verify package version" -ForegroundColor Yellow
}

# Step 4: Detect and configure RenderDoc
Write-Host ""
Write-Host "Step 4: Detecting RenderDoc installations..." -ForegroundColor Yellow

# Create temporary Python script for detection
$detection_script_path = "temp_renderdoc_detection.py"
$detection_script_content = @'
import sys
sys.path.insert(0, '.')
from renderdoc_tools.utils.renderdoc_detector import find_renderdoc_installations, get_preferred_renderdoc

installations = find_renderdoc_installations()
preferred = get_preferred_renderdoc()

if installations:
    print('Found RenderDoc installations:')
    for inst in installations:
        print('  - {}: {}'.format(inst['name'], inst['path']))
    if preferred:
        print('\nUsing: {} ({})'.format(preferred['name'], preferred['path']))
        print('PYTHONPATH: {}'.format(preferred['pymodules_path']))
else:
    print('No RenderDoc installations found')
    print('Please install RenderDoc or RenderDoc Meta Fork')
'@

try {
    $detection_script_content | Out-File -FilePath $detection_script_path -Encoding utf8 -NoNewline
    $detection_output = & "venv36\Scripts\python.exe" $detection_script_path 2>&1
    Write-Host $detection_output
    
    $renderdoc_found = $detection_output -match "Found RenderDoc"
    if ($renderdoc_found) {
        Write-Host "  ✓ RenderDoc detected and will be used automatically" -ForegroundColor Green
        Write-Host "  Note: The package automatically detects RenderDoc - no manual PYTHONPATH needed!" -ForegroundColor Cyan
    } else {
        Write-Host "  ⚠ RenderDoc not found in common locations" -ForegroundColor Yellow
        Write-Host "  You may need to install RenderDoc or set PYTHONPATH manually" -ForegroundColor Yellow
    }
} finally {
    # Clean up temp file
    if (Test-Path $detection_script_path) {
        Remove-Item $detection_script_path -ErrorAction SilentlyContinue
    }
}

# Step 5: Create wrapper scripts (they should already exist, but verify)
Write-Host ""
Write-Host "Step 5: Checking convenience wrappers..." -ForegroundColor Yellow

if (Test-Path "rdc-tools.ps1") {
    Write-Host "  ✓ rdc-tools.ps1 found" -ForegroundColor Green
} else {
    Write-Host "  ⚠ rdc-tools.ps1 not found (should be in repository)" -ForegroundColor Yellow
}

# Step 6: Add to PATH (current session and profile)
Write-Host ""
Write-Host "Step 6: Adding to PATH..." -ForegroundColor Yellow
$venvScriptsPath = Join-Path $PWD "venv36\Scripts"

# Add to current session PATH
if ($env:Path -notlike "*$venvScriptsPath*") {
    $env:Path += ";$venvScriptsPath"
    Write-Host "  ✓ Added venv36\Scripts to PATH for this session" -ForegroundColor Green
} else {
    Write-Host "  ✓ venv36\Scripts already in PATH for this session" -ForegroundColor Green
}

# Add to PowerShell profile for persistence
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path -Parent $profilePath

try {
    # Create profile directory if it doesn't exist
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    
    # Check if already in profile
    $profileContent = ""
    if (Test-Path $profilePath) {
        $profileContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
    }
    
    $pathLine = '$env:Path += ";' + $venvScriptsPath + '"'
    $pathComment = '# RenderDoc Tools - Add venv36\Scripts to PATH'
    
    if ($profileContent -and $profileContent -like "*$venvScriptsPath*") {
        Write-Host "  ✓ venv36\Scripts already in PowerShell profile" -ForegroundColor Green
    } else {
        # Add to profile
        $addition = "`n$pathComment`n$pathLine`n"
        Add-Content -Path $profilePath -Value $addition -ErrorAction Stop
        Write-Host "  ✓ Added venv36\Scripts to PowerShell profile (persists across sessions)" -ForegroundColor Green
        Write-Host "    Profile: $profilePath" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ⚠ Could not add to PowerShell profile: $_" -ForegroundColor Yellow
    Write-Host "  You can manually add this line to your profile:" -ForegroundColor Yellow
    Write-Host ('    $env:Path += ";' + $venvScriptsPath + '"') -ForegroundColor White
}

# Final instructions
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now use RenderDoc Tools:" -ForegroundColor Cyan
Write-Host ""
Write-Host "The 'rdc-tools' command is now available (added to PATH):" -ForegroundColor Yellow
Write-Host "  rdc-tools workflow capture.rdc --preset quick" -ForegroundColor White
Write-Host "  rdc-tools workflow --list-presets" -ForegroundColor White
Write-Host ""
Write-Host "Or use the convenience wrapper:" -ForegroundColor Yellow
Write-Host "  .\rdc-tools.ps1 workflow capture.rdc --preset quick" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. RenderDoc is automatically detected (if installed)" -ForegroundColor White
Write-Host "  2. Run: python setup_check.py (to verify RenderDoc detection)" -ForegroundColor White
Write-Host "  3. Test: rdc-tools workflow --list-presets" -ForegroundColor White
Write-Host ""
Write-Host "Note: RenderDoc detection is automatic - no manual PYTHONPATH setup needed!" -ForegroundColor Green
Write-Host ""

