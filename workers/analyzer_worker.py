"""
Worker for folder analysis.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from core.base_worker import BaseWorker
from services.analysis_service import AnalysisResult, AnalysisService


class AnalyzerWorker(BaseWorker):
    """
    Worker for analyzing folders.
    """

    result = Signal(object)

    def __init__(
        self,
        folder: Path,
    ) -> None:
        super().__init__()

        self._folder = folder
        self._service = AnalysisService()

    def execute(self) -> None:
        """
        Execute folder analysis.
        """
        result: AnalysisResult = self._service.execute(self._folder)

        self.result.emit(result)