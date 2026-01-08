import os
import sys
from pathlib import Path

# Add DLL directory for Python 3.8+
renderdoc_dir = Path(r"C:\Users\vsiva\dev\RD\renderdoc\x64\Development")
pymodules = renderdoc_dir / "pymodules"

print(f"Adding DLL directory: {renderdoc_dir}")
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(str(renderdoc_dir))

print(f"Adding to sys.path: {pymodules}")
sys.path.insert(0, str(pymodules))

try:
    import renderdoc
    print(f"\n✓ Successfully imported renderdoc!")
    print(f"  API Version: {renderdoc.RENDERDOC_API_VERSION}")
    print(f"  Module file: {renderdoc.__file__}")
except Exception as e:
    print(f"\n✗ Failed to import: {e}")
    import traceback
    traceback.print_exc()
