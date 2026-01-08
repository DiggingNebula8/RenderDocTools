#!/usr/bin/env python3
"""Simple test script to check RenderDoc import"""

import sys
import os

print("Starting RenderDoc import test...")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Add standard RenderDoc path
renderdoc_base = r"C:\Program Files\RenderDoc"
renderdoc_pymodules = os.path.join(renderdoc_base, "pymodules")

print(f"\nChecking RenderDoc path: {renderdoc_pymodules}")
print(f"Path exists: {os.path.exists(renderdoc_pymodules)}")

if os.path.exists(renderdoc_pymodules):
    print("Adding pymodules to sys.path...")
    sys.path.insert(0, renderdoc_pymodules)
    
    # Add parent path if needed
    if renderdoc_base not in sys.path:
        sys.path.insert(0, renderdoc_base)
    
    print(f"sys.path[0]: {sys.path[0]}")
else:
    print(f"WARNING: RenderDoc path not found: {renderdoc_pymodules}")

print("\nAttempting to import renderdoc...")
try:
    import renderdoc as rd
    print("SUCCESS: RenderDoc module imported!")
    try:
        print(f"Module location: {rd.__file__}")
    except:
        print("Module location: (not available)")
except ImportError as e:
    print(f"ERROR: ImportError: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\nTest complete.")

