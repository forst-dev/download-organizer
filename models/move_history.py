"""
Model representing a file move history entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass(slots=True)
class MoveHistory:
    """
    Represents a completed file move operation.

    Attributes:
        source:
            Original file path before moving.

        destination:
            New file path after moving.

        moved_at:
            Time when the move completed.
    """

    source: Path
    destination: Path
    moved_at: datetime