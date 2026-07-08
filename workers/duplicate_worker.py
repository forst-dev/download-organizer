"""
Worker thread for finding duplicate files.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.duplicate_finder import DuplicateFinder

logger = logging.getLogger(__name__)


class DuplicateWorker(QObject):
    """
    Worker object for finding duplicate files
    in a background thread.
    """

    finished = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        folder: Path,
    ) -> None:
        """
        Initialize worker.

        Args:
            folder:
                Folder to analyze.
        """
        super().__init__()

        self._folder = folder

    @Slot()
    def run(self) -> None:
        """
        Execute duplicate file search.
        """
        try:
            logger.info("DuplicateWorker started.")

            finder = DuplicateFinder()

            result = finder.find(self._folder)

            self.finished.emit(result)

            logger.info(
                "DuplicateWorker finished. %d groups found.",
                len(result),
            )

        except Exception as exception:
            logger.exception("DuplicateWorker failed.")
            self.error.emit(str(exception))


def create_duplicate_thread(
    folder: Path,
) -> tuple[QThread, DuplicateWorker]:
    """
    Create a worker thread for duplicate file search.

    Args:
        folder:
            Folder to analyze.

    Returns:
        Configured thread and worker.
    """
    thread = QThread()

    worker = DuplicateWorker(folder)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)

    thread.finished.connect(thread.deleteLater)

    return thread, worker