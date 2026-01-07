@echo off
REM Convenience wrapper script for rdc-tools (Windows batch)
REM Automatically activates venv36 and runs rdc-tools command

if not exist "venv36\Scripts\activate.bat" (
    echo ERROR: venv36 not found!
    echo Run setup_venv.ps1 first to create the virtual environment
    exit /b 1
)

call venv36\Scripts\activate.bat
rdc-tools %*
deactivate

