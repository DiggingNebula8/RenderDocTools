# Python Version Compatibility

RenderDocTools works with modern Python versions.

## Recommended: Python 3.10+

For the best experience, use Python 3.10 or higher.

## Minimum: Python 3.8

Python 3.8+ is required for security updates and modern features.

## Installation

```bash
# Standard install
pip install -e .

# With development tools
pip install -e .[dev]

# With all features
pip install -e .[dev,cli]
```

## Troubleshooting

If you encounter issues, run diagnostics:
```bash
python diagnose.py
```

## Legacy Python 3.6 (Not Recommended)

Python 3.6 reached end-of-life in December 2021 and is **not supported** by modern RenderDocTools.

If you absolutely must use Python 3.6 for older RenderDoc versions:
1. Use an older version of RenderDocTools (before v2.1.0)
2. Install Python 3.6 from python.org archives
3. Be aware of security risks
