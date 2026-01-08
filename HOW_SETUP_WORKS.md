# How Setup Works

This document explains how `setup_all.py` builds RenderDoc with your Python version.

---

## Overview

```
setup_all.py
    │
    ├─► Initialize Git Submodules
    │       └── Fetches RenderDoc source code
    │
    ├─► Detect Python Environment  
    │       └── Finds Python DLL, headers, and libs
    │
    ├─► Retarget Solution
    │       └── Updates Visual Studio toolset to your version
    │
    └─► Build RenderDoc
            ├── Sets RENDERDOC_PYTHON_PREFIX64 env var
            ├── Calls MSBuild with your Python paths
            └── Copies Python DLL to output
```

---

## Step 1: Git Submodules

```bash
git submodule update --init --recursive
```

Downloads the RenderDoc repository into `renderdoc/` folder.

---

## Step 2: Python Detection

**Script:** `scripts/detect_python.py`

Detects your active Python and locates:

| Item | Example |
|------|---------|
| Version | `3.14.2` |
| DLL | `C:\Users\...\python314.dll` |
| Headers | `C:\Users\...\Include\Python.h` |
| Library | `C:\Users\...\libs\python314.lib` |
| Prefix | `C:\Users\...\python\current` |

**Why it matters:** RenderDoc's Python bindings must be compiled against your exact Python ABI.

---

## Step 3: Retarget Solution

**Script:** `scripts/retarget.py`

Runs Visual Studio's upgrade tool:
```
devenv /Upgrade renderdoc.sln
```

Updates all projects to use your installed Visual Studio toolset (e.g., v143 for VS 2022).

---

## Step 4: Build RenderDoc

**Script:** `scripts/build.py`

### Key: Python Prefix Environment Variable

RenderDoc's build system (`python.props`) looks for custom Python via:
```
RENDERDOC_PYTHON_PREFIX64 = C:\Users\...\python\current
```

The build script sets this before calling MSBuild:
```python
build_env['RENDERDOC_PYTHON_PREFIX64'] = python_prefix
subprocess.run(msbuild_args, env=build_env)
```

### Build Command
```
MSBuild renderdoc.sln /p:Configuration=Development /p:Platform=x64 /m
```

### Output
```
renderdoc/x64/Development/
├── renderdoc.dll       # Core library
├── qrenderdoc.exe      # GUI application
├── renderdoccmd.exe    # Command-line tool
├── python314.dll       # Your Python runtime
└── ...
```

---

## How RenderDoc Finds Python

**File:** `renderdoc/qrenderdoc/Code/pyrenderdoc/python.props`

This MSBuild props file searches for Python versions in order:
```
315 → 314 → 313 → 312 → 311 → 310 → 39 → 38 → 37 → 36 → 35 → 34
```

For each version, it checks if these exist at `$(RENDERDOC_PYTHON_PREFIX64)`:
- `include/Python.h`
- `pythonXY.zip`
- `pythonXY.lib` or `libs/pythonXY.lib`

When found, it sets:
- `$(PythonMajorMinor)` = e.g., `314`
- `$(PythonIncludeDir)` = path to headers
- `$(PythonImportLib)` = path to .lib file

---

## Build Artifacts

After successful build:

| File | Purpose |
|------|---------|
| `renderdoc.dll` | Core rendering capture/replay library |
| `qrenderdoc.exe` | Qt-based GUI application |
| `renderdoccmd.exe` | Command-line capture tool |
| `python314.dll` | Python runtime (your version) |
| `renderdoc.pyd` | Python extension module |

---

## Known Issues & Fixes

### Issue 1: Breakpad Library Dependencies
Breakpad uses `wininet.lib`, `version.lib`, etc., but as a static library, these must be linked by `renderdoc.dll`.

**Fix:** Added to `renderdoc.vcxproj`:
```xml
<AdditionalDependencies>...;wininet.lib;version.lib;msimg32.lib;usp10.lib</AdditionalDependencies>
```

### Issue 2: Runtime Library Mismatch
Breakpad uses debug runtime (`MTd`) but RenderDoc Development config uses release runtime (`MD`).

**Fix:** Changed in 4 breakpad vcxproj files:
- `_DEBUG` → `NDEBUG`
- `MultiThreadedDebug` → `MultiThreadedDLL`

See [BUILD_FIXES.md](BUILD_FIXES.md) for complete details.

---

## Verifying Setup

### Check Python Version in RenderDoc
1. Launch `renderdoc/x64/Development/qrenderdoc.exe`
2. Open **Window → Python Shell**
3. Verify the header shows your Python version:
   ```
   RenderDoc Python console, powered by python 3.14.2
   ```

### Run Diagnostics
```bash
python diagnose.py
```

---

## Manual Build (Advanced)

If you need to rebuild manually:

```powershell
# 1. Set Python prefix
$env:RENDERDOC_PYTHON_PREFIX64 = "C:\path\to\python"

# 2. Build
& "C:\...\MSBuild.exe" .\renderdoc\renderdoc.sln /p:Configuration=Development /p:Platform=x64 /m
```

---

## Related Documentation

- [BUILD_FIXES.md](BUILD_FIXES.md) - Detailed fix documentation
- [CONTRIBUTE.md](CONTRIBUTE.md) - Upstream contribution guide
