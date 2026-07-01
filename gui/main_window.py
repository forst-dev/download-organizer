"""
Main application window.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QMainWindow
from qfluentwidgets import FluentWindow, PrimaryPushButton, ProgressBar


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:
        super().__init__()

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

        self.select_folder_button = PrimaryPushButton("📂 폴더 선택")

        self.status_label = QLabel("상태 : 준비 완료")

        self.progress_bar = ProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        layout.addWidget(self.title_label)
        layout.addSpacing(20)
        layout.addWidget(self.select_folder_button)
        layout.addWidget(self.status_label)
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

    def on_select_folder_clicked(self) -> None:
        """
        Handle folder selection button click.

        This method will be implemented in STEP 2.
        """
        logger.info("Folder selection button clicked.")
        # TODO: Implement in STEP 2
        pass