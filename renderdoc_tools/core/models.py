"""Data models for RenderDoc capture data"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class API(str, Enum):
    """Graphics API types"""
    D3D11 = "D3D11"
    D3D12 = "D3D12"
    VULKAN = "Vulkan"
    OPENGL = "OpenGL"


class CaptureInfo(BaseModel):
    """Capture file metadata"""
    api: int  # RenderDoc API type (will be converted to API enum if needed)
    frame_info: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="frame_info")
    
    class Config:
        populate_by_name = True


class Action(BaseModel):
    """Represents a single action (draw call, dispatch, etc.)"""
    event_id: int = Field(..., alias="eventId")
    action_id: int = Field(..., alias="actionId")
    name: str
    flags: str
    depth: int = 0
    
    # Draw call specific
    num_indices: Optional[int] = Field(None, alias="numIndices")
    num_instances: Optional[int] = Field(None, alias="numInstances")
    index_offset: Optional[int] = Field(None, alias="indexOffset")
    vertex_offset: Optional[int] = Field(None, alias="vertexOffset")
    instance_offset: Optional[int] = Field(None, alias="instanceOffset")
    
    # Dispatch specific
    dispatch_dimension: Optional[Dict[str, int]] = Field(None, alias="dispatchDimension")
    dispatch_threads_dimension: Optional[Dict[str, int]] = Field(None, alias="dispatchThreadsDimension")
    
    class Config:
        populate_by_name = True


class TextureInfo(BaseModel):
    """Texture resource information"""
    width: int
    height: int
    depth: int = 1
    mips: int = 1
    array_size: int = Field(1, alias="arraysize")
    format: str
    texture_type: str = Field(..., alias="type")


class BufferInfo(BaseModel):
    """Buffer resource information"""
    length: Optional[int] = None
    note: Optional[str] = None
    error: Optional[str] = None


class Resource(BaseModel):
    """Represents a resource (texture, buffer, etc.)"""
    resource_id: str = Field(..., alias="resourceId")
    name: str
    resource_type: str = Field(..., alias="type")
    texture: Optional[TextureInfo] = None
    buffer: Optional[BufferInfo] = None
    
    class Config:
        populate_by_name = True


class Shader(BaseModel):
    """Shader information"""
    resource_id: str = Field(..., alias="resourceId")
    name: str
    stage: str
    entry_point: Optional[str] = Field(None, alias="entryPoint")
    reflection: Optional[Dict[str, Any]] = None
    
    class Config:
        populate_by_name = True


class PipelineState(BaseModel):
    """Pipeline state at a specific event"""
    event_id: int = Field(..., alias="eventId")
    graphics_shader_stages: List[Dict[str, str]] = Field(
        default_factory=list,
        alias="graphicsShaderStages"
    )
    
    class Config:
        populate_by_name = True


class PerformanceCounter(BaseModel):
    """Performance counter information"""
    counter_id: int = Field(..., alias="counterId")
    name: str
    description: str
    category: str
    unit: str


class CaptureData(BaseModel):
    """Complete capture data structure"""
    capture_info: CaptureInfo = Field(..., alias="captureInfo")
    actions: List[Action] = Field(default_factory=list)
    resources: List[Resource] = Field(default_factory=list)
    shaders: List[Shader] = Field(default_factory=list)
    pipeline_states: Optional[List[PipelineState]] = Field(
        None,
        alias="pipelineStates"
    )
    performance_counters: Optional[Dict[str, Any]] = Field(
        None,
        alias="performanceCounters"
    )
    
    class Config:
        populate_by_name = True

