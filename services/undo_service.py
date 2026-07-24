"""
Undo previously moved files.
"""

from __future__ import annotations

import shutil

from core.base_service import BaseService
from models.move_history import MoveHistory
from models.move_result import MoveResult
from services.history_service import HistoryService


class UndoService(BaseService):
    """
    Restore moved files to their original locations.
    """

    def __init__(
        self,
        history_service: HistoryService,
    ) -> None:
        super().__init__()

        self._history_service = history_service

    def execute(
        self,
    ) -> list[MoveResult]:
        """
        Restore all moved files.

        Returns:
            Undo results.
        """
        histories = self._history_service.get_all()

        results: list[MoveResult] = []

        if not histories:
            self.logger.info(
                "No history to undo."
            )
            return results

        self.logger.info(
            "Undo started. %d files.",
            len(histories),
        )

        for history in reversed(histories):

            results.append(
                self._undo_one(history)
            )

        if all(
            result.success
            for result in results
        ):
            self._history_service.clear()

        self.logger.info(
            "Undo completed."
        )

        return results

    def _undo_one(
        self,
        history: MoveHistory,
    ) -> MoveResult:
        """
        Restore one file.
        """
        try:
            history.source.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(history.destination),
                str(history.source),
            )

            self.logger.info(
                "Restored: %s",
                history.source.name,
            )

            return MoveResult(
                source=history.destination,
                destination=history.source,
                success=True,
                message="Undo completed.",
            )

        except Exception as exception:

            self.logger.exception(
                "Undo failed: %s",
                history.destination,
            )

            return MoveResult(
                source=history.destination,
                destination=history.source,
                success=False,
                message=str(exception),
            )