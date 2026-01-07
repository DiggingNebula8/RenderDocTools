"""Base classes for data extractors"""

from abc import ABC, abstractmethod
from typing import List, Any
import logging

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):
    """Abstract base class for all data extractors"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def extract(self, controller) -> List[Any]:
        """
        Extract data from RenderDoc controller
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            List of extracted data items
            
        Raises:
            ExtractionError: If extraction fails
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name identifier for this extractor"""
        pass
    
    def validate(self, controller) -> bool:
        """
        Validate that extraction is possible
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            True if extraction is possible
        """
        return controller is not None

