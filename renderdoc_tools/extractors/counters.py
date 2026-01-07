"""Performance counter extraction module"""

from typing import Dict, Any, List
import logging

from renderdoc_tools.extractors.base import BaseExtractor
from renderdoc_tools.core.models import PerformanceCounter
from renderdoc_tools.core.exceptions import CounterExtractionError

logger = logging.getLogger(__name__)


class CounterExtractor(BaseExtractor):
    """Extracts performance counters (Meta fork specific)"""
    
    def extract(self, controller) -> Dict[str, Any]:
        """
        Extract performance counters from the capture
        
        Args:
            controller: RenderDoc ReplayController instance
            
        Returns:
            Dictionary with counter information
            
        Raises:
            CounterExtractionError: If extraction fails
        """
        if not self.validate(controller):
            raise CounterExtractionError("Invalid controller provided")
        
        self.logger.info("Extracting performance counters...")
        counters_data = {
            'available': False,
            'counters': []
        }
        
        try:
            # Enumerate available counters
            if hasattr(controller, 'EnumerateCounters'):
                counters = controller.EnumerateCounters()
                if counters:
                    counters_data['available'] = True
                    for counter in counters:
                        try:
                            counter_model = PerformanceCounter(
                                counterId=counter.counter,
                                name=counter.name,
                                description=counter.description,
                                category=str(counter.category),
                                unit=str(counter.unit)
                            )
                            counters_data['counters'].append(counter_model)
                        except Exception as e:
                            self.logger.warning(f"Failed to create counter model: {e}")
                    
                    self.logger.info(f"Extracted {len(counters_data['counters'])} performance counters")
                else:
                    self.logger.info("No performance counters available")
            else:
                self.logger.debug("EnumerateCounters() not available in this RenderDoc version")
            
            return counters_data
            
        except Exception as e:
            self.logger.error(f"Failed to extract performance counters: {e}")
            counters_data['error'] = str(e)
            # Don't raise - counters are optional
            return counters_data
    
    @property
    def name(self) -> str:
        return "counters"

