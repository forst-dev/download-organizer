"""
Find duplicate files in a folder.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from core.base_service import BaseService

BUFFER_SIZE = 1024 * 1024  # 1 MB


@dataclass(slots=True)
class DuplicateFile:
    """
    Information about a duplicate file.
    """

    path: Path
    name: str
    size: int
    hash: str


class DuplicateFileService(BaseService):
    """
    Find duplicate files using file size and SHA-256 hash.
    """

    def execute(
        self,
        folder: Path,
    ) -> list[list[DuplicateFile]]:
        """
        Find duplicate files.

        Args:
            folder:
                Folder to analyze.

        Returns:
            Duplicate groups.
        """
        if not folder.exists():
            self.logger.error("Folder does not exist: %s", folder)
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            self.logger.error("Path is not a directory: %s", folder)
            raise NotADirectoryError(folder)

        self.logger.info("Searching duplicate files: %s", folder)

        size_groups: dict[int, list[Path]] = {}

        for path in folder.rglob("*"):
            try:
                if not path.is_file():
                    continue

                size = path.stat().st_size

                size_groups.setdefault(size, []).append(path)

            except OSError:
                self.logger.exception("Failed to read file: %s", path)

        duplicate_groups: list[list[DuplicateFile]] = []

        for size, paths in size_groups.items():
            if len(paths) < 2:
                continue

            hash_groups: dict[str, list[DuplicateFile]] = {}

            for path in paths:
                try:
                    file_hash = self._calculate_hash(path)

                    duplicate = DuplicateFile(
                        path=path,
                        name=path.name,
                        size=size,
                        hash=file_hash,
                    )

                    hash_groups.setdefault(
                        file_hash,
                        [],
                    ).append(duplicate)

                except OSError:
                    self.logger.exception(
                        "Failed to hash file: %s",
                        path,
                    )

            for duplicates in hash_groups.values():
                if len(duplicates) >= 2:
                    duplicate_groups.append(duplicates)

        self.logger.info(
            "Duplicate groups found: %d",
            len(duplicate_groups),
        )

        return duplicate_groups

    def _calculate_hash(
        self,
        path: Path,
    ) -> str:
        """
        Calculate SHA-256 hash.

        Args:
            path:
                File path.

        Returns:
            SHA-256 hash.
        """
        sha256 = hashlib.sha256()

        with path.open("rb") as file:
            while chunk := file.read(BUFFER_SIZE):
                sha256.update(chunk)

        return sha256.hexdigest()