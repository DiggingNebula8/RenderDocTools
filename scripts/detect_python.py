#!/usr/bin/env python
"""
Auto-detect current Python environment for RenderDoc build.
Works with any Python 3.8+ version.
"""

import sys
import sysconfig
from pathlib import Path
import json


def get_python_info():
    """Get Python configuration for RenderDoc build"""
    
    info = {
        'version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'version_short': f"{sys.version_info.major}.{sys.version_info.minor}",
        'version_nodot': f"{sys.version_info.major}{sys.version_info.minor}",
        'executable': sys.executable,
        'prefix': sys.prefix,
        'include_dir': sysconfig.get_path('include'),
        'library_dir': sysconfig.get_config_var('LIBDIR'),
        'stdlib_dir': sysconfig.get_path('stdlib'),
    }
    
    # Windows-specific: Find pythonXX.dll and pythonXX.lib
    if sys.platform == 'win32':
        base_path = Path(sys.prefix)
        
        # python3XX.dll is usually in the same dir as python.exe
        dll_name = f"python{info['version_nodot']}.dll"
        dll_path = base_path / dll_name
        if not dll_path.exists():
            # Try Scripts dir or base
            for loc in [base_path, base_path / 'Scripts', base_path / 'DLLs']:
                test_path = loc / dll_name
                if test_path.exists():
                    dll_path = test_path
                    break
        
        info['dll_path'] = str(dll_path) if dll_path.exists() else None
        
        # python3XX.lib is in libs/ directory
        lib_name = f"python{info['version_nodot']}.lib"
        lib_path = base_path / 'libs' / lib_name
        info['lib_path'] = str(lib_path) if lib_path.exists() else None
        
        # Standard library zip (for RenderDoc embedding)
        zip_name = f"python{info['version_nodot']}.zip"
        # We'll need to create this from Lib/
        info['stdlib_source'] = str(base_path / 'Lib')
        info['zip_name'] = zip_name
    
    return info


def print_cmake_vars(info):
    """Print CMake variable assignments"""
    print(f"set(PYTHON_VERSION_STRING \"{info['version']}\")")
    print(f"set(PYTHON_VERSION_MAJOR {sys.version_info.major})")
    print(f"set(PYTHON_VERSION_MINOR {sys.version_info.minor})")
    print(f"set(Python3_EXECUTABLE \"{info['executable']}\")")
    print(f"set(Python3_INCLUDE_DIRS \"{info['include_dir']}\")")
    
    if sys.platform == 'win32':
        if info.get('lib_path'):
            print(f"set(Python3_LIBRARIES \"{info['lib_path']}\")")
        if info.get('dll_path'):
            print(f"set(PYTHON_DLL_PATH \"{info['dll_path']}\")")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Detect Python for RenderDoc build')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--cmake', action='store_true', help='Output as CMake variables')
    parser.add_argument('--summary', action='store_true', help='Human-readable summary')
    
    args = parser.parse_args()
    
    info = get_python_info()
    
    if args.json:
        print(json.dumps(info, indent=2))
    elif args.cmake:
        print_cmake_vars(info)
    else:
        # Default: summary
        print("=" * 60)
        print("Detected Python Environment")
        print("=" * 60)
        print(f"Version:     {info['version']}")
        print(f"Executable:  {info['executable']}")
        print(f"Prefix:      {info['prefix']}")
        print(f"Include:     {info['include_dir']}")
        
        if sys.platform == 'win32':
            print(f"DLL:         {info.get('dll_path', 'NOT FOUND')}")
            print(f"LIB:         {info.get('lib_path', 'NOT FOUND')}")
            print(f"Stdlib:      {info['stdlib_source']}")
            print(f"Zip name:    {info['zip_name']}")
        
        print("=" * 60)
        
        # Validation
        issues = []
        if sys.version_info < (3, 8):
            issues.append("⚠ Python 3.8+ required")
        if sys.platform == 'win32':
            if not info.get('dll_path'):
                issues.append("⚠ Python DLL not found")
            if not info.get('lib_path'):
                issues.append("⚠ Python .lib not found")
        
        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("\n[OK] Python environment is valid for RenderDoc build")


if __name__ == '__main__':
    main()
