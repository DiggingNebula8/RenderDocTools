# Install Python 3.6 for RenderDoc Meta Fork

## Why Python 3.6?

RenderDoc Meta Fork includes `python36.dll`, indicating it was built for **Python 3.6**. The Python module requires the exact version it was compiled for.

## Installation Options

### Option 1: Download Python 3.6.15 (Recommended)

1. Download Python 3.6.15 from:
   https://www.python.org/downloads/release/python-3615/

2. Run the installer:
   - Check "Add Python 3.6 to PATH"
   - Choose "Install Now"

3. Verify installation:
   ```powershell
   python3.6 --version
   # Should show: Python 3.6.15
   ```

4. Create venv:
   ```powershell
   python3.6 -m venv venv36
   .\venv36\Scripts\Activate.ps1
   ```

### Option 2: Use Scoop (if available)

```powershell
scoop bucket add versions
scoop install versions/python36
```

### Option 3: Portable Python 3.6

If you don't want to install system-wide:
1. Download portable Python 3.6
2. Extract to a folder
3. Use full path: `C:\path\to\python36\python.exe -m venv venv36`

## After Installation

Once Python 3.6 is installed:

```powershell
# Create venv with Python 3.6
python3.6 -m venv venv36

# Activate
.\venv36\Scripts\Activate.ps1

# Test RenderDoc import
python test_renderdoc.py

# Should work now!
python -m renderdoc_tools.cli workflow 2.rdc --preset quick
```

## Why Not Python 3.9?

Even though Python 3.9 is supposed to be backward compatible, RenderDoc's Python module (`renderdoc.pyd`) was compiled against Python 3.6's C API. The ABI (Application Binary Interface) differences can cause:
- Import hangs
- DLL loading failures
- Runtime crashes

Using Python 3.6 ensures perfect compatibility.


