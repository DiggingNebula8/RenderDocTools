# RDC Parser Workflow Guide

## Quick Start

### 1. Setup Check
```bash
python setup_check.py
```

### 2. Single File Processing

**Quick Export (Recommended for most cases):**
```bash
python -m renderdoc_tools.cli workflow capture.rdc --preset quick
```

**Full Analysis:**
```bash
python -m renderdoc_tools.cli workflow capture.rdc --preset full
```

**Parse with Options:**
```bash
python -m renderdoc_tools.cli parse capture.rdc -o output.json --counters
```

### 3. Batch Processing

**Process all RDC files in a directory:**
```bash
python batch_process.py captures/ --preset quick
```

**Recursive search:**
```bash
python batch_process.py captures/ --recursive --preset full
```

## Workflow Presets

### `quick` - Quick Export
- **Use when:** You need fast JSON export
- **Includes:** JSON export only
- **Time:** ~1-5 seconds per capture
- **Output:** `{filename}.json`

### `full` - Full Analysis
- **Use when:** Complete analysis needed
- **Includes:** JSON + CSV + Pipeline state + Counters
- **Time:** ~10-30 seconds (depends on capture size)
- **Output:** All data formats + pipeline states

### `performance` - Performance Analysis
- **Use when:** Performance profiling and optimization
- **Includes:** JSON + Counters
- **Time:** ~5-10 seconds
- **Output:** Data + performance analysis

## Output Organization

All outputs are organized in a structured directory:

```
rdc_output/
├── capture_name.json          # Main JSON export
├── capture_name_actions.csv    # Actions/draw calls CSV
└── capture_name_resources.csv  # Resources CSV
```

## Common Workflows

### Daily Development Workflow

```bash
# Quick check of latest capture
python -m renderdoc_tools.cli workflow latest.rdc --preset quick

# If issues found, run full analysis
python -m renderdoc_tools.cli workflow latest.rdc --preset full
```

### CI/CD Integration

```bash
# Batch process all captures from test run
python batch_process.py test_captures/ --preset quick --output-dir ./ci_results

# Check batch_report.json for failures
# Analyze results programmatically
```

### Research/Analysis Workflow

```bash
# Process large batch with full analysis
python batch_process.py research_captures/ --recursive --preset full

# All results organized in batch_output/
# Use batch_report.json for summary statistics
```

## Advanced Usage

### Custom Output Directory

```bash
python -m renderdoc_tools.cli workflow capture.rdc --preset full --output-dir ./my_results
```

### Parse Command Options

```bash
# Export to JSON with counters
python -m renderdoc_tools.cli parse capture.rdc -o output.json --counters

# Export to CSV only
python -m renderdoc_tools.cli parse capture.rdc --actions actions.csv --resources resources.csv

# Include pipeline state
python -m renderdoc_tools.cli parse capture.rdc -o output.json --pipeline
```

### Batch Processing with Error Handling

```bash
# Continue on errors (default)
python batch_process.py captures/ --preset quick

# Stop on first error
python batch_process.py captures/ --preset quick --stop-on-error
```

## Integration Examples

### Python Script Integration

```python
from renderdoc_tools.workflows import WorkflowRunner, get_preset
from pathlib import Path

# Process single file
preset = get_preset('full')
runner = WorkflowRunner(preset)
capture_data = runner.run(Path('capture.rdc'), output_dir=Path('./output'))

# Access results
print(f"Actions: {len(capture_data.actions)}")
print(f"Resources: {len(capture_data.resources)}")
```

### Using Parser Directly

```python
from renderdoc_tools.parser import Parser
from renderdoc_tools.exporters import JSONExporter
from pathlib import Path

# Parse capture
parser = Parser(include_counters=True)
capture_data = parser.parse(Path("capture.rdc"))

# Export
exporter = JSONExporter()
exporter.export(capture_data, Path("output.json"))
```

### Shell Script Integration

```bash
#!/bin/bash
# Process all captures and generate report

python batch_process.py captures/ --preset full --output-dir ./results

# Check if any failed
FAILED=$(python -c "
import json
with open('./results/batch_report.json') as f:
    report = json.load(f)
    print(report['summary']['failed'])
")

if [ "$FAILED" -gt 0 ]; then
    echo "Warning: $FAILED captures failed to process"
    exit 1
fi
```

## Performance Tips

1. **Use `quick` preset** for initial analysis - it's 5-10x faster
2. **Use `full` preset** only when you need pipeline state details
3. **Batch processing** is efficient - processes files sequentially
4. **Large captures** (>10k actions) may take 30+ seconds with `full` preset

## Troubleshooting

### "renderdoc module not found"
Run `python setup_check.py` for setup instructions

### "Capture cannot be replayed"
- Ensure you're on a compatible system
- Some captures require specific GPU/drivers
- Try on the machine that created the capture

### Batch processing fails
- Check individual files with CLI first
- Use `--stop-on-error` to identify problematic files
- Review `batch_report.json` for error details

### Package import errors
- Ensure package is installed: `pip install -e .`
- Check Python path includes the package directory
- Verify dependencies: `pip install -r requirements.txt`

## Next Steps

1. Try `python -m renderdoc_tools.cli workflow --list-presets` to see all options
2. Process a test capture with different presets
3. Set up batch processing for your workflow
4. Explore the Python API for custom workflows
