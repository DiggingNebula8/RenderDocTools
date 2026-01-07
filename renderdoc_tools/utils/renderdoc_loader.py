"""Centralized RenderDoc module loading"""

import sys
import os
from pathlib import Path
from typing import Optional
import logging

from renderdoc_tools.core.exceptions import RenderDocNotFoundError

logger = logging.getLogger(__name__)

# Global variable to store the loaded module
_rd_module: Optional[object] = None


def load_renderdoc() -> object:
    """
    Load and return the RenderDoc module
    
    Returns:
        RenderDoc module object
        
    Raises:
        RenderDocNotFoundError: If RenderDoc module cannot be loaded
    """
    global _rd_module
    
    if _rd_module is not None:
        return _rd_module
    
    # First try standard import
    try:
        import renderdoc as rd
        _rd_module = rd
        logger.info("Loaded RenderDoc module from standard location")
        return rd
    except ImportError:
        pass
    
    # Try Meta Fork location
    meta_quest_base = Path(r"C:\Program Files\RenderDocForMetaQuest")
    meta_quest_pymodules = meta_quest_base / "pymodules"
    
    if meta_quest_pymodules.exists():
        logger.info(f"Trying Meta Fork location: {meta_quest_pymodules}")
        
        # Add pymodules to Python path FIRST
        sys.path.insert(0, str(meta_quest_pymodules))
        
        # Collect all directories that might contain DLLs
        path_parts = [str(meta_quest_base)]
        
        # Add all subdirectories (including nested ones for PySide2, etc.)
        try:
            for item in os.listdir(meta_quest_base):
                subdir = meta_quest_base / item
                if subdir.is_dir():
                    path_parts.append(str(subdir))
                    # Also add nested subdirectories (like PySide2/plugins)
                    try:
                        for nested_item in os.listdir(subdir):
                            nested_subdir = subdir / nested_item
                            if nested_subdir.is_dir():
                                path_parts.append(str(nested_subdir))
                    except Exception:
                        pass
        except Exception:
            pass
        
        # Update PATH - put RenderDoc paths FIRST (before venv paths)
        old_path = os.environ.get('PATH', '')
        new_path = os.pathsep.join(path_parts)
        # Insert at beginning, but after current directory if present
        if new_path not in old_path:
            # Split by path separator and rebuild with RenderDoc first
            path_list = old_path.split(os.pathsep)
            # Remove RenderDoc paths if already present to avoid duplicates
            path_list = [p for p in path_list if str(meta_quest_base) not in p]
            # Prepend RenderDoc paths
            os.environ['PATH'] = new_path + os.pathsep + os.pathsep.join(path_list)
        
        # Set Qt plugin path (Qt5 applications need this)
        qt_plugin_path = meta_quest_base / "qtplugins"
        if qt_plugin_path.exists():
            os.environ['QT_PLUGIN_PATH'] = str(qt_plugin_path)
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = str(qt_plugin_path)
        
        # Prevent Qt from trying to initialize GUI (headless mode)
        os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
        
        # Disable Qt logging to console
        os.environ.setdefault('QT_LOGGING_RULES', '*.debug=false')
        
        # For Python 3.8+, add DLL directories (must be done before import)
        if sys.version_info >= (3, 8):
            for path_part in path_parts:
                try:
                    if os.path.exists(path_part):
                        os.add_dll_directory(path_part)
                except Exception:
                    pass
        
        # Try importing with retry mechanism
        try:
            import renderdoc as rd
            _rd_module = rd
            logger.info("Loaded RenderDoc module from Meta Fork location")
            return rd
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Failed to import RenderDoc from Meta Fork: {e}")
    
    # If still not found, raise error
    error_msg = (
        "RenderDoc module not found!\n"
        "Make sure you have RenderDoc installed and the Python module in your path.\n"
        "For Meta Fork, ensure: C:\\Program Files\\RenderDocForMetaQuest\\pymodules\n"
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

