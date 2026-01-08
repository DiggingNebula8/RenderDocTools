#!/usr/bin/env python
"""
One-command setup for RenderDocTools.
Initializes submodules, builds RenderDoc, installs package.

Usage:
    python setup_all.py              # Full setup
    python setup_all.py --skip-build # Skip RenderDoc build
"""

import sys
import subprocess
from pathlib import Path
import argparse


C_GREEN = '\033[92m'
C_YELLOW = '\033[93m'
C_RED = '\033[91m'
C_CYAN = '\033[96m'
C_RESET = '\033[0m'
C_BOLD = '\033[1m'


def run_cmd(cmd, cwd=None, check=True):
    """Run command"""
    print(f"  $ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=True if isinstance(cmd, str) else False)
    if check and result.returncode != 0:
        print(f"{C_RED}✗ Command failed{C_RESET}")
        sys.exit(1)
    return result


def main():
    parser = argparse.ArgumentParser(description='Setup RenderDocTools (all-in-one)')
    parser.add_argument('--skip-build', action='store_true', help='Skip building RenderDoc')
    parser.add_argument('--skip-install', action='store_true', help='Skip installing package')
    
    args = parser.parse_args()
    
    root = Path(__file__).parent
    
    print(f"\n{C_BOLD}{C_CYAN}{'=' * 70}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'RenderDocTools One-Command Setup':^70}{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}{'=' * 70}{C_RESET}\n")
    
    # Step 1: Init submodules
    print(f"{C_BOLD}[1] Initializing git submodules...{C_RESET}")
    run_cmd(['git', 'submodule', 'update', '--init', '--recursive'], cwd=root)
    print(f"{C_GREEN}[OK] Submodules initialized{C_RESET}\n")
    
    # Step 2: Check Python
    print(f"\n{C_BOLD}[2] Checking Python environment...{C_RESET}")
    run_cmd([sys.executable, str(root / 'scripts' / 'detect_python.py')])
    
    # Step 3: Build RenderDoc
    if not args.skip_build:
        print(f"\n{C_BOLD}[3] Building RenderDoc...{C_RESET}")
        print(f"{C_YELLOW}Note: Directory.Build.targets handles retargeting automatically.{C_RESET}")
        print(f"{C_YELLOW}This will take 10-30 minutes...{C_RESET}\n")
        run_cmd([sys.executable, str(root / 'scripts' / 'build.py')], cwd=root)
    else:
        print(f"\n{C_YELLOW}[3] Skipping RenderDoc build{C_RESET}\n")
    
    # Step 4: Install package
    if not args.skip_install:
        print(f"{C_BOLD}[4] Installing RenderDocTools package...{C_RESET}")
        run_cmd([sys.executable, '-m', 'pip', 'install', '-e', '.'], cwd=root)
        print(f"{C_GREEN}[OK] Package installed{C_RESET}\n")
    else:
        print(f"{C_YELLOW}[4] Skipping package install{C_RESET}\n")
    
    # Step 5: Verify
    print(f"{C_BOLD}[5] Running diagnostics...{C_RESET}\n")
    run_cmd([sys.executable, str(root / 'diagnose.py')], cwd=root, check=False)
    
    # Done!
    print(f"\n{C_BOLD}{C_GREEN}{'=' * 70}{C_RESET}")
    print(f"{C_BOLD}{C_GREEN}{'SETUP COMPLETE':^70}{C_RESET}")
    print(f"{C_BOLD}{C_GREEN}{'=' * 70}{C_RESET}\n")
    
    print(f"{C_CYAN}Next steps:{C_RESET}")
    print(f"  1. See BUILD_GUIDE.md for build options")
    print(f"  2. See MOBILE_CAPTURE_WORKFLOW.md for usage")
    print(f"  3. Start capturing: ./renderdoc/x64/Development/qrenderdoc.exe\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C_YELLOW}Setup cancelled{C_RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{C_RED}Setup failed: {e}{C_RESET}")
        sys.exit(1)
