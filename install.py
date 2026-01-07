"""
Cross-platform Python installer for RenderDocTools.

This script provides a Python-based installation fallback
if PowerShell scripts are unavailable or don't work.
"""
import sys
import os
import subprocess
import platform
from pathlib import Path


class Colors:
    """ANSI color codes (disabled on Windows cmd)."""
    if platform.system() != "Windows" or os.getenv("WT_SESSION"):
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        CYAN = '\033[96m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
    else:
        GREEN = YELLOW = RED = CYAN = RESET = BOLD = ''


def print_status(message, level="info"):
    """Print styled status message."""
    if level == "success":
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
    elif level == "error":
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
    elif level == "warning":
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {message}")
    else:
        print(f"{Colors.CYAN}→{Colors.RESET} {message}")


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")


def find_python36():
    """Find Python 3.6 installation."""
    print_status("Searching for Python 3.6...")
    
    # Common Python 3.6 command names
    candidates = ["python3.6", "python36", "python"]
    
    # Common installation paths (Windows)
    if platform.system() == "Windows":
        candidates.extend([
            Path(os.path.expanduser("~")) / "scoop/apps/python36/current/python.exe",
            Path("C:/Python36/python.exe"),
            Path("C:/Program Files/Python36/python.exe"),
        ])
    
    for candidate in candidates:
        try:
            # Try as command
            if isinstance(candidate, str):
                result = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and "3.6" in result.stdout:
                    print_status(f"Found: {candidate} ({result.stdout.strip()})", "success")
                    return candidate
            # Try as path
            elif candidate.exists():
                result = subprocess.run(
                    [str(candidate), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and "3.6" in result.stdout:
                    print_status(f"Found: {candidate} ({result.stdout.strip()})", "success")
                    return str(candidate)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue
    
    return None


def create_venv(python_exe):
    """Create Python 3.6 virtual environment."""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv36")
    
    if venv_path.exists():
        print_status(f"Virtual environment already exists: {venv_path}", "warning")
        response = input(f"{Colors.YELLOW}Recreate? (y/N):{Colors.RESET} ").lower()
        if response != 'y':
            return True
        
        # Remove existing venv
        import shutil
        shutil.rmtree(venv_path)
    
    print_status(f"Creating venv36 with {python_exe}...")
    
    try:
        subprocess.run(
            [python_exe, "-m", "venv", "venv36"],
            check=True
        )
        print_status("Virtual environment created successfully", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to create virtual environment: {e}", "error")
        return False


def install_package():
    """Install the package in editable mode."""
    print_header("Installing Package")
    
    # Determine pip path
    if platform.system() == "Windows":
        pip_exe = Path("venv36/Scripts/pip.exe")
        python_exe = Path("venv36/Scripts/python.exe")
    else:
        pip_exe = Path("venv36/bin/pip")
        python_exe = Path("venv36/bin/python")
    
    if not pip_exe.exists():
        print_status(f"Pip not found: {pip_exe}", "error")
        return False
    
    # Upgrade pip first
    print_status("Upgrading pip...")
    try:
        subprocess.run(
            [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
    except subprocess.CalledProcessError:
        print_status("Failed to upgrade pip (continuing anyway)", "warning")
    
    # Install package
    print_status("Installing renderdoc-tools...")
    try:
        subprocess.run(
            [str(pip_exe), "install", "-e", "."],
            check=True
        )
        print_status("Package installed successfully", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install package: {e}", "error")
        return False


def verify_installation():
    """Verify the installation."""
    print_header("Verifying Installation")
    
    # Determine python path
    if platform.system() == "Windows":
        python_exe = Path("venv36/Scripts/python.exe")
    else:
        python_exe = Path("venv36/bin/python")
    
    try:
        result = subprocess.run(
            [str(python_exe), "-c", "import renderdoc_tools; print(renderdoc_tools.__version__)"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_status(f"Package version: {version}", "success")
        return True
    except subprocess.CalledProcessError:
        print_status("Package verification failed", "error")
        return False


def show_next_steps():
    """Show next steps to user."""
    print_header("Installation Complete!")
    
    print(f"{Colors.GREEN}✓ RenderDocTools is ready to use{Colors.RESET}\n")
    
    print(f"{Colors.CYAN}Next steps:{Colors.RESET}\n")
    
    if platform.system() == "Windows":
        print(f"1. Use the wrapper script (recommended):")
        print(f"   {Colors.BOLD}.\\rdc-tools.ps1 workflow capture.rdc --preset quick{Colors.RESET}\n")
        print(f"2. Or activate the virtual environment:")
        print(f"   {Colors.BOLD}.\\venv36\\Scripts\\Activate.ps1{Colors.RESET}")
        print(f"   {Colors.BOLD}rdc-tools workflow --list-presets{Colors.RESET}\n")
    else:
        print(f"1. Use the wrapper script (recommended):")
        print(f"   {Colors.BOLD}./rdc-tools.sh workflow capture.rdc --preset quick{Colors.RESET}\n")
        print(f"2. Or activate the virtual environment:")
        print(f"   {Colors.BOLD}source venv36/bin/activate{Colors.RESET}")
        print(f"   {Colors.BOLD}rdc-tools workflow --list-presets{Colors.RESET}\n")
    
    print(f"3. Verify setup:")
    print(f"   {Colors.BOLD}python diagnose.py{Colors.RESET}\n")


def main():
    """Main installation flow."""
    print_header("RenderDocTools Installer")
    
    print(f"{Colors.CYAN}This script will:{Colors.RESET}")
    print("  1. Find Python 3.6")
    print("  2. Create virtual environment (venv36)")
    print("  3. Install the package")
    print("  4. Verify installation\n")
    
    # Step 1: Find Python 3.6
    python36 = find_python36()
    
    if not python36:
        print_status("Python 3.6 not found", "error")
        print(f"\n{Colors.YELLOW}Install Python 3.6:{Colors.RESET}")
        print(f"  • Download: https://www.python.org/downloads/release/python-3615/")
        if platform.system() == "Windows":
            print(f"  • Or via Scoop: {Colors.BOLD}scoop bucket add versions; scoop install versions/python36{Colors.RESET}")
        print(f"\nSee INSTALL_PYTHON36.md for detailed instructions.")
        sys.exit(1)
    
    # Step 2: Create venv
    if not create_venv(python36):
        sys.exit(1)
    
    # Step 3: Install package
    if not install_package():
        sys.exit(1)
    
    # Step 4: Verify
    if not verify_installation():
        print_status("Verification failed, but package may still work", "warning")
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Installation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
