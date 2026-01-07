#!/bin/bash
# Complete setup script for RenderDoc Tools (Linux/Mac)
# Handles venv creation, activation, and package installation

set -e

SKIP_VENV=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-venv)
            SKIP_VENV=true
            shift
            ;;
        --help)
            echo "RenderDoc Tools Setup Script"
            echo ""
            echo "Usage: ./setup.sh [options]"
            echo ""
            echo "Options:"
            echo "  --skip-venv    Skip venv creation (use existing venv36)"
            echo "  --help         Show this help message"
            echo ""
            echo "This script will:"
            echo "  1. Create Python 3.6 virtual environment (venv36)"
            echo "  2. Install the package with pip install -e ."
            echo "  3. Create convenience wrapper scripts"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "============================================================"
echo "RenderDoc Tools Setup"
echo "============================================================"
echo ""

# Step 1: Create virtual environment
if [ "$SKIP_VENV" = false ]; then
    echo "Step 1: Setting up Python 3.6 virtual environment..."
    
    if [ -d "venv36" ]; then
        echo "  venv36 already exists, skipping creation"
    else
        # Find Python 3.6
        PYTHON36=""
        for py in python3.6 python36; do
            if command -v $py &> /dev/null; then
                VERSION=$($py --version 2>&1)
                if echo "$VERSION" | grep -q "3\.6"; then
                    PYTHON36=$py
                    break
                fi
            fi
        done
        
        if [ -z "$PYTHON36" ]; then
            echo "  ERROR: Python 3.6 not found!"
            echo "  RenderDoc Meta Fork requires Python 3.6 (exact version)"
            echo ""
            echo "  Installation options:"
            echo "  1. Download from: https://www.python.org/downloads/release/python-3615/"
            echo "  2. Or use your system package manager"
            echo ""
            echo "  See INSTALL_PYTHON36.md for detailed instructions"
            exit 1
        fi
        
        echo "  Found Python 3.6: $PYTHON36"
        echo "  Creating virtual environment..."
        $PYTHON36 -m venv venv36
        
        if [ ! -d "venv36" ]; then
            echo "  ERROR: Failed to create virtual environment"
            exit 1
        fi
        
        echo "  ✓ Virtual environment created"
    fi
else
    echo "Step 1: Skipping venv creation (using existing venv36)"
    if [ ! -d "venv36" ]; then
        echo "  ERROR: venv36 not found! Cannot skip venv creation."
        exit 1
    fi
fi

# Step 2: Install package
echo ""
echo "Step 2: Installing package..."

if [ ! -f "venv36/bin/python" ]; then
    echo "  ERROR: venv36/bin/python not found!"
    exit 1
fi

echo "  Running: pip install -e ."
venv36/bin/python -m pip install --upgrade pip
venv36/bin/python -m pip install --upgrade setuptools wheel
venv36/bin/python -m pip install -e .

if [ $? -ne 0 ]; then
    echo "  ERROR: Package installation failed"
    exit 1
fi

echo "  ✓ Package installed successfully"

# Step 3: Verify installation
echo ""
echo "Step 3: Verifying installation..."

VERSION=$(venv36/bin/python -c "import renderdoc_tools; print(renderdoc_tools.__version__)" 2>&1 || echo "")
if [ -n "$VERSION" ]; then
    echo "  ✓ Package version: $VERSION"
else
    echo "  ⚠ Could not verify package version"
fi

# Step 4: Detect and configure RenderDoc
echo ""
echo "Step 4: Detecting RenderDoc installations..."

# Create temporary Python script for detection
DETECTION_SCRIPT=$(cat << 'PYTHON_SCRIPT'
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
PYTHON_SCRIPT
)

DETECTION_OUTPUT=$(venv36/bin/python -c "$DETECTION_SCRIPT" 2>&1)

echo "$DETECTION_OUTPUT"

if echo "$DETECTION_OUTPUT" | grep -q "Found RenderDoc"; then
    echo "  ✓ RenderDoc detected and will be used automatically"
    echo "  Note: The package automatically detects RenderDoc - no manual PYTHONPATH needed!"
else
    echo "  ⚠ RenderDoc not found in common locations"
    echo "  You may need to install RenderDoc or set PYTHONPATH manually"
fi

# Step 5: Make wrapper script executable
echo ""
echo "Step 5: Setting up convenience wrappers..."

if [ -f "rdc-tools.sh" ]; then
    chmod +x rdc-tools.sh
    echo "  ✓ rdc-tools.sh is executable"
else
    echo "  ⚠ rdc-tools.sh not found (should be in repository)"
fi

# Final instructions
echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "You can now use RenderDoc Tools:"
echo ""
echo "The rdc-tools command automatically uses venv36 (no activation needed!):"
echo "  rdc-tools workflow capture.rdc --preset quick"
echo ""
echo "Alternative: Use convenience wrapper:"
echo "  ./rdc-tools.sh workflow capture.rdc --preset quick"
echo ""
echo "Next steps:"
echo "  1. RenderDoc is automatically detected (if installed)"
echo "  2. Run: python setup_check.py (to verify RenderDoc detection)"
echo "  3. Test: rdc-tools workflow --list-presets"
echo ""
echo "Note: RenderDoc detection is automatic - no manual PYTHONPATH setup needed!"
echo ""

