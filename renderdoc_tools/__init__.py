"""
RenderDoc Tools - A Python package for parsing and analyzing RenderDoc capture files
"""

__version__ = "2.0.0"

from renderdoc_tools.core import CaptureFile
from renderdoc_tools.core.models import (
    CaptureInfo,
    Action,
    Resource,
    Shader,
    PipelineState,
    PerformanceCounter,
    CaptureData
)
from renderdoc_tools.core.exceptions import (
    RenderDocError,
    RenderDocNotFoundError,
    CaptureError,
    CaptureOpenError,
    CaptureReplayError,
    ExtractionError,
    ExportError
)

__all__ = [
    # Version
    "__version__",
    
    # Core
    "CaptureFile",
    
    # Models
    "CaptureInfo",
    "Action",
    "Resource",
    "Shader",
    "PipelineState",
    "PerformanceCounter",
    "CaptureData",
    
    # Exceptions
    "RenderDocError",
    "RenderDocNotFoundError",
    "CaptureError",
    "CaptureOpenError",
    "CaptureReplayError",
    "ExtractionError",
    "ExportError",
]

