# RenderDocTools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Open-source parser for extracting structured data from RenderDoc capture files (.rdc) to JSON and CSV formats.

---

## Quick Start

```bash
# 1. Clone and setup
git clone --recursive git@github.com:DiggingNebula8/renderdoc.git
cd RenderDocTools
python setup_all.py

# 2. Use it
rdc-tools workflow capture.rdc --quick
```

**That's it!** The setup script builds RenderDoc with your Python version and installs everything automatically.

---

## Features

- **Extract draw calls, dispatches, and all actions**
- **Export resources** (textures, buffers) with metadata
- **Extract shaders** and reflection data
- **Pipeline state** extraction per event (optional)
- **JSON and CSV output** formats
- **API-agnostic** (D3D11, D3D12, Vulkan, OpenGL)
- **Streamlined workflow presets** (quick, full, performance)
- **Type-safe** data models using Pydantic
- **Modular architecture** - plugin-ready extractors/exporters

## Setup

### Requirements

- **Python 3.8+** (any version - auto-detected)
- **Visual Studio 2019/2022** with C++ Desktop Development workload
- **Git** (for submodules)

### One-Command Setup

```bash
python setup_all.py
```

This command:
1. **Initializes submodules** - downloads RenderDoc source
2. **Detects your Python** - finds DLL, headers, and libs
3. **Retargets solution** - updates to your Visual Studio version
4. **Builds RenderDoc** - compiles with your Python version
5. **Installs tools** - `pip install -e .`

**Build time:** 10-30 minutes (first build only)

> [!NOTE]
> **Python Version Flexibility**: RenderDocTools automatically builds RenderDoc with YOUR Python version (3.8-3.14+). No need to install a specific version!

### What Gets Built

```
renderdoc/x64/Development/
├── qrenderdoc.exe     # GUI application
├── renderdoccmd.exe   # Command-line tool  
├── renderdoc.dll      # Core library
└── python314.dll      # Your Python runtime
```

See [HOW_SETUP_WORKS.md](HOW_SETUP_WORKS.md) for technical details.

---

## Android Support

To capture from Android devices, build the Android APK separately:

```bash
# In WSL2/Linux
cd /mnt/c/Users/<user>/dev/RD/RenderDocTools/renderdoc
mkdir build-android-arm64 && cd build-android-arm64
cmake -DBUILD_ANDROID=On -DANDROID_ABI=arm64-v8a \
      -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
      -G "Unix Makefiles" ..
make -j$(nproc)

# Copy APK to Windows
cp bin/*.apk ../x64/Development/
```

See [AndroidSupportLinux.md](AndroidSupportLinux.md) for complete setup guide.


## Usage

### Workflow Presets

| Command | Output | Use Case |
|---------|--------|----------|
| `rdc-tools workflow capture.rdc --quick` | JSON | Daily development |
| `rdc-tools workflow capture.rdc --full` | JSON+CSV+Pipeline | Complete analysis |
| `rdc-tools workflow capture.rdc --csv-only` | CSV | Data tools |
| `rdc-tools workflow capture.rdc --performance` | JSON+Counters | Profiling |

### List All Presets
```bash
rdc-tools workflow --list-presets
```

### Batch Processing
```bash
python batch_process.py captures/ --preset quick
```

---

## Output Formats

### JSON Structure
```json
{
  "capture_info": {
    "api": "D3D11",
    "frame_info": {
      "frame_number": 5633,
      "capture_time": 0
    }
  },
  "actions": [
    {
      "eventId": 1,
      "name": "DrawIndexed",
      "flags": "Drawcall",
      "numIndices": 36,
      "numInstances": 1
    }
  ],
  "resources": [...],
  "shaders": [...]
}
```

### CSV Format
**actions.csv:**
```csv
eventId,actionId,name,flags,numIndices,numInstances
1,1,DrawIndexed,Drawcall,36,1
```

---

## Python API

### Basic Usage
```python
from renderdoc_tools.parser import Parser
from renderdoc_tools.exporters import JSONExporter

parser = Parser()
data = parser.parse("capture.rdc")

exporter = JSONExporter()
exporter.export(data, Path("output.json"))
```

### Custom Workflow
```python
from renderdoc_tools.workflows.base import Workflow
from renderdoc_tools.extractors import ActionExtractor, ResourceExtractor
from renderdoc_tools.exporters import JSONExporter
from renderdoc_tools.workflows import WorkflowRunner

custom_workflow = Workflow(
    name="custom",
    extractors=[ActionExtractor(), ResourceExtractor()],
    exporters=[JSONExporter()]
)

runner = WorkflowRunner(custom_workflow)
data = runner.run(Path("capture.rdc"))
```

---

## How It Works

RenderDocTools uses **version-agnostic build automation**:

1. **Detects your Python** (3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14...)
2. **Builds RenderDoc** with that exact Python version
3. **Deploys Python DLL** to ensure ABI compatibility
4. **Installs tools** - ready to use

This solves the common Python version mismatch problem with RenderDoc's Python bindings.

---

## Troubleshooting

### Run Diagnostics
```bash
python diagnose.py
```

### Common Issues

**Build fails:**
- Ensure Visual Studio 2019/2022 is installed with C++ Desktop Development workload
- Check Python is detected: `python scripts/detect_python.py`

**"renderdoc module not found":**
- Run `python setup_all.py` to rebuild with correct Python version
- Verify: `python diagnose.py`

**RenderDoc shows wrong Python version:**
- See [BUILD_FIXES.md](BUILD_FIXES.md) - Python version detection section
- Ensure `RENDERDOC_PYTHON_PREFIX64` is set during build

**"rdc-tools command not found":**
```bash
pip install -e .[cli]
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [HOW_SETUP_WORKS.md](HOW_SETUP_WORKS.md) | Build process and Python detection |
| [AndroidSupportLinux.md](AndroidSupportLinux.md) | Android APK build guide for WSL2/Linux |
| [BUILD_FIXES.md](BUILD_FIXES.md) | Build issues and fixes (linker errors) |
| [CONTRIBUTE.md](CONTRIBUTE.md) | Upstream contribution guide |
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) | Complete workflow guide |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | CLI command reference |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture overview |

---

## Development

```bash
# Install with dev dependencies
pip install -r requirements-dev.txt

# Code quality tools
black renderdoc_tools/       # Format
ruff check renderdoc_tools/  # Lint
mypy renderdoc_tools/        # Type check

# Run tests (when implemented)
pytest tests/
```

---

## Contributing

Contributions welcome! Areas for contribution:

- Additional extractors (vertex buffers, texture data)
- New exporters (XML, Protobuf, etc.)
- Custom analyzers
- Performance optimizations
- Test coverage
- GUI wrapper

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Project Status

- Python 3.8-3.14+ support (version-agnostic)
- Automated build system with Python DLL deployment
- Modular architecture with plugin-ready components
- Type-safe data models (Pydantic)
- Streamlined workflow presets
- Comprehensive test suite (in progress)

---

**RenderDocTools** - Streamlined graphics profiling for game development.
