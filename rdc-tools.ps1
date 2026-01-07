# Convenience wrapper script for rdc-tools
# Automatically activates venv36 and runs rdc-tools command

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Check if venv36 exists
if (-not (Test-Path "venv36\Scripts\Activate.ps1")) {
    Write-Host "ERROR: venv36 not found!" -ForegroundColor Red
    Write-Host "Run .\setup_venv.ps1 first to create the virtual environment" -ForegroundColor Yellow
    exit 1
}

# Run the installed entry point directly
& "venv36\Scripts\rdc-tools.exe" $Arguments

