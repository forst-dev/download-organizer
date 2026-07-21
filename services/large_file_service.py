"""
Find large files in a folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from core.base_service import BaseService


@dataclass(slots=True)
class LargeFile:
    """
    Information about a large file.
    """

    path: Path
    name: str
    size: int


class LargeFileService(BaseService):
    """
    Find the largest files in a folder.
    """

    def execute(
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
            self.logger.error("Folder does not exist: %s", folder)
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            self.logger.error("Path is not a directory: %s", folder)
            raise NotADirectoryError(folder)

        self.logger.info(
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
                self.logger.exception(
                    "Failed to read file: %s",
                    path,
                )

        files.sort(
            key=lambda file: file.size,
            reverse=True,
        )

        result = files[:limit]

        self.logger.info(
            "Found %d large files.",
            len(result),
        )

        return result