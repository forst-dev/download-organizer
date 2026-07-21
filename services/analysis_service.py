"""
Analyze files and folders.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from core.base_service import BaseService


@dataclass(slots=True)
class AnalysisResult:
    """
    Result of folder analysis.
    """

    file_count: int
    folder_count: int
    total_size: int


class AnalysisService(BaseService):
    """
    Analyze a folder and collect basic statistics.
    """

    def execute(self, folder: Path) -> AnalysisResult:
        """
        Analyze the specified folder.

        Args:
            folder: Folder to analyze.

        Returns:
            AnalysisResult: Analysis result.

        Raises:
            FileNotFoundError: If folder does not exist.
            NotADirectoryError: If path is not a directory.
        """
        if not folder.exists():
            self.logger.error("Folder does not exist: %s", folder)
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            self.logger.error("Path is not a directory: %s", folder)
            raise NotADirectoryError(folder)

        file_count = 0
        folder_count = 0
        total_size = 0

        self.logger.info("Start analyzing: %s", folder)

        for path in folder.rglob("*"):
            try:
                if path.is_file():
                    file_count += 1
                    total_size += path.stat().st_size

                elif path.is_dir():
                    folder_count += 1

            except OSError:
                self.logger.exception("Failed to analyze: %s", path)

        self.logger.info(
            "Analysis complete. Files=%d, Folders=%d, Size=%d bytes",
            file_count,
            folder_count,
            total_size,
        )

        return AnalysisResult(
            file_count=file_count,
            folder_count=folder_count,
            total_size=total_size,
        )