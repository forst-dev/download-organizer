"""
Application entry point.

Starts the application, initializes logging, loads settings,
and displays the main window.
"""

from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from config.settings import Settings
from gui.main_window import MainWindow
from utils.logger import setup_logging


def main() -> int:
    """
    Application entry point.

    Returns:
        int: Application exit code.
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Download Organizer...")

        app = QApplication(sys.argv)

        # Load settings (creates settings.json automatically if it doesn't exist)
        Settings.load()

        window = MainWindow()
        window.show()

        logger.info("Application started successfully.")

        return app.exec()

    except Exception:
        logger.exception("Unexpected error occurred while starting the application.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
