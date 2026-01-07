#!/usr/bin/env python3
"""Simple test script to check RenderDoc import"""

import sys
import os

print("Starting RenderDoc import test...")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Add Meta Fork path
meta_quest_base = r"C:\Program Files\RenderDocForMetaQuest"
meta_quest_pymodules = os.path.join(meta_quest_base, "pymodules")

print(f"\nChecking Meta Fork path: {meta_quest_pymodules}")
print(f"Path exists: {os.path.exists(meta_quest_pymodules)}")

if os.path.exists(meta_quest_pymodules):
    print("Adding pymodules to sys.path...")
    sys.path.insert(0, meta_quest_pymodules)
    
    # Collect all directories
    path_parts = [meta_quest_base]
    try:
        for item in os.listdir(meta_quest_base):
            subdir = os.path.join(meta_quest_base, item)
            if os.path.isdir(subdir):
                path_parts.append(subdir)
                # Add nested subdirectories too
                try:
                    for nested_item in os.listdir(subdir):
                        nested_subdir = os.path.join(subdir, nested_item)
                        if os.path.isdir(nested_subdir):
                            path_parts.append(nested_subdir)
                except:
                    pass
    except:
        pass
    
    if sys.version_info >= (3, 8):
        print("Python 3.8+ detected, adding DLL directories...")
        for path_part in path_parts:
            try:
                if os.path.exists(path_part):
                    os.add_dll_directory(path_part)
                    print(f"  Added: {path_part}")
            except Exception as e:
                print(f"  Failed to add {path_part}: {e}")
    
    print("Adding to PATH environment variable...")
    old_path = os.environ.get('PATH', '')
    new_path = os.pathsep.join(path_parts)
    path_list = old_path.split(os.pathsep)
    path_list = [p for p in path_list if meta_quest_base not in p]
    os.environ['PATH'] = new_path + os.pathsep + os.pathsep.join(path_list)
    
    # Set Qt plugin path and use offscreen platform
    qt_plugin_path = os.path.join(meta_quest_base, "qtplugins")
    if os.path.exists(qt_plugin_path):
        os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Prevent GUI initialization
        os.environ['QT_LOGGING_RULES'] = '*.debug=false'
        print(f"Set QT_PLUGIN_PATH: {qt_plugin_path}")
        print(f"Set QT_QPA_PLATFORM: offscreen (headless mode)")
    
    print(f"sys.path[0]: {sys.path[0]}")
    print(f"PATH starts with: {os.environ['PATH'][:150]}...")
else:
    print(f"WARNING: Meta Fork path not found: {meta_quest_pymodules}")

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

