"""Resource extraction module"""

from typing import List
import logging

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.core.models import Resource, TextureInfo, BufferInfo
from renderdoc_tools.core.exceptions import ResourceExtractionError

logger = logging.getLogger(__name__)


class ResourceExtractor(BaseExtractor):
    """Extracts resources (textures, buffers) from capture"""
    
    def extract(self, controller) -> List[Resource]:
        """
        Extract all resources from the capture
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            List of Resource models
            
        Raises:
            ResourceExtractionError: If extraction fails
        """
        if not self.validate(controller):
            raise ResourceExtractionError("Invalid controller provided")
        
        self.logger.info("Extracting resources...")
        resources = []
        
        try:
            from renderdoc_tools.utils.renderdoc_loader import get_renderdoc_module
            rd = get_renderdoc_module()
            
            for res in controller.GetResources():
                res_data = {
                    'resourceId': str(res.resourceId),
                    'name': res.name,
                    'type': str(res.type),
                }
                
                # Get texture info if applicable
                if res.type == rd.ResourceType.Texture:
                    try:
                        textures = controller.GetTextures()
                        tex_desc = None
                        for tex in textures:
                            if tex.resourceId == res.resourceId:
                                tex_desc = tex
                                break
                        
                        if tex_desc:
                            texture_info = TextureInfo(
                                width=tex_desc.width,
                                height=tex_desc.height,
                                depth=tex_desc.depth,
                                mips=tex_desc.mips,
                                arraysize=tex_desc.arraysize,
                                format=str(tex_desc.format.Name()) if hasattr(tex_desc.format, 'Name') else str(tex_desc.format),
                                type=str(tex_desc.type)
                            )
                            res_data['texture'] = texture_info
                        else:
                            self.logger.warning(f"Texture not found in GetTextures() list: {res.name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to extract texture info for {res.name}: {e}")
                
                # Get buffer info if applicable
                elif res.type == rd.ResourceType.Buffer:
                    try:
                        if hasattr(controller, 'GetBuffer'):
                            buf_desc = controller.GetBuffer(res.resourceId)
                            buffer_info = BufferInfo(length=buf_desc.length)
                            res_data['buffer'] = buffer_info
                        else:
                            buffer_info = BufferInfo(
                                length=None,
                                note='Buffer details not available in this RenderDoc version'
                            )
                            res_data['buffer'] = buffer_info
                    except Exception as e:
                        buffer_info = BufferInfo(
                            length=None,
                            error=f'Could not extract buffer information: {e}'
                        )
                        res_data['buffer'] = buffer_info
                
                # Create Resource model
                try:
                    resource_model = Resource(**res_data)
                    resources.append(resource_model)
                except Exception as e:
                    self.logger.warning(f"Failed to create Resource model: {e}")
            
            self.logger.info(f"Extracted {len(resources)} resources")
            return resources
            
        except Exception as e:
            self.logger.error(f"Failed to extract resources: {e}")
            raise ResourceExtractionError(f"Resource extraction failed: {e}") from e
    
    @property
    def name(self) -> str:
        return "resources"

