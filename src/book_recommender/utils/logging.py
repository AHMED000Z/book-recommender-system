"""Logging utilities for the Book Recommender System."""

import sys
from pathlib import Path
from loguru import logger

from ..core.config import config


def setup_logging() -> None:
    """Setup logging configuration."""
    # Remove default handler
    logger.remove()

    # Create logs directory if it doesn't exist
    log_file = Path(config.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Add console handler
    logger.add(
        sys.stderr,
        format=config.logging.format,
        level=config.logging.level,
        colorize=True,
    )

    # Add file handler
    logger.add(
        str(log_file),
        format=config.logging.format,
        level=config.logging.level,
        rotation="10 MB",
        retention="1 week",
    )
