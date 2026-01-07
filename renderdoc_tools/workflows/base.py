"""Base workflow classes"""

from typing import List, Optional
from dataclasses import dataclass, field

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.exporters.base import BaseExporter
from renderdoc_tools.analyzers.base import BaseAnalyzer
from renderdoc_tools.core.capture_info import CaptureInfoExtractor


@dataclass
class Workflow:
    """Workflow definition"""
    name: str
    description: str
    extractors: List[BaseExtractor] = field(default_factory=list)
    exporters: List[BaseExporter] = field(default_factory=list)
    analyzers: List[BaseAnalyzer] = field(default_factory=list)
    capture_info_extractor: Optional[CaptureInfoExtractor] = None

