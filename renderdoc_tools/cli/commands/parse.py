"""Parse CLI command"""

import sys
import argparse
from pathlib import Path

from renderdoc_tools.parser import Parser
from renderdoc_tools.exporters import JSONExporter, CSVExporter
from renderdoc_tools.utils.logging_config import setup_logging


def parse_command(args):
    """Execute parse command"""
    parser = argparse.ArgumentParser(description='Parse RDC file')
    parser.add_argument('rdc_file', help='Path to RDC capture file')
    parser.add_argument('-o', '--output', help='Output JSON file path')
    parser.add_argument('--actions', help='Export actions to CSV')
    parser.add_argument('--resources', help='Export resources to CSV')
    parser.add_argument('--pipeline', action='store_true', help='Include pipeline state')
    parser.add_argument('--counters', action='store_true', help='Include performance counters')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    
    parsed_args = parser.parse_args(args)
    
    setup_logging(level=parsed_args.log_level)
    
    rdc_path = Path(parsed_args.rdc_file)
    if not rdc_path.exists():
        print(f"ERROR: File not found: {rdc_path}")
        sys.exit(1)
    
    if not any([parsed_args.output, parsed_args.actions, parsed_args.resources]):
        print("ERROR: Specify at least one output option (-o, --actions, or --resources)")
        parser.print_help()
        sys.exit(1)
    
    try:
        parser = Parser(
            include_pipeline=parsed_args.pipeline,
            include_counters=parsed_args.counters
        )
        capture_data = parser.parse(rdc_path)
        
        # Export JSON
        if parsed_args.output:
            json_exporter = JSONExporter()
            json_exporter.export(capture_data, Path(parsed_args.output))
        
        # Export CSV
        if parsed_args.actions or parsed_args.resources:
            csv_exporter = CSVExporter()
            base_path = Path(parsed_args.actions or parsed_args.resources or 'output')
            
            if parsed_args.actions:
                # Export just actions
                from renderdoc_tools.core.models import CaptureData
                actions_only = CaptureData(
                    capture_info=capture_data.capture_info,
                    actions=capture_data.actions
                )
                csv_exporter.export(actions_only, base_path)
            
            if parsed_args.resources:
                # Export just resources
                from renderdoc_tools.core.models import CaptureData
                resources_only = CaptureData(
                    capture_info=capture_data.capture_info,
                    resources=capture_data.resources
                )
                csv_exporter.export(resources_only, Path(parsed_args.resources))
        
        print("\n✓ Parsing complete!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

