"""CSV export module"""

import csv
from pathlib import Path
from typing import Any, List, Dict
import logging

from renderdoc_tools.exporters.base import BaseExporter
from renderdoc_tools.core.exceptions import CSVExportError
from renderdoc_tools.core.models import CaptureData, Action, Resource

logger = logging.getLogger(__name__)


class CSVExporter(BaseExporter):
    """Exports data to CSV format"""
    
    def export(self, data: Any, output_path: Path) -> None:
        """
        Export data to CSV file(s)
        
        Args:
            data: Data to export (CaptureData model or dict)
            output_path: Output CSV file path (base path, will create multiple files)
            
        Raises:
            CSVExportError: If export fails
        """
        if not self.validate_output_path(output_path):
            raise CSVExportError(f"Invalid output path: {output_path}")
        
        self.logger.info(f"Exporting to CSV: {output_path}")
        
        try:
            # Handle CaptureData model
            if isinstance(data, CaptureData):
                # Export actions
                if data.actions:
                    actions_path = output_path.parent / f"{output_path.stem}_actions.csv"
                    self._export_actions(data.actions, actions_path)
                
                # Export resources
                if data.resources:
                    resources_path = output_path.parent / f"{output_path.stem}_resources.csv"
                    self._export_resources(data.resources, resources_path)
            
            # Handle dict with actions/resources keys
            elif isinstance(data, dict):
                if 'actions' in data and data['actions']:
                    actions_path = output_path.parent / f"{output_path.stem}_actions.csv"
                    self._export_actions(data['actions'], actions_path)
                
                if 'resources' in data and data['resources']:
                    resources_path = output_path.parent / f"{output_path.stem}_resources.csv"
                    self._export_resources(data['resources'], resources_path)
            
            else:
                raise CSVExportError(f"Unsupported data type for CSV export: {type(data)}")
            
            self.logger.info(f"Successfully exported CSV files")
            
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {e}")
            raise CSVExportError(f"CSV export failed: {e}") from e
    
    def _export_actions(self, actions: List[Action], output_path: Path):
        """Export actions to CSV"""
        if not actions:
            return
        
        # Convert to dicts
        action_dicts = []
        for action in actions:
            if isinstance(action, Action):
                action_dict = action.dict(by_alias=True, exclude_none=True)
            else:
                action_dict = action
            action_dicts.append(action_dict)
        
        # Get all unique keys
        fieldnames = sorted(set().union(*[a.keys() for a in action_dicts]))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(action_dicts)
        
        self.logger.debug(f"Exported {len(action_dicts)} actions to {output_path}")
    
    def _export_resources(self, resources: List[Resource], output_path: Path):
        """Export resources to CSV"""
        if not resources:
            return
        
        # Flatten nested dicts for CSV
        flat_resources = []
        for res in resources:
            if isinstance(res, Resource):
                res_dict = res.dict(by_alias=True, exclude_none=True)
            else:
                res_dict = res
            
            flat_res = {
                'resourceId': res_dict.get('resourceId', ''),
                'name': res_dict.get('name', ''),
                'type': res_dict.get('type', ''),
            }
            
            # Flatten texture info
            if 'texture' in res_dict and res_dict['texture']:
                tex = res_dict['texture']
                if isinstance(tex, dict):
                    for k, v in tex.items():
                        flat_res[f'texture_{k}'] = v
                else:
                    # Pydantic model
                    for k, v in tex.dict().items():
                        flat_res[f'texture_{k}'] = v
            
            # Flatten buffer info
            if 'buffer' in res_dict and res_dict['buffer']:
                buf = res_dict['buffer']
                if isinstance(buf, dict):
                    for k, v in buf.items():
                        flat_res[f'buffer_{k}'] = v
                else:
                    # Pydantic model
                    for k, v in buf.dict().items():
                        flat_res[f'buffer_{k}'] = v
            
            flat_resources.append(flat_res)
        
        # Get all unique keys
        fieldnames = sorted(set().union(*[r.keys() for r in flat_resources]))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_resources)
        
        self.logger.debug(f"Exported {len(flat_resources)} resources to {output_path}")
    
    @property
    def format_name(self) -> str:
        return "csv"
    
    @property
    def file_extension(self) -> str:
        return "csv"

