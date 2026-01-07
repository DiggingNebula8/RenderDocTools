#!/usr/bin/env python3
"""
Quest Analysis Script
Uses the renderdoc_tools package for Quest-specific analysis
"""

import sys
from pathlib import Path

from renderdoc_tools.core import CaptureFile
from renderdoc_tools.analyzers.quest import (
    QuestPerformanceAnalyzer,
    MultiviewAnalyzer,
    FoveationAnalyzer,
    QuestReportGenerator
)
from renderdoc_tools.parser import Parser
from renderdoc_tools.utils.logging_config import setup_logging


def analyze_quest_performance(rdc_path: str):
    """Extract Quest-specific profiling data"""
    setup_logging(level="INFO")
    
    parser = Parser(include_counters=True)
    capture_data = parser.parse(Path(rdc_path))
    
    analyzer = QuestPerformanceAnalyzer()
    result = analyzer.analyze(capture_data.dict(by_alias=True))
    
    print(f"\n=== Quest Performance Analysis ===")
    if result.get('performance_counters_available'):
        print(f"✓ Performance counters available!")
        print(f"Total counters: {result['counter_count']}")
        print(f"\nCounters by category:")
        for cat, count in result.get('counters_by_category', {}).items():
            print(f"  {cat}: {count} counters")
    else:
        print(f"⚠ Performance counters not available")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        print(f"   Note: This feature requires RenderDoc Meta Fork with Quest capture")


def analyze_multiview_rendering(rdc_path: str):
    """Analyze multiview/stereo rendering patterns"""
    setup_logging(level="INFO")
    
    parser = Parser()
    capture_data = parser.parse(Path(rdc_path))
    
    analyzer = MultiviewAnalyzer()
    result = analyzer.analyze(capture_data.dict(by_alias=True))
    
    print(f"\n=== Multiview/Stereo Analysis ===")
    multiview_rts = result.get('multiview_render_targets', [])
    print(f"Found {len(multiview_rts)} potential multiview render targets")
    
    if multiview_rts:
        print(f"\nMultiview textures:")
        for rt in multiview_rts[:5]:  # Top 5
            print(f"  {rt['name']}: {rt['width']}x{rt['height']} (array={rt['array_size']})")


def analyze_foveation(rdc_path: str):
    """Check for fixed foveated rendering artifacts"""
    setup_logging(level="INFO")
    
    parser = Parser()
    capture_data = parser.parse(Path(rdc_path))
    
    analyzer = FoveationAnalyzer()
    result = analyzer.analyze(capture_data.dict(by_alias=True))
    
    print(f"\n=== Fixed Foveated Rendering Check ===")
    print(f"Total actions: {result['total_actions']}")
    print(f"Render passes found: {result['summary']['render_pass_count']}")
    
    if result['multiple_passes_detected']:
        print(f"\n⚠ Multiple render passes detected")
        print(f"   This might indicate FFR or post-processing")
        print(f"   Check tile timeline in RenderDoc Meta Fork for confirmation")


def quest_optimization_report(rdc_path: str, output: str):
    """Generate Quest optimization report"""
    setup_logging(level="INFO")
    
    parser = Parser(include_counters=True)
    capture_data = parser.parse(Path(rdc_path))
    
    report_gen = QuestReportGenerator()
    report_path = report_gen.generate_report_file(
        capture_data.dict(by_alias=True),
        Path(output)
    )
    
    report = report_gen.analyze(capture_data.dict(by_alias=True))
    
    print(f"\n=== Quest Optimization Report ===")
    stats = report.get('statistics', {})
    print(f"Draw calls: {stats.get('draw_calls', 0)}")
    print(f"Textures: {stats.get('total_textures', 0)}")
    print(f"Estimated VRAM: {stats.get('estimated_vram_mb', 0)} MB")
    
    recommendations = report.get('recommendations', [])
    if recommendations:
        print(f"\nRecommendations:")
        for rec in recommendations:
            print(f"  [{rec['priority']}] {rec['issue']}")
            print(f"     → {rec['suggestion']}")
    
    print(f"\n✓ Full report saved to: {report_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python quest_analysis.py <quest_capture.rdc>")
        print("\nThis script analyzes Quest-specific capture data:")
        print("  - Performance counters (Meta fork)")
        print("  - Multiview rendering detection")
        print("  - Fixed foveated rendering check")
        print("  - Optimization recommendations")
        sys.exit(1)
    
    rdc_path = sys.argv[1]
    
    try:
        analyze_quest_performance(rdc_path)
        analyze_multiview_rendering(rdc_path)
        analyze_foveation(rdc_path)
        quest_optimization_report(rdc_path, 'quest_report.json')
        
        print("\n✓ Quest analysis complete!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
