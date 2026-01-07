"""Setup script for renderdoc-tools"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from package
__version__ = "2.0.0"
try:
    import importlib.util
    init_file = Path(__file__).parent / "renderdoc_tools" / "__init__.py"
    if init_file.exists():
        spec = importlib.util.spec_from_file_location("renderdoc_tools", init_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            __version__ = getattr(module, "__version__", "2.0.0")
except Exception:
    pass

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    try:
        long_description = readme_file.read_text(encoding="utf-8")
    except Exception:
        pass

setup(
    name="renderdoc-tools",
    version=__version__,
    description="Open-source parser for extracting structured data from RenderDoc capture files (.rdc) to JSON and CSV formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Siva",
    license="MIT",
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "pydantic>=1.8.0,<3.0.0",
        "typing-extensions>=4.0.0; python_version<'3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=13.0.0",
            "tqdm>=4.65.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rdc-tools=renderdoc_tools.cli.entry_point:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
    ],
)
