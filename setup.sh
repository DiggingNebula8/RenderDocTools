#!/bin/bash
# Optional convenience script - modern Python makes this simple!
# You can just run: pip install -e .

echo "RenderDocTools Setup"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found! Please install Python 3.8+ first."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
VERSION=$(python3 --version)
echo "Found: $VERSION"

# Install package
echo ""
echo "Installing RenderDocTools..."
python3 -m pip install -e .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation complete!"
    echo ""
    echo "Try it:"
    echo "  rdc-tools workflow --list-presets"
    echo ""
    echo "Or run diagnostics:"
    echo "  python diagnose.py"
else
    echo ""
    echo "✗ Installation failed"
    echo "Try manual install: pip install -e ."
    exit 1
fi
