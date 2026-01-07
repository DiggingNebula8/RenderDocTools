"""Base classes for data exporters"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """Abstract base class for all data exporters"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def export(self, data: Any, output_path: Path) -> None:
        """
        Export data to file
        
        Args:
            data: Data to export
            output_path: Output file path
            
        Raises:
            ExportError: If export fails
        """
        pass
    
    @property
    @abstractmethod
    def format_name(self) -> str:
        """Format identifier (e.g., 'json', 'csv')"""
        pass
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """Default file extension for this format"""
        pass
    
    def validate_output_path(self, output_path: Path) -> bool:
        """
        Validate output path
        
        Args:
            output_path: Path to validate
            
        Returns:
            True if path is valid
        """
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return True

