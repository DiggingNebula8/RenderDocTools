"""Pipeline state extraction module"""

from typing import List, Optional
import logging

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.core.models import PipelineState
from renderdoc_tools.core.exceptions import PipelineExtractionError

logger = logging.getLogger(__name__)


class PipelineExtractor(BaseExtractor):
    """Extracts pipeline state information from capture"""
    
    def __init__(self, event_ids: Optional[List[int]] = None):
        """
        Initialize pipeline extractor
        
        Args:
            event_ids: Optional list of event IDs to extract pipeline state for.
                      If None, extracts for all actions.
        """
        super().__init__()
        self.event_ids = event_ids
    
    def extract(self, controller) -> List[PipelineState]:
        """
        Extract pipeline states from the capture
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            List of PipelineState models
            
        Raises:
            PipelineExtractionError: If extraction fails
        """
        if not self.validate(controller):
            raise PipelineExtractionError("Invalid controller provided")
        
        self.logger.info("Extracting pipeline states...")
        pipeline_states = []
        
        try:
            from renderdoc_tools.utils.renderdoc_loader import get_renderdoc_module
            rd = get_renderdoc_module()
            
            # Get event IDs to process
            if self.event_ids is None:
                # Extract for all actions
                from renderdoc_tools.extractors.actions import ActionExtractor
                action_extractor = ActionExtractor()
                actions = action_extractor.extract(controller)
                event_ids = [action.event_id for action in actions]
            else:
                event_ids = self.event_ids
            
            for event_id in event_ids:
                try:
                    controller.SetFrameEvent(event_id, False)
                    state = controller.GetPipelineState()
                    
                    pipeline_data = {
                        'eventId': event_id,
                        'graphicsShaderStages': [],
                    }
                    
                    # Extract bound shaders (API-agnostic approach)
                    try:
                        if hasattr(state, 'GetShaderReflection'):
                            for stage in [rd.ShaderStage.Vertex, rd.ShaderStage.Pixel, rd.ShaderStage.Compute]:
                                try:
                                    shader_ref = state.GetShaderReflection(stage)
                                    if shader_ref:
                                        pipeline_data['graphicsShaderStages'].append({
                                            'stage': str(stage),
                                            'resourceId': str(shader_ref.resourceId),
                                        })
                                except Exception:
                                    pass
                    except Exception as e:
                        self.logger.debug(f"Could not extract shader stages: {e}")
                    
                    pipeline_model = PipelineState(**pipeline_data)
                    pipeline_states.append(pipeline_model)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to extract pipeline state for event {event_id}: {e}")
            
            self.logger.info(f"Extracted {len(pipeline_states)} pipeline states")
            return pipeline_states
            
        except Exception as e:
            self.logger.error(f"Failed to extract pipeline states: {e}")
            raise PipelineExtractionError(f"Pipeline extraction failed: {e}") from e
    
    @property
    def name(self) -> str:
        return "pipeline"

