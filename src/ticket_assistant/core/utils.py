"""Utility functions and helpers."""

import logging
import sys
from pathlib import Path


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def ensure_path_in_sys_path(path: Path) -> None:
    """Ensure a path is in sys.path."""
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
