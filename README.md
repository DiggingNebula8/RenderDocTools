# RenderDoc RDC Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Open-source parser for extracting structured data from RenderDoc capture files (.rdc) to JSON and CSV formats.

Compatible with **RenderDoc** and **RenderDoc Meta Fork** (Quest/VR profiling).

---

## Quick Start (2 Steps)

**1. Install**
```bash
pip install -e .
```

**2. Use It**
```bash
rdc-tools workflow capture.rdc --quick
```

**That's it!** 🎉

> **Optional**: Run `python diagnose.py` if you encounter issues.

---

## Features

- Extract draw calls, dispatches, and all actions
- Export resources (textures, buffers) with metadata
- Extract shader information and reflection data
- Optional pipeline state extraction per event
- JSON and CSV output formats
- API-agnostic (works with D3D11, D3D12, Vulkan, OpenGL)
- **Streamlined workflow presets** (quick, full, quest, etc.)
- **Modular architecture** with plugin-ready extractors/exporters
- **Type-safe** data models using Pydantic
- **Structured logging** for debugging and monitoring

## Requirements

- **Python 3.8+** (Recommended: Python 3.10 or higher)
- RenderDoc (with Python bindings) or **RenderDoc Meta Fork**
- **Pydantic** (for data validation)

> [!NOTE]
> **Modern Python Support**: RenderDocTools works with Python 3.8-3.14 using `os.add_dll_directory()` for Windows DLL loading. Python 3.6 is no longer required.

> [!TIP]
> **RenderDoc Meta Fork 63.13+** (with RenderDoc v1.40 integration) fully supports modern Python versions.

---

## Common Usage

### Quick Export
```bash
rdc-tools workflow capture.rdc --quick
```

### Full Analysis
```bash
rdc-tools workflow capture.rdc --full
```

### Quest Analysis
```bash
rdc-tools workflow quest.rdc --quest
```

### List All Presets
```bash
rdc-tools workflow --list-presets
```

### Batch Processing
```bash
python batch_process.py captures/ --preset quick
```

---

## Workflow Presets

| Shorthand | Speed | Output | Use Case |
|-----------|-------|--------|----------|
| `--quick` | ⚡⚡⚡ | JSON | Daily development, quick checks |
| `--full` | ⚡ | JSON+CSV+Pipeline | Complete analysis |
| `--quest` | ⚡⚡ | JSON+CSV+Report | Quest/VR optimization |
| `--csv-only` | ⚡⚡⚡ | CSV only | Data analysis tools |
| `--performance` | ⚡⚡ | JSON+Counters+Report | Performance profiling |

---

## Output Formats

### JSON Structure

```json
{
  "capture_info": {
    "api": 2,
    "is_meta_fork": false,
    "frame_info": {
      "frame_number": 5633,
      "capture_time": 0
    }
  },
  "actions": [
    {
      "eventId": 1,
      "actionId": 1,
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
| eventId | actionId | name | flags | numIndices | numInstances |
|---------|----------|------|-------|------------|--------------|
| 1 | 1 | DrawIndexed | Drawcall | 36 | 1 |

**resources.csv:**
| resourceId | name | type | texture_width | texture_height | texture_format |
|------------|------|------|---------------|----------------|----------------|
| 123 | Backbuffer | Texture | 1920 | 1080 | R8G8B8A8_UNORM |

---

## Meta Quest / VR Support

The parser **fully supports RenderDoc Meta Fork** captures from Quest headsets:

- **Automatic detection** of Quest/VR captures
- **Performance counter extraction** via `CounterExtractor`
- **Quest-specific analyzers**:
  - Performance analysis (`QuestPerformanceAnalyzer`)
  - Multiview rendering detection (`MultiviewAnalyzer`)
  - Fixed foveated rendering check (`FoveationAnalyzer`)
  - Optimization report generation (`QuestReportGenerator`)

The Meta fork adds:
- Tile-level render stage traces
- 45+ low-level GPU metrics per draw call
- Snapdragon-specific profiling data

---

## Troubleshooting

### "renderdoc module not found"
```bash
# Run diagnostics
python diagnose.py

# Ensure RenderDoc is installed
# Package auto-detects standard locations
```

### "rdc-tools command not found"
```bash
# Reinstall package
pip install -e .

# On Linux/Mac, ensure ~/.local/bin is in PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Package import errors
```bash
# Reinstall with dependencies
pip install -e .[cli]
```

---

## Documentation

- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Complete workflow guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[INSTALL_PYTHON36.md](INSTALL_PYTHON36.md)** - Python 3.6 installation guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture overview
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

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

### Quest Analysis

```python
from renderdoc_tools.workflows import WorkflowRunner, get_preset

# Run Quest workflow
preset = get_preset('quest')
runner = WorkflowRunner(preset)
data = runner.run(Path("quest_capture.rdc"))
```

### Custom Workflow

```python
from renderdoc_tools.workflows.base import Workflow
from renderdoc_tools.extractors import ActionExtractor, ResourceExtractor
from renderdoc_tools.exporters import JSONExporter
from renderdoc_tools.workflows import WorkflowRunner

# Create custom workflow
custom_workflow = Workflow(
    name="custom",
    description="Custom workflow",
    extractors=[ActionExtractor(), ResourceExtractor()],
    exporters=[JSONExporter()]
)

runner = WorkflowRunner(custom_workflow)
data = runner.run(Path("capture.rdc"))
```

See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) for more examples.

---

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Running Tests

```bash
# Run tests (when implemented)
pytest tests/

# With coverage
pytest --cov=renderdoc_tools tests/
```

### Code Quality

```bash
# Format code
black renderdoc_tools/

# Lint code
ruff check renderdoc_tools/

# Type checking
mypy renderdoc_tools/
```

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Common areas for contribution:
- Additional extractors (vertex buffers, textures to files)
- New exporters (XML, YAML, etc.)
- Custom analyzers
- Performance optimizations
- Documentation improvements
- GUI wrapper

---

## Advanced Setup

<details>
<summary>Click to expand manual setup instructions</summary>

### Manual Installation

If you prefer manual setup or the automated script doesn't work for your environment:

#### 1. Install Python 3.6

See [INSTALL_PYTHON36.md](INSTALL_PYTHON36.md) for detailed instructions.

Common methods:
- **Direct download**: https://www.python.org/downloads/release/python-3615/
- **Scoop** (Windows): `scoop bucket add versions; scoop install versions/python36`

#### 2. Create Virtual Environment

```bash
# Windows
python3.6 -m venv venv36
.\venv36\Scripts\Activate.ps1

# Linux/Mac
python3.6 -m venv venv36
source venv36/bin/activate
```

#### 3. Install Package

```bash
pip install -e .
```

#### 4. Configure RenderDoc Path (if needed)

The package automatically detects RenderDoc installations, but you can manually set:

**Windows (Standard RenderDoc):**
```bash
set PYTHONPATH=C:\Program Files\RenderDoc\
```

**Windows (Meta Fork):**
```bash
set PYTHONPATH=C:\Program Files\RenderDocForMetaQuest\pymodules
```

**Linux:**
```bash
export PYTHONPATH=/usr/share/renderdoc/
export LD_LIBRARY_PATH=/usr/lib/renderdoc/
```

#### 5. Verify Installation

```bash
python setup_check.py
python test_renderdoc.py
```

</details>

---

## Project Status

✅ **v2.0.0 - Refactored Architecture**

- ✅ Modular architecture with plugin-ready components
- ✅ Type-safe data models (Pydantic)
- ✅ Structured logging
- ✅ Workflow presets
- ✅ Quest-specific analyzers
- ⏳ Comprehensive test suite (in progress)
- ⏳ API documentation (in progress)

---

**RenderDoc Tools v2.0.0** - Streamlined graphics profiling for game development.
