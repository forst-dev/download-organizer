"""
Worker thread for moving files.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, QThread, Signal, Slot

from models.move_plan import MovePlan
from models.move_result import MoveResult
from services.file_mover import FileMover

logger = logging.getLogger(__name__)


class FileMoverWorker(QObject):
    """
    Worker object for moving files in a background thread.
    """

    finished = Signal(object)
    progress = Signal(int, int)
    error = Signal(str)

    def __init__(
        self,
        plans: list[MovePlan],
    ) -> None:
        super().__init__()

        self._plans = plans

    @Slot()
    def run(self) -> None:
        """
        Execute file move operation.
        """
        try:
            logger.info(
                "FileMoverWorker started."
            )

            mover = FileMover()

            results: list[MoveResult] = []

            total = len(self._plans)

            for index, plan in enumerate(
                self._plans,
                start=1,
            ):
                result = mover.move([plan])[0]

                results.append(result)

                self.progress.emit(
                    index,
                    total,
                )

            self.finished.emit(results)

            logger.info(
                "FileMoverWorker finished."
            )

        except Exception as exception:
            logger.exception(
                "FileMoverWorker failed."
            )

            self.error.emit(
                str(exception)
            )


def create_file_mover_thread(
    plans: list[MovePlan],
) -> tuple[QThread, FileMoverWorker]:
    """
    Create and configure a file mover thread.

    Args:
        plans:
            Move plans.

    Returns:
        Thread and worker.
    """
    thread = QThread()

    worker = FileMoverWorker(
        plans
    )

    worker.moveToThread(thread)

    thread.started.connect(
        worker.run
    )

    worker.finished.connect(
        thread.quit
    )

    worker.finished.connect(
        worker.deleteLater
    )

    worker.error.connect(
        thread.quit
    )

    worker.error.connect(
        worker.deleteLater
    )

    thread.finished.connect(
        thread.deleteLater
    )

    return thread, worker