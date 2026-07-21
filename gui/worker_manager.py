"""
Manage background workers.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QThread

from core.base_worker import BaseWorker
from core.worker_factory import WorkerFactory

from models.move_plan import MovePlan

from workers.analyzer_worker import AnalyzerWorker
from workers.large_file_worker import LargeFileWorker
from workers.old_file_worker import OldFileWorker
from workers.duplicate_worker import DuplicateWorker
from workers.organizer_worker import OrganizerWorker
from workers.file_mover_worker import FileMoverWorker
from services.history_service import HistoryService

logger = logging.getLogger(__name__)


class WorkerManager(QObject):

    def __init__(self, handler) -> None:
        super().__init__()

        self._handler = handler
        self._history_service = HistoryService()

        self._threads: list[QThread] = []
        self._workers: list[BaseWorker] = []

    def _cleanup(
        self,
        thread: QThread,
        worker: BaseWorker,
    ) -> None:

        if thread in self._threads:
            self._threads.remove(thread)

        if worker in self._workers:
            self._workers.remove(worker)

        logger.info(
            "Thread removed. Active=%d",
            len(self._threads),
        )

    def _start_worker(
        self,
        worker: BaseWorker,
        result_handler: Callable,
        progress_handler: Callable | None = None,
    ) -> None:

        thread, worker = WorkerFactory.create(worker)

        worker.result.connect(result_handler)
        worker.error.connect(self._handler.on_error)

        if (
            progress_handler is not None
            and hasattr(worker, "progress")
        ):
            worker.progress.connect(progress_handler)

        thread.finished.connect(
            lambda t=thread, w=worker: self._cleanup(t, w)
        )

        self._threads.append(thread)
        self._workers.append(worker)

        logger.info(
            "Starting %s",
            worker.__class__.__name__,
        )

        thread.start()

    def start_analysis(
        self,
        folder: Path,
    ) -> None:

        self._start_worker(
            AnalyzerWorker(folder),
            self._handler.on_analysis_finished,
        )

    def start_large_file_search(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:

        self._start_worker(
            LargeFileWorker(folder, limit),
            self._handler.on_large_file_finished,
        )

    def start_old_file_search(
        self,
        folder: Path,
        limit: int = 20,
    ) -> None:

        self._start_worker(
            OldFileWorker(folder, limit),
            self._handler.on_old_file_finished,
        )

    def start_duplicate_search(
        self,
        folder: Path,
    ) -> None:

        self._start_worker(
            DuplicateWorker(folder),
            self._handler.on_duplicate_finished,
        )

    def start_organizer(
        self,
        folder: Path,
    ) -> None:

        self._start_worker(
            OrganizerWorker(folder),
            self._handler.on_organizer_finished,
        )

    def start_move(
        self,
        plans: list[MovePlan],
    ) -> None:

        self._start_worker(
            FileMoverWorker(plans, self._history_service),
            self._handler.on_move_finished,
            self._handler.on_move_progress,
        )