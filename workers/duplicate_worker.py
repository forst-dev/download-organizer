"""
Worker thread for finding duplicate files.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.duplicate_file_service import DuplicateFileService
from core.base_worker import BaseWorker


class DuplicateWorker(BaseWorker):

    result = Signal(object)

    def __init__(
        self,
        folder: Path,
    ) -> None:
        super().__init__()

        self._folder = folder
        self._service = DuplicateFileService()

    def execute(self) -> None:

        groups = self._service.execute(
            self._folder,
        )

        self.result.emit(groups)