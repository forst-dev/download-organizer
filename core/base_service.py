"""
Base class for application services.
"""

from __future__ import annotations

import logging


class BaseService:
    """
    Base class for all application services.

    Provides a shared logger for services.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__
        )