"""
Main application window.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import PrimaryPushButton, ProgressBar

from services.analyzer import AnalysisResult
from utils.format_utils import format_size
from utils.path_utils import get_downloads_folder
from workers.analyzer_worker import create_analyzer_thread

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:
        super().__init__()

        self._thread = None
        self._worker = None

        self.setWindowTitle("Download Organizer")
        self.resize(800, 600)

        self._init_ui()
        self._connect_signals()

        logger.info("Main window initialized.")

    def _init_ui(self) -> None:
        """
        Initialize UI components.
        """
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title_label = QLabel("Download Organizer")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = self.title_label.font()
        font.setPointSize(18)
        font.setBold(True)
        self.title_label.setFont(font)

        self.select_folder_button = PrimaryPushButton("폴더 선택")

        self.status_label = QLabel("상태 : 준비 완료")

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)

        self.progress_bar = ProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

        self.setCentralWidget(central_widget)

    def _connect_signals(self) -> None:
        """
        Connect UI signals.
        """
        self.select_folder_button.clicked.connect(
            self.on_select_folder_clicked
        )

    def set_status(self, message: str) -> None:
        """
        Update status label.
        """
        self.status_label.setText(f"상태 : {message}")

    def on_select_folder_clicked(self) -> None:
        """
        Open folder dialog and start analysis.
        """
        folder = QFileDialog.getExistingDirectory(
            self,
            "다운로드 폴더 선택",
            str(get_downloads_folder()),
        )

        if not folder:
            return

        self.select_folder_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.set_status("분석 중...")
        self.result_label.clear()

        self._thread, self._worker = create_analyzer_thread(
            Path(folder)
        )
        
        self._worker.finished.connect(self.on_analysis_finished)
        self._worker.error.connect(self.on_analysis_error)

        self._thread.start()

    def on_analysis_finished(
        self,
        result: AnalysisResult,
    ) -> None:
        """
        Called when analysis is completed.
        """
        self.progress_bar.setVisible(False)
        self.select_folder_button.setEnabled(True)

        self.set_status("분석 완료")

        self.result_label.setText(
            "\n".join(
                [
                    f"파일 수 : {result.file_count:,}",
                    f"폴더 수 : {result.folder_count:,}",
                    f"전체 용량 : {format_size(result.total_size)}",
                ]
            )
        )

        logger.info("Analysis completed.")

    def on_analysis_error(
        self,
        message: str,
    ) -> None:
        """
        Called when analysis fails.
        """
        self.progress_bar.setVisible(False)
        self.select_folder_button.setEnabled(True)

        self.set_status("오류 발생")

        QMessageBox.critical(
            self,
            "오류",
            message,
        )

        logger.error("Analysis failed: %s", message)