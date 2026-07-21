"""
Worker thread for finding old files.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.old_file_service import OldFileService


class OldFileWorker(BaseWorker):

    result = Signal(object)

    def __init__(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:
        super().__init__()

        self._folder = folder
        self._limit = limit
        self._service = OldFileService()

    def execute(self) -> None:

        files = self._service.execute(
            self._folder,
            self._limit,
        )

        self.result.emit(files)