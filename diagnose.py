"""
Diagnostic script for RenderDocTools installation.

Checks the setup and provides actionable fixes.
"""
import sys
import os
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a styled header."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")


def print_check(passed, message, fix_hint=None):
    """Print a check result with optional fix hint."""
    if passed:
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
    else:
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
        if fix_hint:
            print(f"  {Colors.YELLOW}→ Fix:{Colors.RESET} {fix_hint}")


def check_python_version():
    """Check if Python 3.6 is being used."""
    version = sys.version_info
    is_36 = version.major == 3 and version.minor == 6
    
    print_check(
        is_36,
        f"Python version: {version.major}.{version.minor}.{version.micro}",
        "Install Python 3.6 (see INSTALL_PYTHON36.md)" if not is_36 else None
    )
    return is_36


def check_virtual_environment():
    """Check if running in a virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    venv_path = Path("venv36")
    venv_exists = venv_path.exists()
    
    print_check(
        in_venv or venv_exists,
        "Virtual environment (venv36)",
        "Run: .\\setup.ps1 to create venv36" if not venv_exists else
        "   Activate with: .\\venv36\\Scripts\\Activate.ps1" if not in_venv else None
    )
    return in_venv or venv_exists


def check_package_installed():
    """Check if renderdoc_tools package is installed."""
    try:
        import renderdoc_tools
        version = getattr(renderdoc_tools, '__version__', 'unknown')
        print_check(True, f"Package installed: v{version}")
        return True
    except ImportError:
        print_check(
            False,
            "Package not installed",
            "Run: pip install -e . (in venv36)"
        )
        return False


def check_renderdoc():
    """Check if RenderDoc can be found and imported."""
    try:
        # Try to use the package's detector
        from renderdoc_tools.utils.renderdoc_detector import find_renderdoc_installations
        installations = find_renderdoc_installations()
        
        if installations:
            for inst in installations:
                print_check(
                    True,
                    f"RenderDoc found: {inst['name']} at {inst['path']}"
                )
            return True
        else:
            print_check(
                False,
                "RenderDoc not found",
                "Install RenderDoc or RenderDoc Meta Fork"
            )
            return False
    except ImportError:
        print_check(
            False,
            "Cannot check RenderDoc (package not installed)",
            "Install package first: pip install -e ."
        )
        return False
    except Exception as e:
        print_check(
            False,
            f"RenderDoc check failed: {e}",
            "Check RenderDoc installation"
        )
        return False


def check_wrapper_scripts():
    """Check if wrapper scripts exist."""
    wrappers = {
        "PowerShell": Path("rdc-tools.ps1"),
        "CMD": Path("rdc-tools.bat"),
        "Bash": Path("rdc-tools.sh")
    }
    
    all_exist = True
    for name, path in wrappers.items():
        exists = path.exists()
        all_exist = all_exist and exists
        print_check(
            exists,
            f"Wrapper script: {name} ({path})",
            f"File missing: {path}" if not exists else None
        )
    
    return all_exist


def run_diagnostics():
    """Run all diagnostic checks."""
    print_header("RenderDocTools Diagnostics")
    
    print(f"{Colors.BOLD}Running checks...{Colors.RESET}\n")
    
    results = {
        "Python 3.6": check_python_version(),
        "Virtual Environment": check_virtual_environment(),
        "Package Installed": check_package_installed(),
        "RenderDoc": check_renderdoc(),
        "Wrapper Scripts": check_wrapper_scripts()
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed ({passed}/{total}){Colors.RESET}")
        print(f"\n{Colors.CYAN}You're ready to use RenderDocTools!{Colors.RESET}")
        print(f"\nTry: {Colors.BOLD}rdc-tools workflow --list-presets{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠ {passed}/{total} checks passed{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Please fix the issues above.{Colors.RESET}")
        print(f"\n{Colors.CYAN}Quick fix:{Colors.RESET} Run {Colors.BOLD}.\\setup.ps1{Colors.RESET} to auto-setup")
    
    return passed == total


def auto_fix():
    """Attempt to automatically fix common issues."""
    print_header("Auto-Fix Mode")
    
    print(f"{Colors.YELLOW}Attempting to fix issues...{Colors.RESET}\n")
    
    # Check if venv exists
    venv_path = Path("venv36")
    if not venv_path.exists():
        print(f"{Colors.CYAN}Creating virtual environment...{Colors.RESET}")
        # This would be risky to do automatically because Python 3.6 may not be found
        print(f"{Colors.YELLOW}Cannot auto-fix: Please run .\\setup.ps1{Colors.RESET}")
        return False
    
    # Check if package is installed
    try:
        import renderdoc_tools
    except ImportError:
        print(f"{Colors.CYAN}Installing package...{Colors.RESET}")
        try:
            subprocess.check_call([
                str(venv_path / "Scripts" / "python.exe"),
                "-m", "pip", "install", "-e", "."
            ])
            print(f"{Colors.GREEN}✓ Package installed{Colors.RESET}")
        except subprocess.CalledProcessError:
            print(f"{Colors.RED}✗ Failed to install package{Colors.RESET}")
            return False
    
    print(f"\n{Colors.GREEN}Auto-fix complete. Re-running diagnostics...{Colors.RESET}")
    return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Diagnose RenderDocTools installation issues"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to automatically fix issues"
    )
    
    args = parser.parse_args()
    
    if args.fix:
        if auto_fix():
            print("\n")
            run_diagnostics()
    else:
        success = run_diagnostics()
        
        if not success:
            print(f"\n{Colors.CYAN}Tip:{Colors.RESET} Run with {Colors.BOLD}--fix{Colors.RESET} to attempt auto-repair:")
            print(f"  {Colors.BOLD}python diagnose.py --fix{Colors.RESET}")
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
