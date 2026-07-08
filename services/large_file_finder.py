"""
Find large files in a folder.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LargeFile:
    """
    Information about a large file.
    """

    path: Path
    name: str
    size: int


class LargeFileFinder:
    """
    Find the largest files in a folder.
    """

    def find(
        self,
        folder: Path,
        limit: int = 20,
    ) -> list[LargeFile]:
        """
        Find the largest files.

        Args:
            folder:
                Target folder.

            limit:
                Number of files to return.

        Returns:
            List of LargeFile sorted by size.
        """
        if not folder.exists():
            logger.error("Folder does not exist: %s", folder)
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            logger.error("Path is not a directory: %s", folder)
            raise NotADirectoryError(folder)

        logger.info(
            "Finding top %d largest files in %s",
            limit,
            folder,
        )

        files: list[LargeFile] = []

        for path in folder.rglob("*"):
            try:
                if not path.is_file():
                    continue

                files.append(
                    LargeFile(
                        path=path,
                        name=path.name,
                        size=path.stat().st_size,
                    )
                )

            except OSError:
                logger.exception(
                    "Failed to read file: %s",
                    path,
                )

        files.sort(
            key=lambda file: file.size,
            reverse=True,
        )

        result = files[:limit]

        logger.info(
            "Found %d large files.",
            len(result),
        )

        return result