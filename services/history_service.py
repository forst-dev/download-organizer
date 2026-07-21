"""
Manage file move history.
"""

from __future__ import annotations

from models.move_history import MoveHistory


class HistoryService:
    """
    Store completed file move histories.
    """

    def __init__(self) -> None:
        self._histories: list[MoveHistory] = []

    def add(
        self,
        history: MoveHistory,
    ) -> None:
        """
        Add move history.
        """
        self._histories.append(history)

    def get_all(
        self,
    ) -> list[MoveHistory]:
        """
        Return all histories.
        """
        return self._histories.copy()

    def clear(self) -> None:
        """
        Clear all histories.
        """
        self._histories.clear()