"""JSON export module"""

import json
from pathlib import Path
from typing import Any, Dict
import logging

from renderdoc_tools.exporters.base import BaseExporter
from renderdoc_tools.core.exceptions import JSONExportError
from renderdoc_tools.core.models import CaptureData

logger = logging.getLogger(__name__)


class JSONExporter(BaseExporter):
    """Exports data to JSON format"""
    
    def __init__(self, pretty: bool = True, indent: int = 2):
        """
        Initialize JSON exporter
        
        Args:
            pretty: Whether to pretty-print JSON
            indent: Indentation level for pretty printing
        """
        super().__init__()
        self.pretty = pretty
        self.indent = indent if pretty else None
    
    def export(self, data: Any, output_path: Path) -> None:
        """
        Export data to JSON file
        
        Args:
            data: Data to export (dict or CaptureData model)
            output_path: Output JSON file path
            
        Raises:
            JSONExportError: If export fails
        """
        if not self.validate_output_path(output_path):
            raise JSONExportError(f"Invalid output path: {output_path}")
        
        self.logger.info(f"Exporting to JSON: {output_path}")
        
        try:
            # Convert Pydantic models to dict if needed
            if isinstance(data, CaptureData):
                json_data = data.dict(by_alias=True, exclude_none=True)
            elif isinstance(data, dict):
                json_data = data
            else:
                # Try to serialize other types
                json_data = self._serialize(data)
            
            # Write JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(
                    json_data,
                    f,
                    indent=self.indent,
                    ensure_ascii=False
                )
            
            self.logger.info(f"Successfully exported to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to export JSON: {e}")
            raise JSONExportError(f"JSON export failed: {e}") from e
    
    def _serialize(self, obj: Any) -> Dict:
        """Serialize object to JSON-serializable dict"""
        if hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        return str(obj)
    
    @property
    def format_name(self) -> str:
        return "json"
    
    @property
    def file_extension(self) -> str:
        return "json"

