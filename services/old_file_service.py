"""
Find old files in a folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from core.base_service import BaseService


@dataclass(slots=True)
class OldFile:
    """
    Information about an old file.
    """

    path: Path
    name: str
    size: int
    modified_time: datetime


class OldFileService(BaseService):
    """
    Find the oldest files in a folder.
    """

    def execute(
        self,
        folder: Path,
        limit: int = 20,
    ) -> list[OldFile]:
        """
        Find the oldest files.

        Args:
            folder:
                Target folder.

            limit:
                Maximum number of files to return.

        Returns:
            List of old files sorted by modified time.
        """
        if not folder.exists():
            self.logger.error("Folder does not exist: %s", folder)
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            self.logger.error("Path is not a directory: %s", folder)
            raise NotADirectoryError(folder)

        self.logger.info(
            "Finding top %d oldest files in %s",
            limit,
            folder,
        )

        files: list[OldFile] = []

        for path in folder.rglob("*"):
            try:
                if not path.is_file():
                    continue

                stat = path.stat()

                files.append(
                    OldFile(
                        path=path,
                        name=path.name,
                        size=stat.st_size,
                        modified_time=datetime.fromtimestamp(
                            stat.st_mtime
                        ),
                    )
                )

            except OSError:
                self.logger.exception(
                    "Failed to read file: %s",
                    path,
                )

        files.sort(
            key=lambda file: file.modified_time
        )

        result = files[:limit]

        self.logger.info(
            "Found %d old files.",
            len(result),
        )

        return result