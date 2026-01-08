#!/usr/bin/env python
"""
Retarget RenderDoc solution to current Visual Studio version.
Fixes v140 (VS 2015) toolset errors when building with VS 2019/2022.
"""

import sys
import subprocess
from pathlib import Path


C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_CYAN = '\033[96m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'


def find_devenv():
    """Find Visual Studio devenv.exe for retargeting"""
    vswhere_path = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    
    if vswhere_path.exists():
        try:
            result = subprocess.run([
                str(vswhere_path),
                '-latest',
                '-products', '*',
                '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
                '-property', 'installationPath'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                vs_path = Path(result.stdout.strip())
                devenv = vs_path / 'Common7' / 'IDE' / 'devenv.com'
                if devenv.exists():
                    return devenv
        except Exception:
            pass
    
    # Fallback
    common_paths = [
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.com"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.com"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.com"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\IDE\devenv.com"),
    ]
    
    for path in common_paths:
        if path.exists():
            return path
    
    return None


def main():
    root = Path(__file__).parent.parent
    sln_file = root / 'renderdoc' / 'renderdoc.sln'
    
    print(f"{C_BOLD}{C_CYAN}RenderDoc Solution Retargeting{C_RESET}\n")
    
    if not sln_file.exists():
        print(f"{C_RED}[X]{C_RESET} Solution file not found: {sln_file}")
        sys.exit(1)
    
    print(f"[1] Finding Visual Studio...")
    devenv = find_devenv()
    
    if not devenv:
        print(f"{C_RED}[X]{C_RESET} Visual Studio not found!")
        print(f"\n{C_YELLOW}Manual retargeting:{C_RESET}")
        print(f"  1. Open {sln_file} in Visual Studio")
        print(f"  2. Right-click solution → 'Retarget Solution'")
        print(f"  3. Select latest Windows SDK and Platform Toolset")
        print(f"  4. Click OK")
        sys.exit(1)
    
    print(f"{C_GREEN}[OK]{C_RESET} Found: {devenv.parent.parent.parent.name}")
    
    print(f"\n[2] Retargeting solution to current toolset...")
    print(f"  $ devenv /Upgrade \"{sln_file}\"")
    
    result = subprocess.run(
        [str(devenv), str(sln_file), '/Upgrade'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"{C_RED}[X]{C_RESET} Retargeting failed")
        if result.stderr:
            print(result.stderr)
        sys.exit(1)
    
    print(f"{C_GREEN}[OK]{C_RESET} Solution retargeted successfully")
    
    print(f"\n{C_GREEN}{C_BOLD}Done!{C_RESET}")
    print(f"\nNow run: {C_BOLD}python scripts/build.py{C_RESET}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}Cancelled{C_RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{C_RED}Error: {e}{C_RESET}")
        sys.exit(1)
