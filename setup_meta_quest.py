#!/usr/bin/env python3
"""
Quick setup script for RenderDoc Meta Fork (Meta Quest)
Helps configure PYTHONPATH for RenderDocForMetaQuest installation
"""

import sys
import os
from pathlib import Path

META_QUEST_PATH = Path('C:/Program Files/RenderDocForMetaQuest')
META_QUEST_PYMODULES = META_QUEST_PATH / 'pymodules'

def check_installation():
    """Check if RenderDocForMetaQuest is installed"""
    if META_QUEST_PATH.exists():
        # Check for renderdoc.pyd in pymodules (Meta Fork location)
        module_path = META_QUEST_PYMODULES / 'renderdoc.pyd'
        
        if module_path.exists():
            print(f"[OK] Found RenderDocForMetaQuest at: {META_QUEST_PATH}")
            print(f"     Module found at: {module_path}")
            return True
        else:
            # Fallback: check other common locations
            possible_paths = [
                META_QUEST_PATH / 'renderdoc.pyd',
                META_QUEST_PATH / 'plugins' / 'renderdoc.pyd',
                META_QUEST_PATH / 'bin' / 'renderdoc.pyd',
            ]
            
            found_path = None
            for path in possible_paths:
                if path.exists():
                    found_path = path
                    break
            
            if found_path:
                print(f"[OK] Found RenderDocForMetaQuest at: {META_QUEST_PATH}")
                print(f"     Module found at: {found_path}")
                return True
            else:
                print(f"[WARN] Directory exists but renderdoc.pyd not found")
                print(f"     Expected at: {module_path}")
                return False
    else:
        print(f"[FAIL] RenderDocForMetaQuest not found at: {META_QUEST_PATH}")
        return False

def check_pythonpath():
    """Check if PYTHONPATH is set correctly"""
    pythonpath = os.environ.get('PYTHONPATH', '')
    meta_path = str(META_QUEST_PYMODULES)  # Use pymodules directory
    
    if meta_path in pythonpath or str(META_QUEST_PATH) in pythonpath:
        print(f"[OK] PYTHONPATH includes RenderDocForMetaQuest")
        print(f"     Should point to: {meta_path}")
        return True
    else:
        print(f"[FAIL] PYTHONPATH does not include RenderDocForMetaQuest")
        print(f"  Current PYTHONPATH: {pythonpath or '(not set)'}")
        print(f"  Should be set to: {meta_path}")
        return False

def test_import():
    """Test if renderdoc module can be imported"""
    try:
        import renderdoc as rd
        print("[OK] renderdoc module imported successfully")
        
        # Try to get version info if available
        try:
            print(f"  RenderDoc module loaded from: {rd.__file__}")
        except:
            pass
        
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import renderdoc module: {e}")
        return False

def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS FOR RENDERDOC META FORK")
    print("="*60)
    print(f"""
1. Verify installation:
   Directory should exist: {META_QUEST_PATH}
   File should exist: {META_QUEST_PATH / 'renderdoc.pyd'}

2. Set PYTHONPATH (choose one method):

   Method A - PowerShell (current session only):
   $env:PYTHONPATH = "C:\\Program Files\\RenderDocForMetaQuest\\pymodules"
   
   Method B - Command Prompt (current session only):
   set PYTHONPATH=C:\\Program Files\\RenderDocForMetaQuest\\pymodules
   
   Method C - Permanent (Environment Variables):
   - Right-click 'This PC' -> Properties -> Advanced System Settings
   - Click 'Environment Variables'
   - Under 'User variables' or 'System variables', find or create PYTHONPATH
   - Add: C:\\Program Files\\RenderDocForMetaQuest\\pymodules
   - Click OK and restart your terminal

3. For Python 3.8+ (add to your scripts if needed):
   import os, sys
   if sys.version_info >= (3, 8):
       os.add_dll_directory(r"C:\\Program Files\\RenderDocForMetaQuest")

4. Test:
   python setup_meta_quest.py
   python setup_check.py

5. Verify with a test:
   python -c "import renderdoc; print('Success!')"
""")
    print("="*60)

def main():
    print("="*60)
    print("RenderDoc Meta Fork Setup Checker")
    print("="*60 + "\n")
    
    checks = {
        'Installation': check_installation(),
        'PYTHONPATH': check_pythonpath(),
        'Import': test_import(),
    }
    
    print(f"\n{'='*60}")
    passed = sum(checks.values())
    total = len(checks)
    print(f"Result: {passed}/{total} checks passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n[SUCCESS] Setup complete! You can use the RDC parser tools.")
        print("\nQuick test:")
        print("  python -m renderdoc_tools.cli workflow --list-presets")
    else:
        print("\n[WARN] Setup incomplete")
        print_setup_instructions()
        
        if checks['Installation'] and not checks['PYTHONPATH']:
            print("\nTIP: Installation found but PYTHONPATH not set.")
            print(f"     Run: $env:PYTHONPATH = \"C:\\Program Files\\RenderDocForMetaQuest\\pymodules\"")
            print(f"     Or: set PYTHONPATH=C:\\Program Files\\RenderDocForMetaQuest\\pymodules")

if __name__ == '__main__':
    main()

