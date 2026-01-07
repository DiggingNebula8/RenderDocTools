"""Shader extraction module"""

from typing import List
import logging

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.core.models import Shader
from renderdoc_tools.core.exceptions import ShaderExtractionError

logger = logging.getLogger(__name__)


class ShaderExtractor(BaseExtractor):
    """Extracts shader information from capture"""
    
    def extract(self, controller) -> List[Shader]:
        """
        Extract all shaders from the capture
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            List of Shader models
            
        Raises:
            ShaderExtractionError: If extraction fails
        """
        if not self.validate(controller):
            raise ShaderExtractionError("Invalid controller provided")
        
        self.logger.info("Extracting shaders...")
        shaders = []
        
        try:
            resources = controller.GetResources()
            for res in resources:
                try:
                    # Try to get shader reflection - if it works, it's a shader
                    reflection = controller.GetShader(res.resourceId)
                    if reflection:
                        shader_data = {
                            'resourceId': str(res.resourceId),
                            'name': res.name,
                            'stage': str(reflection.stage) if hasattr(reflection, 'stage') else 'Unknown',
                            'entryPoint': reflection.entryPoint if hasattr(reflection, 'entryPoint') else None,
                        }
                        
                        # Get reflection details
                        reflection_data = {}
                        try:
                            if hasattr(reflection, 'debugInfo') and reflection.debugInfo:
                                reflection_data['debugInfo'] = reflection.debugInfo.compileFlags
                            if hasattr(reflection, 'inputSignature'):
                                reflection_data['inputSig_count'] = len(reflection.inputSignature)
                            if hasattr(reflection, 'outputSignature'):
                                reflection_data['outputSig_count'] = len(reflection.outputSignature)
                        except Exception as e:
                            self.logger.debug(f"Could not extract full reflection: {e}")
                        
                        if reflection_data:
                            shader_data['reflection'] = reflection_data
                        
                        # Create Shader model
                        try:
                            shader_model = Shader(**shader_data)
                            shaders.append(shader_model)
                        except Exception as e:
                            self.logger.warning(f"Failed to create Shader model: {e}")
                except Exception:
                    # Not a shader or GetShader failed, skip
                    pass
            
            self.logger.info(f"Extracted {len(shaders)} shaders")
            return shaders
            
        except Exception as e:
            self.logger.error(f"Failed to extract shaders: {e}")
            raise ShaderExtractionError(f"Shader extraction failed: {e}") from e
    
    @property
    def name(self) -> str:
        return "shaders"

