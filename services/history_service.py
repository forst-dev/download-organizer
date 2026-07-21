from models.move_history import MoveHistory
from core.base_service import BaseService


class HistoryService(BaseService):

    def __init__(self) -> None:
        super().__init__()

        self._histories: list[MoveHistory] = []

    def add(
        self,
        history: MoveHistory,
    ) -> None:
        self._histories.append(history)

    def get_all(self) -> list[MoveHistory]:
        return self._histories.copy()

    def pop_all(self) -> list[MoveHistory]:
        histories = self._histories.copy()
        self._histories.clear()

        return histories