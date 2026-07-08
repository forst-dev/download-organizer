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
    """
    Create and configure an analyzer worker thread.

    Args:
        folder: Folder to analyze.

    Returns:
        tuple[QThread, AnalyzerWorker]
    """
    thread = QThread()
    worker = AnalyzerWorker(folder)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)

    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)

    thread.finished.connect(thread.deleteLater)

    return thread, worker