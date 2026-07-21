"""
Worker thread for creating organization plans.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot

from models.move_plan import MovePlan
from services.organization_service import OrganizationService
from models.category_option import CategoryOption
from core.base_worker import BaseWorker


class OrganizerWorker(BaseWorker):

    result = Signal(object)

    def __init__(
        self,
        folder: Path,
    ) -> None:
        super().__init__()

        self._folder = folder
        self._service = OrganizationService()

    def execute(self) -> None:

        plans, categories = (
            self._service.execute(
                self._folder,
            )
        )

        self.result.emit(
            {
                "plans": plans,
                "categories": categories,
            }
        )