"""
Move files according to move plans.
"""

from __future__ import annotations

import shutil

from models.move_plan import MovePlan
from models.move_result import MoveResult
from core.base_service import BaseService


class FileMoveService(BaseService):
    """
    Execute file move operations.
    """

    def execute(
        self,
        plans: list[MovePlan],
    ) -> list[MoveResult]:
        """
        Move files according to the given plans.

        Args:
            plans:
                List of move plans.

        Returns:
            List of move results.
        """
        results: list[MoveResult] = []

        self.logger.info(
            "Starting file move. (%d files)",
            len(plans),
        )

        for plan in plans:
            results.append(
                self._move_file(plan)
            )

        success_count = sum(
            result.success
            for result in results
        )

        self.logger.info(
            "File move completed. %d/%d succeeded.",
            success_count,
            len(results),
        )

        return results

    def _move_file(
        self,
        plan: MovePlan,
    ) -> MoveResult:
        """
        Move a single file.

        Args:
            plan:
                File move plan.

        Returns:
            Move result.
        """
        try:
            destination_folder = plan.destination.parent

            destination_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(plan.source),
                str(plan.destination),
            )

            self.logger.info(
                "Moved: %s -> %s",
                plan.source.name,
                plan.destination,
            )

            return MoveResult(
                source=plan.source,
                destination=plan.destination,
                success=True,
                message="Moved successfully.",
            )

        except Exception as exception:
            self.logger.exception(
                "Failed to move: %s",
                plan.source,
            )

            return MoveResult(
                source=plan.source,
                destination=plan.destination,
                success=False,
                message=str(exception),
            )