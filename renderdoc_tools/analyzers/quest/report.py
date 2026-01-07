"""Quest optimization report generator"""

from typing import Dict, Any, List
from pathlib import Path
import json
import logging

from renderdoc_tools.analyzers.base import BaseAnalyzer
from renderdoc_tools.analyzers.quest.performance import QuestPerformanceAnalyzer
from renderdoc_tools.analyzers.quest.multiview import MultiviewAnalyzer
from renderdoc_tools.analyzers.quest.foveation import FoveationAnalyzer

logger = logging.getLogger(__name__)


class QuestReportGenerator(BaseAnalyzer):
    """Generates comprehensive Quest optimization reports"""
    
    def __init__(self):
        super().__init__()
        self.performance_analyzer = QuestPerformanceAnalyzer()
        self.multiview_analyzer = MultiviewAnalyzer()
        self.foveation_analyzer = FoveationAnalyzer()
    
    def analyze(self, capture_data: Dict[str, Any], controller=None) -> Dict[str, Any]:
        """
        Generate comprehensive Quest optimization report
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            controller: Optional RenderDoc controller
            
        Returns:
            Dictionary with optimization report
        """
        self.logger.info("Generating Quest optimization report...")
        
        # Run all Quest analyzers
        perf_analysis = self.performance_analyzer.analyze(capture_data, controller)
        multiview_analysis = self.multiview_analyzer.analyze(capture_data, controller)
        foveation_analysis = self.foveation_analyzer.analyze(capture_data, controller)
        
        # Extract statistics
        actions = capture_data.get('actions', [])
        resources = capture_data.get('resources', [])
        
        # Count draw calls
        draw_calls = []
        for action in actions:
            if hasattr(action, 'flags'):
                flags = action.flags
            else:
                flags = action.get('flags', '')
            
            if 'Drawcall' in str(flags):
                draw_calls.append(action)
        
        # Count textures and estimate VRAM
        textures = []
        total_mem = 0
        for res in resources:
            if hasattr(res, 'resource_type'):
                res_type = res.resource_type
                texture = res.texture
            else:
                res_type = res.get('type', '')
                texture = res.get('texture')
            
            if res_type == 'Texture' and texture:
                textures.append(res)
                
                # Estimate memory
                if hasattr(texture, 'width'):
                    w, h, d, mips = texture.width, texture.height, texture.depth, texture.mips
                else:
                    w = texture.get('width', 0)
                    h = texture.get('height', 0)
                    d = texture.get('depth', 1)
                    mips = texture.get('mips', 1)
                
                # Rough estimate: w * h * d * mips * 4 bytes
                mem = w * h * d * mips * 4
                total_mem += mem
        
        estimated_vram_mb = round(total_mem / (1024 * 1024), 2)
        
        # Generate recommendations
        recommendations = []
        
        if len(draw_calls) > 500:
            recommendations.append({
                'priority': 'HIGH',
                'issue': 'High draw call count',
                'detail': f'{len(draw_calls)} draw calls detected',
                'suggestion': 'Consider GPU instancing or mesh merging'
            })
        
        if estimated_vram_mb > 500:
            recommendations.append({
                'priority': 'MEDIUM',
                'issue': 'High VRAM usage',
                'detail': f'~{estimated_vram_mb} MB estimated',
                'suggestion': 'Check texture compression (use ASTC) and mipmap usage'
            })
        
        # Check for large textures
        large_textures = []
        for tex_res in textures:
            if hasattr(tex_res, 'texture'):
                tex = tex_res.texture
                w = tex.width
                h = tex.height
            else:
                tex = tex_res.get('texture', {})
                w = tex.get('width', 0)
                h = tex.get('height', 0)
            
            if w * h > 2048 * 2048:
                large_textures.append(tex_res)
        
        if large_textures:
            recommendations.append({
                'priority': 'MEDIUM',
                'issue': 'Large textures detected',
                'detail': f'{len(large_textures)} textures larger than 2048x2048',
                'suggestion': 'Reduce texture resolution for Quest hardware'
            })
        
        # Build report
        report = {
            'capture_info': capture_data.get('capture_info') or capture_data.get('captureInfo', {}),
            'statistics': {
                'total_actions': len(actions),
                'draw_calls': len(draw_calls),
                'total_textures': len(textures),
                'estimated_vram_mb': estimated_vram_mb
            },
            'analysis': {
                'performance': perf_analysis,
                'multiview': multiview_analysis,
                'foveation': foveation_analysis
            },
            'recommendations': recommendations
        }
        
        return report
    
    def generate_report_file(
        self,
        capture_data: Dict[str, Any],
        output_path: Path,
        controller=None
    ) -> Path:
        """
        Generate report and save to file
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            output_path: Output file path
            controller: Optional RenderDoc controller
            
        Returns:
            Path to generated report file
        """
        report = self.analyze(capture_data, controller)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Quest optimization report saved to: {output_path}")
        return output_path
    
    @property
    def name(self) -> str:
        return "quest_report"

