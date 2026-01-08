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
    """Check if Python 3.8+ is being used."""
    version = sys.version_info
    is_38_plus = version.major == 3 and version.minor >= 8
    
    print_check(
        is_38_plus,
        f"Python version: {version.major}.{version.minor}.{version.micro}",
        "Python 3.8+ required. See PYTHON_VERSIONS.md" if not is_38_plus else None
    )
    return is_38_plus


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
            "Run: pip install -e ."
        )
        return False


def check_renderdoc():
    """Check if RenderDoc can be found and imported."""
   try:
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
                "Install RenderDoc"
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


def check_cli_command():
    """Check if rdc-tools command is available."""
    try:
        result = subprocess.run(
            ["rdc-tools", "--help"],
            capture_output=True,
            timeout=5
        )
        success = result.returncode == 0
        print_check(
            success,
            "rdc-tools command available",
            "Reinstall: pip install -e ." if not success else None
        )
        return success
    except Exception:
        print_check(
            False,
            "rdc-tools command not available",
            "Reinstall: pip install -e ."
        )
        return False


def run_diagnostics():
    """Run all diagnostic checks."""
    print_header("RenderDocTools Diagnostics")
    
    print(f"{Colors.BOLD}Running checks...{Colors.RESET}\n")
    
    results = {
        "Python 3.8+": check_python_version(),
        "Package Installed": check_package_installed(),
        "RenderDoc": check_renderdoc(),
        "CLI Command": check_cli_command()
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
        print(f"\n{Colors.CYAN}Quick fix:{Colors.RESET} Run {Colors.BOLD}pip install -e .{Colors.RESET}")
    
    return passed == total


def auto_fix():
    """Attempt to automatically fix common issues."""
    print_header("Auto-Fix Mode")
    
    print(f"{Colors.YELLOW}Attempting to fix issues...{Colors.RESET}\n")
    
    # Check if package is installed
    try:
        import renderdoc_tools
    except ImportError:
        print(f"{Colors.CYAN}Installing package...{Colors.RESET}")
        try:
            subprocess.check_call([
                sys.executable,
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
