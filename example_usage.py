#!/usr/bin/env python3
"""
Example: Advanced RDC data extraction
Shows how to use the new renderdoc_tools package
"""

from renderdoc_tools.parser import Parser
from renderdoc_tools.core import CaptureFile
from renderdoc_tools.extractors import ActionExtractor, ResourceExtractor
from renderdoc_tools.exporters import JSONExporter
from pathlib import Path
import json


def analyze_draw_calls(rdc_path: str):
    """Extract and analyze draw call patterns"""
    
    parser = Parser()
    capture_data = parser.parse(Path(rdc_path))
    
    # Filter only draw calls
    draw_calls = [a for a in capture_data.actions if 'Drawcall' in a.flags]
    
    print(f"\n=== Draw Call Analysis ===")
    print(f"Total actions: {len(capture_data.actions)}")
    print(f"Draw calls: {len(draw_calls)}")
    
    # Analyze by type
    if draw_calls:
        total_indices = sum(a.num_indices or 0 for a in draw_calls)
        total_instances = sum(a.num_instances or 0 for a in draw_calls)
        
        print(f"Total indices drawn: {total_indices:,}")
        print(f"Total instances: {total_instances:,}")
        
        # Find expensive draws
        expensive = sorted(draw_calls, 
                         key=lambda x: (x.num_indices or 0) * (x.num_instances or 1),
                         reverse=True)[:5]
        
        print(f"\nTop 5 most expensive draws:")
        for i, dc in enumerate(expensive, 1):
            cost = (dc.num_indices or 0) * (dc.num_instances or 1)
            print(f"  {i}. Event {dc.event_id}: {cost:,} vertices")


def analyze_textures(rdc_path: str):
    """Extract and analyze texture usage"""
    
    parser = Parser()
    capture_data = parser.parse(Path(rdc_path))
    
    textures = [r for r in capture_data.resources if r.resource_type == 'Texture' and r.texture]
    
    print(f"\n=== Texture Analysis ===")
    print(f"Total resources: {len(capture_data.resources)}")
    print(f"Textures: {len(textures)}")
    
    if textures:
        # Memory estimation (rough)
        total_mem = 0
        for tex_res in textures:
            tex = tex_res.texture
            # Rough estimate: width * height * depth * mips * 4 bytes
            mem = tex.width * tex.height * tex.depth * tex.mips * 4
            total_mem += mem
        
        print(f"Estimated VRAM usage: {total_mem / (1024*1024):.2f} MB")
        
        # Find largest textures
        largest = sorted(textures, 
                       key=lambda x: x.texture.width * x.texture.height if x.texture else 0,
                       reverse=True)[:5]
        
        print(f"\nTop 5 largest textures:")
        for i, tex_res in enumerate(largest, 1):
            if tex_res.texture:
                tex = tex_res.texture
                print(f"  {i}. {tex_res.name}: {tex.width}x{tex.height} {tex.format}")


def export_shader_summary(rdc_path: str, output: str):
    """Create a shader usage summary"""
    
    parser = Parser()
    capture_data = parser.parse(Path(rdc_path))
    
    summary = {
        'total_shaders': len(capture_data.shaders),
        'by_stage': {},
        'shaders': []
    }
    
    for shader in capture_data.shaders:
        stage = shader.stage
        summary['by_stage'][stage] = summary['by_stage'].get(stage, 0) + 1
        
        summary['shaders'].append({
            'name': shader.name,
            'stage': stage,
            'entry': shader.entry_point,
        })
    
    with open(output, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n=== Shader Summary ===")
    print(f"Total shaders: {summary['total_shaders']}")
    for stage, count in summary['by_stage'].items():
        print(f"  {stage}: {count}")
    print(f"\n✓ Saved to: {output}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <capture.rdc>")
        print("\nThis will:")
        print("  - Analyze draw calls and find expensive ones")
        print("  - Analyze textures and estimate VRAM usage")
        print("  - Export shader summary to shader_summary.json")
        sys.exit(1)
    
    rdc_path = sys.argv[1]
    
    try:
        analyze_draw_calls(rdc_path)
        analyze_textures(rdc_path)
        export_shader_summary(rdc_path, 'shader_summary.json')
        
        print("\n✓ Analysis complete!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
