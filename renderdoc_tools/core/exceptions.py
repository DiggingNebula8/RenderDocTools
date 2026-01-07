"""Custom exception hierarchy for RenderDoc Tools"""


class RenderDocError(Exception):
    """Base exception for all RenderDoc-related errors"""
    pass


class RenderDocNotFoundError(RenderDocError):
    """Raised when RenderDoc module cannot be found or imported"""
    pass


class CaptureError(RenderDocError):
    """Base exception for capture-related errors"""
    pass


class CaptureOpenError(CaptureError):
    """Raised when a capture file cannot be opened"""
    pass


class CaptureReplayError(CaptureError):
    """Raised when a capture cannot be replayed on the current system"""
    pass


class ExtractionError(RenderDocError):
    """Base exception for data extraction errors"""
    pass


class ActionExtractionError(ExtractionError):
    """Raised when action extraction fails"""
    pass


class ResourceExtractionError(ExtractionError):
    """Raised when resource extraction fails"""
    pass


class ShaderExtractionError(ExtractionError):
    """Raised when shader extraction fails"""
    pass


class PipelineExtractionError(ExtractionError):
    """Raised when pipeline state extraction fails"""
    pass


class CounterExtractionError(ExtractionError):
    """Raised when performance counter extraction fails"""
    pass


class ExportError(RenderDocError):
    """Base exception for export errors"""
    pass


class JSONExportError(ExportError):
    """Raised when JSON export fails"""
    pass


class CSVExportError(ExportError):
    """Raised when CSV export fails"""
    pass

