"""Fixed foveated rendering analysis"""

from typing import Dict, Any
import logging

from renderdoc_tools.analyzers.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class FoveationAnalyzer(BaseAnalyzer):
    """Checks for fixed foveated rendering patterns"""
    
    def analyze(self, capture_data: Dict[str, Any], controller=None) -> Dict[str, Any]:
        """
        Analyze fixed foveated rendering patterns
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            controller: Optional RenderDoc controller
            
        Returns:
            Dictionary with foveation analysis results
        """
        self.logger.info("Analyzing fixed foveated rendering...")
        
        result = {
            'total_actions': 0,
            'render_passes': [],
            'multiple_passes_detected': False,
            'summary': {}
        }
        
        # Extract actions
        actions = capture_data.get('actions', [])
        result['total_actions'] = len(actions)
        
        # Check for render passes
        render_passes = []
        for action in actions:
            # Handle both dict and Pydantic model
            if hasattr(action, 'name'):
                name = action.name
            else:
                name = action.get('name', '')
            
            if 'RenderPass' in name or 'Renderpass' in name:
                render_passes.append({
                    'name': name,
                    'event_id': action.event_id if hasattr(action, 'event_id') else action.get('eventId', 0)
                })
        
        result['render_passes'] = render_passes
        result['multiple_passes_detected'] = len(render_passes) > 1
        
        result['summary'] = {
            'render_pass_count': len(render_passes),
            'possible_ffr': len(render_passes) > 1,
            'note': 'Multiple render passes might indicate FFR or post-processing. Check tile timeline in RenderDoc Meta Fork for confirmation.'
        }
        
        return result
    
    @property
    def name(self) -> str:
        return "foveation"

