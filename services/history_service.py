"""
Manage file move history.
"""

from __future__ import annotations

from core.base_service import BaseService
from models.move_history import MoveHistory


class HistoryService(BaseService):
    """
    Store completed file move histories.
    """

    def __init__(self) -> None:
        super().__init__()

        self._histories: list[MoveHistory] = []

    def add(
        self,
        history: MoveHistory,
    ) -> None:
        """
        Add one history.
        """
        self._histories.append(history)

        self.logger.info(
            "History added. Total=%d",
            len(self._histories),
        )

    def add_many(
        self,
        histories: list[MoveHistory],
    ) -> None:
        """
        Add multiple histories.
        """
        self._histories.extend(histories)

        self.logger.info(
            "%d histories added.",
            len(histories),
        )

    def get_all(
        self,
    ) -> list[MoveHistory]:
        """
        Return all histories.
        """
        return self._histories.copy()

    def has_history(
        self,
    ) -> bool:
        """
        Return whether history exists.
        """
        return bool(self._histories)

    def clear(self) -> None:
        """
        Clear histories.
        """
        self._histories.clear()

        self.logger.info(
            "History cleared."
        )