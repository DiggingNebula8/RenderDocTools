"""Centralized RenderDoc module loading"""

import sys
import os
from pathlib import Path
from typing import Optional
import logging

from renderdoc_tools.core.exceptions import RenderDocNotFoundError
from renderdoc_tools.utils.renderdoc_detector import find_renderdoc_installations

logger = logging.getLogger(__name__)

# Global variable to store the loaded module
_rd_module: Optional[object] = None


def _try_load_from_path(pymodules_path: Path) -> Optional[object]:
    """Try to load RenderDoc from a specific path"""
    if not pymodules_path.exists():
        return None
    
    try:
        # Add to Python path
        if str(pymodules_path) not in sys.path:
            sys.path.insert(0, str(pymodules_path))
        
        
        # Try importing
        import renderdoc as rd
        logger.info(f"Loaded RenderDoc module from: {pymodules_path}")
        return rd
    except ImportError:
        return None
    except Exception as e:
        logger.debug(f"Failed to load from {pymodules_path}: {e}")
        return None


def load_renderdoc() -> object:
    """
    Load and return the RenderDoc module
    Automatically detects and tries standard RenderDoc installations
    
    Returns:
        RenderDoc module object
        
    Raises:
        RenderDocNotFoundError: If RenderDoc module cannot be loaded
    """
    global _rd_module
    
    if _rd_module is not None:
        return _rd_module
    
    # First try standard import (if already in path)
    try:
        import renderdoc as rd
        _rd_module = rd
        logger.info("Loaded RenderDoc module from standard location")
        return rd
    except ImportError:
        pass
    
    # Find all RenderDoc installations and try each one
    installations = find_renderdoc_installations()
    
    # Try each installation
    for inst in installations:
        pymodules_path = Path(inst['pymodules_path'])
        rd_module = _try_load_from_path(pymodules_path)
        if rd_module:
            _rd_module = rd_module
            logger.info(f"Successfully loaded {inst['name']} from {pymodules_path}")
            return rd_module
    
    
    # If still not found, raise error
    error_msg = (
        "RenderDoc module not found!\n"
        "Make sure you have RenderDoc installed.\n"
        "The package automatically detects:\n"
        "  - Standard RenderDoc: C:\\Program Files\\RenderDoc\n"
        "See: https://renderdoc.org/docs/python_api/index.html"
    )
    logger.error(error_msg)
    raise RenderDocNotFoundError(error_msg)


def get_renderdoc_module() -> object:
    """
    Get the RenderDoc module (loads if not already loaded)
    
    Returns:
        RenderDoc module object
        
    Raises:
        RenderDocNotFoundError: If RenderDoc module cannot be loaded
    """
    return load_renderdoc()
