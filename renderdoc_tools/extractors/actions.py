"""Action extraction module"""

from typing import List
import logging

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.core.models import Action
from renderdoc_tools.core.exceptions import ActionExtractionError

logger = logging.getLogger(__name__)


class ActionExtractor(BaseExtractor):
    """Extracts actions (draw calls, dispatches, etc.) from capture"""
    
    def extract(self, controller) -> List[Action]:
        """
        Extract all actions from the capture
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            List of Action models
            
        Raises:
            ActionExtractionError: If extraction fails
        """
        if not self.validate(controller):
            raise ActionExtractionError("Invalid controller provided")
        
        self.logger.info("Extracting actions...")
        actions = []
        
        try:
            # Get RenderDoc module for constants
            from renderdoc_tools.utils.renderdoc_loader import get_renderdoc_module
            rd = get_renderdoc_module()
            
            root_actions = controller.GetRootActions()
            for action in root_actions:
                self._process_action(action, actions, rd, depth=0)
            
            self.logger.info(f"Extracted {len(actions)} actions")
            return actions
            
        except Exception as e:
            self.logger.error(f"Failed to extract actions: {e}")
            raise ActionExtractionError(f"Action extraction failed: {e}") from e
    
    def _process_action(
        self,
        action,
        actions: List[Action],
        rd,
        depth: int = 0
    ):
        """Recursively process an action and its children"""
        action_data = {
            'eventId': action.eventId,
            'actionId': action.actionId,
            'name': action.customName,
            'flags': str(action.flags),
            'depth': depth,
        }
        
        # Add draw call specific info
        if action.flags & rd.ActionFlags.Drawcall:
            action_data.update({
                'numIndices': action.numIndices,
                'numInstances': action.numInstances,
                'indexOffset': action.indexOffset,
                'vertexOffset': action.vertexOffset,
                'instanceOffset': action.instanceOffset,
            })
        
        # Add dispatch info
        if action.flags & rd.ActionFlags.Dispatch:
            # Convert tuple/list to dict if needed
            dispatch_dim = action.dispatchDimension
            if isinstance(dispatch_dim, (list, tuple)):
                action_data['dispatchDimension'] = {
                    'x': dispatch_dim[0] if len(dispatch_dim) > 0 else 0,
                    'y': dispatch_dim[1] if len(dispatch_dim) > 1 else 0,
                    'z': dispatch_dim[2] if len(dispatch_dim) > 2 else 0,
                }
            else:
                action_data['dispatchDimension'] = dispatch_dim
            
            dispatch_threads = action.dispatchThreadsDimension
            if isinstance(dispatch_threads, (list, tuple)):
                action_data['dispatchThreadsDimension'] = {
                    'x': dispatch_threads[0] if len(dispatch_threads) > 0 else 0,
                    'y': dispatch_threads[1] if len(dispatch_threads) > 1 else 0,
                    'z': dispatch_threads[2] if len(dispatch_threads) > 2 else 0,
                }
            else:
                action_data['dispatchThreadsDimension'] = dispatch_threads
        
        # Create Action model
        try:
            action_model = Action(**action_data)
            actions.append(action_model)
        except Exception as e:
            self.logger.warning(f"Failed to create Action model: {e}")
        
        # Process children
        for child in action.children:
            self._process_action(child, actions, rd, depth + 1)
    
    @property
    def name(self) -> str:
        return "actions"

