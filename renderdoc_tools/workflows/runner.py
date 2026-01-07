"""Workflow execution engine"""

from pathlib import Path
from typing import Optional, Callable, Dict, Any
import logging

from renderdoc_tools.core import CaptureFile
from renderdoc_tools.core.models import CaptureData
from renderdoc_tools.core.capture_info import CaptureInfoExtractor
from renderdoc_tools.workflows.base import Workflow
from renderdoc_tools.exporters import JSONExporter

logger = logging.getLogger(__name__)


class WorkflowRunner:
    """Executes workflows on capture files"""
    
    def __init__(
        self,
        workflow: Workflow,
        progress_callback: Optional[Callable[[str], None]] = None
    ):
        """
        Initialize workflow runner
        
        Args:
            workflow: Workflow to execute
            progress_callback: Optional callback for progress updates
        """
        self.workflow = workflow
        self.progress_callback = progress_callback
        self.logger = logging.getLogger(__name__)
    
    def run(
        self,
        rdc_path: Path,
        output_dir: Optional[Path] = None
    ) -> CaptureData:
        """
        Execute workflow on capture file
        
        Args:
            rdc_path: Path to RDC capture file
            output_dir: Output directory (default: rdc_output/)
            
        Returns:
            Extracted capture data
        """
        rdc_path = Path(rdc_path)
        output_dir = output_dir or Path('rdc_output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Running workflow '{self.workflow.name}' on {rdc_path}")
        self._update_progress(f"Running workflow: {self.workflow.name}")
        
        # Open capture
        self._update_progress("Opening capture file...")
        with CaptureFile(rdc_path) as capture:
            # Extract capture info
            capture_info_extractor = self.workflow.capture_info_extractor or CaptureInfoExtractor()
            capture_info = capture_info_extractor.extract(capture.controller)
            
            self._update_progress(f"API: {capture_info.api}, Meta Fork: {capture_info.is_meta_fork}")
            
            # Extract data using configured extractors
            self._update_progress("Extracting data...")
            capture_data = self._extract_data(capture.controller, capture_info)
            
            # Run analyzers
            if self.workflow.analyzers:
                self._update_progress("Running analyzers...")
                analysis_results = self._run_analyzers(capture_data, capture.controller)
                # Store analysis results
                if analysis_results:
                    capture_data_dict = capture_data.dict(by_alias=True) if hasattr(capture_data, 'dict') else capture_data
                    capture_data_dict['analysis'] = analysis_results
            
            # Export data
            if self.workflow.exporters:
                self._update_progress("Exporting data...")
                self._export_data(capture_data, output_dir, rdc_path.stem)
        
        self._update_progress("Workflow complete!")
        return capture_data
    
    def _extract_data(self, controller, capture_info) -> CaptureData:
        """Extract data using configured extractors"""
        actions = []
        resources = []
        shaders = []
        pipeline_states = None
        performance_counters = None
        
        for extractor in self.workflow.extractors:
            self.logger.debug(f"Running extractor: {extractor.name}")
            self._update_progress(f"Extracting {extractor.name}...")
            
            extracted = extractor.extract(controller)
            
            if extractor.name == "actions":
                actions = extracted
            elif extractor.name == "resources":
                resources = extracted
            elif extractor.name == "shaders":
                shaders = extracted
            elif extractor.name == "pipeline":
                pipeline_states = extracted
            elif extractor.name == "counters":
                performance_counters = extracted
        
        capture_data = CaptureData(
            capture_info=capture_info,
            actions=actions,
            resources=resources,
            shaders=shaders,
            pipeline_states=pipeline_states,
            performance_counters=performance_counters
        )
        
        return capture_data
    
    def _run_analyzers(
        self,
        capture_data: CaptureData,
        controller
    ) -> Dict[str, Any]:
        """Run configured analyzers"""
        results = {}
        
        # Convert CaptureData to dict for analyzers
        if hasattr(capture_data, 'dict'):
            capture_data_dict = capture_data.dict(by_alias=True)
        else:
            capture_data_dict = capture_data
        
        for analyzer in self.workflow.analyzers:
            self.logger.debug(f"Running analyzer: {analyzer.name}")
            try:
                analysis_result = analyzer.analyze(capture_data_dict, controller)
                results[analyzer.name] = analysis_result
            except Exception as e:
                self.logger.warning(f"Analyzer {analyzer.name} failed: {e}")
                results[analyzer.name] = {'error': str(e)}
        
        return results
    
    def _export_data(
        self,
        capture_data: CaptureData,
        output_dir: Path,
        base_name: str
    ):
        """Export data using configured exporters"""
        for exporter in self.workflow.exporters:
            # Generate output path
            if exporter.format_name == "csv":
                # CSV exporter handles its own file naming
                output_path = output_dir / f"{base_name}.csv"
            else:
                output_path = output_dir / f"{base_name}.{exporter.file_extension}"
            
            self.logger.debug(f"Exporting to {output_path}")
            self._update_progress(f"Exporting {exporter.format_name}...")
            
            try:
                exporter.export(capture_data, output_path)
            except Exception as e:
                self.logger.error(f"Export failed: {e}")
                raise
    
    def _update_progress(self, message: str):
        """Update progress if callback provided"""
        self.logger.info(message)
        if self.progress_callback:
            self.progress_callback(message)

