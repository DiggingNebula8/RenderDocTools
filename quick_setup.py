#!/usr/bin/env python
"""
Quick setup script for RenderDocTools with custom RenderDoc build
"""

import os
import sys
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print styled header"""
    print(f"\n{CYAN}{BOLD}{'=' * 70}{RESET}")
    print(f"{CYAN}{BOLD}{text:^70}{RESET}")
    print(f"{CYAN}{BOLD}{'=' * 70}{RESET}\n")

def print_step(num, text):
    """Print step number"""
    print(f"{BOLD}{CYAN}[{num}]{RESET} {text}")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{RESET} {text}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗{RESET} {text}")

def setup_environment():
    """Setup environment variables for custom RenderDoc build"""
    
    print_header("RenderDocTools Quick Setup")
    
    # Paths
    renderdoc_path = Path(r"C:\Users\vsiva\dev\RD\renderdoc\x64\Development")
    pymodules_path = renderdoc_path / "pymodules"
    
    print_step(1, "Checking RenderDoc build...")
    
    if not renderdoc_path.exists():
        print_error(f"RenderDoc build not found at {renderdoc_path}")
        print(f"   {YELLOW}Please build RenderDoc first{RESET}")
        sys.exit(1)
    
    if not pymodules_path.exists():
        print_error(f"Python modules not found at {pymodules_path}")
        sys.exit(1)
    
    print_success(f"Found RenderDoc build at {renderdoc_path}")
    
    print_step(2, "Setting up Python path...")
    
    # Add to sys.path for this session
    sys.path.insert(0, str(pymodules_path))
    
    # Add to PYTHONPATH for future sessions (Windows)
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    new_pythonpath = f"{pymodules_path};{current_pythonpath}" if current_pythonpath else str(pymodules_path)
    
    print(f"   {CYAN}Add this to your environment variables:{RESET}")
    print(f"   {BOLD}PYTHONPATH={new_pythonpath}{RESET}")
    print(f"   {YELLOW}(Or run this script before using RenderDocTools){RESET}\n")
    
    print_step(3, "Testing RenderDoc Python module...")
    
    try:
        import renderdoc
        version = getattr(renderdoc, 'RENDERDOC_API_VERSION', 'unknown')
        print_success(f"RenderDoc module loaded successfully (API v{version})")
    except ImportError as e:
        print_error(f"Failed to import renderdoc: {e}")
        sys.exit(1)
    
    print_step(4, "Checking RenderDocTools installation...")
    
    try:
        import renderdoc_tools
        version = getattr(renderdoc_tools, '__version__', 'unknown')
        print_success(f"RenderDocTools installed (v{version})")
    except ImportError:
        print_error("RenderDocTools not installed")
        print(f"   {YELLOW}Run: pip install -e .{RESET}")
        sys.exit(1)
    
    print_step(5, "Verifying setup...")
    
    # Test basic functionality
    try:
        from renderdoc_tools.utils.renderdoc_detector import find_renderdoc_installations
        installations = find_renderdoc_installations()
        
        if installations:
            for inst in installations:
                print_success(f"Found: {inst['name']} at {inst['path']}")
        else:
            print_error("No RenderDoc installations found by detector")
    except Exception as e:
        print_error(f"Error during verification: {e}")
    
    print_header("Setup Complete!")
    
    print(f"{GREEN}{BOLD}✓ Everything is ready!{RESET}\n")
    print(f"{CYAN}Quick Start:{RESET}")
    print(f"  1. Capture a frame: Open {BOLD}qrenderdoc.exe{RESET}")
    print(f"     {renderdoc_path / 'qrenderdoc.exe'}")
    print(f"  2. Extract data: {BOLD}python -m renderdoc_tools.cli.entry_point workflow capture.rdc --quick{RESET}\n")
    
    print(f"{CYAN}Available Presets:{RESET}")
    print(f"  --quick        Fast JSON export")
    print(f"  --full         Complete analysis with CSV")
    print(f"  --csv-only     CSV files only")
    print(f"  --performance  Performance analysis\n")
    
    print(f"{CYAN}Documentation:{RESET}")
    print(f"  See: {BOLD}MOBILE_CAPTURE_WORKFLOW.md{RESET} for complete guide\n")

if __name__ == "__main__":
    try:
        setup_environment()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Setup cancelled{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)
