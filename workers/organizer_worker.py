"""
Worker thread for creating organization plans.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from models.move_plan import MovePlan
from services.organizer import Organizer
from models.category_option import CategoryOption

logger = logging.getLogger(__name__)


class OrganizerWorker(QObject):
    """
    Worker object for creating organization plans
    in a background thread.
    """

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, folder: Path) -> None:
        """
        Initialize worker.

        Args:
            folder:
                Folder to organize.
        """
        super().__init__()

        self._folder = folder

    @Slot()
    def run(self) -> None:
        """
        Create organization plans.
        """
        try:
            logger.info("OrganizerWorker started.")

            organizer = Organizer()

            plans = organizer.create_plan(
                self._folder
            )

            categories = organizer.create_categories(
                plans
            )

            self.finished.emit(
                {
                    "plans": plans,
                    "categories": categories,
                }
            )

            logger.info(
                "OrganizerWorker finished. %d plans, %d categories.",
                len(plans),
                len(categories),
            )

        except Exception as exception:
            logger.exception(
                "OrganizerWorker failed."
            )
            self.error.emit(str(exception))


def create_organizer_thread(
    folder: Path,
) -> tuple[QThread, OrganizerWorker]:
    """
    Create and configure an organizer worker thread.

    Args:
        folder:
            Folder to organize.

    Returns:
        Configured thread and worker.
    """
    thread = QThread()

    worker = OrganizerWorker(folder)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)

    thread.finished.connect(thread.deleteLater)

    return thread, worker