"""RenderDoc installation detector"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def find_renderdoc_installations() -> List[Dict[str, str]]:
    """
    Find all RenderDoc installations
    
    Returns:
        List of dicts with 'type', 'path', 'pymodules_path', 'name'
    """
    installations = []
    
    if sys.platform == "win32":
        # Standard RenderDoc locations
        standard_paths = [
            Path("C:/Program Files/RenderDoc"),
            Path("C:/Program Files (x86)/RenderDoc"),
            Path(os.environ.get("PROGRAMFILES", "")) / "RenderDoc",
            Path(os.environ.get("PROGRAMFILES(X86)", "")) / "RenderDoc",
        ]
        
        # Check standard RenderDoc
        for path in standard_paths:
            if path.exists():
                # Check for renderdoc.pyd or pymodules
                pymodules = path / "pymodules"
                renderdoc_pyd = path / "renderdoc.pyd"
                
                if pymodules.exists() or renderdoc_pyd.exists():
                    installations.append({
                        'type': 'standard',
                        'path': str(path),
                        'pymodules_path': str(pymodules) if pymodules.exists() else str(path),
                        'name': 'RenderDoc (Standard)'
                    })
                    break  # Only need one standard installation
    
    elif sys.platform == "linux":
        # Linux locations
        linux_paths = [
            Path("/usr/share/renderdoc"),
            Path("/usr/local/share/renderdoc"),
            Path.home() / ".local/share/renderdoc",
        ]
        
        for path in linux_paths:
            if path.exists():
                renderdoc_so = path / "renderdoc.so"
                if renderdoc_so.exists():
                    installations.append({
                        'type': 'standard',
                        'path': str(path),
                        'pymodules_path': str(path),
                        'name': 'RenderDoc (Standard)'
                    })
                    break
    
    return installations


def get_preferred_renderdoc() -> Optional[Dict[str, str]]:
    """
    Get the preferred RenderDoc installation
    
    Returns:
        Dict with installation info, or None if not found
    """
    installations = find_renderdoc_installations()
    
    if not installations:
        return None
    
    # Return first installation found
    return installations[0]


def configure_pythonpath_for_renderdoc(installation: Dict[str, str]) -> str:
    """
    Get PYTHONPATH configuration command for an installation
    
    Args:
        installation: Installation dict from find_renderdoc_installations()
        
    Returns:
        Command to set PYTHONPATH (platform-specific)
    """
    pymodules_path = installation['pymodules_path']
    
    if sys.platform == "win32":
        return f'set PYTHONPATH={pymodules_path}'
    else:
        return f'export PYTHONPATH={pymodules_path}'

