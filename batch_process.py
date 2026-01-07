#!/usr/bin/env python3
"""
Batch RDC Processing Tool
Process multiple capture files with progress tracking and error handling
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List
from datetime import datetime
import time

from renderdoc_tools.workflows import WorkflowRunner, get_preset


class BatchProcessor:
    """Process multiple RDC files in batch"""
    
    def __init__(self, output_base_dir: str = './batch_output'):
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.start_time = None
    
    def process_files(self, 
                     rdc_files: List[Path], 
                     preset: str = 'quick',
                     continue_on_error: bool = True):
        """Process multiple RDC files"""
        
        self.start_time = time.time()
        total = len(rdc_files)
        
        print(f"\n{'='*60}")
        print(f"Batch Processing: {total} file(s)")
        print(f"Preset: {preset}")
        print(f"Output: {self.output_base_dir}")
        print(f"{'='*60}\n")
        
        # Get workflow preset
        try:
            workflow_preset = get_preset(preset)
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
        
        for idx, rdc_file in enumerate(rdc_files, 1):
            print(f"\n[{idx}/{total}] Processing: {rdc_file.name}")
            print("-" * 60)
            
            try:
                # Create per-file output directory
                file_output_dir = self.output_base_dir / rdc_file.stem
                
                runner = WorkflowRunner(workflow_preset)
                runner.run(rdc_file, file_output_dir)
                
                self.results.append({
                    'file': str(rdc_file),
                    'status': 'success',
                    'output_dir': str(file_output_dir),
                })
                print(f"✓ [{idx}/{total}] Completed: {rdc_file.name}")
                
            except Exception as e:
                error_msg = str(e)
                print(f"✗ [{idx}/{total}] Failed: {rdc_file.name}")
                print(f"  Error: {error_msg}")
                
                self.results.append({
                    'file': str(rdc_file),
                    'status': 'error',
                    'error': error_msg,
                })
                
                if not continue_on_error:
                    print("\nStopping batch processing due to error")
                    break
        
        # Generate batch report
        self._generate_batch_report(preset)
    
    def _generate_batch_report(self, preset: str):
        """Generate summary report for batch processing"""
        elapsed = time.time() - self.start_time
        
        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'error']
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'preset': preset,
            'summary': {
                'total': len(self.results),
                'successful': len(successful),
                'failed': len(failed),
                'elapsed_seconds': round(elapsed, 2),
            },
            'results': self.results,
        }
        
        report_path = self.output_base_dir / 'batch_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"Batch Processing Complete")
        print(f"{'='*60}")
        print(f"Total files:    {report['summary']['total']}")
        print(f"Successful:     {report['summary']['successful']}")
        print(f"Failed:         {report['summary']['failed']}")
        print(f"Elapsed time:   {report['summary']['elapsed_seconds']:.2f}s")
        print(f"\nReport saved:   {report_path}")
        
        if failed:
            print(f"\nFailed files:")
            for result in failed:
                print(f"  - {Path(result['file']).name}: {result.get('error', 'Unknown error')}")


def find_rdc_files(paths: List[str], recursive: bool = False) -> List[Path]:
    """Find all RDC files from given paths"""
    rdc_files = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if path.is_file() and path.suffix.lower() == '.rdc':
            rdc_files.append(path)
        elif path.is_dir():
            if recursive:
                rdc_files.extend(path.rglob('*.rdc'))
            else:
                rdc_files.extend(path.glob('*.rdc'))
        else:
            print(f"Warning: Skipping invalid path: {path}")
    
    return sorted(set(rdc_files))  # Remove duplicates and sort


def main():
    parser = argparse.ArgumentParser(
        description='Batch process multiple RDC capture files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all RDC files in a directory
  python batch_process.py captures/ --preset quick
  
  # Process specific files
  python batch_process.py file1.rdc file2.rdc --preset quest
  
  # Recursive directory search
  python batch_process.py captures/ --recursive --preset full
  
  # Custom output directory
  python batch_process.py captures/ --output-dir ./results --preset quick
        """
    )
    
    parser.add_argument('paths', nargs='+',
                       help='RDC files or directories containing .rdc files')
    parser.add_argument('--preset', '-p',
                       default='quick',
                       help='Workflow preset to use (default: quick)')
    parser.add_argument('--output-dir', '-o',
                       default='./batch_output',
                       help='Base output directory (default: ./batch_output)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Recursively search directories')
    parser.add_argument('--stop-on-error', action='store_true',
                       help='Stop processing on first error')
    
    args = parser.parse_args()
    
    # Find all RDC files
    rdc_files = find_rdc_files(args.paths, args.recursive)
    
    if not rdc_files:
        print("ERROR: No .rdc files found")
        sys.exit(1)
    
    print(f"Found {len(rdc_files)} RDC file(s)")
    
    # Process files
    processor = BatchProcessor(args.output_dir)
    processor.process_files(
        rdc_files,
        preset=args.preset,
        continue_on_error=not args.stop_on_error
    )


if __name__ == '__main__':
    main()
