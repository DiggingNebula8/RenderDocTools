#!/usr/bin/env python
"""
Simple, intuitive RenderDoc build script for Windows.
Uses Visual Studio solution file (MSBuild), not CMake.
Auto-detects Python version and builds accordingly.

Usage:
    python scripts/build.py              # Development build
    python scripts/build.py --clean      # Clean build
    python scripts/build.py --release    # Release build
"""

import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import json


# Colors for terminal output
class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_step(num, text):
    print(f"\n{C.BOLD}{C.CYAN}[{num}] {text}{C.RESET}")


def print_success(text):
    print(f"{C.GREEN}[OK]{C.RESET} {text}")


def print_error(text):
    print(f"{C.RED}[X]{C.RESET} {text}")


def run_cmd(cmd, cwd=None, check=True):
    """Run command and return result"""
    print(f"  $ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=True if isinstance(cmd, str) else False
    )
    
    if check and result.returncode != 0:
        print(f"{C.RED}Error:{C.RESET}")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        sys.exit(1)
    
    return result


def find_msbuild():
    """Find MSBuild executable"""
    # Try vswhere first (most reliable for VS 2019+)
    vswhere_path = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    
    if vswhere_path.exists():
        try:
            result = subprocess.run([
                str(vswhere_path),
                '-latest',
                '-requires', 'Microsoft.Component.MSBuild',
                '-find', r'MSBuild\**\Bin\MSBuild.exe'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                msbuild_path = Path(result.stdout.strip().split('\n')[0])
                if msbuild_path.exists():
                    return msbuild_path
        except Exception:
            pass
    
    # Fallback: common locations
    common_paths = [
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\MSBuild.exe"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\MSBuild.exe"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\MSBuild.exe"),
    ]
    
    for path in common_paths:
        if path.exists():
            return path
    
    # Try PATH
    result = subprocess.run(['where', 'msbuild'], capture_output=True, text=True)
    if result.returncode == 0:
        return Path(result.stdout.strip().split('\n')[0])
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Build RenderDoc with auto-detected Python')
    parser.add_argument('--clean', action='store_true', help='Clean output directory first')
    parser.add_argument('--release', action='store_true', help='Build Release instead of Development')
    parser.add_argument('--config-only', action='store_true', help='Only show config, do not build')
    
    args = parser.parse_args()
    
    # Determine build configuration
    build_config = 'Release' if args.release else 'Development'
    
    # Paths
    root = Path(__file__).parent.parent
    renderdoc_dir = root / 'renderdoc'
    sln_file = renderdoc_dir / 'renderdoc.sln'
    output_dir = renderdoc_dir / 'x64' / build_config
    
    print(f"{C.BOLD}{C.CYAN}{'=' * 70}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'RenderDoc Build System (Windows)':^70}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'=' * 70}{C.RESET}")
    
    # Step 1: Detect Python
    print_step(1, "Detecting Python environment...")
    
    result = run_cmd([sys.executable, str(root / 'scripts' / 'detect_python.py'), '--json'])
    py_info = json.loads(result.stdout)
    
    print(f"  Python: {py_info['version']}")
    print(f"  DLL: {Path(py_info['dll_path']).name if py_info.get('dll_path') else 'NOT FOUND'}")
    print_success("Python detected")
    
    # Step 2: Check for solution file
    print_step(2, "Checking for Visual Studio solution...")
    
    if not sln_file.exists():
        print_error(f"Solution file not found: {sln_file}")
        print(f"{C.YELLOW}Make sure RenderDoc submodule is initialized{C.RESET}")
        sys.exit(1)
    
    print_success(f"Found {sln_file.name}")
    
    # Step 3: Find MSBuild
    print_step(3, "Finding MSBuild...")
    
    msbuild = find_msbuild()
    if not msbuild:
        print_error("MSBuild not found!")
        print(f"{C.YELLOW}Install Visual Studio 2019 or 2022 with C++ workload{C.RESET}")
        sys.exit(1)
    
    print_success(f"Found MSBuild: {msbuild}")
    
    # Step 4: Clean if requested
    if args.clean and output_dir.exists():
        print_step(4, f"Cleaning output directory...")
        shutil.rmtree(output_dir)
        print_success(f"Removed {output_dir}")
        step_num = 5
    else:
        step_num = 4
    
    if args.config_only:
        print(f"\n{C.GREEN}Configuration check complete!{C.RESET}")
        print(f"\nTo build manually:")
        print(f'  "{msbuild}" "{sln_file}" /p:Configuration={build_config} /p:Platform=x64')
        return
    
    # Step 5: Build with MSBuild
    print_step(step_num, f"Building RenderDoc ({build_config})...")
    print(f"{C.YELLOW}This may take 10-30 minutes...{C.RESET}\n")
    
    # Set Python prefix for RenderDoc build
    # RenderDoc's python.props checks RENDERDOC_PYTHON_PREFIX64 for custom Python
    import os
    build_env = os.environ.copy()
    if py_info.get('prefix'):
        python_prefix = py_info['prefix']
        build_env['RENDERDOC_PYTHON_PREFIX64'] = python_prefix
        print(f"  Using Python prefix: {python_prefix}")
    
    # MSBuild command
    msbuild_args = [
        str(msbuild),
        str(sln_file),
        f'/p:Configuration={build_config}',
        '/p:Platform=x64',
        '/m',  # Multi-core build
        '/v:minimal'  # Minimal verbosity
    ]
    
    # Run with custom environment
    print(f"  $ {' '.join(msbuild_args)}")
    result = subprocess.run(
        msbuild_args,
        cwd=renderdoc_dir,
        env=build_env,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"{C.RED}Error:{C.RESET}")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        sys.exit(1)
    
    print_success("Build complete!")
    
    # Step 6: Copy Python DLL if needed
    step_num += 1
    print_step(step_num, "Setting up Python runtime...")
    
    if py_info.get('dll_path'):
        dll_src = Path(py_info['dll_path'])
        dll_dst = output_dir / dll_src.name
        
        if dll_src.exists():
            # Only copy if not already there or if different
            if not dll_dst.exists() or dll_src.stat().st_size != dll_dst.stat().st_size:
                shutil.copy2(dll_src, dll_dst)
                print_success(f"Copied {dll_src.name} to output directory")
            else:
                print_success(f"{dll_src.name} already present")
        else:
            print_error(f"Python DLL not found: {dll_src}")
    else:
        print_error("Python DLL path not detected")
    
    # Step 7: Verify output
    step_num += 1
    print_step(step_num, "Verifying build output...")
    
    expected_files = [
        output_dir / 'renderdoc.dll',
        output_dir / 'qrenderdoc.exe',
        output_dir / 'renderdoccmd.exe',
    ]
    
    all_good = True
    for file in expected_files:
        if file.exists():
            print_success(f"Found: {file.name}")
        else:
            print_error(f"Missing: {file}")
            all_good = False
    
    if not all_good:
        print(f"\n{C.YELLOW}Build completed but some files are missing{C.RESET}")
        print(f"Check build output in: {output_dir}")
        sys.exit(1)
    
    # Success!
    print(f"\n{C.BOLD}{C.GREEN}{'=' * 70}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}{'BUILD SUCCESSFUL':^70}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}{'=' * 70}{C.RESET}")
    
    print(f"\n{C.CYAN}Output directory:{C.RESET} {output_dir}")
    print(f"{C.CYAN}Python version:{C.RESET} {py_info['version']}")
    
    print(f"\n{C.CYAN}Next steps:{C.RESET}")
    print(f"  1. Test RenderDoc: {C.BOLD}{output_dir / 'qrenderdoc.exe'}{C.RESET}")
    print(f"  2. Install tools: {C.BOLD}pip install -e .{C.RESET}")
    print(f"  3. Run diagnostics: {C.BOLD}python diagnose.py{C.RESET}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Build cancelled{C.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{C.RED}Build failed: {e}{C.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
