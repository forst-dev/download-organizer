"""
Manage background workers.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QThread, QObject, Signal

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
            logger.info("Cleanup start")

            # 1. 스레드가 이벤트 루프를 안전하게 종료하도록 요청
            if thread.isRunning():
                thread.quit()
                # 스레드가 완전히 종료될 때까지 최대 1000ms(1초) 대기
                if not thread.wait(1000):
                    logger.warning("Thread did not terminate gracefully, forcing exit.")

            # 2. worker 및 thread 리스트 안전 제거
            if worker in self._workers:
                self._workers.remove(worker)

            if thread in self._threads:
                self._threads.remove(thread)

            # 3. Qt C++ 메모리 지연 삭제 예약 (GC가 즉시 파괴하지 못하도록 안전 처리)
            worker.deleteLater()
            thread.deleteLater()

            logger.info("Cleanup end")
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
            lambda: self._cleanup(
                thread,
                worker,
            )
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
            FileMoverWorker(
                plans,
                self._history_service,
            ),
            self._handler.on_move_finished,
            self._handler.on_move_progress,
        )