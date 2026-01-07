"""Quest performance analysis"""

from typing import Dict, Any
import logging

from renderdoc_tools.analyzers.base import BaseAnalyzer

logger = logging.getLogger(__name__)


class QuestPerformanceAnalyzer(BaseAnalyzer):
    """Analyzes Quest-specific performance data"""
    
    def analyze(self, capture_data: Dict[str, Any], controller=None) -> Dict[str, Any]:
        """
        Analyze Quest performance counters
        
        Args:
            capture_data: Capture data dictionary or CaptureData model
            controller: Optional RenderDoc controller
            
        Returns:
            Dictionary with performance analysis results
        """
        self.logger.info("Analyzing Quest performance...")
        
        result = {
            'performance_counters_available': False,
            'counter_count': 0,
            'counters_by_category': {},
            'summary': {}
        }
        
        # Extract performance counters from capture data
        perf_counters = capture_data.get('performance_counters') or capture_data.get('performanceCounters')
        
        if perf_counters and perf_counters.get('available'):
            result['performance_counters_available'] = True
            counters = perf_counters.get('counters', [])
            result['counter_count'] = len(counters)
            
            # Group by category
            by_category = {}
            for counter in counters:
                # Handle both dict and Pydantic model
                if hasattr(counter, 'category'):
                    cat = counter.category
                else:
                    cat = counter.get('category', 'Unknown')
                
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(counter)
            
            result['counters_by_category'] = {
                cat: len(ctrs) for cat, ctrs in by_category.items()
            }
            
            result['summary'] = {
                'total_counters': len(counters),
                'categories': list(by_category.keys())
            }
        else:
            result['summary'] = {
                'note': 'Performance counters not available. Requires RenderDoc Meta Fork with Quest capture.'
            }
            if perf_counters and 'error' in perf_counters:
                result['error'] = perf_counters['error']
        
        return result
    
    @property
    def name(self) -> str:
        return "quest_performance"

