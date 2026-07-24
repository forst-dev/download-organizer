"""
Worker thread for moving files.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Signal
from models.move_plan import MovePlan
from models.move_result import MoveResult
from services.file_move_service import FileMoveService
from core.base_worker import BaseWorker
from services.history_service import HistoryService


logger = logging.getLogger(__name__)

class FileMoverWorker(BaseWorker):

    result = Signal(object)
    progress = Signal(int, int)

    def __init__(
        self,
        plans: list[MovePlan],
        history_service: HistoryService,
    ) -> None:
        super().__init__()

        self._plans = plans

        self._service = FileMoveService(
            history_service
        )

    def execute(self) -> None:
        """
        Move files.
        """

        results = self._service.execute(
            self._plans
        )

        total = len(results)

        for current in range(total):

            self.progress.emit(
                current + 1,
                total,
            )

        logger.info(
            "FileMoverWorker emitting result. count=%d",
            total,
        )

        self.result.emit(results)

        logger.info(
            "FileMoverWorker result emitted."
        )