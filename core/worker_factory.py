"""
Factory for creating worker threads.
"""

from __future__ import annotations

from typing import TypeVar

from PySide6.QtCore import QThread

from core.base_worker import BaseWorker

T = TypeVar(
    "T",
    bound=BaseWorker,
)


class WorkerFactory:
    """
    Create and configure worker threads.
    """

    @staticmethod
    def create(
        worker: T,
    ) -> tuple[QThread, T]:

        thread = QThread()

        worker.moveToThread(thread)

        thread.started.connect(
            worker.run,
        )

        worker.finished.connect(
            thread.quit,
        )

        worker.error.connect(
            thread.quit,
        )

        thread.finished.connect(
            thread.deleteLater,
        )

        return (
            thread,
            worker,
        )