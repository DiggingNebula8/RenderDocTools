"""Workflow preset definitions"""

from renderdoc_tools.workflows.base import Workflow
from renderdoc_tools.core import CaptureInfoExtractor
from renderdoc_tools.extractors import (
    ActionExtractor,
    ResourceExtractor,
    ShaderExtractor,
    PipelineExtractor,
    CounterExtractor
)
from renderdoc_tools.exporters import JSONExporter, CSVExporter
from renderdoc_tools.analyzers.quest.report import QuestReportGenerator


def get_preset(name: str) -> Workflow:
    """
    Get workflow preset by name
    
    Args:
        name: Preset name
        
    Returns:
        Workflow instance
        
    Raises:
        ValueError: If preset not found
    """
    presets = {
        'quick': _create_quick_preset(),
        'full': _create_full_preset(),
        'quest': _create_quest_preset(),
        'csv-only': _create_csv_only_preset(),
        'performance': _create_performance_preset(),
    }
    
    if name not in presets:
        available = ', '.join(presets.keys())
        raise ValueError(f"Unknown preset: {name}. Available: {available}")
    
    return presets[name]


def list_presets() -> dict:
    """
    List all available presets
    
    Returns:
        Dictionary mapping preset names to descriptions
    """
    return {
        'quick': 'Quick export - JSON only, no pipeline state',
        'full': 'Full analysis - JSON with pipeline state and counters',
        'quest': 'Quest analysis - Full Quest-specific profiling',
        'csv-only': 'CSV export only - Actions and resources to CSV',
        'performance': 'Performance analysis - Counters and optimization report',
    }


def _create_quick_preset() -> Workflow:
    """Create quick workflow preset"""
    return Workflow(
        name='quick',
        description='Quick export - JSON only, no pipeline state',
        extractors=[
            ActionExtractor(),
            ResourceExtractor(),
        ],
        exporters=[
            JSONExporter(),
        ],
        analyzers=[],
        capture_info_extractor=CaptureInfoExtractor()
    )


def _create_full_preset() -> Workflow:
    """Create full workflow preset"""
    return Workflow(
        name='full',
        description='Full analysis - JSON with pipeline state and counters',
        extractors=[
            ActionExtractor(),
            ResourceExtractor(),
            ShaderExtractor(),
        ],
        exporters=[
            JSONExporter(),
            CSVExporter(),
        ],
        analyzers=[],
        capture_info_extractor=CaptureInfoExtractor()
    )


def _create_quest_preset() -> Workflow:
    """Create Quest workflow preset"""
    return Workflow(
        name='quest',
        description='Quest analysis - Full Quest-specific profiling',
        extractors=[
            ActionExtractor(),
            ResourceExtractor(),
            ShaderExtractor(),
            CounterExtractor(),
        ],
        exporters=[
            JSONExporter(),
            CSVExporter(),
        ],
        analyzers=[
            QuestReportGenerator(),
        ],
        capture_info_extractor=CaptureInfoExtractor()
    )


def _create_csv_only_preset() -> Workflow:
    """Create CSV-only workflow preset"""
    return Workflow(
        name='csv-only',
        description='CSV export only - Actions and resources to CSV',
        extractors=[
            ActionExtractor(),
            ResourceExtractor(),
        ],
        exporters=[
            CSVExporter(),
        ],
        analyzers=[],
        capture_info_extractor=CaptureInfoExtractor()
    )


def _create_performance_preset() -> Workflow:
    """Create performance workflow preset"""
    return Workflow(
        name='performance',
        description='Performance analysis - Counters and optimization report',
        extractors=[
            ActionExtractor(),
            ResourceExtractor(),
            CounterExtractor(),
        ],
        exporters=[
            JSONExporter(),
        ],
        analyzers=[
            QuestReportGenerator(),
        ],
        capture_info_extractor=CaptureInfoExtractor()
    )

