"""
Main application window.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QMainWindow,
)

from qfluentwidgets import ProgressBar

from config.settings import Settings
from gui.handlers import UIHandler
from gui.table_manager import TableManager
from gui.worker_manager import WorkerManager
from services.analyzer import AnalysisResult
from utils.format_utils import format_size
from utils.path_utils import get_downloads_folder

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.current_folder: Path | None = None

        self._init_ui()

        self.table_manager = TableManager(
            self.result_table
        )

        self.handler = UIHandler(
            self,
            self.table_manager,
        )

        self.worker_manager = WorkerManager(
            self.handler,
        )

        logger.info("Main window initialized.")
        
    def _init_ui(self) -> None:
        """
        Initialize UI.
        """

        self.setWindowTitle("Download Organizer")

        self.resize(1100, 750)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.setSpacing(15)
        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.title_label = QLabel(
            "📂 Download Organizer"
        )

        font = self.title_label.font()
        font.setPointSize(20)
        font.setBold(True)

        self.title_label.setFont(font)

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.title_label)

        self.status_label = QLabel(
            "상태 : 준비 완료"
        )

        layout.addWidget(self.status_label)

        self.summary_label = QLabel("")

        layout.addWidget(self.summary_label)

        self.select_folder_button = QPushButton(
            "다운로드 폴더 선택"
        )

        layout.addWidget(
            self.select_folder_button
        )

        self.large_file_button = QPushButton(
            "큰 파일"
        )

        layout.addWidget(
            self.large_file_button
        )

        self.old_file_button = QPushButton(
            "오래된 파일"
        )

        layout.addWidget(
            self.old_file_button
        )

        self.duplicate_button = QPushButton(
            "중복 파일"
        )

        layout.addWidget(
            self.duplicate_button
        )

        self.progress_bar = ProgressBar()

        self.progress_bar.setVisible(False)

        layout.addWidget(self.progress_bar)

        self.result_table = QTableWidget()

        layout.addWidget(self.result_table)

        self.select_folder_button.clicked.connect(
            self.on_select_folder_clicked
        )

        self.large_file_button.clicked.connect(
            self.on_large_file_clicked
        )

        self.old_file_button.clicked.connect(
            self.on_old_file_clicked
        )

        self.duplicate_button.clicked.connect(
            self.on_duplicate_clicked
        )

    def on_select_folder_clicked(self) -> None:
        """
        Select a folder and start analysis.
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "다운로드 폴더 선택",
            str(get_downloads_folder()),
        )

        if not folder:
            return

        self.current_folder = Path(folder)

        # Settings.save_last_folder(self.current_folder)

        self.show_loading(True)
        self.set_status("분석 중...")

        logger.info(
            "Selected folder: %s",
            self.current_folder,
        )

        self.worker_manager.start_analysis(
            self.current_folder,
        )

    def on_large_file_clicked(self) -> None:
        """
        Find large files.
        """
        if self.current_folder is None:
            self.show_error("먼저 폴더를 선택해주세요.")
            return

        self.show_loading(True)
        self.set_status("큰 파일 검색 중...")

        self.worker_manager.start_large_file_search(
            self.current_folder,
        )

    def on_old_file_clicked(self) -> None:
        """
        Find old files.
        """
        if self.current_folder is None:
            self.show_error("먼저 폴더를 선택해주세요.")
            return

        self.show_loading(True)
        self.set_status("오래된 파일 검색 중...")

        self.worker_manager.start_old_file_search(
            self.current_folder,
        )

    def on_duplicate_clicked(self) -> None:
        """
        Find duplicate files.
        """
        if self.current_folder is None:
            self.show_error("먼저 폴더를 선택해주세요.")
            return

        self.show_loading(True)
        self.set_status("중복 파일 검색 중...")

        self.worker_manager.start_duplicate_search(
            self.current_folder,
        )

    def show_loading(
        self,
        loading: bool,
    ) -> None:
        """
        Show or hide loading state.
        """
        self.progress_bar.setVisible(loading)

        self.select_folder_button.setEnabled(not loading)
        self.large_file_button.setEnabled(not loading)
        self.old_file_button.setEnabled(not loading)
        self.duplicate_button.setEnabled(not loading)

    def set_status(
        self,
        text: str,
    ) -> None:
        """
        Update status label.
        """
        self.status_label.setText(
            f"상태 : {text}"
        )

    def show_summary(
        self,
        result: AnalysisResult,
    ) -> None:
        """
        Display analysis summary.
        """
        self.summary_label.setText(
            "\n".join(
                [
                    f"파일 수 : {result.file_count:,}",
                    f"폴더 수 : {result.folder_count:,}",
                    f"전체 용량 : {format_size(result.total_size)}",
                ]
            )
        )

    def clear_summary(self) -> None:
        """
        Clear summary label.
        """
        self.summary_label.clear()

    def show_error(
        self,
        message: str,
    ) -> None:
        """
        Display an error dialog.
        """
        QMessageBox.critical(
            self,
            "오류",
            message,
        )

    def has_selected_folder(self) -> bool:
        """
        Check whether a folder is selected.
        """
        return self.current_folder is not None