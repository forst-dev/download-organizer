"""
Base class for application services.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """
    Base class for all application services.

    Services contain business logic only.
    Workers are responsible for threading and
    exception handling.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    @abstractmethod
    def execute(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the service.

        Returns:
            Service-specific result.
        """
        raise NotImplementedError