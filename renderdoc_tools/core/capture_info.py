"""Capture info extraction"""

from typing import Dict, Any
import logging

from renderdoc_tools.core.models import CaptureInfo
from renderdoc_tools.core.exceptions import ExtractionError

logger = logging.getLogger(__name__)


class CaptureInfoExtractor:
    """Extracts basic capture metadata"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract(self, controller) -> CaptureInfo:
        """
        Extract basic capture metadata
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            CaptureInfo model
            
        Raises:
            ExtractionError: If extraction fails
        """
        try:
            from renderdoc_tools.utils.renderdoc_loader import get_renderdoc_module
            rd = get_renderdoc_module()
            
            api_props = controller.GetAPIProperties()
            
            # Detect Meta fork from API properties
            is_meta_fork = False
            try:
                api_str = str(api_props)
                is_meta_fork = 'Qualcomm' in api_str or 'Adreno' in api_str
            except Exception:
                pass
            
            # Get frame info
            frame_info = {}
            try:
                frame_desc = controller.GetFrameInfo()
                frame_info['frame_number'] = frame_desc.frameNumber
                frame_info['capture_time'] = frame_desc.captureTime
                frame_info['uncompressed_size'] = frame_desc.uncompressedFileSize
                frame_info['compressed_size'] = frame_desc.compressedFileSize
            except Exception as e:
                self.logger.debug(f"Could not extract frame info: {e}")
            
            capture_info = CaptureInfo(
                api=api_props.pipelineType,
                is_meta_fork=is_meta_fork,
                frame_info=frame_info
            )
            
            return capture_info
            
        except Exception as e:
            self.logger.error(f"Failed to extract capture info: {e}")
            raise ExtractionError(f"Capture info extraction failed: {e}") from e

