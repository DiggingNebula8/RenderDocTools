#!/bin/bash
# Convenience wrapper script for rdc-tools (Linux/Mac)
# Automatically activates venv36 and runs rdc-tools command

if [ ! -f "venv36/bin/activate" ]; then
    echo "ERROR: venv36 not found!"
    echo "Run setup_venv.ps1 or create venv36 manually first"
    exit 1
fi

source venv36/bin/activate
rdc-tools "$@"
deactivate

