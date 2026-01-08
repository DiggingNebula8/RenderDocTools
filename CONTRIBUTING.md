# Contributing to RenderDoc RDC Parser

Thank you for your interest in contributing!

## Development Setup

1. **Install Python 3.8+**
   - Required for modern features and security updates
   - See README.md for installation instructions

2. **Create Virtual Environment**
   ```powershell
   .\setup_venv.ps1
   .\venv36\Scripts\Activate.ps1
   ```

3. **Verify Setup**
   ```powershell
   python setup_check.py
   python test_renderdoc.py
   ```

## Code Style

- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

## Testing

- Test with sample RDC files
- Test all workflow presets

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation if needed
6. Submit a pull request with a clear description

## Areas for Contribution

- Additional export formats
- Performance optimizations
- GUI wrapper
- More analysis tools
- Documentation improvements
- Bug fixes

## Questions?

Open an issue for discussion or questions.

