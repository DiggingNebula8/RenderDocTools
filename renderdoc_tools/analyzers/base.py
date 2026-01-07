"""Base classes for analyzers"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """Abstract base class for all analyzers"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def analyze(self, capture_data: Dict[str, Any], controller=None) -> Dict[str, Any]:
        """
        Analyze capture data
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            controller: Optional RenderDoc controller for additional analysis
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name identifier for this analyzer"""
        pass

