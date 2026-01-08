# RenderDoc Build Fixes - Technical Reference

This document explains the build issues encountered when integrating RenderDoc as a submodule and how they are resolved. Use this as context for future development sessions.

---

## Overview

RenderDoc's build system has several issues that only manifest when building via **command-line MSBuild** (not Visual Studio IDE). These affect CI/CD pipelines, automated builds, and developer workflows.

### Summary of Fixes

| # | Issue | Root Cause | Fix Location |
|---|-------|------------|--------------|
| 1 | Missing breakpad libraries | Static lib deps not propagated | `renderdoc.vcxproj` |
| 2 | Runtime library mismatch | Breakpad uses MTd, RenderDoc uses MD | 4 breakpad `.vcxproj` files |
| 3 | Python version hardcoded | No env var for custom Python | `scripts/build.py` |

---

## Issue 1: Missing Breakpad Library Dependencies

### Problem
Breakpad's `http_upload.cc` uses Windows Internet APIs but since breakpad compiles as static libraries (`.lib`), its dependencies must be linked by the final consumer (`renderdoc.dll`).

### Symptom
```
LNK2019: unresolved external symbol __imp_InternetOpenW
LNK2019: unresolved external symbol __imp_HttpSendRequestW
```

### Fix
**File:** `renderdoc/renderdoc/renderdoc.vcxproj` (line ~82)

Add these libraries to `<AdditionalDependencies>`:
```xml
wininet.lib;version.lib;msimg32.lib;usp10.lib
```

### Why This Works
- `wininet.lib` - HTTP upload functionality
- `version.lib` - File version info APIs
- `msimg32.lib` - Image manipulation
- `usp10.lib` - Unicode script processing

---

## Issue 2: Runtime Library Mismatch (LNK2038)

### Problem
RenderDoc's `Development` configuration is a **hybrid** - debug symbols with release runtime:
- Uses `NDEBUG` (release preprocessor)
- Uses `MultiThreadedDLL` (MD, release runtime)

But breakpad's Development config uses debug settings:
- Uses `_DEBUG` (debug preprocessor)  
- Uses `MultiThreadedDebug` (MTd, debug runtime)

This causes `_ITERATOR_DEBUG_LEVEL` mismatch.

### Symptom
```
LNK2038: mismatch detected for '_ITERATOR_DEBUG_LEVEL': value '2' doesn't match value '0'
LNK2038: mismatch detected for 'RuntimeLibrary': value 'MTd_StaticDebug' doesn't match value 'MD_DynamicRelease'
```

### Fix
**Files (4 total):**
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/common.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/crash_generation/crash_generation_client.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/crash_generation/crash_generation_server.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/handler/exception_handler.vcxproj`

**Changes in each file:**
1. Replace `_DEBUG;` with `NDEBUG;` in PreprocessorDefinitions
2. Replace `<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>` with `<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>`

### PowerShell One-Liner
```powershell
@('common.vcxproj', 'crash_generation\crash_generation_client.vcxproj', 'crash_generation\crash_generation_server.vcxproj', 'handler\exception_handler.vcxproj') | ForEach-Object { 
  $path = ".\renderdoc\renderdoc\3rdparty\breakpad\client\windows\$_"
  $content = Get-Content $path -Raw
  $content = $content -replace '_DEBUG;', 'NDEBUG;'
  $content = $content -replace '<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>', '<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>'
  Set-Content $path $content -NoNewline
}
```

---

## Issue 3: Python Version Detection

### Problem
RenderDoc's build system looks for Python via:
1. `VSPythonOverridePath` MSBuild property
2. `RENDERDOC_PYTHON_PREFIX64` environment variable
3. Falls back to bundled Python 3.6

Without setting the env var, it always builds against Python 3.6.

### How It Works
**File:** `renderdoc/qrenderdoc/Code/pyrenderdoc/python.props`

This file checks for Python installations in order:
```
315, 314, 313, 312, 311, 310, 39, 38, 37, 36, 35, 34
```

For each version, it checks if these files exist at `$(PythonOverride)`:
- `include/Python.h`
- `pythonXY.zip`
- `pythonXY.lib` (or `libs/pythonXY.lib`)

### Fix
**File:** `scripts/build.py`

Set `RENDERDOC_PYTHON_PREFIX64` environment variable before calling MSBuild:
```python
build_env = os.environ.copy()
build_env['RENDERDOC_PYTHON_PREFIX64'] = py_info['prefix']
subprocess.run(msbuild_args, env=build_env, ...)
```

### Result
Build output shows:
```
Built against python from C:\Users\...\python\current
```

---

## Build Process Flow

```
1. python setup_all.py
   │
   ├── git submodule update --init --recursive
   │
   ├── python scripts/detect_python.py
   │   └── Detects Python version, DLL path, prefix
   │
   ├── python scripts/retarget.py
   │   └── Runs devenv /Upgrade to retarget to current VS
   │
   ├── [MANUAL] Apply breakpad fixes (PowerShell one-liner)
   │
   └── python scripts/build.py
       ├── Sets RENDERDOC_PYTHON_PREFIX64
       ├── Calls MSBuild with env
       └── Copies Python DLL to output
```

---

## Important Notes

### After Retargeting
The `devenv /Upgrade` step in `retarget.py` **resets breakpad project files** to their original state. You must re-apply the breakpad fixes after retargeting.

### Files Modified in Submodule
These files in `renderdoc/` are modified:
- `renderdoc/renderdoc.vcxproj` - Added library dependencies
- 4 breakpad `.vcxproj` files - Runtime library fix

Consider submitting these as upstream PRs (see `CONTRIBUTE.md`).

### Visual Studio vs MSBuild
- **VS IDE**: Works due to implicit configuration propagation
- **MSBuild CLI**: Requires explicit Build.0 entries and matching runtime libraries

---

## Quick Reference Commands

### Clean Build
```powershell
Remove-Item -Recurse -Force .\renderdoc\x64\Development -ErrorAction SilentlyContinue
python scripts/build.py
```

### Apply All Fixes After Revert
```powershell
# 1. Add libraries to renderdoc.vcxproj (manual or via agent)

# 2. Fix breakpad projects
@('common.vcxproj', 'crash_generation\crash_generation_client.vcxproj', 'crash_generation\crash_generation_server.vcxproj', 'handler\exception_handler.vcxproj') | ForEach-Object { 
  $path = ".\renderdoc\renderdoc\3rdparty\breakpad\client\windows\$_"
  $content = Get-Content $path -Raw
  $content = $content -replace '_DEBUG;', 'NDEBUG;'
  $content = $content -replace '<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>', '<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>'
  Set-Content $path $content -NoNewline
  Write-Host "Fixed: $_"
}

# 3. Build
python scripts/build.py
```

### Verify Python Version
Launch `qrenderdoc.exe`, open Window → Python Shell, check version in header.
