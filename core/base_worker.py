"""
Base worker for all background tasks.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal, Slot

logger = logging.getLogger(__name__)


class BaseWorker(QObject):
    """
    Base class for all background workers.
    """

    finished = Signal()
    error = Signal(str)

    def __init__(self) -> None:
        super().__init__()

    @Slot()
    def run(self) -> None:
        """
        Execute the worker safely.
        """
        logger.info(
            "%s started.",
            self.__class__.__name__,
        )

        try:
            self.execute()

        except Exception as exception:
            logger.exception(
                "%s failed.",
                self.__class__.__name__,
            )

            self.error.emit(
                str(exception)
            )

            return

        logger.info(
            "%s finished.",
            self.__class__.__name__,
        )

        self.finished.emit()

    def execute(self) -> None:
        """
        Execute worker logic.
        """
        raise NotImplementedError