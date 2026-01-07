# Architecture Overview

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI Layer                              │
│  (click/typer commands: parse, workflow, batch, analyze)    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Workflow Engine                            │
│  (orchestrates extractors, exporters, analyzers)            │
└──────────┬──────────────────────┬────────────────────────────┘
           │                      │
           │                      │
┌──────────▼──────────┐  ┌────────▼──────────┐  ┌─────────────┐
│    Extractors       │  │    Exporters      │  │  Analyzers  │
│  (data extraction)   │  │  (output formats)  │  │  (analysis) │
│                     │  │                    │  │             │
│  - Actions          │  │  - JSON            │  │  - Quest    │
│  - Resources        │  │  - CSV             │  │  - Perf     │
│  - Shaders          │  │  - Custom          │  │  - Custom   │
│  - Pipeline         │  │                    │  │             │
│  - Counters         │  │                    │  │             │
└──────────┬──────────┘  └────────────────────┘  └─────────────┘
           │
           │
┌──────────▼──────────────────────────────────────────────────┐
│                    Core Layer                               │
│  (models, capture handling, exceptions)                     │
└──────────┬──────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│              RenderDoc API Wrapper                           │
│  (centralized RenderDoc module loading)                      │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Core Layer
- **Models**: Data structures (Pydantic models)
- **Capture**: File handling and validation
- **Exceptions**: Custom exception hierarchy
- **Parser**: Main parsing orchestration

### Extractors Layer
- **BaseExtractor**: Abstract interface
- **ActionExtractor**: Extract draw calls, dispatches
- **ResourceExtractor**: Extract textures, buffers
- **ShaderExtractor**: Extract shader information
- **PipelineExtractor**: Extract pipeline state
- **CounterExtractor**: Extract performance counters

### Exporters Layer
- **BaseExporter**: Abstract interface
- **JSONExporter**: JSON output
- **CSVExporter**: CSV output
- **Registry**: Plugin registration system

### Analyzers Layer
- **BaseAnalyzer**: Abstract interface
- **QuestAnalyzer**: Quest-specific analysis
- **PerformanceAnalyzer**: General performance analysis
- **Registry**: Analyzer registration system

### Workflows Layer
- **Workflow**: Workflow definition
- **WorkflowRunner**: Execution engine
- **Presets**: Predefined workflow configurations

### CLI Layer
- **Commands**: Individual CLI commands
- **Formatters**: Output formatting
- **Main**: Entry point

## Data Flow

```
RDC File
    │
    ▼
CaptureFile (opens file, validates)
    │
    ▼
Parser (orchestrates extraction)
    │
    ├──► ActionExtractor ──► Actions
    ├──► ResourceExtractor ──► Resources
    ├──► ShaderExtractor ──► Shaders
    ├──► PipelineExtractor ──► Pipeline States
    └──► CounterExtractor ──► Performance Counters
    │
    ▼
WorkflowRunner (combines data)
    │
    ├──► Analyzers (analyze data)
    │   ├──► QuestAnalyzer
    │   └──► PerformanceAnalyzer
    │
    └──► Exporters (output data)
        ├──► JSONExporter
        └──► CSVExporter
```

## Dependency Graph

```
CLI
 ├──► Workflows
 │     ├──► Extractors
 │     │     └──► Core
 │     ├──► Exporters
 │     │     └──► Core
 │     └──► Analyzers
 │           └──► Core
 └──► Utils
       └──► RenderDoc Loader
```

## Plugin System Architecture

### Extractor Plugin
```python
# Custom extractor example
from renderdoc_tools.extractors import BaseExtractor

class CustomExtractor(BaseExtractor):
    def extract(self, controller):
        # Custom extraction logic
        pass
    
    @property
    def name(self):
        return "custom"
```

### Exporter Plugin
```python
# Custom exporter example
from renderdoc_tools.exporters import BaseExporter

class XMLExporter(BaseExporter):
    def export(self, data, output_path):
        # Custom export logic
        pass
    
    @property
    def format_name(self):
        return "xml"
    
    @property
    def file_extension(self):
        return "xml"
```

### Analyzer Plugin
```python
# Custom analyzer example
from renderdoc_tools.analyzers import BaseAnalyzer

class CustomAnalyzer(BaseAnalyzer):
    def analyze(self, capture_data):
        # Custom analysis logic
        return {"result": "..."}
    
    @property
    def name(self):
        return "custom"
```

## Configuration System

```
Environment Variables
    │
    ▼
Settings (Pydantic)
    │
    ├──► Config File (JSON/YAML/TOML)
    │
    └──► Defaults
```

## Error Handling Strategy

```
Custom Exceptions Hierarchy:
RenderDocError (base)
├── RenderDocNotFoundError
├── CaptureError
│   ├── CaptureOpenError
│   └── CaptureReplayError
├── ExtractionError
│   ├── ActionExtractionError
│   ├── ResourceExtractionError
│   └── ShaderExtractionError
└── ExportError
    ├── JSONExportError
    └── CSVExportError
```

## Logging Architecture

```
Logger Hierarchy:
renderdoc_tools
├── renderdoc_tools.core
├── renderdoc_tools.extractors
├── renderdoc_tools.exporters
├── renderdoc_tools.analyzers
└── renderdoc_tools.workflows

Log Levels:
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors
```

## Testing Strategy

```
Test Pyramid:
        /\
       /  \  Integration Tests (few)
      /────\  
     /      \ Unit Tests (many)
    /────────\
```

### Unit Tests
- Mock RenderDoc API
- Test individual extractors
- Test individual exporters
- Test individual analyzers
- Test utilities

### Integration Tests
- Test full parsing pipeline
- Test workflow execution
- Test with real RDC files (small samples)

## Performance Considerations

1. **Lazy Loading**: Extractors only run when needed
2. **Streaming**: Large file support via streaming exporters
3. **Caching**: Cache extracted data within workflow
4. **Parallelization**: Batch processing can be parallelized
5. **Memory Management**: Clear references after extraction

## Security Considerations

1. **Path Validation**: Validate all file paths
2. **Input Sanitization**: Validate RDC file headers
3. **Resource Limits**: Limit memory usage for large captures
4. **Error Messages**: Don't leak sensitive information

