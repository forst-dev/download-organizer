"""
Manage worker threads.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject

from workers.analyzer_worker import create_analyzer_thread
from workers.duplicate_worker import create_duplicate_thread
from workers.large_file_worker import create_large_file_thread
from workers.old_file_worker import create_old_file_thread

logger = logging.getLogger(__name__)


class WorkerManager(QObject):
    """
    Manage background worker threads.
    """

    def __init__(
        self,
        handler,
    ) -> None:
        super().__init__()

        self._handler = handler

        self._thread = None
        self._worker = None

    def start_analysis(
        self,
        folder: Path,
    ) -> None:
        """Start folder analysis."""

        logger.info("Starting analyzer worker.")

        self._thread, self._worker = create_analyzer_thread(folder)

        self._worker.finished.connect(
            self._handler.on_analysis_finished
        )

        self._worker.error.connect(
            self._handler.on_error
        )

        self._thread.start()

    def start_large_file_search(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:
        """Start large file search."""

        logger.info("Starting large file worker.")

        self._thread, self._worker = create_large_file_thread(
            folder,
            limit,
        )

        self._worker.finished.connect(
            self._handler.on_large_file_finished
        )

        self._worker.error.connect(
            self._handler.on_error
        )

        self._thread.start()

    def start_old_file_search(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:
        """Start old file search."""

        logger.info("Starting old file worker.")

        self._thread, self._worker = create_old_file_thread(
            folder,
            limit,
        )

        self._worker.finished.connect(
            self._handler.on_old_file_finished
        )

        self._worker.error.connect(
            self._handler.on_error
        )

        self._thread.start()

    def start_duplicate_search(
        self,
        folder: Path,
    ) -> None:
        """Start duplicate file search."""

        logger.info("Starting duplicate worker.")

        self._thread, self._worker = create_duplicate_thread(
            folder,
        )

        self._worker.finished.connect(
            self._handler.on_duplicate_finished
        )

        self._worker.error.connect(
            self._handler.on_error
        )

        self._thread.start()