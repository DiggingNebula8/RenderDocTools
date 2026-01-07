#!/usr/bin/env python3
"""
Setup verification and helper script for RDC Parser
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("❌ Python 3.6+ required")
        return False
    else:
        print("✓ Python version OK")
        return True


def check_renderdoc_module():
    """Check if renderdoc module can be imported"""
    try:
        import renderdoc as rd
        print("✓ renderdoc module found")
        return True
    except ImportError as e:
        print(f"❌ renderdoc module not found")
        print(f"   Error: {e}")
        return False


def find_renderdoc_paths():
    """Try to find RenderDoc installation"""
    print("\nSearching for RenderDoc installation...")
    
    possible_paths = []
    
    if sys.platform == 'win32':
        possible_paths = [
            Path('C:/Program Files/RenderDocForMetaQuest'),  # Meta Fork
            Path('C:/Program Files/RenderDoc'),  # Standard RenderDoc
            Path('C:/Program Files (x86)/RenderDoc'),
            Path(os.environ.get('PROGRAMFILES', '')) / 'RenderDocForMetaQuest',
            Path(os.environ.get('PROGRAMFILES', '')) / 'RenderDoc',
        ]
    elif sys.platform == 'linux':
        possible_paths = [
            Path('/usr/share/renderdoc'),
            Path('/usr/local/share/renderdoc'),
            Path.home() / '.local/share/renderdoc',
        ]
    
    found = []
    for path in possible_paths:
        if path.exists():
            # Look for the module
            if sys.platform == 'win32':
                module = path / 'renderdoc.pyd'
            else:
                module = path / 'renderdoc.so'
            
            if module.exists():
                found.append(path)
                print(f"  Found: {path}")
    
    if not found:
        print("  No RenderDoc installations found in common locations")
    
    return found


def print_setup_instructions():
    """Print setup instructions based on platform"""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    
    if sys.platform == 'win32':
        print("""
1. Download RenderDoc from https://renderdoc.org/builds
   OR RenderDoc Meta Fork from Meta Developer site

2. Install RenderDoc (use default location)
   - Standard: C:\\Program Files\\RenderDoc
   - Meta Fork: C:\\Program Files\\RenderDocForMetaQuest

3. Set PYTHONPATH to RenderDoc directory:
   
   Option A - Command line (temporary):
   # For standard RenderDoc:
   set PYTHONPATH=C:\\Program Files\\RenderDoc
   
   # For Meta Fork:
   set PYTHONPATH=C:\\Program Files\\RenderDocForMetaQuest
   
   Option B - Environment variable (permanent):
   - Right-click 'This PC' → Properties → Advanced System Settings
   - Click 'Environment Variables'
   - Add new System variable:
     Name: PYTHONPATH
     Value: C:\\Program Files\\RenderDocForMetaQuest
     (or C:\\Program Files\\RenderDoc for standard version)

4. On Python 3.8+, also add DLL directory in your script:
   import os, sys
   if sys.version_info >= (3, 8):
       os.add_dll_directory("C:\\\\Program Files\\\\RenderDocForMetaQuest")
       # or: os.add_dll_directory("C:\\\\Program Files\\\\RenderDoc")

5. Test: python setup_check.py
        """)
    
    else:  # Linux/Mac
        print("""
1. Install RenderDoc:
   
   Ubuntu/Debian:
   sudo apt install renderdoc
   
   Or download from: https://renderdoc.org/builds

2. Find module location:
   dpkg -L renderdoc | grep renderdoc.so
   
   Common locations:
   - /usr/lib/renderdoc/
   - /usr/share/renderdoc/

3. Set environment variables:
   
   Add to ~/.bashrc or ~/.zshrc:
   export PYTHONPATH=/usr/share/renderdoc:$PYTHONPATH
   export LD_LIBRARY_PATH=/usr/lib/renderdoc:$LD_LIBRARY_PATH

4. Reload shell:
   source ~/.bashrc

5. Test: python3 setup_check.py
        """)
    
    print("="*60)


def main():
    print("="*60)
    print("RDC Parser Setup Checker")
    print("="*60 + "\n")
    
    checks_passed = 0
    total_checks = 2
    
    # Check Python version
    if check_python_version():
        checks_passed += 1
    
    # Check renderdoc module
    if check_renderdoc_module():
        checks_passed += 1
    
    # Find installations
    found_paths = find_renderdoc_paths()
    
    print(f"\n{'='*60}")
    print(f"Result: {checks_passed}/{total_checks} checks passed")
    print(f"{'='*60}")
    
    if checks_passed == total_checks:
        print("\n✓ Setup complete! You can use renderdoc_tools")
        print("\nQuick start:")
        print("  python -m renderdoc_tools.cli workflow your_capture.rdc --preset quick")
        print("  python -m renderdoc_tools.cli parse your_capture.rdc -o output.json")
    else:
        print("\n⚠ Setup incomplete")
        print_setup_instructions()
        
        if found_paths:
            print("\nTIP: RenderDoc found at:")
            for path in found_paths:
                print(f"  {path}")
            print("\nTry setting PYTHONPATH to one of these locations")


if __name__ == '__main__':
    main()
