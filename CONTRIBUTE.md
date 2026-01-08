# Contributing to RenderDoc

This document describes issues and fixes discovered while integrating RenderDoc as a submodule, which may be useful for upstream contributions.

---

## Motivation

We are building **RenderDocTools**, a Python-based tooling layer on top of RenderDoc for graphics profiling and capture analysis. As part of this effort, we integrate RenderDoc as a Git submodule and build it programmatically using MSBuild.

During this integration, we encountered several build issues that don't manifest when building manually through Visual Studio IDE. These issues affect:

- **CI/CD pipelines** - Automated builds fail
- **Reproducible builds** - Different results between IDE and command-line
- **Cross-platform tooling** - Scripts that invoke MSBuild directly
- **Developer onboarding** - New developers hit cryptic linker errors

We believe fixing these issues benefits the broader RenderDoc community:

1. **Enables reliable automation** - Build servers, GitHub Actions, and custom build scripts work correctly
2. **Reduces friction** - Developers using command-line workflows get consistent results
3. **Documents implicit assumptions** - Makes Development configuration behavior explicit
4. **Supports integration projects** - Tools like RenderDocTools that embed RenderDoc as a dependency

Our goal is to contribute these fixes upstream so future users don't encounter the same issues.

---

## Issue: Missing Build.0 Entries for Breakpad Projects in Development Configuration

### Problem Description

The breakpad projects (`breakpad_common`, `crash_generation_client`, `crash_generation_server`, `exception_handler`) have `ActiveCfg` entries for `Development|x64` and `Development|x86` configurations in `renderdoc.sln`, but are missing the corresponding `Build.0` entries.

This causes **command-line MSBuild** to skip building these projects during Development configuration, leading to linker errors when `renderdoc.dll` tries to link against the missing libraries.

### Affected Files
- `renderdoc.sln`

### Symptoms
When building with command-line MSBuild:
```bash
msbuild renderdoc.sln /p:Configuration=Development /p:Platform=x64 /m
```

Error:
```
LNK1104: cannot open file 'breakpad_common.lib'
```

### Why It Works in Visual Studio IDE

**Visual Studio IDE Behavior:**
- Honors `ProjectSection(ProjectDependencies)` declarations in project files
- Automatically builds dependencies even when `Build.0` entries are missing
- Smart dependency resolution overrides strict solution configuration

**MSBuild Command-Line Behavior:**
- Strictly follows solution configuration's `Build.0` entries
- No `Build.0` entry = project is skipped from build
- Does not automatically infer build requirements from `ProjectDependencies`

This explains why:
- ✅ Opening `renderdoc.sln` in Visual Studio and building **works**
- ❌ Running `msbuild renderdoc.sln` from command-line **fails**
- ✅ Using "Retarget Solution" in VS may auto-add `Build.0` entries

### Proposed Fix

Add `Build.0` entries for all breakpad projects in the Development configuration:

**File:** `renderdoc.sln`

**Changes needed (8 lines total):**

```diff
 {EA1242CF-BB42-B1AC-9B6A-A508D96D1CB7}.Development|x64.ActiveCfg = Development|x64
+{EA1242CF-BB42-B1AC-9B6A-A508D96D1CB7}.Development|x64.Build.0 = Development|x64
 {EA1242CF-BB42-B1AC-9B6A-A508D96D1CB7}.Development|x86.ActiveCfg = Development|Win32
+{EA1242CF-BB42-B1AC-9B6A-A508D96D1CB7}.Development|x86.Build.0 = Development|Win32
 
 {EC847717-119A-2391-0477-212E1140082C}.Development|x64.ActiveCfg = Development|x64
+{EC847717-119A-2391-0477-212E1140082C}.Development|x64.Build.0 = Development|x64
 {EC847717-119A-2391-0477-212E1140082C}.Development|x86.ActiveCfg = Development|Win32
+{EC847717-119A-2391-0477-212E1140082C}.Development|x86.Build.0 = Development|Win32
 
 {7893E300-3ED0-7F4C-158F-67EA63934C57}.Development|x64.ActiveCfg = Development|x64
+{7893E300-3ED0-7F4C-158F-67EA63934C57}.Development|x64.Build.0 = Development|x64
 {7893E300-3ED0-7F4C-158F-67EA63934C57}.Development|x86.ActiveCfg = Development|Win32
+{7893E300-3ED0-7F4C-158F-67EA63934C57}.Development|x86.Build.0 = Development|Win32
 
 {B7399F39-300F-450E-F471-9490F959D2A7}.Development|x64.ActiveCfg = Development|x64
+{B7399F39-300F-450E-F471-9490F959D2A7}.Development|x64.Build.0 = Development|x64
 {B7399F39-300F-450E-F471-9490F959D2A7}.Development|x86.ActiveCfg = Development|Win32
+{B7399F39-300F-450E-F471-9490F959D2A7}.Development|x86.Build.0 = Development|Win32
```

### Impact

**Without this fix:**
- ❌ Command-line builds fail
- ❌ CI/CD pipelines fail
- ❌ Automated build scripts fail
- ✅ Manual VS IDE builds work (due to smart dependency handling)

**With this fix:**
- ✅ Command-line builds succeed
- ✅ CI/CD pipelines work
- ✅ Automated build scripts work
- ✅ Manual VS IDE builds continue to work

### Alternative Interpretations

If omitting breakpad from Development builds was intentional (e.g., for faster builds), then:
1. Remove `ProjectSection(ProjectDependencies)` on breakpad from `renderdoc.vcxproj` for Development config
2. OR make the linker dependency on breakpad conditional on Release-only builds

However, given that:
- `renderdoc.vcxproj` declares explicit dependencies on breakpad
- The project expects these libraries to exist
- No conditional logic exists for Development vs Release

This appears to be an **unintentional omission** rather than a design decision.

---

## Submitting to Upstream

**Recommended Approach:**

1. **Title:** `Fix: Add Build.0 entries for breakpad projects in Development configuration`

2. **Description:**
   ```
   The breakpad projects have ActiveCfg entries for Development configurations 
   but are missing Build.0 entries. This causes command-line MSBuild to skip 
   building these projects, leading to linker errors.
   
   Visual Studio IDE builds work because the IDE honors ProjectDependencies 
   even without Build.0 entries, but command-line builds strictly follow the 
   solution configuration.
   
   This fix ensures consistency between IDE and command-line builds.
   ```

3. **Testing:**
   - Clean build with `msbuild renderdoc.sln /p:Configuration=Development /p:Platform=x64 /m`
   - Verify all breakpad libraries are built
   - Verify `renderdoc.dll` links successfully

---

## Questions for Maintainers

Before submitting, consider asking:
- Is crash reporting intended to be disabled in Development builds?
- If so, should the dependency structure be different?
- Are there performance reasons for the current configuration?

This ensures the fix aligns with project goals rather than just fixing the symptom.

---

## Issue: Runtime Library Mismatch Between Breakpad and RenderDoc in Development Configuration

### Problem Description

The breakpad projects are configured with **debug runtime settings** for the Development configuration, while RenderDoc uses **release-like runtime settings**. This causes `LNK2038` linker errors when linking `renderdoc.dll`.

### Root Cause

| Project | RuntimeLibrary | PreprocessorDefinitions |
|---------|----------------|------------------------|
| `renderdoc.vcxproj` | `MultiThreadedDLL` (MD) | `NDEBUG` |
| `breakpad/*.vcxproj` | `MultiThreadedDebug` (MTd) | `_DEBUG` |

This mismatch causes:
- `_ITERATOR_DEBUG_LEVEL` mismatch (2 vs 0)
- `RuntimeLibrary` mismatch (MTd vs MD)

### Symptoms

```
http_upload.obj : error LNK2038: mismatch detected for '_ITERATOR_DEBUG_LEVEL': value '2' doesn't match value '0' in catch.obj
http_upload.obj : error LNK2038: mismatch detected for 'RuntimeLibrary': value 'MTd_StaticDebug' doesn't match value 'MD_DynamicRelease' in catch.obj
```

### Affected Files

- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/common.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/crash_generation/crash_generation_client.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/crash_generation/crash_generation_server.vcxproj`
- `renderdoc/renderdoc/3rdparty/breakpad/client/windows/handler/exception_handler.vcxproj`

### Proposed Fix

In each of the 4 breakpad `.vcxproj` files, for all `Development|*` configurations:

**1. Replace `_DEBUG` with `NDEBUG` in PreprocessorDefinitions:**
```diff
-<PreprocessorDefinitions>_DEBUG;_WIN32_WINNT=0x0600;...
+<PreprocessorDefinitions>NDEBUG;_WIN32_WINNT=0x0600;...
```

**2. Replace `MultiThreadedDebug` with `MultiThreadedDLL` in RuntimeLibrary:**
```diff
-<RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>
+<RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>
```

### Impact

**Without this fix:**
- ❌ Development builds fail with LNK2038 errors
- ❌ Cannot build renderdoc.dll in Development config

**With this fix:**
- ✅ Development builds succeed
- ✅ Breakpad runtime matches RenderDoc runtime
- ⚠️ Breakpad loses debug-specific features in Development builds

### Design Consideration

RenderDoc's "Development" configuration is a **hybrid** - it's meant for faster iteration with debug symbols but uses release runtime (`MD`). The breakpad projects were not updated to match this philosophy.

**Question for maintainers:** Should breakpad maintain debug runtime in Development config for better crash debugging, or should it match RenderDoc's settings for link compatibility?

---

## Issue: Missing Breakpad Library Dependencies in renderdoc.vcxproj

### Problem Description

The breakpad libraries depend on several Windows SDK libraries (`wininet.lib`, `version.lib`, `msimg32.lib`, `usp10.lib`) for HTTP upload and system information functionality. Since breakpad is built as static libraries, these dependencies must be specified in the final consuming project (`renderdoc.vcxproj`) rather than in the breakpad project files themselves.

### Affected Files

- `renderdoc/renderdoc/renderdoc.vcxproj`

### Symptoms

When linking `renderdoc.dll`:
```
LNK2019: unresolved external symbol __imp_InternetOpenW referenced in function ...
LNK2019: unresolved external symbol __imp_HttpSendRequestW referenced in function ...
LNK2019: unresolved external symbol __imp_GetFileVersionInfoW referenced in function ...
```

### Proposed Fix

Add the missing libraries to `AdditionalDependencies` in `renderdoc.vcxproj`:

**File:** `renderdoc/renderdoc/renderdoc.vcxproj` (line ~82)

```diff
 <AdditionalDependencies>
-  ws2_32.lib;kernel32.lib;user32.lib;shlwapi.lib;setupapi.lib;%(AdditionalDependencies)
+  ws2_32.lib;kernel32.lib;user32.lib;shlwapi.lib;setupapi.lib;wininet.lib;version.lib;msimg32.lib;usp10.lib;%(AdditionalDependencies)
 </AdditionalDependencies>
```

### Impact

**Without this fix:**
- ❌ Linker errors for unresolved Windows API symbols

**With this fix:**
- ✅ All breakpad functionality (crash reporting, HTTP upload) works correctly
- ✅ Clean linking of renderdoc.dll

---

## Summary of All Fixes

| # | Issue | Fix Location | Type |
|---|-------|--------------|------|
| 1 | Missing `Build.0` entries | `renderdoc.sln` | Solution config |
| 2 | Runtime library mismatch | 4 breakpad `.vcxproj` files | Project config |
| 3 | Missing library dependencies | `renderdoc.vcxproj` | Linker config |

---

## Submitting to Upstream

**Recommended Approach:**

1. **Issue Title:** `Fix: Development configuration build issues with breakpad`

2. **Description:**
   ```
   This PR fixes three related issues that prevent command-line MSBuild from 
   building RenderDoc in Development configuration:
   
   1. Add Build.0 entries for breakpad projects in solution file
   2. Align breakpad runtime library and preprocessor settings with renderdoc
   3. Add missing Windows SDK library dependencies for breakpad
   
   These issues don't manifest in Visual Studio IDE but break CI/CD and 
   automated build scripts.
   ```

3. **Testing:**
   - Clean build: `msbuild renderdoc.sln /p:Configuration=Development /p:Platform=x64 /m`
   - Verify all projects build successfully
   - Verify `renderdoc.dll` links without errors

