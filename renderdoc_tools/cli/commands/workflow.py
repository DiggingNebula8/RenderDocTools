"""Workflow CLI command"""

import sys
import argparse
from pathlib import Path

from renderdoc_tools.workflows import WorkflowRunner, get_preset, list_presets
from renderdoc_tools.utils.logging_config import setup_logging


def workflow_command(args):
    """Execute workflow command"""
    parser = argparse.ArgumentParser(description='Run workflow preset on RDC file')
    parser.add_argument('rdc_file', nargs='?', help='Path to RDC capture file')
    parser.add_argument('--preset', '-p', default='quick', help='Workflow preset')
    parser.add_argument('--output-dir', '-o', help='Output directory')
    parser.add_argument('--list-presets', action='store_true', help='List all presets')
    parser.add_argument('--log-level', default='INFO', help='Logging level')
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.list_presets:
        print("\nAvailable Workflow Presets:")
        print("=" * 60)
        presets = list_presets()
        for name, desc in presets.items():
            print(f"  {name:12} - {desc}")
        print()
        return
    
    if not parsed_args.rdc_file:
        parser.error("rdc_file is required when not using --list-presets")
    
    setup_logging(level=parsed_args.log_level)
    
    rdc_path = Path(parsed_args.rdc_file)
    if not rdc_path.exists():
        print(f"ERROR: File not found: {rdc_path}")
        sys.exit(1)
    
    output_dir = Path(parsed_args.output_dir) if parsed_args.output_dir else None
    
    try:
        preset = get_preset(parsed_args.preset)
        runner = WorkflowRunner(preset)
        capture_data = runner.run(rdc_path, output_dir)
        
        print(f"\n✓ Workflow '{parsed_args.preset}' completed!")
        print(f"  Actions: {len(capture_data.actions)}")
        print(f"  Resources: {len(capture_data.resources)}")
        print(f"  Shaders: {len(capture_data.shaders)}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

