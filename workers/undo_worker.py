"""
Worker for undoing file move operations.
"""

from __future__ import annotations

from PySide6.QtCore import Signal

from core.base_worker import BaseWorker
from models.move_result import MoveResult
from services.history_service import HistoryService
from services.undo_service import UndoService


class UndoWorker(BaseWorker):
    """
    Worker for restoring moved files.
    """

    result = Signal(object)

    def __init__(
        self,
        history_service: HistoryService,
    ) -> None:
        super().__init__()

        self._service = UndoService(
            history_service,
        )

    def execute(self) -> None:
        """
        Restore previously moved files.
        """
        results: list[MoveResult] = (
            self._service.undo()
        )

        self.result.emit(results)