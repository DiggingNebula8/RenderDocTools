# Build & Setup Guide

## 🚀 Quick Start (One Command)

Build RenderDoc with your current Python (works with any 3.8+):

```bash
python scripts/build.py
```

That's it! The build system:
- ✅ Auto-detects your Python version (3.11, 3.14, etc.)
- ✅ Configures RenderDoc to use it
- ✅ Builds everything
- ✅ No hardcoded paths

---

## 📋 Prerequisites

1. **Visual Studio 2019 or 2022** (with C++ Desktop Development workload)
2. **Python 3.8+** (any version - auto-detected)
3. **Git** (for submodules)

**Note**: RenderDoc on Windows uses Visual Studio solution files (MSBuild), not CMake.

---

## 🔧 Build Options

```bash
# Development build (default - includes debug symbols and faster iteration)
python scripts/build.py

# Clean build (removes output directory first)
python scripts/build.py --clean

# Release build (optimized, smaller binaries)
python scripts/build.py --release

# Just verify configuration (don't build)
python scripts/build.py --config-only
```

---

## 📁 Project Structure

```
RenderDocTools/
├── renderdoc/                  # Git submodule
│   ├── x64/Development/        # Build output (auto-created)
│   │   ├── qrenderdoc.exe
│   │   ├── renderdoc.dll
│   │   ├── pymodules/
│   │   │   └── renderdoc.pyd
│   │   └── python3XX.dll       # Your Python version
│   └── build/                  # CMake build files
├── renderdoc_tools/            # Python package
│   └── utils/
│       ├── renderdoc_detector.py  # Finds local build (relative paths)
│       └── renderdoc_loader.py    # Loads module with DLL handling
└── scripts/
    ├── detect_python.py        # Auto-detect Python
    └── build.py                # Build RenderDoc
```

---

## ✅ Verification

After building:

```bash
# Check what Python was detected
python scripts/detect_python.py

# Run full diagnostics
python diagnose.py

# Test RenderDoc module
python test_import.py
```

---

## 🎯 How It Works

### Version-Agnostic Design

1. **Python Detection**: `scripts/detect_python.py`
   - Reads `sys.version_info`, `sys.executable`
   - Finds pythonXX.dll, pythonXX.lib
   - No hardcoded versions!

2. **Build Process**: `scripts/build.py` (Windows)
   - Finds MSBuild via vswhere or common paths
   - Uses `renderdoc.sln` (Visual Studio solution)
   - Builds with detected Python version
   - Copies pythonXX.dll to output directory
   - Works with 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14...

3. **Module Loading**: `renderdoc_loader.py`
   - Uses relative paths to local build
   - Adds DLL directory for current Python
   - Fallback to system RenderDoc if needed

### Priority Order

Detector searches in this order:
1. **Local submodule** (`./renderdoc/x64/Development`) ← HIGHEST
2. Custom dev paths (backward compat)
3. System installation (`C:\Program Files\RenderDoc`)

---

## 🔍 Troubleshooting

### Build Fails

```bash
# Check Python is detected correctly
python scripts/detect_python.py

# Should show:
# ✓ Python environment is valid for RenderDoc build
```

### Python DLL Not Found

Ensure you have a standard Python installation with:
- `python3XX.dll` (in Python root)
- `python3XX.lib` (in Python/libs/)

### CMake Not Found

Install CMake: https://cmake.org/download/

---

## 📦 After Building

Install RenderDocTools:

```bash
pip install -e .
```

Use it:

```bash
python -m renderdoc_tools.cli.entry_point workflow capture.rdc --quick
```

---

## 🌟 Benefits

✅ **Portable**: No absolute paths, works anywhere  
✅ **Version-Agnostic**: Works with any Python 3.8+  
✅ **Reproducible**: Anyone can clone and build  
✅ **CI-Ready**: Can be automated  
✅ **Intuitive**: One command to build everything
