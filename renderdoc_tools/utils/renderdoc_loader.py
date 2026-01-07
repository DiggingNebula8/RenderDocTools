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
        
        # For Windows Meta Fork, also need to update PATH for DLLs
        if sys.platform == "win32" and "RenderDocForMetaQuest" in str(pymodules_path):
            base_path = pymodules_path.parent
            path_parts = [str(base_path)]
            
            # Add subdirectories for DLLs
            try:
                for item in os.listdir(base_path):
                    subdir = base_path / item
                    if subdir.is_dir():
                        path_parts.append(str(subdir))
                        # Add nested subdirectories
                        try:
                            for nested_item in os.listdir(subdir):
                                nested_subdir = subdir / nested_item
                                if nested_subdir.is_dir():
                                    path_parts.append(str(nested_subdir))
                        except Exception:
                            pass
            except Exception:
                pass
            
            # Update PATH
            old_path = os.environ.get('PATH', '')
            new_path = os.pathsep.join(path_parts)
            if new_path not in old_path:
                path_list = old_path.split(os.pathsep)
                path_list = [p for p in path_list if str(base_path) not in p]
                os.environ['PATH'] = new_path + os.pathsep + os.pathsep.join(path_list)
            
            # Set Qt plugin paths
            qt_plugin_path = base_path / "qtplugins"
            if qt_plugin_path.exists():
                os.environ['QT_PLUGIN_PATH'] = str(qt_plugin_path)
                os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = str(qt_plugin_path)
            
            # Prevent Qt GUI initialization
            os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
            os.environ.setdefault('QT_LOGGING_RULES', '*.debug=false')
            
            # Add DLL directories for Python 3.8+
            if sys.version_info >= (3, 8):
                for path_part in path_parts:
                    try:
                        if os.path.exists(path_part):
                            os.add_dll_directory(path_part)
                    except Exception:
                        pass
        
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
    Automatically detects and tries both standard RenderDoc and Meta Fork
    
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
    
    # Try each installation (prefer Meta Fork if both available)
    # Sort so Meta Fork comes first
    installations_sorted = sorted(installations, key=lambda x: 0 if x['type'] == 'meta_fork' else 1)
    
    for inst in installations_sorted:
        pymodules_path = Path(inst['pymodules_path'])
        rd_module = _try_load_from_path(pymodules_path)
        if rd_module:
            _rd_module = rd_module
            logger.info(f"Successfully loaded {inst['name']} from {pymodules_path}")
            return rd_module
    
    # Fallback: try hardcoded Meta Fork location (for backward compatibility)
    meta_quest_base = Path(r"C:\Program Files\RenderDocForMetaQuest")
    meta_quest_pymodules = meta_quest_base / "pymodules"
    
    if meta_quest_pymodules.exists():
        logger.info(f"Trying fallback Meta Fork location: {meta_quest_pymodules}")
        rd_module = _try_load_from_path(meta_quest_pymodules)
        if rd_module:
            _rd_module = rd_module
            return rd_module
    
    # If still not found, raise error
    error_msg = (
        "RenderDoc module not found!\n"
        "Make sure you have RenderDoc installed.\n"
        "The package automatically detects:\n"
        "  - Standard RenderDoc: C:\\Program Files\\RenderDoc\n"
        "  - Meta Fork: C:\\Program Files\\RenderDocForMetaQuest\n"
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
