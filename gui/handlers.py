"""
UI event handlers.
"""

from __future__ import annotations

import logging

from services.analysis_service import AnalysisResult
from services.duplicate_file_service import DuplicateFile
from services.large_file_service import LargeFile
from services.old_file_service import OldFile

from .table_manager import TableManager
from models.move_plan import MovePlan
from models.move_result import MoveResult

logger = logging.getLogger(__name__)


class UIHandler:
    """
    Handle worker results and update the UI.
    """

    def __init__(
        self,
        window,
        table_manager: TableManager,
    ) -> None:
        self._window = window
        self._table = table_manager
        self._window.category_panel.selection_changed.connect(
            self.on_category_changed
        )

    def on_analysis_finished(
        self,
        result: AnalysisResult,
    ) -> None:
        """Handle analysis completion."""

        self._window.show_loading(False)
        self._window.set_status("분석 완료")
        self._window.show_summary(result)

        self._table.show_analysis(
            result.file_count,
            result.folder_count,
            result.total_size,
        )

        logger.info("Analysis completed.")

    def on_large_file_finished(
        self,
        files: list[LargeFile],
    ) -> None:
        """Handle large file completion."""

        self._window.show_loading(False)
        self._window.set_status("큰 파일 검색 완료")

        self._table.show_large_files(files)

        logger.info(
            "Displayed %d large files.",
            len(files),
        )

    def on_old_file_finished(
        self,
        files: list[OldFile],
    ) -> None:
        """Handle old file completion."""

        self._window.show_loading(False)
        self._window.set_status("오래된 파일 검색 완료")

        self._table.show_old_files(files)

        logger.info(
            "Displayed %d old files.",
            len(files),
        )

    def on_duplicate_finished(
        self,
        groups: list[list[DuplicateFile]],
    ) -> None:
        """Handle duplicate file completion."""

        self._window.show_loading(False)
        self._window.set_status("중복 파일 검색 완료")

        self._table.show_duplicate_files(groups)

        logger.info(
            "Displayed %d duplicate groups.",
            len(groups),
        )

    def on_error(
        self,
        message: str,
    ) -> None:
        """Handle worker error."""
        self._window.show_loading(False)
        self._window.set_status("오류 발생")
        self._table.clear()
        self._window.show_error(message)

        logger.error(message)
    
    def on_organizer_finished(
        self,
        data,
    ) -> None:
        plans = data["plans"]
        categories = data["categories"]
        
        self._window._move_plans = plans

        self._window.show_loading(False)

        self._window.set_status(
            f"정리 미리보기 완료 ({len(plans)}개)"
        )

        self._window.category_panel.set_categories(categories)
        self._window.category_panel.show()
        self._window.start_move_button.show()

        self._table.show_move_plans(plans)

        logger.info(
            "Displayed %d move plans.",
            len(plans),
        )

    def on_category_changed(
        self,
        categories: list[str],
    ) -> None:
        """
        Filter preview by selected categories.
        """
        if not self._window._move_plans:
            return

        filtered = [
            plan
            for plan in self._window._move_plans
            if plan.category in categories
        ]

        self._table.show_move_plans(filtered)

        self._window.set_status(
            f"{len(filtered)}개 파일 선택됨"
        )

        logger.info(
            "Filtered %d files.",
            len(filtered),
        )

    def on_move_finished(
        self,
        results: list[MoveResult],
    ) -> None:
        """
        Handle file move completion.

        Args:
            results:
                File move results.
        """
        logger.info(">>> on_move_finished entered")
        self._window.show_loading(False)
        logger.info("show_loading")

        success_count = sum(
            result.success
            for result in results
        )

        failed_count = len(results) - success_count
        logger.info("failed_count")

        self._window.set_status(
            f"정리 완료 (성공 {success_count}, 실패 {failed_count})"
        )
        logger.info("move completion")

        self._table.show_move_results(results)
        logger.info("BEFORE BUTTON ENABLE")

        self._window.start_move_button.setEnabled(True)

        logger.info(
            "Move finished. Success=%d, Failed=%d",
            success_count,
            failed_count,
        )

    def on_move_progress(
        self,
        current: int,
        total: int,
    ) -> None:
        """
        Update move progress.
        """
        percent = int(
            current * 100 / total
        )

        self._window.progress_bar.setValue(
            percent
        )

        self._window.set_status(
            f"파일 이동 중... ({current}/{total})"
        )