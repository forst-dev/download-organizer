"""
Worker thread for finding old files.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.old_file_finder import OldFileFinder

logger = logging.getLogger(__name__)


class OldFileWorker(QObject):
    """
    Worker object for finding old files in a background thread.
    """

    finished = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:
        """
        Initialize worker.

        Args:
            folder:
                Folder to analyze.

            limit:
                Maximum number of files to return.
        """
        super().__init__()

        self._folder = folder
        self._limit = limit

    @Slot()
    def run(self) -> None:
        """
        Execute old file search.
        """
        try:
            logger.info("OldFileWorker started.")

            finder = OldFileFinder()

            result = finder.find(
                self._folder,
                self._limit,
            )

            self.finished.emit(result)

            logger.info(
                "OldFileWorker finished. %d files found.",
                len(result),
            )

        except Exception as exception:
            logger.exception("OldFileWorker failed.")
            self.error.emit(str(exception))


def create_old_file_thread(
    folder: Path,
    limit: int = 20,
) -> tuple[QThread, OldFileWorker]:
    """
    Create a worker thread for old file search.

    Args:
        folder:
            Folder to analyze.

        limit:
            Maximum number of files.

    Returns:
        Configured thread and worker.
    """
    thread = QThread()

    worker = OldFileWorker(
        folder=folder,
        limit=limit,
    )

    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)

    thread.finished.connect(thread.deleteLater)

    return thread, worker