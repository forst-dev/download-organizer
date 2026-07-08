"""
UI event handlers.
"""

from __future__ import annotations

import logging

from services.analyzer import AnalysisResult
from services.duplicate_finder import DuplicateFile
from services.large_file_finder import LargeFile
from services.old_file_finder import OldFile

from .table_manager import TableManager

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
        self._window.show_error(message)

        logger.error(message)