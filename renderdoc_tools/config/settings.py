"""Application settings"""

from pydantic import BaseSettings, Field
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # RenderDoc paths
    renderdoc_path: Optional[Path] = Field(
        None,
        env="RENDERDOC_PATH",
        description="Path to RenderDoc installation"
    )
    
    # Output settings
    output_dir: Path = Field(
        Path("./rdc_output"),
        env="RDC_OUTPUT_DIR",
        description="Default output directory"
    )
    
    # Logging settings
    log_level: str = Field(
        "INFO",
        env="LOG_LEVEL",
        description="Logging level"
    )
    
    log_format: str = Field(
        "text",
        env="LOG_FORMAT",
        description="Log format (text or json)"
    )
    
    # Performance settings
    max_memory_mb: int = Field(
        4096,
        env="MAX_MEMORY_MB",
        description="Maximum memory usage in MB"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

