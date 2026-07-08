"""
Worker thread for folder analysis.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from services.analyzer import AnalysisResult, Analyzer


logger = logging.getLogger(__name__)


class AnalyzerWorker(QObject):
    """
    Worker object for analyzing a folder in a background thread.
    """

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, folder: Path) -> None:
        """
        Initialize the worker.

        Args:
            folder: Folder to analyze.
        """
        super().__init__()

        self._folder = folder

    @Slot()
    def run(self) -> None:
        """
        Execute folder analysis.
        """
        try:
            logger.info("AnalyzerWorker started.")

            analyzer = Analyzer()
            result = analyzer.analyze(self._folder)

            self.finished.emit(result)

            logger.info("AnalyzerWorker finished.")

        except Exception as exception:
            logger.exception("AnalyzerWorker failed.")
            self.error.emit(str(exception))


def create_analyzer_thread(folder: Path) -> tuple[QThread, AnalyzerWorker]:
    logger.info("1. Create QThread")
    thread = QThread()

    logger.info("2. Create Worker")
    worker = AnalyzerWorker(folder)

    logger.info("3. Move Worker")
    worker.moveToThread(thread)

    logger.info("4. Connect started")
    thread.started.connect(worker.run)

    logger.info("5. Connect finished")
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    logger.info("6. Connect error")
    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)

    logger.info("7. Connect thread finished")
    thread.finished.connect(thread.deleteLater)

    logger.info("8. Return")

    return thread, worker