# RenderDocTools Tests

This directory contains unit and integration tests for the RenderDocTools package.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=renderdoc_tools

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## Test Structure

- `test_models.py` - Pydantic model validation tests
- `test_extractors.py` - Extractor logic tests (with mocked RenderDoc API)
- `test_exporters.py` - JSON/CSV export functionality tests

## Note on RenderDoc Mocking

Since RenderDoc's Python API is not pip-installable, we use mocks for unit testing. For integration tests with real RDC files, see the examples in the main README.
