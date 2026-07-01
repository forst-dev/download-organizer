"""
Application settings management.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path


logger = logging.getLogger(__name__)

SETTINGS_FILE = Path("settings.json")


@dataclass
class AppSettings:
    """
    Application settings model.
    """

    last_selected_folder: str = ""
    theme: str = "Auto"


class Settings:
    """
    Load and save application settings.
    """

    _settings: AppSettings | None = None

    @classmethod
    def load(cls) -> AppSettings:
        """
        Load settings from settings.json.

        If the file does not exist, it will be created with default values.

        Returns:
            AppSettings: Loaded settings.
        """
        if cls._settings is not None:
            return cls._settings

        try:
            if not SETTINGS_FILE.exists():
                cls._settings = AppSettings()
                cls.save()
                logger.info("Created default settings.json")
                return cls._settings

            with SETTINGS_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            cls._settings = AppSettings(**data)
            logger.info("Settings loaded successfully.")

        except Exception:
            logger.exception("Failed to load settings. Using default settings.")
            cls._settings = AppSettings()

        return cls._settings

    @classmethod
    def save(cls) -> None:
        """
        Save current settings to settings.json.
        """
        try:
            if cls._settings is None:
                cls._settings = AppSettings()

            with SETTINGS_FILE.open("w", encoding="utf-8") as file:
                json.dump(
                    asdict(cls._settings),
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            logger.info("Settings saved successfully.")

        except Exception:
            logger.exception("Failed to save settings.")

    @classmethod
    def get(cls) -> AppSettings:
        """
        Get current settings.

        Returns:
            AppSettings: Current settings instance.
        """
        return cls.load()