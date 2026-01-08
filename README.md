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

---

## Requirements

- **Python 3.8+** (any version - auto-detected and configured)
- **Visual Studio 2019/2022** (for building RenderDoc)
- **Git** (for submodules)

> [!NOTE]
> **Python Version Flexibility**: Unlike typical RenderDoc Python integrations, RenderDocTools automatically builds RenderDoc with YOUR active Python version (3.8-3.14+). No need to install a specific Python version!

---

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

See [BUILD_GUIDE.md](BUILD_GUIDE.md) for technical details.

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

**"rdc-tools command not found":**
```bash
pip install -e .[cli]
```

---

## Documentation

- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Build system and Python version handling
- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Complete workflow guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - CLI command reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture overview
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

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
