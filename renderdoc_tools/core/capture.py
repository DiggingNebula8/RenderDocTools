"""Capture file handling"""

from pathlib import Path
from typing import Optional
import logging

from renderdoc_tools.utils.renderdoc_loader import get_renderdoc_module
from renderdoc_tools.core.exceptions import (
    CaptureOpenError,
    CaptureReplayError,
    RenderDocNotFoundError
)

logger = logging.getLogger(__name__)


class CaptureFile:
    """Context manager for RenderDoc capture files"""
    
    def __init__(self, rdc_path: Path):
        """
        Initialize capture file handler
        
        Args:
            rdc_path: Path to RDC capture file
            
        Raises:
            FileNotFoundError: If RDC file doesn't exist
        """
        self.rdc_path = Path(rdc_path)
        if not self.rdc_path.exists():
            raise FileNotFoundError(f"RDC file not found: {self.rdc_path}")
        
        self.cap = None
        self.controller = None
        self._rd = None
    
    def __enter__(self):
        """Open capture file and initialize replay"""
        try:
            # Load RenderDoc module
            self._rd = get_renderdoc_module()
            
            # Initialize replay
            self._rd.InitialiseReplay(self._rd.GlobalEnvironment(), [])
            
            # Open capture file
            self.cap = self._rd.OpenCaptureFile()
            result = self.cap.OpenFile(str(self.rdc_path), '', None)
            
            if result != self._rd.ResultCode.Succeeded:
                raise CaptureOpenError(f"Couldn't open file: {result}")
            
            if not self.cap.LocalReplaySupport():
                raise CaptureReplayError("Capture cannot be replayed on this system")
            
            # Open capture for replay
            result, self.controller = self.cap.OpenCapture(self._rd.ReplayOptions(), None)
            
            if result != self._rd.ResultCode.Succeeded:
                raise CaptureReplayError(f"Couldn't initialize replay: {result}")
            
            logger.info(f"Successfully opened capture: {self.rdc_path}")
            return self
        
        except RenderDocNotFoundError:
            raise
        except (CaptureOpenError, CaptureReplayError):
            raise
        except Exception as e:
            logger.error(f"Failed to open capture: {e}")
            raise CaptureOpenError(f"Failed to open capture: {e}") from e
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources"""
        try:
            if self.controller:
                self.controller.Shutdown()
            if self.cap:
                self.cap.Shutdown()
            if self._rd:
                self._rd.ShutdownReplay()
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
        finally:
            self.controller = None
            self.cap = None
            self._rd = None

