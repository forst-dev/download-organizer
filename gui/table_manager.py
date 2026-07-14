"""
Manage QTableWidget contents.
"""

from __future__ import annotations

from typing import Sequence

from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from services.duplicate_finder import DuplicateFile
from services.large_file_finder import LargeFile
from services.old_file_finder import OldFile
from utils.format_utils import format_size
from models.move_plan import MovePlan
from models.move_result import MoveResult

class TableManager:
    """
    Helper class for displaying data in a QTableWidget.
    """

    def __init__(self, table: QTableWidget) -> None:
        """
        Initialize the table manager.

        Args:
            table:
                Target table widget.
        """
        self._table = table
        self._initialize()

    def _initialize(self) -> None:
        """
        Configure the table.
        """
        self._table.setColumnCount(0)
        self._table.setRowCount(0)

        self._table.verticalHeader().setVisible(False)

        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

    def clear(self) -> None:
        """
        Clear the table.
        """
        self._table.clear()
        self._table.setRowCount(0)
        self._table.setColumnCount(0)

    def show_analysis(
        self,
        file_count: int,
        folder_count: int,
        total_size: int,
    ) -> None:
        """
        Display analysis summary.
        """
        self.clear()

        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(
            [
                "항목",
                "값",
            ]
        )

        rows = [
            ("파일 수", f"{file_count:,}"),
            ("폴더 수", f"{folder_count:,}"),
            ("전체 용량", format_size(total_size)),
        ]

        self._table.setRowCount(len(rows))

        for row, (title, value) in enumerate(rows):
            self._table.setItem(
                row,
                0,
                QTableWidgetItem(title),
            )
            self._table.setItem(
                row,
                1,
                QTableWidgetItem(value),
            )

    def show_large_files(
        self,
        files: Sequence[LargeFile],
    ) -> None:
        """
        Display large files.
        """
        self.clear()

        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(
            [
                "파일명",
                "크기",
                "경로",
            ]
        )

        self._table.setRowCount(len(files))

        for row, file in enumerate(files):
            self._table.setItem(
                row,
                0,
                QTableWidgetItem(file.name),
            )
            self._table.setItem(
                row,
                1,
                QTableWidgetItem(format_size(file.size)),
            )
            self._table.setItem(
                row,
                2,
                QTableWidgetItem(str(file.path)),
            )

    def show_old_files(
        self,
        files: Sequence[OldFile],
    ) -> None:
        """
        Display old files.
        """
        self.clear()

        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            [
                "파일명",
                "수정일",
                "크기",
                "경로",
            ]
        )

        self._table.setRowCount(len(files))

        for row, file in enumerate(files):
            self._table.setItem(
                row,
                0,
                QTableWidgetItem(file.name),
            )

            self._table.setItem(
                row,
                1,
                QTableWidgetItem(
                    file.modified_time.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                ),
            )

            self._table.setItem(
                row,
                2,
                QTableWidgetItem(
                    format_size(file.size)
                ),
            )

            self._table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(file.path)
                ),
            )

    def show_duplicate_files(
        self,
        groups: Sequence[Sequence[DuplicateFile]],
    ) -> None:
        """
        Display duplicate files.
        """
        self.clear()

        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            [
                "그룹",
                "파일명",
                "크기",
                "경로",
            ]
        )

        row = 0

        total_rows = sum(
            len(group)
            for group in groups
        )

        self._table.setRowCount(total_rows)

        for group_index, group in enumerate(
            groups,
            start=1,
        ):
            for file in group:
                self._table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        f"Group {group_index}"
                    ),
                )

                self._table.setItem(
                    row,
                    1,
                    QTableWidgetItem(file.name),
                )

                self._table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        format_size(file.size)
                    ),
                )

                self._table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        str(file.path)
                    ),
                )

                row += 1

    def show_move_plans(
        self,
        plans: list[MovePlan],
    ) -> None:
        """
        Display organization preview.

        Args:
            plans:
                List of planned file moves.
        """
        self.clear()

        self._table.setColumnCount(3)

        self._table.setHorizontalHeaderLabels(
            [
                "파일명",
                "대상 폴더",
                "이유",
            ]
        )

        self._table.setRowCount(len(plans))

        for row, plan in enumerate(plans):
            self._table.setItem(
                row,
                0,
                QTableWidgetItem(
                    plan.file_name,
                ),
            )

            self._table.setItem(
                row,
                1,
                QTableWidgetItem(
                    f"📁 {plan.category}",
                ),
            )

            self._table.setItem(
                row,
                2,
                QTableWidgetItem(
                    plan.reason,
                ),
            )

        self._table.resizeColumnsToContents()

    def show_move_results(
        self,
        results: list[MoveResult],
    ) -> None:
        """
        Display file move results.

        Args:
            results:
                Results of file move operations.
        """
        self.clear()

        self._table.setColumnCount(4)

        self._table.setHorizontalHeaderLabels(
            [
                "상태",
                "파일명",
                "대상",
                "메시지",
            ]
        )

        self._table.setRowCount(
            len(results)
        )

        for row, result in enumerate(results):

            status = (
                "✅ 완료"
                if result.success
                else "❌ 실패"
            )

            self._table.setItem(
                row,
                0,
                QTableWidgetItem(status),
            )

            self._table.setItem(
                row,
                1,
                QTableWidgetItem(
                    result.file_name,
                ),
            )

            self._table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(result.destination.parent.name),
                ),
            )

            self._table.setItem(
                row,
                3,
                QTableWidgetItem(
                    result.message,
                ),
            )

        self._table.resizeColumnsToContents()