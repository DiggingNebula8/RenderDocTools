"""
Modern parser using the new architecture
Provides a high-level interface for parsing RDC files
"""

from pathlib import Path
from typing import Optional, List
import logging

from renderdoc_tools.core import CaptureFile, CaptureInfoExtractor
from renderdoc_tools.core.models import CaptureData
from renderdoc_tools.extractors import (
    ActionExtractor,
    ResourceExtractor,
    ShaderExtractor,
    PipelineExtractor,
    CounterExtractor
)
from renderdoc_tools.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


class Parser:
    """High-level parser for RDC capture files"""
    
    def __init__(
        self,
        include_pipeline: bool = False,
        include_counters: bool = False,
        log_level: str = "INFO"
    ):
        """
        Initialize parser
        
        Args:
            include_pipeline: Whether to include pipeline state extraction
            include_counters: Whether to include performance counters
            log_level: Logging level
        """
        setup_logging(level=log_level)
        self.include_pipeline = include_pipeline
        self.include_counters = include_counters
        
        # Initialize extractors
        self.capture_info_extractor = CaptureInfoExtractor()
        self.action_extractor = ActionExtractor()
        self.resource_extractor = ResourceExtractor()
        self.shader_extractor = ShaderExtractor()
        self.pipeline_extractor = PipelineExtractor() if include_pipeline else None
        self.counter_extractor = CounterExtractor() if include_counters else None
    
    def parse(self, rdc_path: Path) -> CaptureData:
        """
        Parse an RDC capture file
        
        Args:
            rdc_path: Path to RDC capture file
            
        Returns:
            CaptureData model with extracted data
        """
        rdc_path = Path(rdc_path)
        logger.info(f"Parsing capture: {rdc_path}")
        
        with CaptureFile(rdc_path) as capture:
            # Extract capture info
            capture_info = self.capture_info_extractor.extract(capture.controller)
            
            # Extract actions
            actions = self.action_extractor.extract(capture.controller)
            
            # Extract resources
            resources = self.resource_extractor.extract(capture.controller)
            
            # Extract shaders
            shaders = self.shader_extractor.extract(capture.controller)
            
            # Extract pipeline states (optional)
            pipeline_states = None
            if self.pipeline_extractor:
                pipeline_states = self.pipeline_extractor.extract(capture.controller)
            
            # Extract performance counters (optional)
            performance_counters = None
            if self.counter_extractor:
                performance_counters = self.counter_extractor.extract(capture.controller)
            
            # Build capture data
            capture_data = CaptureData(
                capture_info=capture_info,
                actions=actions,
                resources=resources,
                shaders=shaders,
                pipeline_states=pipeline_states,
                performance_counters=performance_counters
            )
            
            logger.info(f"Successfully parsed capture: {len(actions)} actions, {len(resources)} resources")
            return capture_data

