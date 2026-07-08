"""
Worker thread for finding large files.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.large_file_finder import LargeFile, LargeFileFinder

logger = logging.getLogger(__name__)


class LargeFileWorker(QObject):
    """
    Worker object for finding large files in a background thread.
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
        Execute large file search.
        """
        try:
            logger.info("LargeFileWorker started.")

            finder = LargeFileFinder()

            result = finder.find(
                self._folder,
                self._limit,
            )

            self.finished.emit(result)

            logger.info(
                "LargeFileWorker finished. %d files found.",
                len(result),
            )

        except Exception as exception:
            logger.exception("LargeFileWorker failed.")
            self.error.emit(str(exception))


def create_large_file_thread(
    folder: Path,
    limit: int = 20,
) -> tuple[QThread, LargeFileWorker]:
    """
    Create a worker thread for large file search.

    Args:
        folder:
            Folder to analyze.

        limit:
            Maximum number of files.

    Returns:
        Configured thread and worker.
    """
    thread = QThread()

    worker = LargeFileWorker(
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