"""Multiview rendering analysis"""

from typing import Dict, Any, List
import logging

from renderdoc_tools.analyzers.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class MultiviewAnalyzer(BaseAnalyzer):
    """Analyzes multiview/stereo rendering patterns"""
    
    def analyze(self, capture_data: Dict[str, Any], controller=None) -> Dict[str, Any]:
        """
        Analyze multiview rendering patterns
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            controller: Optional RenderDoc controller
            
        Returns:
            Dictionary with multiview analysis results
        """
        self.logger.info("Analyzing multiview rendering...")
        
        result = {
            'multiview_render_targets': [],
            'stereo_textures': [],
            'summary': {}
        }
        
        # Extract resources
        resources = capture_data.get('resources', [])
        
        # Find multiview render targets (array size 2 typically indicates stereo)
        multiview_rts = []
        for res in resources:
            # Handle both dict and Pydantic model
            if hasattr(res, 'resource_type'):
                res_type = res.resource_type
                texture = res.texture
            else:
                res_type = res.get('type', '')
                texture = res.get('texture')
            
            if res_type == 'Texture' and texture:
                # Handle both dict and Pydantic model
                if hasattr(texture, 'array_size'):
                    array_size = texture.array_size
                    width = texture.width
                    height = texture.height
                else:
                    array_size = texture.get('arraysize', texture.get('array_size', 0))
                    width = texture.get('width', 0)
                    height = texture.get('height', 0)
                
                # Quest typically uses array size 2 for stereo
                if array_size == 2:
                    multiview_rts.append({
                        'name': res.name if hasattr(res, 'name') else res.get('name', ''),
                        'width': width,
                        'height': height,
                        'array_size': array_size
                    })
        
        result['multiview_render_targets'] = multiview_rts
        result['stereo_textures'] = multiview_rts  # Alias for clarity
        
        result['summary'] = {
            'multiview_targets_found': len(multiview_rts),
            'likely_stereo_rendering': len(multiview_rts) > 0
        }
        
        return result
    
    @property
    def name(self) -> str:
        return "multiview"

