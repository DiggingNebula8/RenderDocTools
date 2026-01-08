# Quick Reference

## Installation

```bash
pip install -e .
```

## Basic Commands

### Quick Export
```bash
rdc-tools workflow capture.rdc --quick
```

### Full Analysis
```bash
rdc-tools workflow capture.rdc --full
```

### List Presets
```bash
rdc-tools workflow --list-presets
```

## Workflow Presets

| Preset | Shorthand | Speed | Output |
|--------|-----------|-------|--------|
| `quick` | `--quick` | ⚡⚡⚡ | JSON only |
| `full` | `--full` | ⚡ | JSON+CSV+Pipeline |
| `csv-only` | `--csv-only` | ⚡⚡⚡ | CSV only |
| `performance` | `--performance` | ⚡⚡ | JSON+Counters |

## Python API

### Basic Usage
```python
from renderdoc_tools.parser import Parser
from renderdoc_tools.exporters import JSONExporter

parser = Parser()
data = parser.parse("capture.rdc")

exporter = JSONExporter()
exporter.export(data, "output.json")
```

## Troubleshooting

```bash
# Run diagnostics
python diagnose.py

# Reinstall
pip install -e .

# Verify RenderDoc
python -c "from renderdoc_tools.utils.renderdoc_loader import load_renderdoc; rd = load_renderdoc(); print('✓ Works!')"
```

## Batch Processing

```bash
python batch_process.py captures/ --preset quick
```

## Documentation

- [README.md](README.md) - Full documentation
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Detailed workflows
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [PYTHON_VERSIONS.md](PYTHON_VERSIONS.md) - Python compatibility
