# RenderDoc RDC Parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Open-source parser for extracting structured data from RenderDoc capture files (.rdc) to JSON and CSV formats.

Compatible with **RenderDoc** and **RenderDoc Meta Fork** (Quest/VR profiling).

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

- **Python 3.6** (Required for RenderDoc Meta Fork - must match the version RenderDoc was built for)
- RenderDoc (with Python bindings) or **RenderDoc Meta Fork**
- **Pydantic** (for data validation)

**Important:** RenderDoc Meta Fork includes `python36.dll`, indicating it was built for **Python 3.6**. You must use Python 3.6 for the Python module to work. Python 3.9+ will cause import hangs. See `INSTALL_PYTHON36.md` for installation instructions.

**Meta Fork Compatible**: This parser works with RenderDoc Meta Fork captures. The Meta fork adds Quest-specific tile profiling and metrics, but uses the same underlying capture format and Python API.

## Quick Start

### Automated Setup (Recommended)

**Windows PowerShell:**
```bash
# One command does everything: creates venv, installs package, sets up wrappers
.\setup.ps1
```

**Linux/Mac:**
```bash
# Make executable and run
chmod +x setup.sh
./setup.sh
```

This will:
1. ✅ Create Python 3.6 virtual environment (`venv36`)
2. ✅ Install the package (`pip install -e .`)
3. ✅ Automatically detect RenderDoc (standard and Meta Fork)
4. ✅ Set up convenience wrapper scripts
5. ✅ Verify installation

### Manual Setup (Alternative)

If you prefer manual setup:

**Step 1: Create Virtual Environment**
```bash
# Windows
.\setup_venv.ps1
.\venv36\Scripts\Activate.ps1

# Linux/Mac
python3.6 -m venv venv36
source venv36/bin/activate
```

**Step 2: Install Package**
```bash
pip install -e .
```

**Note:** RenderDoc Meta Fork requires Python 3.6 exactly. See `INSTALL_PYTHON36.md` for installation instructions.

### 3. RenderDoc Detection (Automatic!)

**The package automatically detects RenderDoc installations!**

The setup script will:
- ✅ Automatically detect both standard RenderDoc and RenderDoc Meta Fork
- ✅ Use Meta Fork if both are available (preferred for Quest development)
- ✅ Configure everything automatically - **no manual PYTHONPATH setup needed!**

**Manual setup (only if automatic detection fails):**

If RenderDoc is installed in a non-standard location, you can set PYTHONPATH manually:

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

**Note:** In most cases, manual setup is not needed - the package handles it automatically!

### 3. Verify Setup

```bash
python setup_check.py
python test_renderdoc.py
```

### 4. Process a Capture

**After running setup, use the convenience wrapper scripts (recommended):**
```bash
# Windows PowerShell
.\rdc-tools.ps1 workflow capture.rdc --preset quick
.\rdc-tools.ps1 workflow quest_capture.rdc --preset quest
.\rdc-tools.ps1 parse capture.rdc -o output.json --counters
.\rdc-tools.ps1 workflow --list-presets

# Windows CMD
rdc-tools.bat workflow capture.rdc --preset quick

# Linux/Mac
./rdc-tools.sh workflow capture.rdc --preset quick
```

**Alternative: Add to PATH to use `rdc-tools` directly:**
```bash
# Windows PowerShell (add to current session)
$env:Path += ";$PWD\venv36\Scripts"
rdc-tools workflow capture.rdc --preset quick

# Or add permanently to your PowerShell profile
# Add: $env:Path += ";C:\Users\vsiva\dev\RenderDocTools\venv36\Scripts"
```

**Note:** The wrapper scripts automatically use `venv36`, so you never need to manually activate it!

**Or using Python module (if not installed):**
```bash
# Quick export
python -m renderdoc_tools.cli workflow capture.rdc --preset quick

# Quest analysis
python -m renderdoc_tools.cli workflow quest_capture.rdc --preset quest

# Parse with options
python -m renderdoc_tools.cli parse capture.rdc -o output.json --counters
```

**Using Python API:**
```python
from renderdoc_tools.workflows import WorkflowRunner, get_preset
from pathlib import Path

# Run workflow preset
preset = get_preset('quest')
runner = WorkflowRunner(preset)
capture_data = runner.run(Path("capture.rdc"), output_dir=Path("./output"))
```


## Installation

### 1. Install RenderDoc

Download from: https://renderdoc.org/builds

For Quest development, download **RenderDoc Meta Fork** from Meta Developer site.

### 2. Create Virtual Environment

**For RenderDoc Meta Fork (requires Python 3.6):**
```bash
# Windows - use setup script
.\setup_venv.ps1
.\venv36\Scripts\Activate.ps1

# Or manually
python3.6 -m venv venv36
.\venv36\Scripts\Activate.ps1  # Windows
source venv36/bin/activate     # Linux/Mac
```

**For Standard RenderDoc (Python 3.6+):**
```bash
# Create venv with your Python version
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
```

### 3. Install Python Package

```bash
# After activating virtual environment
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

**Important:** Always activate your virtual environment before running `pip install -e .` or using the tools.

### 4. Setup Python Module Path

The package automatically detects RenderDoc installation, but you can also set it manually:

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

### 5. Install Python 3.6 (Meta Fork Only)

See [INSTALL_PYTHON36.md](INSTALL_PYTHON36.md) for detailed instructions.

**Note:** This step is only needed if you're using RenderDoc Meta Fork, which requires Python 3.6 exactly.

### 6. Verify Installation

```bash
python setup_check.py
python test_renderdoc.py
```

## Usage

### Quick Answer: Do I Need to Activate venv36 Every Time?

**Short answer:** No! Use the wrapper scripts - they automatically use `venv36` for you.

**Just use the wrapper scripts:**
```bash
# Windows PowerShell - no activation needed!
.\rdc-tools.ps1 workflow capture.rdc --preset quick
.\rdc-tools.ps1 parse capture.rdc -o output.json

# Linux/Mac
./rdc-tools.sh workflow capture.rdc --preset quick
```

**How it works:** The wrapper scripts automatically detect `venv36` in your project directory and use its Python interpreter. You never need to manually activate the virtual environment.

**Alternative:** If you add `venv36\Scripts` (Windows) or `venv36/bin` (Linux/Mac) to your PATH, you can use `rdc-tools` directly:
```bash
# After adding to PATH
rdc-tools workflow capture.rdc --preset quick
```

### New Architecture (Recommended)

The refactored package provides a clean, modular API:

#### Using Workflows

```python
from renderdoc_tools.workflows import WorkflowRunner, get_preset
from pathlib import Path

# Get a preset workflow
preset = get_preset('quest')  # Options: quick, full, quest, csv-only, performance

# Run workflow
runner = WorkflowRunner(preset)
capture_data = runner.run(Path("capture.rdc"), output_dir=Path("./output"))

# Access results
print(f"Actions: {len(capture_data.actions)}")
print(f"Resources: {len(capture_data.resources)}")
```

#### Using Parser Directly

```python
from renderdoc_tools.parser import Parser
from renderdoc_tools.exporters import JSONExporter, CSVExporter
from pathlib import Path

# Parse capture
parser = Parser(include_pipeline=False, include_counters=True)
capture_data = parser.parse(Path("capture.rdc"))

# Export to JSON
json_exporter = JSONExporter()
json_exporter.export(capture_data, Path("output.json"))

# Export to CSV
csv_exporter = CSVExporter()
csv_exporter.export(capture_data, Path("output.csv"))
```

#### Using Extractors and Exporters Separately

```python
from renderdoc_tools.core import CaptureFile
from renderdoc_tools.extractors import ActionExtractor, ResourceExtractor
from renderdoc_tools.exporters import JSONExporter

with CaptureFile("capture.rdc") as capture:
    # Extract specific data
    action_extractor = ActionExtractor()
    actions = action_extractor.extract(capture.controller)
    
    resource_extractor = ResourceExtractor()
    resources = resource_extractor.extract(capture.controller)
    
    # Export
    exporter = JSONExporter()
    exporter.export({'actions': actions, 'resources': resources}, Path("output.json"))
```

### CLI Usage

#### Workflow Command

```bash
# List all presets
.\rdc-tools.ps1 workflow --list-presets  # Windows PowerShell
./rdc-tools.sh workflow --list-presets   # Linux/Mac

# Run workflow preset
.\rdc-tools.ps1 workflow capture.rdc --preset quick

# Quest analysis
.\rdc-tools.ps1 workflow quest.rdc --preset quest --output-dir ./results

# Custom log level
.\rdc-tools.ps1 workflow capture.rdc --preset full --log-level DEBUG
```

#### Parse Command

```bash
# Export to JSON
.\rdc-tools.ps1 parse capture.rdc -o output.json

# Export with pipeline state
.\rdc-tools.ps1 parse capture.rdc -o output.json --pipeline

# Export with performance counters
.\rdc-tools.ps1 parse capture.rdc -o output.json --counters

# Export to CSV
.\rdc-tools.ps1 parse capture.rdc --actions actions.csv --resources resources.csv
```

**Note:** Use the wrapper scripts (`.\rdc-tools.ps1` or `./rdc-tools.sh`) - they automatically use `venv36`. Alternatively, add `venv36\Scripts` to PATH to use `rdc-tools` directly.

### Workflow Presets

| Preset | Speed | Output | Use Case |
|--------|-------|--------|----------|
| `quick` | ⚡⚡⚡ | JSON | Daily development, quick checks |
| `full` | ⚡ | JSON+CSV+Pipeline | Complete analysis |
| `quest` | ⚡⚡ | JSON+CSV+Report | Quest/VR optimization |
| `csv-only` | ⚡⚡⚡ | CSV only | Data analysis in Excel/CSV tools |
| `performance` | ⚡⚡ | JSON+Counters+Report | Performance profiling |


## Architecture

The package is organized into modular components:

```
renderdoc_tools/
├── core/           # Domain models, capture handling, exceptions
├── extractors/     # Data extraction modules (plugin-ready)
├── exporters/      # Output format modules (plugin-ready)
├── analyzers/      # Analysis modules (Quest-specific, etc.)
├── workflows/      # Workflow presets and execution
├── config/         # Configuration management
├── utils/          # Utilities (RenderDoc loader, logging)
└── cli/            # Command-line interface
```

### Key Components

- **Core**: Data models (Pydantic), capture file handling, exceptions
- **Extractors**: Modular extractors for actions, resources, shaders, pipeline, counters
- **Exporters**: Plugin-ready exporters (JSON, CSV, extensible)
- **Analyzers**: Quest-specific analysis and optimization reports
- **Workflows**: Predefined workflow presets for common tasks
- **CLI**: Command-line interface for easy usage

### Extensibility

The architecture supports easy extension:

```python
# Create custom extractor
from renderdoc_tools.extractors.base import BaseExtractor

class CustomExtractor(BaseExtractor):
    def extract(self, controller):
        # Your extraction logic
        return []
    
    @property
    def name(self):
        return "custom"

# Create custom exporter
from renderdoc_tools.exporters.base import BaseExporter

class XMLExporter(BaseExporter):
    def export(self, data, output_path):
        # Your export logic
        pass
    
    @property
    def format_name(self):
        return "xml"
    
    @property
    def file_extension(self):
        return "xml"
```

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

**Note:** Tile timeline visualization requires the Meta Fork UI; Python API provides counter data.

## Troubleshooting

### "renderdoc module not found"
- Run `python setup_check.py` for setup instructions
- Ensure RenderDoc is installed
- Check PYTHONPATH includes renderdoc module location
- Verify Python version matches RenderDoc build (Python 3.6 for Meta Fork)
- The package automatically detects RenderDoc, but manual PYTHONPATH may be needed

### "Capture cannot be replayed"
- Check API support on your system
- Some captures require specific GPU/drivers
- Try on the machine that created the capture

### Import hangs with Python 3.9+
- RenderDoc Meta Fork requires Python 3.6 (exact version)
- Install Python 3.6 and create a venv: `.\setup_venv.ps1`
- See `INSTALL_PYTHON36.md` for details

### Workflow Issues
- Use `python -m renderdoc_tools.cli workflow --list-presets` to see all options
- Check `WORKFLOW_GUIDE.md` for detailed workflow examples
- Review logs with `--log-level DEBUG` for detailed information

### Package Import Errors
- Ensure package is installed: `pip install -e .`
- Check Python path includes the package directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

## Documentation

- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Complete workflow guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[INSTALL_PYTHON36.md](INSTALL_PYTHON36.md)** - Python 3.6 installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Migration guide from old to new architecture
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture overview
- **[REFACTORING_PLAN.md](REFACTORING_PLAN.md)** - Refactoring plan and details

## Examples

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
from renderdoc_tools.analyzers.quest import QuestReportGenerator

# Run Quest workflow
preset = get_preset('quest')
runner = WorkflowRunner(preset)
data = runner.run(Path("quest_capture.rdc"))

# Generate optimization report
report_gen = QuestReportGenerator()
report = report_gen.analyze(data.dict(by_alias=True))
report_gen.generate_report_file(data.dict(by_alias=True), Path("quest_report.json"))
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

See `example_usage.py` for more advanced examples.

## API Documentation

- **Package API**: See `renderdoc_tools/` module structure
- **RenderDoc Python API**: https://renderdoc.org/docs/python_api/

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

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Common areas for contribution:
- Additional extractors (vertex buffers, textures to files)
- New exporters (XML, YAML, etc.)
- Custom analyzers
- Performance optimizations
- Documentation improvements
- GUI wrapper

## Project Status

✅ **v2.0.0 - Refactored Architecture**

- ✅ Modular architecture with plugin-ready components
- ✅ Type-safe data models (Pydantic)
- ✅ Structured logging
- ✅ Workflow presets
- ✅ Quest-specific analyzers
- ⏳ Comprehensive test suite (in progress)
- ⏳ API documentation (in progress)

## Changelog

### v2.0.0 (Current)
- **Major refactoring**: Modular architecture with clear separation of concerns
- **New**: Plugin-ready extractors, exporters, and analyzers
- **New**: Type-safe data models using Pydantic
- **New**: Structured logging system
- **New**: Workflow presets and runner
- **New**: CLI interface
- **Improved**: Error handling with custom exception hierarchy


See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
