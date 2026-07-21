"""
Worker for finding large files.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from core.base_worker import BaseWorker
from services.large_file_service import (
    LargeFile,
    LargeFileService,
)


class LargeFileWorker(BaseWorker):
    """
    Worker for finding large files.
    """

    result = Signal(object)

    def __init__(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:
        super().__init__()

        self._folder = folder
        self._limit = limit
        self._service = LargeFileService()

    def execute(self) -> None:
        """
        Find large files.
        """
        files: list[LargeFile] = (
            self._service.execute(
                self._folder,
                self._limit,
            )
        )

        self.result.emit(files)