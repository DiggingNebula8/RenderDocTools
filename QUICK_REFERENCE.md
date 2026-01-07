# Quick Reference Card

## Most Common Commands

**First time setup:**
```bash
# Create Python 3.6 virtual environment (required for RenderDoc Meta Fork)
.\setup_venv.ps1
.\venv36\Scripts\Activate.ps1

# Install package
pip install -e .
```

**Then use normally:**
```bash
# Quick export (fastest, recommended)
python -m renderdoc_tools.cli workflow capture.rdc --preset quick

# Quest analysis
python -m renderdoc_tools.cli workflow quest.rdc --preset quest

# Batch process directory
python batch_process.py captures/ --preset quick

# List all presets
python -m renderdoc_tools.cli workflow --list-presets
```

## Workflow Presets

| Preset | Speed | Output | Use Case |
|--------|-------|--------|----------|
| `quick` | ⚡⚡⚡ | JSON | Daily development, quick checks |
| `full` | ⚡ | JSON+CSV+Pipeline | Complete analysis |
| `quest` | ⚡⚡ | JSON+CSV+Report | Quest/VR optimization |
| `csv-only` | ⚡⚡⚡ | CSV only | Data analysis in Excel/CSV tools |
| `performance` | ⚡⚡ | JSON+Counters+Report | Performance profiling |

## File Structure

```
project/
├── renderdoc_tools/     ⭐ Main package
│   ├── core/            Core domain logic
│   ├── extractors/      Data extraction
│   ├── exporters/       Output formats
│   ├── analyzers/       Analysis modules
│   ├── workflows/       Workflow system
│   └── cli/             Command-line interface
├── batch_process.py     ⭐ Batch processing
├── quest_analysis.py    Quest analysis script
├── example_usage.py     Usage examples
└── setup_check.py       Setup verification
```

## Output Structure

```
rdc_output/
├── capture_name.json
├── capture_name_actions.csv
├── capture_name_resources.csv
└── capture_name_quest_report.json  (if Quest preset)
```

## Common Workflows

### Daily Development
```bash
python -m renderdoc_tools.cli workflow latest.rdc --preset quick
```

### Quest Optimization
```bash
python -m renderdoc_tools.cli workflow quest.rdc --preset quest
# Review quest_report.json for recommendations
```

### CI/CD Integration
```bash
python batch_process.py test_captures/ --preset quick
# Check batch_report.json for results
```

### Research/Analysis
```bash
python batch_process.py research/ --recursive --preset full
```

## Tips

- ✅ Start with `quick` preset - it's fastest
- ✅ Use `quest` preset for Quest/VR captures
- ✅ Batch processing organizes outputs automatically
- ✅ Use Python API for programmatic access
- ✅ Review `batch_report.json` after batch processing

## Getting Help

```bash
# List presets
python -m renderdoc_tools.cli workflow --list-presets

# Help for workflow command
python -m renderdoc_tools.cli workflow --help

# Help for parse command
python -m renderdoc_tools.cli parse --help

# Help for batch processing
python batch_process.py --help

# Setup check
python setup_check.py
```

## Python API Usage

```python
from renderdoc_tools.workflows import WorkflowRunner, get_preset
from pathlib import Path

# Run workflow
preset = get_preset('quest')
runner = WorkflowRunner(preset)
data = runner.run(Path("capture.rdc"))
```
