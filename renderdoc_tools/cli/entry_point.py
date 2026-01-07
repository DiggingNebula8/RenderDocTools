"""
Entry point wrapper that automatically uses venv36
This ensures rdc-tools always runs with the correct Python environment
"""

import sys
import os
from pathlib import Path


def find_venv36_python():
    """Find Python executable in venv36"""
    # Get the project root (where setup.py/pyproject.toml is)
    # This script is in renderdoc_tools/cli/, so go up 2 levels
    project_root = Path(__file__).parent.parent.parent
    venv36_python = project_root / "venv36"
    
    if sys.platform == "win32":
        python_exe = venv36_python / "Scripts" / "python.exe"
    else:
        python_exe = venv36_python / "bin" / "python"
    
    if python_exe.exists():
        return str(python_exe)
    
    return None


def main():
    """Main entry point that uses venv36 Python"""
    # Try to find venv36 Python
    venv36_python = find_venv36_python()
    
    if venv36_python:
        # Use venv36 Python to run the actual CLI
        import subprocess
        
        # Build command: python -m renderdoc_tools.cli.main <args>
        cmd = [venv36_python, "-m", "renderdoc_tools.cli.main"] + sys.argv[1:]
        
        # Run with venv36 Python
        sys.exit(subprocess.call(cmd))
    else:
        # Fallback: try to run normally (might work if installed in current Python)
        # But warn the user
        print("WARNING: venv36 not found!", file=sys.stderr)
        print("Attempting to run with current Python environment...", file=sys.stderr)
        print("For best results, run: .\\setup.ps1 (Windows) or ./setup.sh (Linux/Mac)", file=sys.stderr)
        print("", file=sys.stderr)
        
        # Try to import and run the CLI
        try:
            from renderdoc_tools.cli.main import main as cli_main
            sys.exit(cli_main())
        except ImportError as e:
            print(f"ERROR: Could not import renderdoc_tools: {e}", file=sys.stderr)
            print("", file=sys.stderr)
            print("Please run the setup script first:", file=sys.stderr)
            if sys.platform == "win32":
                print("  .\\setup.ps1", file=sys.stderr)
            else:
                print("  ./setup.sh", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

