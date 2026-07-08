"""
Utilities for working with file system paths.
"""

from __future__ import annotations

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def get_downloads_folder() -> Path:
    """
    Return the user's Downloads folder.

    Returns:
        Path: Path to the Downloads folder.

    Raises:
        FileNotFoundError:
            If the Downloads folder cannot be found.
    """
    downloads = Path.home() / "Downloads"

    if not downloads.exists():
        logger.error("Downloads folder not found: %s", downloads)
        raise FileNotFoundError(
            f"Downloads folder not found: {downloads}"
        )

    logger.info("Downloads folder: %s", downloads)

    return downloads