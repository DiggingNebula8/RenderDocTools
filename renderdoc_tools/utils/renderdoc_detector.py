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
        # Priority 1: Local submodule build (relative path - most portable)
        project_root = Path(__file__).parent.parent.parent  # From utils/ up to project root
        local_submodule_paths = [
            project_root / "renderdoc" / "x64" / "Development",
            project_root / "renderdoc" / "x64" / "Release",
            project_root / "renderdoc" / "build" / "x64" / "Development",
        ]
        
        for path in local_submodule_paths:
            if path.exists():
                pymodules = path / "pymodules"
                renderdoc_pyd = pymodules / "renderdoc.pyd" if pymodules.exists() else None
                
                if renderdoc_pyd and renderdoc_pyd.exists():
                    installations.append({
                        'type': 'local_submodule',
                        'path': str(path),
                        'pymodules_path': str(pymodules),
                        'name': f'RenderDoc (Local Build - {path.parent.name}/{path.name})'
                    })
                    logger.info(f"Found local submodule build at {path}")
                    # Return immediately - local build has highest priority
                    return installations
        
        # Priority 2: Custom development build (for backward compatibility)
        custom_dev_paths = [
            Path("C:/dev/renderdoc/x64/Development"),
        ]
        
        for path in custom_dev_paths:
            if path.exists():
                pymodules = path / "pymodules"
                renderdoc_pyd = pymodules / "renderdoc.pyd" if pymodules.exists() else None
                
                if renderdoc_pyd and renderdoc_pyd.exists():
                    installations.append({
                        'type': 'custom_dev',
                        'path': str(path),
                        'pymodules_path': str(pymodules),
                        'name': f'RenderDoc (Custom Build - {path.name})'
                    })
                    logger.info(f"Found custom development build at {path}")
        
        # Priority 3: Standard RenderDoc locations (system install)
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

