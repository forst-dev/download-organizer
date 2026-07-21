"""
Application entry point.

Starts the application, initializes logging, loads settings,
and displays the main window.
"""

from __future__ import annotations

import logging
import sys
import traceback
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

        app.lastWindowClosed.connect(
            lambda: logger.info("LAST WINDOW CLOSED")
        )

        app.aboutToQuit.connect(
            lambda: logger.info("APP ABOUT TO QUIT")
        )

        # Load settings (creates settings.json automatically if it doesn't exist)
        Settings.load()

        window = MainWindow()
        window.show()

        logger.info("Application started successfully.")

        return app.exec()

    except Exception:
        logger.exception("Unexpected error occurred while starting the application.")
        return 1

def exception_hook(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))

    print("=" * 50)
    print("Uncaught Exception Occurred:")
    print(err_msg)
    print("=" * 50)

    logger.critical("Unhandled exception caught by sys.excepthook:\n%s", err_msg)

    sys.__excepthook__(exctype, value, tb)


if __name__ == "__main__":
    sys.excepthook = exception_hook
    sys.exit(main())