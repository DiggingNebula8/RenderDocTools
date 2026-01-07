"""Unit tests for exporters"""
import pytest
import json
import tempfile
from pathlib import Path
from renderdoc_tools.exporters import JSONExporter, CSVExporter
from renderdoc_tools.core.models import CaptureData, CaptureInfo, Action


class TestJSONExporter:
    """Tests for JSONExporter"""
    
    def test_exporter_properties(self):
        """Test exporter has correct properties"""
        exporter = JSONExporter()
        assert exporter.format_name == "json"
        assert exporter.file_extension == "json"
    
    def test_export_basic_data(self):
        """Test exporting basic capture data to JSON"""
        # Create test data
        capture_data = CaptureData(
            capture_info=CaptureInfo(api=2),
            actions=[
                Action(eventId=1, actionId=1, name="DrawIndexed", flags="Drawcall")
            ]
        )
        
        # Export to temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.json"
            exporter = JSONExporter()
            exporter.export(capture_data, output_path)
            
            # Verify file was created
            assert output_path.exists()
            
            # Verify content is valid JSON
            with open(output_path) as f:
                data = json.load(f)
                assert "captureInfo" in data or "capture_info" in data
                assert "actions" in data


class TestCSVExporter:
    """Tests for CSVExporter"""
    
    def test_exporter_properties(self):
        """Test exporter has correct properties"""
        exporter = CSVExporter()
        assert exporter.format_name == "csv"
        assert exporter.file_extension == "csv"
