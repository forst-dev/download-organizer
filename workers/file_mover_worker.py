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
    ) -> None:
        super().__init__()

        self._plans = plans

        self._history_service = HistoryService()

        self._service = FileMoveService(
            self._history_service
        )

    def execute(self) -> None:

        results: list[MoveResult] = []

        total = len(self._plans)

        for current, plan in enumerate(
            self._plans,
            start=1,
        ):

            result = self._service.execute(
                [plan]
            )[0]

            results.append(result)

            logger.info(
                "FileMoverWorker emitting result. count=%d",
                len(results),
            )
            self.progress.emit(
                current,
                total,
            )

        self.result.emit(results)

        logger.info(
            "FileMoverWorker result emitted."
        )